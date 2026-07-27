"""Tests for deterministic asset and scene discovery."""

from jam_asset_manager.core.catalog import (
    get_assets,
    get_episodes,
    get_extension,
    get_scenes,
    is_allowed_extension,
    is_path_within,
    is_valid_animation_scene_name,
)
from jam_asset_manager.core.config import load_application_config
from tests.support import TemporaryProjectTestCase


class CatalogTestCase(TemporaryProjectTestCase):
    def test_assets_and_scene_state_are_discovered(self):
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

    def test_asset_results_are_recursive_sorted_and_filtered(self):
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

    def test_only_episode_directories_are_listed_in_order(self):
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

    def test_scene_name_requires_three_digit_shot_number(self):
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

    def test_path_containment_respects_directory_boundaries(self):
        parent = self.root / "assets"
        self.assertTrue(is_path_within(parent / "models" / "tree.ma", parent))
        self.assertFalse(is_path_within(self.root / "assets-old" / "tree.ma", parent))
        self.assertFalse(is_path_within("", parent))
