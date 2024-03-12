# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'jam.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide2.QtWidgets import (QAction, QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QListView, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextBrowser,
    QToolButton, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_jam(object):
    def setupUi(self, jam):
        if not jam.objectName():
            jam.setObjectName(u"jam")
        jam.setWindowModality(Qt.NonModal)
        jam.resize(1105, 581)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(jam.sizePolicy().hasHeightForWidth())
        jam.setSizePolicy(sizePolicy)
        jam.setMinimumSize(QSize(1105, 581))
        jam.setMaximumSize(QSize(1105, 16777215))
        jam.setAcceptDrops(True)
        icon = QIcon()
        icon.addFile(u"icons/check.png", QSize(), QIcon.Normal, QIcon.Off)
        jam.setWindowIcon(icon)
        jam.setStyleSheet(u"")
        jam.setIconSize(QSize(64, 64))
        jam.setToolButtonStyle(Qt.ToolButtonIconOnly)
        jam.setAnimated(False)
        jam.setDocumentMode(False)
        jam.setTabShape(QTabWidget.Rounded)
        jam.setDockNestingEnabled(False)
        jam.setUnifiedTitleAndToolBarOnMac(False)
        self.actionNewScene = QAction(jam)
        self.actionNewScene.setObjectName(u"actionNewScene")
        self.actionUpdate = QAction(jam)
        self.actionUpdate.setObjectName(u"actionUpdate")
        self.actionPublish = QAction(jam)
        self.actionPublish.setObjectName(u"actionPublish")
        self.actionImport = QAction(jam)
        self.actionImport.setObjectName(u"actionImport")
        self.actionDenoise = QAction(jam)
        self.actionDenoise.setObjectName(u"actionDenoise")
        self.actionCheck = QAction(jam)
        self.actionCheck.setObjectName(u"actionCheck")
        self.actionRenderManager = QAction(jam)
        self.actionRenderManager.setObjectName(u"actionRenderManager")
        self.actionDenoise_2 = QAction(jam)
        self.actionDenoise_2.setObjectName(u"actionDenoise_2")
        self.actionBake = QAction(jam)
        self.actionBake.setObjectName(u"actionBake")
        self.actionRenderManager_2 = QAction(jam)
        self.actionRenderManager_2.setObjectName(u"actionRenderManager_2")
        self.actionDenoise_3 = QAction(jam)
        self.actionDenoise_3.setObjectName(u"actionDenoise_3")
        self.actionRender_Manager = QAction(jam)
        self.actionRender_Manager.setObjectName(u"actionRender_Manager")
        self.actionOptimizer = QAction(jam)
        self.actionOptimizer.setObjectName(u"actionOptimizer")
        self.actionOpen = QAction(jam)
        self.actionOpen.setObjectName(u"actionOpen")
        self.centralwidget = QWidget(jam)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 0, 791, 531))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout_3.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 5)
        self.toolButton_newScene = QToolButton(self.verticalLayoutWidget_3)
        self.toolButton_newScene.setObjectName(u"toolButton_newScene")
        sizePolicy.setHeightForWidth(self.toolButton_newScene.sizePolicy().hasHeightForWidth())
        self.toolButton_newScene.setSizePolicy(sizePolicy)
        self.toolButton_newScene.setMinimumSize(QSize(80, 70))
        self.toolButton_newScene.setMaximumSize(QSize(80, 70))
        self.toolButton_newScene.setBaseSize(QSize(0, 0))
        self.toolButton_newScene.setFocusPolicy(Qt.NoFocus)
        self.toolButton_newScene.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.toolButton_newScene.setLayoutDirection(Qt.LeftToRight)
        self.toolButton_newScene.setAutoFillBackground(False)
        self.toolButton_newScene.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        icon1 = QIcon()
        icon1.addFile(u"../icons/new_scene.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_newScene.setIcon(icon1)
        self.toolButton_newScene.setIconSize(QSize(40, 40))
        self.toolButton_newScene.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolButton_newScene.setAutoRaise(False)

        self.horizontalLayout_2.addWidget(self.toolButton_newScene)

        self.toolButton_update = QToolButton(self.verticalLayoutWidget_3)
        self.toolButton_update.setObjectName(u"toolButton_update")
        sizePolicy.setHeightForWidth(self.toolButton_update.sizePolicy().hasHeightForWidth())
        self.toolButton_update.setSizePolicy(sizePolicy)
        self.toolButton_update.setMinimumSize(QSize(80, 70))
        self.toolButton_update.setMaximumSize(QSize(80, 70))
        self.toolButton_update.setFocusPolicy(Qt.NoFocus)
        self.toolButton_update.setAutoFillBackground(False)
        self.toolButton_update.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        icon2 = QIcon()
        icon2.addFile(u"../icons/update.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_update.setIcon(icon2)
        self.toolButton_update.setIconSize(QSize(40, 40))
        self.toolButton_update.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.horizontalLayout_2.addWidget(self.toolButton_update)

        self.toolButton_import = QToolButton(self.verticalLayoutWidget_3)
        self.toolButton_import.setObjectName(u"toolButton_import")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.toolButton_import.sizePolicy().hasHeightForWidth())
        self.toolButton_import.setSizePolicy(sizePolicy1)
        self.toolButton_import.setMinimumSize(QSize(80, 70))
        self.toolButton_import.setMaximumSize(QSize(80, 70))
        self.toolButton_import.setBaseSize(QSize(0, 0))
        self.toolButton_import.setFocusPolicy(Qt.NoFocus)
        self.toolButton_import.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        self.toolButton_import.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        icon3 = QIcon()
        icon3.addFile(u"../icons/import.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_import.setIcon(icon3)
        self.toolButton_import.setIconSize(QSize(40, 40))
        self.toolButton_import.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.horizontalLayout_2.addWidget(self.toolButton_import)

        self.toolButton_publish = QToolButton(self.verticalLayoutWidget_3)
        self.toolButton_publish.setObjectName(u"toolButton_publish")
        sizePolicy1.setHeightForWidth(self.toolButton_publish.sizePolicy().hasHeightForWidth())
        self.toolButton_publish.setSizePolicy(sizePolicy1)
        self.toolButton_publish.setMinimumSize(QSize(80, 70))
        self.toolButton_publish.setMaximumSize(QSize(80, 70))
        self.toolButton_publish.setBaseSize(QSize(0, 0))
        self.toolButton_publish.setFocusPolicy(Qt.NoFocus)
        self.toolButton_publish.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        icon4 = QIcon()
        icon4.addFile(u"../icons/publish.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_publish.setIcon(icon4)
        self.toolButton_publish.setIconSize(QSize(43, 43))
        self.toolButton_publish.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.horizontalLayout_2.addWidget(self.toolButton_publish)

        self.toolButton_check = QToolButton(self.verticalLayoutWidget_3)
        self.toolButton_check.setObjectName(u"toolButton_check")
        sizePolicy1.setHeightForWidth(self.toolButton_check.sizePolicy().hasHeightForWidth())
        self.toolButton_check.setSizePolicy(sizePolicy1)
        self.toolButton_check.setMinimumSize(QSize(80, 70))
        self.toolButton_check.setMaximumSize(QSize(80, 70))
        self.toolButton_check.setBaseSize(QSize(0, 0))
        self.toolButton_check.setFocusPolicy(Qt.NoFocus)
        self.toolButton_check.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        icon5 = QIcon()
        icon5.addFile(u"../icons/check.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_check.setIcon(icon5)
        self.toolButton_check.setIconSize(QSize(40, 40))
        self.toolButton_check.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.horizontalLayout_2.addWidget(self.toolButton_check)

        self.toolButton_denoise = QToolButton(self.verticalLayoutWidget_3)
        self.toolButton_denoise.setObjectName(u"toolButton_denoise")
        sizePolicy1.setHeightForWidth(self.toolButton_denoise.sizePolicy().hasHeightForWidth())
        self.toolButton_denoise.setSizePolicy(sizePolicy1)
        self.toolButton_denoise.setMinimumSize(QSize(80, 70))
        self.toolButton_denoise.setMaximumSize(QSize(80, 70))
        self.toolButton_denoise.setBaseSize(QSize(0, 0))
        self.toolButton_denoise.setFocusPolicy(Qt.NoFocus)
        self.toolButton_denoise.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        icon6 = QIcon()
        icon6.addFile(u"../icons/denoise.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_denoise.setIcon(icon6)
        self.toolButton_denoise.setIconSize(QSize(40, 40))
        self.toolButton_denoise.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolButton_denoise.setAutoRaise(False)

        self.horizontalLayout_2.addWidget(self.toolButton_denoise)

        self.toolButton_statistics = QToolButton(self.verticalLayoutWidget_3)
        self.toolButton_statistics.setObjectName(u"toolButton_statistics")
        sizePolicy1.setHeightForWidth(self.toolButton_statistics.sizePolicy().hasHeightForWidth())
        self.toolButton_statistics.setSizePolicy(sizePolicy1)
        self.toolButton_statistics.setMinimumSize(QSize(80, 70))
        self.toolButton_statistics.setMaximumSize(QSize(80, 70))
        self.toolButton_statistics.setBaseSize(QSize(0, 0))
        self.toolButton_statistics.setFocusPolicy(Qt.NoFocus)
        self.toolButton_statistics.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        icon7 = QIcon()
        icon7.addFile(u"../icons/statistics.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_statistics.setIcon(icon7)
        self.toolButton_statistics.setIconSize(QSize(40, 40))
        self.toolButton_statistics.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolButton_statistics.setAutoRaise(False)

        self.horizontalLayout_2.addWidget(self.toolButton_statistics)

        self.horizontalSpacer_mainPanel = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_mainPanel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.line = QFrame(self.verticalLayoutWidget_3)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 5, -1, -1)
        self.lineEdit_fullPath = QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_fullPath.setObjectName(u"lineEdit_fullPath")
        self.lineEdit_fullPath.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_fullPath.setClearButtonEnabled(False)

        self.horizontalLayout_5.addWidget(self.lineEdit_fullPath)

        self.toolButton_goto = QToolButton(self.verticalLayoutWidget_3)
        self.toolButton_goto.setObjectName(u"toolButton_goto")
        self.toolButton_goto.setFocusPolicy(Qt.ClickFocus)
        self.toolButton_goto.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        icon8 = QIcon()
        icon8.addFile(u"../icons/goto.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_goto.setIcon(icon8)

        self.horizontalLayout_5.addWidget(self.toolButton_goto)

        self.toolButton_copyClipboard = QToolButton(self.verticalLayoutWidget_3)
        self.toolButton_copyClipboard.setObjectName(u"toolButton_copyClipboard")
        self.toolButton_copyClipboard.setFocusPolicy(Qt.ClickFocus)
        self.toolButton_copyClipboard.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        icon9 = QIcon()
        icon9.addFile(u"../icons/clipboard.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_copyClipboard.setIcon(icon9)

        self.horizontalLayout_5.addWidget(self.toolButton_copyClipboard)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 5, -1, 5)
        self.label_projName = QLabel(self.verticalLayoutWidget_3)
        self.label_projName.setObjectName(u"label_projName")
        sizePolicy.setHeightForWidth(self.label_projName.sizePolicy().hasHeightForWidth())
        self.label_projName.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_projName)

        self.comboBox_projName = QComboBox(self.verticalLayoutWidget_3)
        self.comboBox_projName.addItem("")
        self.comboBox_projName.addItem("")
        self.comboBox_projName.addItem("")
        self.comboBox_projName.setObjectName(u"comboBox_projName")

        self.horizontalLayout.addWidget(self.comboBox_projName)

        self.horizontalSpacer_projName = QSpacerItem(600, 10, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_projName)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(self.verticalLayoutWidget_3)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setElideMode(Qt.ElideRight)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayoutWidget_2 = QWidget(self.tab)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 791, 381))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(5)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_8.setContentsMargins(5, 0, 0, 0)
        self.lineEdit_filter = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_filter.setObjectName(u"lineEdit_filter")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_filter.sizePolicy().hasHeightForWidth())
        self.lineEdit_filter.setSizePolicy(sizePolicy2)
        self.lineEdit_filter.setFocusPolicy(Qt.ClickFocus)

        self.horizontalLayout_8.addWidget(self.lineEdit_filter)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_7.setContentsMargins(5, 0, 0, 0)
        self.toolButton_aImport = QToolButton(self.verticalLayoutWidget_2)
        self.toolButton_aImport.setObjectName(u"toolButton_aImport")
        sizePolicy.setHeightForWidth(self.toolButton_aImport.sizePolicy().hasHeightForWidth())
        self.toolButton_aImport.setSizePolicy(sizePolicy)
        self.toolButton_aImport.setMinimumSize(QSize(0, 0))
        self.toolButton_aImport.setMaximumSize(QSize(70, 25))
        self.toolButton_aImport.setFocusPolicy(Qt.NoFocus)
        self.toolButton_aImport.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        self.toolButton_aImport.setIcon(icon3)
        self.toolButton_aImport.setIconSize(QSize(20, 20))
        self.toolButton_aImport.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_7.addWidget(self.toolButton_aImport)

        self.toolButton_aPublish = QToolButton(self.verticalLayoutWidget_2)
        self.toolButton_aPublish.setObjectName(u"toolButton_aPublish")
        sizePolicy.setHeightForWidth(self.toolButton_aPublish.sizePolicy().hasHeightForWidth())
        self.toolButton_aPublish.setSizePolicy(sizePolicy)
        self.toolButton_aPublish.setMaximumSize(QSize(70, 25))
        self.toolButton_aPublish.setFocusPolicy(Qt.NoFocus)
        self.toolButton_aPublish.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        self.toolButton_aPublish.setIcon(icon4)
        self.toolButton_aPublish.setIconSize(QSize(20, 20))
        self.toolButton_aPublish.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_7.addWidget(self.toolButton_aPublish)

        self.horizontalSpacer_4 = QSpacerItem(100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.toolButton_aRefresh = QToolButton(self.verticalLayoutWidget_2)
        self.toolButton_aRefresh.setObjectName(u"toolButton_aRefresh")
        sizePolicy.setHeightForWidth(self.toolButton_aRefresh.sizePolicy().hasHeightForWidth())
        self.toolButton_aRefresh.setSizePolicy(sizePolicy)
        self.toolButton_aRefresh.setMaximumSize(QSize(70, 25))
        self.toolButton_aRefresh.setFocusPolicy(Qt.NoFocus)
        self.toolButton_aRefresh.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        icon10 = QIcon()
        icon10.addFile(u"../icons/refresh.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_aRefresh.setIcon(icon10)
        self.toolButton_aRefresh.setIconSize(QSize(20, 30))
        self.toolButton_aRefresh.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_7.addWidget(self.toolButton_aRefresh)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.splitter_2 = QSplitter(self.verticalLayoutWidget_2)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy3)
        self.splitter_2.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.splitter_2.setOpaqueResize(True)
        self.splitter_2.setChildrenCollapsible(True)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.comboBox_aTypes = QComboBox(self.layoutWidget)
        self.comboBox_aTypes.addItem("")
        self.comboBox_aTypes.addItem("")
        self.comboBox_aTypes.addItem("")
        self.comboBox_aTypes.addItem("")
        self.comboBox_aTypes.setObjectName(u"comboBox_aTypes")
        sizePolicy2.setHeightForWidth(self.comboBox_aTypes.sizePolicy().hasHeightForWidth())
        self.comboBox_aTypes.setSizePolicy(sizePolicy2)
        self.comboBox_aTypes.setBaseSize(QSize(0, 0))
        self.comboBox_aTypes.setFocusPolicy(Qt.NoFocus)
        self.comboBox_aTypes.setEditable(False)
        self.comboBox_aTypes.setDuplicatesEnabled(False)
        self.comboBox_aTypes.setFrame(True)

        self.verticalLayout.addWidget(self.comboBox_aTypes)

        self.lineEdit_aFilter = QLineEdit(self.layoutWidget)
        self.lineEdit_aFilter.setObjectName(u"lineEdit_aFilter")
        sizePolicy2.setHeightForWidth(self.lineEdit_aFilter.sizePolicy().hasHeightForWidth())
        self.lineEdit_aFilter.setSizePolicy(sizePolicy2)
        self.lineEdit_aFilter.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_aFilter.setDragEnabled(False)
        self.lineEdit_aFilter.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.lineEdit_aFilter)

        self.treeWidget_assetFolders = QTreeWidget(self.layoutWidget)
        __qtreewidgetitem = QTreeWidgetItem(self.treeWidget_assetFolders)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem2 = QTreeWidgetItem(self.treeWidget_assetFolders)
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3 = QTreeWidgetItem(self.treeWidget_assetFolders)
        QTreeWidgetItem(__qtreewidgetitem3)
        __qtreewidgetitem4 = QTreeWidgetItem(self.treeWidget_assetFolders)
        QTreeWidgetItem(__qtreewidgetitem4)
        QTreeWidgetItem(__qtreewidgetitem4)
        __qtreewidgetitem5 = QTreeWidgetItem(self.treeWidget_assetFolders)
        QTreeWidgetItem(__qtreewidgetitem5)
        __qtreewidgetitem6 = QTreeWidgetItem(self.treeWidget_assetFolders)
        QTreeWidgetItem(__qtreewidgetitem6)
        QTreeWidgetItem(__qtreewidgetitem6)
        QTreeWidgetItem(self.treeWidget_assetFolders)
        self.treeWidget_assetFolders.setObjectName(u"treeWidget_assetFolders")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.treeWidget_assetFolders.sizePolicy().hasHeightForWidth())
        self.treeWidget_assetFolders.setSizePolicy(sizePolicy4)
        self.treeWidget_assetFolders.setMaximumSize(QSize(16777215, 16777215))
        self.treeWidget_assetFolders.setFocusPolicy(Qt.NoFocus)
        self.treeWidget_assetFolders.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.treeWidget_assetFolders.setProperty("showDropIndicator", True)
        self.treeWidget_assetFolders.setDragEnabled(False)
        self.treeWidget_assetFolders.setSelectionMode(QAbstractItemView.SingleSelection)
        self.treeWidget_assetFolders.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.treeWidget_assetFolders.setRootIsDecorated(True)
        self.treeWidget_assetFolders.setItemsExpandable(True)
        self.treeWidget_assetFolders.setExpandsOnDoubleClick(True)
        self.treeWidget_assetFolders.header().setVisible(False)
        self.treeWidget_assetFolders.header().setMinimumSectionSize(19)
        self.treeWidget_assetFolders.header().setDefaultSectionSize(100)
        self.treeWidget_assetFolders.header().setProperty("showSortIndicator", False)
        self.treeWidget_assetFolders.header().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.treeWidget_assetFolders)

        self.splitter_2.addWidget(self.layoutWidget)
        self.listWidget_assets = QListWidget(self.splitter_2)
        self.listWidget_assets.setObjectName(u"listWidget_assets")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(2)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.listWidget_assets.sizePolicy().hasHeightForWidth())
        self.listWidget_assets.setSizePolicy(sizePolicy5)
        self.listWidget_assets.setMinimumSize(QSize(0, 0))
        self.listWidget_assets.setBaseSize(QSize(0, 0))
        self.listWidget_assets.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.listWidget_assets.setProperty("isWrapping", True)
        self.listWidget_assets.setResizeMode(QListView.Adjust)
        self.listWidget_assets.setLayoutMode(QListView.SinglePass)
        self.listWidget_assets.setSpacing(15)
        self.listWidget_assets.setViewMode(QListView.IconMode)
        self.listWidget_assets.setUniformItemSizes(False)
        self.listWidget_assets.setSelectionRectVisible(True)
        self.listWidget_assets.setSortingEnabled(False)
        self.splitter_2.addWidget(self.listWidget_assets)

        self.verticalLayout_2.addWidget(self.splitter_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayoutWidget = QWidget(self.tab_2)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 791, 371))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEdit_scenes_filter = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_scenes_filter.setObjectName(u"lineEdit_scenes_filter")
        sizePolicy2.setHeightForWidth(self.lineEdit_scenes_filter.sizePolicy().hasHeightForWidth())
        self.lineEdit_scenes_filter.setSizePolicy(sizePolicy2)
        self.lineEdit_scenes_filter.setFocusPolicy(Qt.ClickFocus)

        self.horizontalLayout_4.addWidget(self.lineEdit_scenes_filter)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.toolButton_sCreate = QToolButton(self.verticalLayoutWidget)
        self.toolButton_sCreate.setObjectName(u"toolButton_sCreate")
        self.toolButton_sCreate.setMaximumSize(QSize(70, 25))
        self.toolButton_sCreate.setFocusPolicy(Qt.NoFocus)
        self.toolButton_sCreate.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        self.toolButton_sCreate.setIcon(icon1)
        self.toolButton_sCreate.setIconSize(QSize(20, 20))
        self.toolButton_sCreate.setAutoRepeat(False)
        self.toolButton_sCreate.setAutoExclusive(False)
        self.toolButton_sCreate.setPopupMode(QToolButton.DelayedPopup)
        self.toolButton_sCreate.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_6.addWidget(self.toolButton_sCreate)

        self.toolButton_sUpdate = QToolButton(self.verticalLayoutWidget)
        self.toolButton_sUpdate.setObjectName(u"toolButton_sUpdate")
        self.toolButton_sUpdate.setMaximumSize(QSize(70, 25))
        self.toolButton_sUpdate.setFocusPolicy(Qt.NoFocus)
        self.toolButton_sUpdate.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        self.toolButton_sUpdate.setIcon(icon2)
        self.toolButton_sUpdate.setIconSize(QSize(20, 20))
        self.toolButton_sUpdate.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_6.addWidget(self.toolButton_sUpdate)

        self.toolButton_sPublish = QToolButton(self.verticalLayoutWidget)
        self.toolButton_sPublish.setObjectName(u"toolButton_sPublish")
        self.toolButton_sPublish.setMaximumSize(QSize(70, 25))
        self.toolButton_sPublish.setFocusPolicy(Qt.NoFocus)
        self.toolButton_sPublish.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        self.toolButton_sPublish.setIcon(icon4)
        self.toolButton_sPublish.setIconSize(QSize(20, 20))
        self.toolButton_sPublish.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_6.addWidget(self.toolButton_sPublish)

        self.horizontalSpacer_3 = QSpacerItem(100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.toolButton_sRefresh = QToolButton(self.verticalLayoutWidget)
        self.toolButton_sRefresh.setObjectName(u"toolButton_sRefresh")
        self.toolButton_sRefresh.setMaximumSize(QSize(70, 25))
        self.toolButton_sRefresh.setFocusPolicy(Qt.NoFocus)
        self.toolButton_sRefresh.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        self.toolButton_sRefresh.setIcon(icon10)
        self.toolButton_sRefresh.setIconSize(QSize(20, 20))
        self.toolButton_sRefresh.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_6.addWidget(self.toolButton_sRefresh)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.listWidget_episodes = QListWidget(self.verticalLayoutWidget)
        QListWidgetItem(self.listWidget_episodes)
        QListWidgetItem(self.listWidget_episodes)
        self.listWidget_episodes.setObjectName(u"listWidget_episodes")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.listWidget_episodes.sizePolicy().hasHeightForWidth())
        self.listWidget_episodes.setSizePolicy(sizePolicy6)
        self.listWidget_episodes.setMaximumSize(QSize(70, 16777215))
        self.listWidget_episodes.setBaseSize(QSize(0, 0))
        self.listWidget_episodes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listWidget_episodes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.listWidget_episodes.setSortingEnabled(True)

        self.horizontalLayout_3.addWidget(self.listWidget_episodes)

        self.tableWidget_scenesTable = QTableWidget(self.verticalLayoutWidget)
        if (self.tableWidget_scenesTable.columnCount() < 3):
            self.tableWidget_scenesTable.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_scenesTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_scenesTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_scenesTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.tableWidget_scenesTable.rowCount() < 8):
            self.tableWidget_scenesTable.setRowCount(8)
        brush = QBrush(QColor(92, 113, 245, 255))
        brush.setStyle(Qt.SolidPattern)
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font);
        __qtablewidgetitem3.setBackground(brush);
        self.tableWidget_scenesTable.setItem(0, 0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_scenesTable.setItem(0, 1, __qtablewidgetitem4)
        brush1 = QBrush(QColor(148, 55, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setBackground(brush1);
        self.tableWidget_scenesTable.setItem(1, 0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_scenesTable.setItem(1, 1, __qtablewidgetitem6)
        brush2 = QBrush(QColor(130, 95, 193, 255))
        brush2.setStyle(Qt.SolidPattern)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setBackground(brush2);
        self.tableWidget_scenesTable.setItem(2, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_scenesTable.setItem(2, 1, __qtablewidgetitem8)
        brush3 = QBrush(QColor(96, 199, 70, 128))
        brush3.setStyle(Qt.SolidPattern)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setBackground(brush3);
        self.tableWidget_scenesTable.setItem(3, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_scenesTable.setItem(3, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_scenesTable.setItem(4, 1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_scenesTable.setItem(5, 1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_scenesTable.setItem(6, 1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_scenesTable.setItem(7, 1, __qtablewidgetitem14)
        self.tableWidget_scenesTable.setObjectName(u"tableWidget_scenesTable")
        self.tableWidget_scenesTable.setFrameShape(QFrame.NoFrame)
        self.tableWidget_scenesTable.setFrameShadow(QFrame.Sunken)
        self.tableWidget_scenesTable.setLineWidth(1)
        self.tableWidget_scenesTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_scenesTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget_scenesTable.setAutoScroll(True)
        self.tableWidget_scenesTable.setAutoScrollMargin(16)
        self.tableWidget_scenesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_scenesTable.setTabKeyNavigation(True)
        self.tableWidget_scenesTable.setProperty("showDropIndicator", True)
        self.tableWidget_scenesTable.setDragDropOverwriteMode(True)
        self.tableWidget_scenesTable.setAlternatingRowColors(True)
        self.tableWidget_scenesTable.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget_scenesTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_scenesTable.setTextElideMode(Qt.ElideRight)
        self.tableWidget_scenesTable.setShowGrid(False)
        self.tableWidget_scenesTable.setGridStyle(Qt.NoPen)
        self.tableWidget_scenesTable.setSortingEnabled(True)
        self.tableWidget_scenesTable.setWordWrap(True)
        self.tableWidget_scenesTable.setCornerButtonEnabled(True)
        self.tableWidget_scenesTable.horizontalHeader().setVisible(True)
        self.tableWidget_scenesTable.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_scenesTable.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget_scenesTable.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_scenesTable.verticalHeader().setVisible(False)
        self.tableWidget_scenesTable.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_scenesTable.verticalHeader().setMinimumSectionSize(21)
        self.tableWidget_scenesTable.verticalHeader().setDefaultSectionSize(21)
        self.tableWidget_scenesTable.verticalHeader().setHighlightSections(True)
        self.tableWidget_scenesTable.verticalHeader().setProperty("showSortIndicator", False)

        self.horizontalLayout_3.addWidget(self.tableWidget_scenesTable)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.verticalLayoutWidget_4 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(810, 0, 281, 531))
        self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(20)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalSpacer = QSpacerItem(20, 70, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.horizontalLayout_11.addItem(self.verticalSpacer)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(2)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.toolButton_addReport = QToolButton(self.verticalLayoutWidget_4)
        self.toolButton_addReport.setObjectName(u"toolButton_addReport")
        self.toolButton_addReport.setMaximumSize(QSize(80, 25))
        self.toolButton_addReport.setFocusPolicy(Qt.NoFocus)
        self.toolButton_addReport.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        icon11 = QIcon()
        icon11.addFile(u"../icons/add_report.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_addReport.setIcon(icon11)
        self.toolButton_addReport.setIconSize(QSize(20, 20))
        self.toolButton_addReport.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_9.addWidget(self.toolButton_addReport)

        self.toolButton_addNote = QToolButton(self.verticalLayoutWidget_4)
        self.toolButton_addNote.setObjectName(u"toolButton_addNote")
        self.toolButton_addNote.setMaximumSize(QSize(70, 25))
        self.toolButton_addNote.setFocusPolicy(Qt.NoFocus)
        self.toolButton_addNote.setStyleSheet(u"border: 1px solid #575757;\n"
"background-color : #464646;")
        icon12 = QIcon()
        icon12.addFile(u"../icons/add_note.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_addNote.setIcon(icon12)
        self.toolButton_addNote.setIconSize(QSize(20, 20))
        self.toolButton_addNote.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_9.addWidget(self.toolButton_addNote)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)

        self.splitter = QSplitter(self.verticalLayoutWidget_4)
        self.splitter.setObjectName(u"splitter")
        sizePolicy3.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy3)
        self.splitter.setOrientation(Qt.Vertical)
        self.textBrowser_history = QTextBrowser(self.splitter)
        self.textBrowser_history.setObjectName(u"textBrowser_history")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.textBrowser_history.sizePolicy().hasHeightForWidth())
        self.textBrowser_history.setSizePolicy(sizePolicy7)
        self.splitter.addWidget(self.textBrowser_history)
        self.textBrowser_metadata = QTextBrowser(self.splitter)
        self.textBrowser_metadata.setObjectName(u"textBrowser_metadata")
        self.splitter.addWidget(self.textBrowser_metadata)

        self.verticalLayout_6.addWidget(self.splitter)

        jam.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(jam)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1105, 24))
        self.menubar.setTabletTracking(False)
        self.menubar.setAcceptDrops(True)
        self.menubar.setDefaultUp(False)
        self.menuAsset = QMenu(self.menubar)
        self.menuAsset.setObjectName(u"menuAsset")
        self.menuAsset.setTearOffEnabled(True)
        self.menuAsset.setToolTipsVisible(False)
        self.menuRender_2 = QMenu(self.menubar)
        self.menuRender_2.setObjectName(u"menuRender_2")
        self.menuRenderman = QMenu(self.menuRender_2)
        self.menuRenderman.setObjectName(u"menuRenderman")
        self.menuArnold = QMenu(self.menuRender_2)
        self.menuArnold.setObjectName(u"menuArnold")
        self.menuRedshift = QMenu(self.menuRender_2)
        self.menuRedshift.setObjectName(u"menuRedshift")
        jam.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(jam)
        self.statusbar.setObjectName(u"statusbar")
        jam.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuAsset.menuAction())
        self.menubar.addAction(self.menuRender_2.menuAction())
        self.menuAsset.addAction(self.actionNewScene)
        self.menuAsset.addAction(self.actionOpen)
        self.menuAsset.addAction(self.actionUpdate)
        self.menuAsset.addSeparator()
        self.menuAsset.addAction(self.actionImport)
        self.menuAsset.addAction(self.actionPublish)
        self.menuAsset.addAction(self.actionCheck)
        self.menuAsset.addSeparator()
        self.menuAsset.addAction(self.actionDenoise)
        self.menuRender_2.addAction(self.menuRenderman.menuAction())
        self.menuRender_2.addAction(self.menuArnold.menuAction())
        self.menuRender_2.addAction(self.menuRedshift.menuAction())
        self.menuRenderman.addAction(self.actionRenderManager)
        self.menuRenderman.addAction(self.actionDenoise_2)
        self.menuRenderman.addAction(self.actionBake)
        self.menuArnold.addAction(self.actionRenderManager_2)
        self.menuArnold.addAction(self.actionDenoise_3)
        self.menuRedshift.addAction(self.actionRender_Manager)
        self.menuRedshift.addAction(self.actionOptimizer)

        self.retranslateUi(jam)

        self.tabWidget.setCurrentIndex(1)
        self.listWidget_episodes.setCurrentRow(0)


        QMetaObject.connectSlotsByName(jam)
    # setupUi

    def retranslateUi(self, jam):
        jam.setWindowTitle(QCoreApplication.translate("jam", u"JAM Asset Manager", None))
        self.actionNewScene.setText(QCoreApplication.translate("jam", u"New Scene", None))
        self.actionUpdate.setText(QCoreApplication.translate("jam", u"Update Scene", None))
        self.actionPublish.setText(QCoreApplication.translate("jam", u"Publish", None))
        self.actionImport.setText(QCoreApplication.translate("jam", u"Import", None))
        self.actionDenoise.setText(QCoreApplication.translate("jam", u"Denoise", None))
        self.actionCheck.setText(QCoreApplication.translate("jam", u"Check", None))
        self.actionRenderManager.setText(QCoreApplication.translate("jam", u"Render Manager", None))
        self.actionDenoise_2.setText(QCoreApplication.translate("jam", u"Denoise", None))
        self.actionBake.setText(QCoreApplication.translate("jam", u"Bake", None))
        self.actionRenderManager_2.setText(QCoreApplication.translate("jam", u"Render Manager", None))
        self.actionDenoise_3.setText(QCoreApplication.translate("jam", u"Denoise", None))
        self.actionRender_Manager.setText(QCoreApplication.translate("jam", u"Render Manager", None))
        self.actionOptimizer.setText(QCoreApplication.translate("jam", u"Optimizer", None))
        self.actionOpen.setText(QCoreApplication.translate("jam", u"Open", None))
        self.toolButton_newScene.setText(QCoreApplication.translate("jam", u"New Scene", None))
#if QT_CONFIG(shortcut)
        self.toolButton_newScene.setShortcut("")
#endif // QT_CONFIG(shortcut)
        self.toolButton_update.setText(QCoreApplication.translate("jam", u"Update", None))
        self.toolButton_import.setText(QCoreApplication.translate("jam", u"Import", None))
        self.toolButton_publish.setText(QCoreApplication.translate("jam", u"Publish", None))
        self.toolButton_check.setText(QCoreApplication.translate("jam", u"Check", None))
        self.toolButton_denoise.setText(QCoreApplication.translate("jam", u"Denoise", None))
        self.toolButton_statistics.setText(QCoreApplication.translate("jam", u"Statistics", None))
        self.toolButton_goto.setText(QCoreApplication.translate("jam", u"->", None))
        self.toolButton_copyClipboard.setText(QCoreApplication.translate("jam", u"CC", None))
        self.label_projName.setText(QCoreApplication.translate("jam", u"Project:", None))
        self.comboBox_projName.setItemText(0, QCoreApplication.translate("jam", u"Fixies5", None))
        self.comboBox_projName.setItemText(1, QCoreApplication.translate("jam", u"Flo-Flo", None))
        self.comboBox_projName.setItemText(2, QCoreApplication.translate("jam", u"Kids", None))

        self.lineEdit_filter.setPlaceholderText(QCoreApplication.translate("jam", u"Filter Asset Name..", None))
        self.toolButton_aImport.setText(QCoreApplication.translate("jam", u"Import", None))
        self.toolButton_aPublish.setText(QCoreApplication.translate("jam", u"Publish", None))
        self.toolButton_aRefresh.setText(QCoreApplication.translate("jam", u"Refresh", None))
        self.comboBox_aTypes.setItemText(0, QCoreApplication.translate("jam", u"Master Lights", None))
        self.comboBox_aTypes.setItemText(1, QCoreApplication.translate("jam", u"Master Shots", None))
        self.comboBox_aTypes.setItemText(2, QCoreApplication.translate("jam", u"HDRI Library", None))
        self.comboBox_aTypes.setItemText(3, QCoreApplication.translate("jam", u"Misc", None))

        self.lineEdit_aFilter.setText("")
        self.lineEdit_aFilter.setPlaceholderText(QCoreApplication.translate("jam", u"Filter Name..", None))
        ___qtreewidgetitem = self.treeWidget_assetFolders.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("jam", u"main", None));

        __sortingEnabled = self.treeWidget_assetFolders.isSortingEnabled()
        self.treeWidget_assetFolders.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget_assetFolders.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("jam", u"childrenroom", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("jam", u"day", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("jam", u"evening", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("jam", u"night", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem4.child(0)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("jam", u"new_year_table", None));
        ___qtreewidgetitem6 = self.treeWidget_assetFolders.topLevelItem(1)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("jam", u"kitchen", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem6.child(0)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("jam", u"day", None));
        ___qtreewidgetitem8 = ___qtreewidgetitem6.child(1)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("jam", u"morning", None));
        ___qtreewidgetitem9 = self.treeWidget_assetFolders.topLevelItem(2)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("jam", u"livingroom", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem9.child(0)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("jam", u"day", None));
        ___qtreewidgetitem11 = self.treeWidget_assetFolders.topLevelItem(3)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("jam", u"corridor", None));
        ___qtreewidgetitem12 = ___qtreewidgetitem11.child(0)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("jam", u"day", None));
        ___qtreewidgetitem13 = ___qtreewidgetitem11.child(1)
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("jam", u"electrical", None));
        ___qtreewidgetitem14 = self.treeWidget_assetFolders.topLevelItem(4)
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("jam", u"bathroom", None));
        ___qtreewidgetitem15 = ___qtreewidgetitem14.child(0)
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("jam", u"main", None));
        ___qtreewidgetitem16 = self.treeWidget_assetFolders.topLevelItem(5)
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("jam", u"inside_device", None));
        ___qtreewidgetitem17 = ___qtreewidgetitem16.child(0)
        ___qtreewidgetitem17.setText(0, QCoreApplication.translate("jam", u"main", None));
        ___qtreewidgetitem18 = ___qtreewidgetitem16.child(1)
        ___qtreewidgetitem18.setText(0, QCoreApplication.translate("jam", u"flash", None));
        self.treeWidget_assetFolders.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("jam", u"Asstes", None))
        self.lineEdit_scenes_filter.setPlaceholderText(QCoreApplication.translate("jam", u"Filter Scenes Name..", None))
        self.toolButton_sCreate.setText(QCoreApplication.translate("jam", u"Create", None))
        self.toolButton_sUpdate.setText(QCoreApplication.translate("jam", u"Update", None))
        self.toolButton_sPublish.setText(QCoreApplication.translate("jam", u"Publish", None))
        self.toolButton_sRefresh.setText(QCoreApplication.translate("jam", u"Refresh", None))

        __sortingEnabled1 = self.listWidget_episodes.isSortingEnabled()
        self.listWidget_episodes.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget_episodes.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("jam", u"ep049", None));
        ___qlistwidgetitem1 = self.listWidget_episodes.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("jam", u"ep053", None));
        self.listWidget_episodes.setSortingEnabled(__sortingEnabled1)

        ___qtablewidgetitem = self.tableWidget_scenesTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("jam", u"Status", None));
        ___qtablewidgetitem1 = self.tableWidget_scenesTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("jam", u"Scene", None));
        ___qtablewidgetitem2 = self.tableWidget_scenesTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("jam", u"Note", None));

        __sortingEnabled2 = self.tableWidget_scenesTable.isSortingEnabled()
        self.tableWidget_scenesTable.setSortingEnabled(False)
        ___qtablewidgetitem3 = self.tableWidget_scenesTable.item(0, 0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("jam", u"ready to start", None));
        ___qtablewidgetitem4 = self.tableWidget_scenesTable.item(0, 1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("jam", u"ep053_sc001", None));
        ___qtablewidgetitem5 = self.tableWidget_scenesTable.item(1, 0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("jam", u"in progress", None));
        ___qtablewidgetitem6 = self.tableWidget_scenesTable.item(1, 1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("jam", u"ep053_sc002", None));
        ___qtablewidgetitem7 = self.tableWidget_scenesTable.item(2, 0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("jam", u"in progress", None));
        ___qtablewidgetitem8 = self.tableWidget_scenesTable.item(2, 1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("jam", u"ep053_sc003", None));
        ___qtablewidgetitem9 = self.tableWidget_scenesTable.item(3, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("jam", u"published", None));
        ___qtablewidgetitem10 = self.tableWidget_scenesTable.item(3, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("jam", u"ep053_sc004", None));
        self.tableWidget_scenesTable.setSortingEnabled(__sortingEnabled2)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("jam", u"Scenes", None))
        self.toolButton_addReport.setText(QCoreApplication.translate("jam", u"+ Report", None))
        self.toolButton_addNote.setText(QCoreApplication.translate("jam", u"+ Note", None))
        self.textBrowser_history.setHtml(QCoreApplication.translate("jam", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.menuAsset.setTitle(QCoreApplication.translate("jam", u"Asset", None))
        self.menuRender_2.setTitle(QCoreApplication.translate("jam", u"Utilites", None))
        self.menuRenderman.setTitle(QCoreApplication.translate("jam", u"Renderman", None))
        self.menuArnold.setTitle(QCoreApplication.translate("jam", u"Arnold", None))
        self.menuRedshift.setTitle(QCoreApplication.translate("jam", u"Redshift", None))
    # retranslateUi

