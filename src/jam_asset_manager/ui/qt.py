"""Qt compatibility imports for supported Maya versions."""

# ruff: noqa: F401, I001

try:
    from PySide6.QtCore import (
        QCoreApplication,
        QDate,
        QDateTime,
        QLocale,
        QMetaObject,
        QObject,
        QPoint,
        QRect,
        QSize,
        QTime,
        QUrl,
        Qt,
    )
    from PySide6.QtGui import (
        QAction,
        QBrush,
        QColor,
        QConicalGradient,
        QCursor,
        QFont,
        QFontDatabase,
        QGradient,
        QIcon,
        QImage,
        QKeySequence,
        QLinearGradient,
        QPainter,
        QPalette,
        QPixmap,
        QRadialGradient,
        QTransform,
    )
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QAbstractScrollArea,
        QApplication,
        QComboBox,
        QFrame,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QLayout,
        QLineEdit,
        QListView,
        QListWidget,
        QListWidgetItem,
        QMainWindow,
        QMenu,
        QMenuBar,
        QPushButton,
        QSizePolicy,
        QSpacerItem,
        QSpinBox,
        QSplitter,
        QStatusBar,
        QTabWidget,
        QTableWidget,
        QTableWidgetItem,
        QTextBrowser,
        QTextEdit,
        QToolButton,
        QTreeWidget,
        QTreeWidgetItem,
        QVBoxLayout,
        QWidget,
    )
    from shiboken6 import wrapInstance
except ImportError:
    from PySide2.QtCore import (
        QCoreApplication,
        QDate,
        QDateTime,
        QLocale,
        QMetaObject,
        QObject,
        QPoint,
        QRect,
        QSize,
        QTime,
        QUrl,
        Qt,
    )
    from PySide2.QtGui import (
        QBrush,
        QColor,
        QConicalGradient,
        QCursor,
        QFont,
        QFontDatabase,
        QGradient,
        QIcon,
        QImage,
        QKeySequence,
        QLinearGradient,
        QPainter,
        QPalette,
        QPixmap,
        QRadialGradient,
        QTransform,
    )
    from PySide2.QtWidgets import (
        QAction,
        QAbstractItemView,
        QAbstractScrollArea,
        QApplication,
        QComboBox,
        QFrame,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QLayout,
        QLineEdit,
        QListView,
        QListWidget,
        QListWidgetItem,
        QMainWindow,
        QMenu,
        QMenuBar,
        QPushButton,
        QSizePolicy,
        QSpacerItem,
        QSpinBox,
        QSplitter,
        QStatusBar,
        QTabWidget,
        QTableWidget,
        QTableWidgetItem,
        QTextBrowser,
        QTextEdit,
        QToolButton,
        QTreeWidget,
        QTreeWidgetItem,
        QVBoxLayout,
        QWidget,
    )
    from shiboken2 import wrapInstance


def _enum_container(owner, scoped_name):
    return getattr(owner, scoped_name, owner)


QSizePolicyPolicy = _enum_container(QSizePolicy, "Policy")
MATCH_EXACTLY = _enum_container(Qt, "MatchFlag").MatchExactly
ASCENDING_ORDER = _enum_container(Qt, "SortOrder").AscendingOrder
POSITION_AT_TOP = _enum_container(QAbstractItemView, "ScrollHint").PositionAtTop
