"""Tests for UI dependency injection without requiring Maya or Qt."""

import importlib
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from tests.support import install_maya_stubs, install_qt_stubs

install_maya_stubs()
install_qt_stubs()

jam_asset_manager = importlib.import_module("jam_asset_manager")


class EntrypointTestCase(unittest.TestCase):
    def test_run_injects_config_and_parents_window_to_maya(self):
        config = object()
        maya_parent = object()
        window = MagicMock()
        omui = SimpleNamespace(MQtUtil=SimpleNamespace(mainWindow=MagicMock(return_value=123)))

        with patch.object(jam_asset_manager, "omui", omui), patch.object(
            jam_asset_manager, "wrapInstance", return_value=maya_parent
        ) as wrap_instance, patch.object(
            jam_asset_manager, "MainWindow", return_value=window
        ) as main_window:
            result = jam_asset_manager.jam_asset_manager_run(config=config)

        self.assertIs(result, window)
        wrap_instance.assert_called_once_with(123, jam_asset_manager.QWidget)
        main_window.assert_called_once_with(parent=maya_parent, config=config)
        window.show.assert_called_once_with()

    def test_run_fails_clearly_when_maya_window_is_unavailable(self):
        omui = SimpleNamespace(MQtUtil=SimpleNamespace(mainWindow=MagicMock(return_value=None)))
        with patch.object(jam_asset_manager, "omui", omui):
            with self.assertRaisesRegex(RuntimeError, "unavailable"):
                jam_asset_manager.jam_asset_manager_run(config=object())

    def test_legacy_helpers_accept_explicit_config_without_global_state(self):
        project = SimpleNamespace(root="/projects/demo", episode_path="episodes")
        application = SimpleNamespace(allowed_extensions=("ma",))
        config = SimpleNamespace(
            application=application,
            project=lambda name: project if name == "Demo" else None,
        )
        self.assertEqual(jam_asset_manager.getProjectPath("Demo", config), "/projects/demo")
        self.assertEqual(jam_asset_manager.getEpisodePath("Demo", config), "episodes")
        self.assertTrue(jam_asset_manager.isAllowedExtension("scene.MA", config))
        self.assertFalse(jam_asset_manager.isAllowedExtension("notes.txt", config))


if __name__ == "__main__":
    unittest.main()
