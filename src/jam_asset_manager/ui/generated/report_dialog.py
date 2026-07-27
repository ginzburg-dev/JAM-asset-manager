# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'report_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from ..qt import (
    QApplication, QBrush, QColor, QConicalGradient, QCoreApplication, QCursor,
    QDate, QDateTime, QFont, QFontDatabase, QGradient, QHBoxLayout,
    QHeaderView, QIcon, QImage, QKeySequence, QLabel, QLayout, QLineEdit,
    QLinearGradient, QLocale, QMainWindow, QMenuBar, QMetaObject, QObject,
    QPainter, QPalette, QPixmap, QPoint, QPushButton, QRadialGradient, QRect,
    QSize, QSizePolicy, QSizePolicyPolicy, QSpacerItem, QSpinBox, QStatusBar,
    QTextEdit, QTime, QTransform, QTreeWidget, QTreeWidgetItem, QUrl,
    QVBoxLayout, QWidget, Qt,
)

class Ui_ReportDialog(object):
    def setupUi(self, report_dialog):
        if not report_dialog.objectName():
            report_dialog.setObjectName(u"ReportDialog")
        report_dialog.resize(553, 401)
        report_dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        report_dialog.setAcceptDrops(True)
        report_dialog.setToolButtonStyle(Qt.ToolButtonIconOnly)
        report_dialog.setDocumentMode(False)
        report_dialog.setDockNestingEnabled(False)
        report_dialog.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)
        report_dialog.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(report_dialog)
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
        sizePolicy = QSizePolicy(QSizePolicyPolicy.Expanding, QSizePolicyPolicy.Expanding)
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

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicyPolicy.Expanding, QSizePolicyPolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.verticalLayoutWidget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.verticalLayoutWidget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        report_dialog.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(report_dialog)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 553, 24))
        report_dialog.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(report_dialog)
        self.statusbar.setObjectName(u"statusbar")
        report_dialog.setStatusBar(self.statusbar)

        self.retranslateUi(report_dialog)

        QMetaObject.connectSlotsByName(report_dialog)
    # setupUi

    def retranslateUi(self, report_dialog):
        report_dialog.setWindowTitle(QCoreApplication.translate("ReportDialog", u"Create report", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("ReportDialog", u"Upload progress", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("ReportDialog", u"Path", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("ReportDialog", u"Preview", None));
        self.label.setText(QCoreApplication.translate("ReportDialog", u"Hours", None))
        self.pushButton_ok.setText(QCoreApplication.translate("ReportDialog", u"OK", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("ReportDialog", u"Cancel", None))
    # retranslateUi
