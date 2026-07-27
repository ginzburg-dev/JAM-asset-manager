"""Unit tests for Maya asset operations using a mocked command layer."""

import importlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from tests.support import install_maya_stubs

install_maya_stubs()

maya_assets = importlib.import_module("jam_asset_manager.maya.assets")


class MayaAssetTestCase(unittest.TestCase):
    def setUp(self):
        self.cmds = MagicMock()
        self.cmds_patcher = patch.object(maya_assets, "cmds", self.cmds)
        self.cmds_patcher.start()

    def tearDown(self):
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
        self.assertTrue(maya_assets.publish_asset())
        self.assertEqual(self.cmds.file.call_count, 2)
        self.cmds.file.assert_any_call(save=True)
        self.cmds.confirmDialog.assert_called_once_with(
            title="Publish complete",
            message="The asset was published successfully.",
            button=["OK"],
        )


if __name__ == "__main__":
    unittest.main()
