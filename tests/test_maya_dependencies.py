"""Tests for Maya dependency discovery and file snapshots."""

import importlib
from pathlib import Path
from unittest.mock import MagicMock, patch

from tests.support import TemporaryProjectTestCase, install_maya_stubs

install_maya_stubs()

maya_dependencies = importlib.import_module("jam_asset_manager.maya.dependencies")


class MayaDependenciesTestCase(TemporaryProjectTestCase):
    def setUp(self):
        super().setUp()
        self.cmds = MagicMock()
        self.cmds_patcher = patch.object(maya_dependencies, "cmds", self.cmds)
        self.cmds_patcher.start()

    def tearDown(self):
        self.cmds_patcher.stop()
        super().tearDown()

    def test_collects_references_textures_and_missing_caches(self):
        scene_path = self.root / "shots" / "render.ma"
        reference_path = self.root / "shots" / "animation.ma"
        texture_path = self.root / "sourceimages" / "diffuse.tx"
        reference_path.parent.mkdir(parents=True)
        texture_path.parent.mkdir(parents=True)
        reference_path.write_text("animation", encoding="utf-8")
        texture_path.write_text("texture", encoding="utf-8")

        self.cmds.file.return_value = [str(reference_path)]
        self.cmds.referenceQuery.return_value = "animationRN"
        nodes_by_type = {
            "file": ["diffuseFile"],
            "gpuCache": ["missingCache"],
        }
        self.cmds.ls.side_effect = lambda type: nodes_by_type.get(type, [])
        attribute_paths = {
            "diffuseFile.fileTextureName": "sourceimages/diffuse.tx",
            "missingCache.cacheFileName": "cache/missing.abc",
        }
        self.cmds.getAttr.side_effect = lambda attribute: attribute_paths[attribute]
        self.cmds.workspace.side_effect = lambda expandName: str(self.root / expandName)

        collection = maya_dependencies.collect_dependencies(str(scene_path))
        dependencies = collection.dependencies

        self.assertEqual(
            [(item["kind"], item.get("node")) for item in dependencies],
            [
                ("cache", "missingCache"),
                ("reference", "animationRN"),
                ("texture", "diffuseFile"),
            ],
        )
        reference = next(item for item in dependencies if item["kind"] == "reference")
        texture = next(item for item in dependencies if item["kind"] == "texture")
        cache = next(item for item in dependencies if item["kind"] == "cache")
        self.assertEqual(reference["resolvedPath"], str(reference_path))
        self.assertTrue(reference["exists"])
        self.assertEqual(texture["resolvedPath"], str(texture_path))
        self.assertEqual(texture["size"], len("texture"))
        self.assertFalse(cache["exists"])
        self.assertEqual(collection.errors, ())
        self.cmds.file.assert_called_once_with(
            query=True,
            reference=True,
            withoutCopyNumber=True,
        )

    def test_dependency_order_is_deterministic_and_duplicates_are_removed(self):
        repeated = self.root / "texture.tx"
        repeated.touch()
        self.cmds.file.return_value = []
        self.cmds.ls.side_effect = lambda type: ["b", "a", "a"] if type == "file" else []
        self.cmds.getAttr.return_value = str(repeated)
        self.cmds.workspace.side_effect = lambda expandName: expandName

        dependencies = maya_dependencies.collect_dependencies().dependencies

        self.assertEqual([item["node"] for item in dependencies], ["a", "b"])
        self.assertTrue(all(Path(item["resolvedPath"]).is_absolute() for item in dependencies))

    def test_udim_patterns_capture_all_matching_tiles(self):
        first_tile = self.root / "sourceimages" / "diffuse.1001.exr"
        second_tile = self.root / "sourceimages" / "diffuse.1011.exr"
        first_tile.parent.mkdir()
        first_tile.write_text("first", encoding="utf-8")
        second_tile.write_text("second", encoding="utf-8")
        texture_pattern = self.root / "sourceimages" / "diffuse.<UDIM>.exr"

        self.cmds.file.return_value = []
        self.cmds.ls.side_effect = lambda type: ["udimFile"] if type == "file" else []
        self.cmds.getAttr.side_effect = lambda attribute: (
            str(texture_pattern) if attribute == "udimFile.computedFileTextureNamePattern" else ""
        )
        self.cmds.workspace.side_effect = lambda expandName: expandName

        collection = maya_dependencies.collect_dependencies()

        self.assertEqual(collection.errors, ())
        self.assertEqual(len(collection.dependencies), 1)
        dependency = collection.dependencies[0]
        self.assertTrue(dependency["exists"])
        self.assertEqual(dependency["fileCount"], 2)
        self.assertEqual(dependency["size"], len("first") + len("second"))

    def test_collection_errors_are_returned_with_the_snapshot(self):
        self.cmds.file.side_effect = RuntimeError("reference query failed")
        self.cmds.ls.return_value = []

        with self.assertLogs(maya_dependencies.LOGGER, level="ERROR"):
            collection = maya_dependencies.collect_dependencies()

        self.assertEqual(collection.dependencies, ())
        self.assertEqual(
            collection.errors,
            ("Could not list scene references: reference query failed",),
        )
