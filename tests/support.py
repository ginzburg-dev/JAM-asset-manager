"""Test-only module stubs for optional Maya and Qt dependencies."""

import sys
import types


class Placeholder:
    """Import-compatible stand-in for Qt classes used only at runtime."""


class DynamicModule(types.ModuleType):
    def __getattr__(self, _name):
        return Placeholder


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
    """Install import-only PySide2 and shiboken2 modules outside Maya."""
    pyside = sys.modules.get("PySide2")
    if pyside is None:
        pyside = DynamicModule("PySide2")
        pyside.__path__ = []
        sys.modules["PySide2"] = pyside

    for child_name in ("QtCore", "QtGui", "QtWidgets"):
        qualified_name = "PySide2." + child_name
        child = sys.modules.get(qualified_name)
        if child is None:
            child = DynamicModule(qualified_name)
            sys.modules[qualified_name] = child
        setattr(pyside, child_name, child)

    if "shiboken2" not in sys.modules:
        sys.modules["shiboken2"] = DynamicModule("shiboken2")
