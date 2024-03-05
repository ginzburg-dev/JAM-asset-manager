# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'report.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_report(object):
    def setupUi(self, report):
        if not report.objectName():
            report.setObjectName(u"report")
        report.resize(553, 401)
        report.setContextMenuPolicy(Qt.DefaultContextMenu)
        report.setAcceptDrops(True)
        report.setToolButtonStyle(Qt.ToolButtonIconOnly)
        report.setDocumentMode(False)
        report.setDockNestingEnabled(False)
        report.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)
        report.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(report)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setContextMenuPolicy(Qt.NoContextMenu)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 2, 531, 371))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
#ifndef Q_OS_MAC
        self.horizontalLayout_2.setSpacing(-1)
#endif
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 5)
        self.lineEdit = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)
        self.lineEdit.setFocusPolicy(Qt.NoFocus)
        self.lineEdit.setFrame(True)

        self.horizontalLayout_2.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.textEdit_maintext = QTextEdit(self.verticalLayoutWidget)
        self.textEdit_maintext.setObjectName(u"textEdit_maintext")

        self.verticalLayout.addWidget(self.textEdit_maintext)

        self.treeWidget = QTreeWidget(self.verticalLayoutWidget)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.header().setVisible(True)

        self.verticalLayout.addWidget(self.treeWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox_hours = QSpinBox(self.verticalLayoutWidget)
        self.spinBox_hours.setObjectName(u"spinBox_hours")
        self.spinBox_hours.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.spinBox_hours)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.verticalLayoutWidget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.verticalLayoutWidget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        report.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(report)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 553, 24))
        report.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(report)
        self.statusbar.setObjectName(u"statusbar")
        report.setStatusBar(self.statusbar)

        self.retranslateUi(report)

        QMetaObject.connectSlotsByName(report)
    # setupUi

    def retranslateUi(self, report):
        report.setWindowTitle(QCoreApplication.translate("report", u"Create report", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("report", u"Upload progress", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("report", u"Path", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("report", u"Preview", None));
        self.label.setText(QCoreApplication.translate("report", u"Hours", None))
        self.pushButton_ok.setText(QCoreApplication.translate("report", u"OK", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("report", u"Cancel", None))
    # retranslateUi

