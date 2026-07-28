"""Maya application entry point."""

try:
    from maya import OpenMayaUI as omui

    from .ui.main_window import MainWindow
    from .ui.qt import QWidget, wrapInstance
except ImportError as error:
    omui = None
    MainWindow = None
    QWidget = None
    wrapInstance = None
    _IMPORT_ERROR = error
else:
    _IMPORT_ERROR = None


def run(config=None):
    """Create and show JAM parented to Maya's main window."""
    if _IMPORT_ERROR is not None:
        raise RuntimeError(
            "JAM must run inside Maya with a supported PySide binding"
        ) from _IMPORT_ERROR

    maya_window_pointer = omui.MQtUtil.mainWindow()
    if maya_window_pointer is None:
        raise RuntimeError("Maya's main window is unavailable")

    maya_window = wrapInstance(int(maya_window_pointer), QWidget)
    window = MainWindow(parent=maya_window, config=config)
    window.show()
    return window
