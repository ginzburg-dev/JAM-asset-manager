"""Tests for typed shared configuration and local user state."""

import os
from unittest.mock import patch

from jam_asset_manager.core.config import (
    BaseConfig,
    ConfigurationError,
    JamConfig,
    ProjectState,
    UserState,
    load_application_config,
    load_user_state,
    resolve_path,
    save_user_state,
)
from jam_asset_manager.core.storage import read_json, write_json
from tests.support import TemporaryProjectTestCase


class ConfigTestCase(TemporaryProjectTestCase):
    def test_application_config_is_typed_and_resolves_relative_paths(self):
        config = load_application_config(self.write_config(), self.root)
        project = config.project("Demo")
        self.assertEqual(config.name, "Test JAM")
        self.assertEqual(config.allowed_extensions, ("ma", "hdr"))
        self.assertEqual(project.root, (self.root / "projects" / "Demo").resolve())
        self.assertEqual(project.asset_types[0].name, "HDRI")

    def test_duplicate_projects_are_rejected(self):
        project = {
            "projectName": "Demo",
            "projectPath": "Demo",
            "episodePath": "episodes",
            "rsScene": "template.ma",
            "assets": [],
        }
        with self.assertRaisesRegex(ConfigurationError, "unique"):
            load_application_config(self.write_config([project, project]), self.root)

    def test_missing_and_invalid_values_are_rejected(self):
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

    def test_malformed_json_is_wrapped_as_configuration_error(self):
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

    def test_empty_paths_are_rejected(self):
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

    def test_stale_project_and_asset_type_are_discarded(self):
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

    def test_invalid_user_config_list_is_rejected(self):
        config = load_application_config(self.write_config(), self.root)
        state_path = self.root / "config.user.json"
        write_json(state_path, {"configs": {}})
        with self.assertRaisesRegex(ConfigurationError, "must be a list"):
            load_user_state(config, state_path)

    def test_jam_config_is_environment_driven_and_persists_state(self):
        config_path = self.write_config()
        state_path = self.root / "state" / "config.user.json"
        custom_icons = self.root / "icons"
        custom_icons.mkdir()
        environ = {
            "JAM_ASSET_MANAGER_PATH": str(self.root),
            "JAM_CONFIG_PATH": str(config_path),
            "JAM_USER_CONFIG_PATH": str(state_path),
        }

        with patch.dict(os.environ, environ, clear=True):
            base_config = BaseConfig()
            self.assertEqual(base_config.asset_manager_path, self.root.resolve())
            self.assertEqual(base_config.config_path, config_path.resolve())
            self.assertEqual(base_config.user_config_path, state_path.resolve())

            config = JamConfig()
            self.assertEqual(config.asset_manager_path, self.root.resolve())
            self.assertEqual(config.icons_path, custom_icons.resolve())
            self.assertEqual(config.project("Demo").name, "Demo")

            config.user_state.project("Demo").episode = "ep010"
            config.save()
            reloaded = JamConfig()
        self.assertEqual(reloaded.user_state.project("Demo").episode, "ep010")

        config.user_state.project("Demo").episode = "not saved"
        config.reload()
        self.assertEqual(config.user_state.project("Demo").episode, "ep010")
