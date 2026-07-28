"""Unit tests for Maya asset operations using a mocked command layer."""

import importlib
import tempfile
import unittest
from contextlib import contextmanager, nullcontext
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from tests.support import install_maya_stubs

install_maya_stubs()

maya_assets = importlib.import_module("jam_asset_manager.maya.assets")


class MayaAssetTestCase(unittest.TestCase):
    def setUp(self):
        self.cmds = MagicMock()
        self.cmds_patcher = patch.object(maya_assets, "cmds", self.cmds)
        self.cmds_patcher.start()
        self.lock_patcher = patch.object(
            maya_assets,
            "publish_lock",
            side_effect=lambda _path: nullcontext(),
        )
        self.lock_patcher.start()

    def tearDown(self):
        self.lock_patcher.stop()
        self.cmds_patcher.stop()

    def test_import_asset_rejects_missing_file(self):
        self.assertFalse(maya_assets.import_asset("missing.ma"))
        self.cmds.warning.assert_called_once_with("Asset does not exist: missing.ma")
        self.cmds.file.assert_not_called()

    def test_import_asset_uses_safe_maya_options(self):
        with tempfile.TemporaryDirectory() as directory:
            asset_path = Path(directory) / "asset.ma"
            asset_path.touch()
            self.assertTrue(maya_assets.import_asset(str(asset_path)))

        self.cmds.file.assert_called_once_with(
            str(asset_path),
            i=True,
            mergeNamespacesOnClash=True,
            namespace=":",
            ra=True,
        )

    def test_check_asset_displays_success(self):
        self.assertTrue(maya_assets.check_asset())
        self.cmds.confirmDialog.assert_called_once_with(
            title="Asset check complete",
            message="No asset problems were found.",
            button=["OK"],
        )

    def test_publish_asset_requires_a_saved_scene(self):
        self.cmds.file.return_value = ""
        self.assertFalse(maya_assets.publish_asset())
        self.cmds.warning.assert_called_once()
        self.cmds.confirmDialog.assert_not_called()

    def test_publish_asset_stops_when_validation_fails(self):
        self.cmds.file.return_value = "asset.ma"
        with patch.object(maya_assets, "asset_check_message", return_value=[0, "Broken"]):
            self.assertFalse(maya_assets.publish_asset())

        self.cmds.confirmDialog.assert_called_once_with(
            title="Asset was not published",
            message="Broken",
            button=["OK"],
        )

    def test_publish_asset_handles_maya_save_error(self):
        self.cmds.file.side_effect = ["asset.ma", RuntimeError("save failed")]
        with self.assertLogs(maya_assets.LOGGER, level="ERROR"):
            self.assertFalse(maya_assets.publish_asset())
        self.cmds.warning.assert_called_once_with(
            "The asset could not be published. See the Script Editor for details."
        )

    def test_publish_asset_saves_and_confirms_success(self):
        self.cmds.file.side_effect = ["asset.ma", None]
        dependencies = [{"kind": "texture", "path": "diffuse.tx"}]
        with patch.object(
            maya_assets,
            "collect_dependencies",
            return_value=SimpleNamespace(dependencies=dependencies, errors=()),
        ) as collect_dependencies, patch.object(
            maya_assets,
            "record_publish",
            return_value={"versionLabel": "v007", "dependencyStatus": "complete"},
        ) as record_publish:
            self.assertTrue(maya_assets.publish_asset())

        self.assertEqual(self.cmds.file.call_count, 2)
        self.cmds.file.assert_any_call(save=True)
        collect_dependencies.assert_called_once_with("asset.ma")
        record_publish.assert_called_once_with(
            "asset.ma",
            "asset",
            dependencies=dependencies,
            dependency_errors=(),
        )
        self.cmds.confirmDialog.assert_called_once_with(
            title="Publish complete",
            message="The asset was published successfully as v007.",
            button=["OK"],
        )

    def test_publish_asset_reports_metadata_failure_after_save(self):
        self.cmds.file.side_effect = ["asset.ma", None]
        with patch.object(
            maya_assets,
            "collect_dependencies",
            return_value=SimpleNamespace(dependencies=(), errors=()),
        ), patch.object(
            maya_assets,
            "record_publish",
            side_effect=OSError("metadata unavailable"),
        ):
            with self.assertLogs(maya_assets.LOGGER, level="ERROR"):
                self.assertFalse(maya_assets.publish_asset())

        self.cmds.file.assert_any_call(save=True)
        self.cmds.warning.assert_called_once_with(
            "The asset was saved, but its publish metadata could not be recorded. "
            "See the Script Editor for details."
        )
        self.cmds.confirmDialog.assert_not_called()

    def test_publish_asset_reports_an_incomplete_dependency_scan(self):
        self.cmds.file.side_effect = ["asset.ma", None]
        collection = SimpleNamespace(
            dependencies=(),
            errors=("Could not list scene references",),
        )
        with patch.object(
            maya_assets,
            "collect_dependencies",
            return_value=collection,
        ), patch.object(
            maya_assets,
            "record_publish",
            return_value={"versionLabel": "v003", "dependencyStatus": "incomplete"},
        ) as record_publish:
            self.assertTrue(maya_assets.publish_asset())

        record_publish.assert_called_once_with(
            "asset.ma",
            "asset",
            dependencies=(),
            dependency_errors=collection.errors,
        )
        self.cmds.warning.assert_called_once_with(
            "The asset was published with an incomplete dependency snapshot."
        )
        self.cmds.confirmDialog.assert_called_once_with(
            title="Publish complete",
            message=(
                "The asset was published successfully as v003. "
                "The dependency scan was incomplete; see the metadata pane."
            ),
            button=["OK"],
        )

    def test_publish_asset_stops_when_the_publish_lock_is_busy(self):
        self.cmds.file.return_value = "asset.ma"
        with patch.object(
            maya_assets,
            "publish_lock",
            side_effect=TimeoutError("busy"),
        ):
            with self.assertLogs(maya_assets.LOGGER, level="ERROR"):
                self.assertFalse(maya_assets.publish_asset())

        self.cmds.file.assert_called_once_with(query=True, sceneName=True)
        self.cmds.warning.assert_called_once_with(
            "Another publish is active or the asset publish lock is unavailable."
        )

    def test_publish_lock_covers_save_dependency_collection_and_metadata(self):
        events = []

        @contextmanager
        def tracked_lock(_path):
            events.append("lock entered")
            yield
            events.append("lock exited")

        def file_command(*_args, **kwargs):
            if kwargs.get("query") and kwargs.get("sceneName"):
                return "asset.ma"
            if kwargs.get("save"):
                events.append("saved")
            return None

        def collect(_path):
            events.append("dependencies collected")
            return SimpleNamespace(dependencies=(), errors=())

        def record(*_args, **_kwargs):
            events.append("metadata recorded")
            return {"versionLabel": "v001", "dependencyStatus": "complete"}

        self.cmds.file.side_effect = file_command
        with patch.object(
            maya_assets,
            "publish_lock",
            side_effect=tracked_lock,
        ), patch.object(
            maya_assets,
            "collect_dependencies",
            side_effect=collect,
        ), patch.object(
            maya_assets,
            "record_publish",
            side_effect=record,
        ):
            self.assertTrue(maya_assets.publish_asset())

        self.assertEqual(
            events,
            [
                "lock entered",
                "saved",
                "dependencies collected",
                "metadata recorded",
                "lock exited",
            ],
        )


if __name__ == "__main__":
    unittest.main()
