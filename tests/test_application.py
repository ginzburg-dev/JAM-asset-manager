"""Tests for UI dependency injection without requiring Maya or Qt."""

import importlib
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from tests.support import install_maya_stubs, install_qt_stubs

install_maya_stubs()
install_qt_stubs()

application = importlib.import_module("jam_asset_manager.application")
main_window = importlib.import_module("jam_asset_manager.ui.main_window")
report_dialog = importlib.import_module("jam_asset_manager.ui.report_dialog")


class ApplicationTestCase(unittest.TestCase):
    def test_run_injects_config_and_parents_window_to_maya(self):
        config = object()
        maya_parent = object()
        window = MagicMock()
        omui = SimpleNamespace(MQtUtil=SimpleNamespace(mainWindow=MagicMock(return_value=123)))

        with patch.object(application, "omui", omui), patch.object(
            application, "wrapInstance", return_value=maya_parent
        ) as wrap_instance, patch.object(
            application, "MainWindow", return_value=window
        ) as main_window:
            result = application.run(config=config)

        self.assertIs(result, window)
        wrap_instance.assert_called_once_with(123, application.QWidget)
        main_window.assert_called_once_with(parent=maya_parent, config=config)
        window.show.assert_called_once_with()

    def test_run_fails_clearly_when_maya_window_is_unavailable(self):
        omui = SimpleNamespace(MQtUtil=SimpleNamespace(mainWindow=MagicMock(return_value=None)))
        with patch.object(application, "omui", omui):
            with self.assertRaisesRegex(RuntimeError, "unavailable"):
                application.run(config=object())

    def test_ui_helpers_require_explicit_config(self):
        project = SimpleNamespace(root="/projects/demo", episode_path="episodes")
        application_config = SimpleNamespace(allowed_extensions=("ma",))
        config = SimpleNamespace(
            application=application_config,
            project=lambda name: project if name == "Demo" else None,
        )
        self.assertEqual(main_window.get_project_path("Demo", config), "/projects/demo")
        self.assertEqual(main_window.get_episode_path("Demo", config), "episodes")
        self.assertTrue(main_window.is_allowed_asset("scene.MA", config))
        self.assertFalse(main_window.is_allowed_asset("notes.txt", config))

    def test_asset_tree_does_not_follow_directory_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "nested"
            nested.mkdir()
            try:
                os.symlink(str(root), str(nested / "loop"))
            except OSError as error:
                self.skipTest("Directory symlinks are unavailable: {}".format(error))

            with patch.object(
                main_window, "QTreeWidgetItem", MagicMock()
            ) as item_class, patch.object(
                main_window,
                "_icon",
                return_value=object(),
            ):
                main_window.load_project_structure(str(root), object())

            self.assertEqual(item_class.call_count, 1)

    def test_check_dispatches_to_the_current_element_type(self):
        window = SimpleNamespace(
            is_scene_path=lambda _path: False,
            is_asset_path=lambda _path: True,
        )
        with patch.object(
            main_window.maya_scenes,
            "get_current_scene_path",
            return_value="/project/assets/model.ma",
        ), patch.object(
            main_window.maya_assets,
            "check_asset",
            return_value=True,
        ) as check_asset:
            self.assertTrue(main_window.MainWindow.check_element(window))
        check_asset.assert_called_once_with()

    def test_report_dialog_keeps_its_original_target(self):
        dialog = object.__new__(report_dialog.ReportDialog)
        dialog.selected_item = ("original", "/assets/original.ma")
        dialog.message_type = "note"
        dialog.ui = SimpleNamespace(
            textEdit_maintext=SimpleNamespace(toPlainText=lambda: "Looks good"),
            spinBox_hours=SimpleNamespace(value=lambda: 0),
        )
        dialog.close = MagicMock()
        parent = SimpleNamespace(
            get_selected_item_data=lambda: ["changed", "/assets/changed.ma"],
            update_report_note=MagicMock(),
        )

        with patch.object(report_dialog, "append_message") as append_message:
            dialog.submit(parent)

        append_message.assert_called_once_with(
            "/assets/original.ma",
            "original",
            "note",
            "Looks good",
            0,
        )
        parent.update_report_note.assert_called_once_with()
        dialog.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
