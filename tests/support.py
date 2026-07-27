"""Test-only module stubs for optional Maya and Qt dependencies."""

import sys
import tempfile
import types
import unittest
from pathlib import Path

from jam_asset_manager.core.storage import write_json


class Placeholder:
    """Import-compatible stand-in for Qt classes used only at runtime."""


class DynamicModule(types.ModuleType):
    def __getattr__(self, _name):
        return Placeholder


class TemporaryProjectTestCase(unittest.TestCase):
    """Base case with an isolated project configuration."""

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


def install_maya_stubs():
    """Install minimal Maya modules when tests run outside Autodesk Maya."""
    maya = sys.modules.get("maya")
    if maya is None:
        maya = DynamicModule("maya")
        maya.__path__ = []
        sys.modules["maya"] = maya

    for child_name in ("cmds", "mel", "OpenMayaUI"):
        qualified_name = "maya." + child_name
        child = sys.modules.get(qualified_name)
        if child is None:
            child = DynamicModule(qualified_name)
            sys.modules[qualified_name] = child
        setattr(maya, child_name, child)


def install_qt_stubs():
    """Install import-only PySide and shiboken modules outside Maya."""
    for binding_name in ("PySide6", "PySide2"):
        pyside = DynamicModule(binding_name)
        pyside.__path__ = []
        sys.modules[binding_name] = pyside

        for child_name in ("QtCore", "QtGui", "QtWidgets"):
            qualified_name = binding_name + "." + child_name
            child = DynamicModule(qualified_name)
            sys.modules[qualified_name] = child
            setattr(pyside, child_name, child)

    for module_name in ("shiboken6", "shiboken2"):
        sys.modules[module_name] = DynamicModule(module_name)
