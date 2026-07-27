"""Maya application entry point."""

from maya import OpenMayaUI as omui

from .ui.main_window import MainWindow
from .ui.qt import QWidget, wrapInstance


def run(config=None):
    """Create and show JAM parented to Maya's main window."""
    maya_window_pointer = omui.MQtUtil.mainWindow()
    if maya_window_pointer is None:
        raise RuntimeError("Maya's main window is unavailable")

    maya_window = wrapInstance(int(maya_window_pointer), QWidget)
    window = MainWindow(parent=maya_window, config=config)
    window.show()
    return window
