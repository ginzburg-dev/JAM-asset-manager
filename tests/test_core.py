"""Tests for the framework-independent JAM core."""

import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from jam_core.catalog import (
    get_assets,
    get_episodes,
    get_extension,
    get_scenes,
    is_allowed_extension,
    is_path_within,
    is_valid_animation_scene_name,
)
from jam_core.config import (
    ConfigurationError,
    JamConfig,
    ProjectState,
    UserState,
    load_application_config,
    load_user_state,
    resolve_path,
    save_user_state,
)
from jam_core.reports import (
    append_message,
    metadata_path,
    new_metadata,
    read_messages,
    render_history,
)
from jam_core.storage import read_json, write_json


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def write_config(self, projects=None):
        config_path = self.root / "config.json"
        write_json(
            config_path,
            {
                "assetManagerName": "Test JAM",
                "currentProject": "Demo",
                "projects": projects
                or [
                    {
                        "projectName": "Demo",
                        "projectPath": "projects/Demo",
                        "episodePath": "scenes/episodes",
                        "rsScene": "projects/Demo/assets/RS/template.ma",
                        "assets": [
                            {
                                "assetType": "HDRI",
                                "assetTypePath": "assets/HDRI",
                            }
                        ],
                    }
                ],
                "allowedExtensions": [".MA", "hdr", "ma"],
                "excludedNames": [".DS_Store"],
                "iconSize": 128,
            },
        )
        return config_path

    def test_storage_round_trip_is_formatted(self):
        path = self.root / "nested" / "data.json"
        write_json(path, {"name": "JAM"})
        self.assertEqual(read_json(path), {"name": "JAM"})
        self.assertTrue(path.read_text(encoding="utf-8").endswith("\n"))

    def test_storage_returns_requested_default_for_missing_file(self):
        sentinel = object()
        self.assertIs(read_json(self.root / "missing.json", sentinel), sentinel)
        self.assertEqual(read_json(self.root / "missing.json"), {})

    def test_storage_removes_temporary_file_when_replace_fails(self):
        path = self.root / "data.json"
        with patch("jam_core.storage.os.replace", side_effect=OSError("disk error")):
            with self.assertRaisesRegex(OSError, "disk error"):
                write_json(path, {"name": "JAM"})
        self.assertFalse((self.root / "data.json.tmp").exists())

    def test_application_config_is_typed_and_resolves_relative_paths(self):
        config = load_application_config(self.write_config(), self.root)
        project = config.project("Demo")
        self.assertEqual(config.name, "Test JAM")
        self.assertEqual(config.allowed_extensions, ("ma", "hdr"))
        self.assertEqual(project.root, (self.root / "projects" / "Demo").resolve())
        self.assertEqual(project.asset_types[0].name, "HDRI")

    def test_application_config_rejects_duplicate_projects(self):
        project = {
            "projectName": "Demo",
            "projectPath": "Demo",
            "episodePath": "episodes",
            "rsScene": "template.ma",
            "assets": [],
        }
        with self.assertRaisesRegex(ConfigurationError, "unique"):
            load_application_config(self.write_config([project, project]), self.root)

    def test_application_config_rejects_missing_and_invalid_values(self):
        with self.assertRaisesRegex(ConfigurationError, "was not found"):
            load_application_config(self.root / "missing.json", self.root)

        config_path = self.write_config()
        data = read_json(config_path)
        data["currentProject"] = "Unknown"
        write_json(config_path, data)
        with self.assertRaisesRegex(ConfigurationError, "unknown project"):
            load_application_config(config_path, self.root)

        data["currentProject"] = "Demo"
        data["iconSize"] = 0
        write_json(config_path, data)
        with self.assertRaisesRegex(ConfigurationError, "positive integer"):
            load_application_config(config_path, self.root)

    def test_application_config_rejects_malformed_json(self):
        path = self.root / "config.json"
        path.write_text("{invalid", encoding="utf-8")
        with self.assertRaisesRegex(ConfigurationError, "Could not read"):
            load_application_config(path, self.root)

    def test_environment_markers_are_expanded_in_paths(self):
        with patch.dict(os.environ, {"JAM_TEST_PROJECT": str(self.root / "project")}):
            self.assertEqual(
                resolve_path("$JAM_TEST_PROJECT/assets", self.root),
                (self.root / "project" / "assets").resolve(),
            )

    def test_resolve_path_rejects_empty_values(self):
        for value in (None, "", "  "):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ConfigurationError, "non-empty"):
                    resolve_path(value, self.root)

    def test_user_state_round_trip_merges_project_defaults(self):
        config = load_application_config(self.write_config(), self.root)
        state_path = self.root / "config.user.json"
        state = UserState("Demo", {"Demo": ProjectState("HDRI", "ep001")})
        save_user_state(state, state_path)
        loaded = load_user_state(config, state_path)
        self.assertEqual(loaded.current_project, "Demo")
        self.assertEqual(loaded.project("Demo").episode, "ep001")

    def test_user_state_discards_stale_project_and_asset_type(self):
        config = load_application_config(self.write_config(), self.root)
        state_path = self.root / "config.user.json"
        write_json(
            state_path,
            {
                "currentProject": "DeletedProject",
                "configs": [
                    {
                        "projectName": "Demo",
                        "currentAssetType": "DeletedType",
                        "currentEpisode": "ep020",
                    },
                    {"projectName": "DeletedProject", "currentEpisode": "ep999"},
                ],
            },
        )
        state = load_user_state(config, state_path)
        self.assertEqual(state.current_project, "Demo")
        self.assertEqual(state.project("Demo"), ProjectState("HDRI", "ep020"))
        self.assertNotIn("DeletedProject", state.projects)

    def test_user_state_rejects_invalid_config_list(self):
        config = load_application_config(self.write_config(), self.root)
        state_path = self.root / "config.user.json"
        write_json(state_path, {"configs": {}})
        with self.assertRaisesRegex(ConfigurationError, "must be a list"):
            load_user_state(config, state_path)

    def test_jam_config_is_loaded_from_environment_and_can_be_passed_around(self):
        config_path = self.write_config()
        state_path = self.root / "state" / "config.user.json"
        environ = {
            "JAM_ASSET_MANAGER_PATH": str(self.root),
            "JAM_CONFIG_PATH": str(config_path),
            "JAM_USER_CONFIG_PATH": str(state_path),
        }

        config = JamConfig.from_environment(environ)
        self.assertEqual(config.asset_manager_path, self.root.resolve())
        self.assertEqual(config.icons_path, self.root.resolve() / "icons")
        self.assertEqual(config.project("Demo").name, "Demo")

        config.user_state.project("Demo").episode = "ep010"
        config.save()
        reloaded = JamConfig.from_environment(environ)
        self.assertEqual(reloaded.user_state.project("Demo").episode, "ep010")

        config.user_state.project("Demo").episode = "not saved"
        config.reload()
        self.assertEqual(config.user_state.project("Demo").episode, "ep010")

    def test_catalog_discovers_assets_and_scene_state(self):
        config = load_application_config(self.write_config(), self.root)
        project = config.project("Demo")
        asset_directory = project.root / "assets" / "HDRI"
        asset_directory.mkdir(parents=True)
        (asset_directory / "studio.HDR").touch()
        (asset_directory / "ignore.txt").touch()
        assets = get_assets(asset_directory, config.allowed_extensions)
        self.assertEqual([asset.name for asset in assets], ["studio"])
        self.assertTrue(is_allowed_extension("LOOK.MA", config.allowed_extensions))

        animation_directory = project.root / "scenes" / "episodes" / "ep001" / "maya" / "animation"
        render_directory = project.root / "scenes" / "episodes" / "ep001" / "render" / "ep001_001"
        animation_directory.mkdir(parents=True)
        render_directory.mkdir(parents=True)
        (animation_directory / "ep001_001.ma").touch()
        (render_directory / "ep001_001.ma").touch()
        scenes = get_scenes(project, "ep001")
        self.assertEqual(len(scenes), 1)
        self.assertTrue(scenes[0].render_exists)

    def test_catalog_results_are_recursive_sorted_and_filtered(self):
        asset_root = self.root / "assets"
        (asset_root / "z_folder").mkdir(parents=True)
        (asset_root / "a_folder").mkdir()
        (asset_root / "z_folder" / "second.ma").touch()
        (asset_root / "a_folder" / "first.HDR").touch()
        (asset_root / "a_folder" / "ignore.txt").touch()
        assets = get_assets(asset_root, ("ma", "hdr"))
        self.assertEqual([asset.name for asset in assets], ["first", "second"])
        self.assertEqual(get_extension("archive.LOOK.MA"), "ma")
        self.assertFalse(is_allowed_extension("readme", ("ma",)))

    def test_catalog_lists_only_episode_directories_in_order(self):
        config = load_application_config(self.write_config(), self.root)
        project = config.project("Demo")
        episode_root = project.root / project.episode_path
        (episode_root / "ep002").mkdir(parents=True)
        (episode_root / "ep001").mkdir()
        (episode_root / "notes.txt").touch()
        self.assertEqual(
            [episode.name for episode in get_episodes(project)],
            ["ep001", "ep002"],
        )

    def test_animation_scene_name_requires_three_digit_shot_number(self):
        valid_names = ("ep001_001.ma", "ep001_999.MA")
        invalid_names = (
            "ep001_01.ma",
            "ep001_0001.ma",
            "ep001_abc.ma",
            "ep002_001.ma",
            "ep001_001.mb",
        )
        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(is_valid_animation_scene_name("ep001", name))
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(is_valid_animation_scene_name("ep001", name))

    def test_is_path_within_respects_directory_boundaries(self):
        parent = self.root / "assets"
        self.assertTrue(is_path_within(parent / "models" / "tree.ma", parent))
        self.assertFalse(is_path_within(self.root / "assets-old" / "tree.ma", parent))
        self.assertFalse(is_path_within("", parent))

    def test_reports_preserve_hours_and_escape_html(self):
        asset_path = self.root / "asset.ma"
        append_message(
            asset_path,
            "asset",
            "report",
            "<b>created</b>",
            hours=2,
            user="artist",
            now=datetime(2026, 7, 23, 12, 30),
        )
        messages = read_messages(asset_path)
        self.assertEqual(messages[0]["hours"], 2)
        self.assertEqual(messages[0]["createdTime"], "23/07/2026 12:30:00")
        rendered = render_history(messages)
        self.assertIn("&lt;b&gt;created&lt;/b&gt;", rendered)
        self.assertNotIn("<b>created</b>", rendered)

    def test_reports_preserve_initial_created_time_across_messages(self):
        asset_path = self.root / "asset.ma"
        first_time = datetime(2026, 7, 23, 10, 0)
        second_time = datetime(2026, 7, 24, 11, 30)
        append_message(asset_path, "asset", "note", "First", now=first_time)
        data = append_message(asset_path, "asset", "report", "Second", now=second_time)
        self.assertEqual(data["createdTime"], "23/07/2026 10:00:00")
        self.assertEqual(len(data["messages"]), 2)
        self.assertEqual(metadata_path(asset_path), self.root / "asset.json")

    def test_report_renderer_ignores_unknown_types_and_escapes_byline(self):
        messages = [
            {"type": "unknown", "message": "hidden"},
            {
                "type": "note",
                "createdTime": "today",
                "user": "<artist>",
                "message": "line one\nline two",
                "hours": 99,
            },
        ]
        rendered = render_history(messages)
        self.assertNotIn("hidden", rendered)
        self.assertIn("&lt;artist&gt;", rendered)
        self.assertIn("line one<br>line two", rendered)
        self.assertNotIn("99h", rendered)
        self.assertEqual(new_metadata()["messages"], [])


if __name__ == "__main__":
    unittest.main()
