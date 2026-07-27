"""Tests for UI dependency injection without requiring Maya or Qt."""

import importlib
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from tests.support import install_maya_stubs, install_qt_stubs

install_maya_stubs()
install_qt_stubs()

application = importlib.import_module("jam_asset_manager.application")
main_window = importlib.import_module("jam_asset_manager.ui.main_window")


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


if __name__ == "__main__":
    unittest.main()
