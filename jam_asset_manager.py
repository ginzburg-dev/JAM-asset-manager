"""JAM Asset Manager's Maya user interface and application entry point."""

import logging
import os
from functools import partial
from typing import NamedTuple

from maya import OpenMayaUI as omui
from PySide2.QtCore import QRect, QSize, Qt
from PySide2.QtGui import QColor, QIcon, QPixmap
from PySide2.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QListWidgetItem,
    QMainWindow,
    QTableWidgetItem,
    QTreeWidgetItem,
    QWidget,
)
from shiboken2 import wrapInstance

import jam_maya_asset
import jam_maya_scene
from jam_core.catalog import (
    AssetRecord,
    SceneRecord,
    get_assets,
    get_episodes,
    get_extension,
    get_scenes,
    is_allowed_extension,
    is_path_within,
    is_valid_animation_scene_name,
)
from jam_core.config import JamConfig
from jam_core.constants import (
    ASSET_MANAGER_PATH,
    DEFAULT_EXCLUDED_NAMES,
    ICONS_PATH,
)
from jam_core.reports import append_message, read_messages, render_history
from jam_core.storage import read_json, write_json
from ui.ui_jam import Ui_jam
from ui.ui_report import Ui_report

LOGGER = logging.getLogger(__name__)

JAM_PATH = str(ASSET_MANAGER_PATH)
_default_config = None


class SceneDisplayRecord(NamedTuple):
    status: str
    color: QColor
    scene: SceneRecord


def _icon(filename, icons_path=ICONS_PATH):
    return QIcon(str(icons_path / filename))


def get_default_config():
    """Return the lazily loaded config used by legacy module-level helpers."""
    global _default_config
    if _default_config is None:
        _default_config = JamConfig.from_environment()
    return _default_config


def readConfig(config=None):
    """Load or register the config used by legacy module-level helpers."""
    global _default_config
    _default_config = config or JamConfig.from_environment()
    return _default_config


def read_user_config(config=None):
    """Refresh current selections for a supplied or default config."""
    active_config = config or get_default_config()
    return active_config.reload()


def readJSON(path):
    """Backward-compatible alias for :func:`jam_core.storage.read_json`."""
    return read_json(path)


def writeJSON(path, data):
    """Backward-compatible alias for :func:`jam_core.storage.write_json`."""
    write_json(path, data)


def addToClipBoard(text):
    """Copy text through Qt's cross-platform clipboard implementation."""
    QApplication.clipboard().setText(text.strip())


def getProjectPath(name, config=None):
    project = (config or get_default_config()).project(name)
    return str(project.root) if project is not None else ""


def getEpisodePath(name, config=None):
    project = (config or get_default_config()).project(name)
    return project.episode_path if project is not None else ""


def getAssetPath(name, current_project, config=None):
    project = (config or get_default_config()).project(current_project)
    directory = project.asset_directory(name) if project is not None else None
    return str(directory) if directory is not None and directory.is_dir() else ""


def isAllowedExtension(name, config=None):
    extensions = (config or get_default_config()).application.allowed_extensions
    return is_allowed_extension(name, extensions)


def getExtension(name):
    return get_extension(name)


def getAssetsPathsList(path, config=None):
    """Return catalog records for supported assets."""
    extensions = (config or get_default_config()).application.allowed_extensions
    return get_assets(path, extensions)


def get_preview_path(item):
    return os.path.join(item.directory, item.name + ".jpg")


def load_project_structure(
    startpath,
    tree,
    excluded_names=DEFAULT_EXCLUDED_NAMES,
    icons_path=ICONS_PATH,
):
    if not os.path.isdir(startpath):
        return
    for element in sorted(os.listdir(startpath)):
        path_info = os.path.join(startpath, element)
        if element not in excluded_names and os.path.isdir(path_info):
            parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
            parent_itm.setData(0, Qt.UserRole, path_info)
            load_project_structure(path_info, parent_itm, excluded_names, icons_path)
            parent_itm.setIcon(0, _icon("folder.png", icons_path))


def get_episodes_list(project_name, config=None):
    project = (config or get_default_config()).project(project_name)
    return get_episodes(project) if project is not None else []


def check_animscene_name(episode, name):
    return is_valid_animation_scene_name(episode, name)


def get_scenes_list(episode, project_name, config=None):
    active_config = config or get_default_config()
    project = active_config.project(project_name)
    excluded_names = active_config.application.excluded_names
    return get_scenes(project, episode, excluded_names) if project is not None else []


class ReportWindow(QMainWindow):
    def __init__(self, message_type, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint)
        self.ui = Ui_report()
        self.ui.setupUi(self)
        self.message_type = message_type
        obj_outline = parent.get_object_outline_path(parent.get_current_assetdata_to_report())
        self.ui.lineEdit.setText(obj_outline)
        if message_type == "note":
            self.setWindowTitle("Create note")
            self.ui.spinBox_hours.setDisabled(True)
        self.ui.pushButton_cancel.pressed.connect(self.close)
        self.ui.pushButton_ok.pressed.connect(partial(self.sendReportNote, parent))

    def sendReportNote(self, parent):
        obj_data = parent.get_current_assetdata_to_report()
        if not obj_data:
            self.close()
            return
        append_message(
            obj_data[1],
            obj_data[0],
            self.message_type,
            self.ui.textEdit_maintext.toPlainText(),
            self.ui.spinBox_hours.value(),
        )
        parent.updateReportNote()
        self.close()


class MainWindow(QMainWindow):
    def getCurrentAssetsPaths(self):
        project = self.config.project(self.ui.comboBox_projName.currentText())
        return project.asset_types if project is not None else ()

    def isAsset(self, name):
        return any(
            is_path_within(
                name,
                os.path.join(self.get_current_project_path(), asset_type.relative_path),
            )
            for asset_type in self.getCurrentAssetsPaths()
        )

    def updateReportNote(self):
        data = self.get_current_assetdata_to_report()
        self.ui.textBrowser_history.clear()
        if not data:
            return
        self.ui.textBrowser_history.setHtml(render_history(read_messages(data[1])))

    def write_prj_state_to_config(self, mode):
        """Persist the selected project, asset type, or episode."""
        current_project = self.ui.comboBox_projName.currentText()
        if not current_project:
            return
        self.config.user_state.current_project = current_project
        project_state = self.config.user_state.project(current_project)
        if mode == "asset":
            project_state.asset_type = self.ui.comboBox_aTypes.currentText()
        elif mode == "episode":
            current_episode = self.ui.listWidget_episodes.currentItem()
            project_state.episode = current_episode.text() if current_episode is not None else ""
        self.config.save()

    def add_message_to_report(self, path, hours, text):
        append_message(path, os.path.splitext(os.path.basename(path))[0], "report", text, hours)
        self.updateReportNote()

    def get_current_project_name(self):
        return self.ui.comboBox_projName.currentText()

    def get_current_project_path(self):
        return getProjectPath(self.ui.comboBox_projName.currentText(), self.config)

    def _current_scene_data(self):
        row = self.ui.tableWidget_scenesTable.currentRow()
        if row < 0:
            return None
        scene_item = self.ui.tableWidget_scenesTable.item(row, 1)
        return scene_item.data(Qt.UserRole) if scene_item is not None else None

    def asset_path_to_outline(self):
        current_item = self.ui.listWidget_assets.currentItem()
        if current_item is None:
            return
        item = current_item.data(Qt.UserRole)
        proj_name = self.ui.comboBox_projName.currentText()
        relative_directory = os.path.relpath(item.directory, self.get_current_project_path())
        text = "|".join([proj_name, relative_directory.replace(os.sep, "|"), item.name])
        self.ui.lineEdit_fullPath.setText(text)

    def scene_path_to_outline(self):
        item = self._current_scene_data()
        if item is None:
            return
        relative_path = os.path.splitext(
            os.path.relpath(item.render_path, self.get_current_project_path())
        )[0]
        text = "|".join([self.get_current_project_name(), relative_path.replace(os.sep, "|")])
        self.ui.lineEdit_fullPath.setText(text)

    def go_to_asset(self):
        outline = self.ui.lineEdit_fullPath.text().strip()
        parts = [part for part in outline.split("|") if part]
        if len(parts) < 2:
            return

        project_index = self.ui.comboBox_projName.findText(parts[0])
        if project_index < 0:
            return
        if project_index != self.ui.comboBox_projName.currentIndex():
            self.ui.comboBox_projName.setCurrentIndex(project_index)

        element_name = parts[-1]
        dir_path = os.path.join(self.get_current_project_path(), *parts[1:-1])
        target_stem = os.path.normcase(os.path.join(dir_path, element_name))
        if self.isAsset(dir_path):
            self.ui.tabWidget.setCurrentWidget(self.ui.tabWidget.findChild(QWidget, "tab"))
            found_items = self.ui.listWidget_assets.findItems(
                element_name, Qt.MatchFlag.MatchExactly
            )
            for item in found_items:
                item_path = item.data(Qt.UserRole).path
                if os.path.normcase(os.path.splitext(item_path)[0]) == target_stem:
                    self.ui.listWidget_assets.setCurrentItem(item)
                    self.ui.listWidget_assets.scrollToItem(item, QAbstractItemView.PositionAtTop)
                    return
            if os.path.isdir(dir_path):
                for filename in sorted(os.listdir(dir_path)):
                    path = os.path.join(dir_path, filename)
                    if (
                        isAllowedExtension(path, self.config)
                        and os.path.normcase(os.path.splitext(path)[0]) == target_stem
                    ):
                        self.ui.listWidget_assets.clear()
                        self.createAssetItem(AssetRecord(element_name, dir_path, path))
                        self.ui.listWidget_assets.setCurrentRow(0)
                        return
        else:
            self.ui.tabWidget.setCurrentWidget(self.ui.tabWidget.findChild(QWidget, "tab_2"))
            for row in range(self.ui.tableWidget_scenesTable.rowCount()):
                item = self.ui.tableWidget_scenesTable.item(row, 1)
                data = item.data(Qt.UserRole) if item is not None else None
                if data and os.path.normcase(os.path.splitext(data.render_path)[0]) == target_stem:
                    self.ui.tableWidget_scenesTable.selectRow(row)
                    self.ui.tableWidget_scenesTable.scrollToItem(
                        item, QAbstractItemView.PositionAtTop
                    )
                    return
            self.ui.tableWidget_scenesTable.clearContents()
            self.ui.tableWidget_scenesTable.setRowCount(1)
            self.createSceneItem(outline)
            self.ui.tableWidget_scenesTable.selectRow(0)

    def updateProject(self):
        self.ui.comboBox_projName.clear()
        self.ui.comboBox_projName.addItems(
            [project.name for project in self.config.application.projects]
        )
        current_index = self.ui.comboBox_projName.findText(self.config.user_state.current_project)
        self.ui.comboBox_projName.setCurrentIndex(max(0, current_index))

    def get_current_asset_type(self):
        return self.config.user_state.project(self.ui.comboBox_projName.currentText()).asset_type

    def get_current_episode(self):
        return self.config.user_state.project(self.ui.comboBox_projName.currentText()).episode

    def initEpisode(self):
        matches = self.ui.listWidget_episodes.findItems(
            self.get_current_episode(), Qt.MatchFlag.MatchExactly
        )
        if matches:
            self.ui.listWidget_episodes.setCurrentItem(matches[0])

    def get_rs_file_path(self):
        project = self.config.project(self.get_current_project_name())
        return str(project.render_scene) if project is not None else ""

    def updateAssetTypes(self):
        self.ui.comboBox_aTypes.clear()
        self.ui.comboBox_aTypes.addItems(
            [asset_type.name for asset_type in self.getCurrentAssetsPaths()]
        )
        current_index = self.ui.comboBox_aTypes.findText(self.get_current_asset_type())
        self.ui.comboBox_aTypes.setCurrentIndex(max(0, current_index))

    def updateAssetTree(self):
        self.ui.treeWidget_assetFolders.clear()
        path = getAssetPath(
            self.ui.comboBox_aTypes.currentText(),
            self.ui.comboBox_projName.currentText(),
            self.config,
        )
        parent_itm = QTreeWidgetItem(self.ui.treeWidget_assetFolders, ["[root]"])
        parent_itm.setIcon(0, _icon("base_01.png", self.config.icons_path))
        parent_itm.setData(0, Qt.UserRole, path)
        if path:
            load_project_structure(
                path,
                parent_itm,
                self.config.application.excluded_names,
                self.config.icons_path,
            )
        self.ui.treeWidget_assetFolders.expandAll()
        self.updateAssets()
        self.write_prj_state_to_config("asset")

    def updateEpisodeList(self):
        self.ui.listWidget_episodes.clear()
        episodes = get_episodes_list(self.ui.comboBox_projName.currentText(), self.config)
        for episode in episodes:
            list_item = QListWidgetItem(episode.name)
            list_item.setData(Qt.UserRole, episode.path)
            self.ui.listWidget_episodes.addItem(list_item)

    def createAssetItem(self, item):
        preview_path = get_preview_path(item)
        icon_path = (
            preview_path
            if os.path.isfile(preview_path)
            else str(self.config.icons_path / self.config.application.icon_placeholder)
        )
        icon_pixmap = QPixmap(icon_path)
        width = icon_pixmap.width()
        height = icon_pixmap.height()
        side = min(width, height)
        x_offset = max(0, int((width - side) / 2))
        y_offset = max(0, int((height - side) / 2))
        scaled = icon_pixmap.copy(QRect(x_offset, y_offset, side, side))
        icon = QIcon(scaled)
        new_item = QListWidgetItem(icon, item.name)
        new_item.setData(Qt.UserRole, item)
        self.ui.listWidget_assets.addItem(new_item)

    def updateScenes_from_list(self, scenes):
        self.ui.tableWidget_scenesTable.setRowCount(len(scenes))
        for row, display in enumerate(scenes):
            new_item_status = QTableWidgetItem(display.status)
            new_item_status.setText(display.status)
            new_item_status.setBackground(display.color)
            new_item_scene = QTableWidgetItem(display.scene.name)
            new_item_note = QTableWidgetItem()
            new_item_scene.setData(Qt.UserRole, display.scene)

            self.ui.tableWidget_scenesTable.setItem(row, 0, new_item_status)
            self.ui.tableWidget_scenesTable.setItem(row, 1, new_item_scene)
            self.ui.tableWidget_scenesTable.setItem(row, 2, new_item_note)

        self.ui.tableWidget_scenesTable.sortByColumn(1, Qt.SortOrder.AscendingOrder)

    def createSceneItem(self, name_am_path):
        parts = [part for part in name_am_path.split("|") if part]
        if len(parts) < 2:
            return
        element_name = parts[-1]
        directory = os.path.join(self.get_current_project_path(), *parts[1:-1])
        render_filename = os.path.join(directory, element_name + ".ma")
        exists = os.path.isfile(render_filename)
        status = "in process" if exists else "ready to start"
        color = QColor(139, 192, 61) if exists else QColor(114, 183, 245)
        new_item_status = QTableWidgetItem(status)
        new_item_status.setText(status)
        new_item_status.setBackground(color)
        new_item_scene = QTableWidgetItem(element_name)
        new_item_note = QTableWidgetItem()
        render_marker = os.sep + "render" + os.sep
        episode_root = directory.split(render_marker, 1)[0]
        animation_filename = os.path.join(episode_root, "maya", "animation", element_name + ".ma")
        scene_data = SceneRecord(element_name, animation_filename, render_filename, exists)
        new_item_scene.setData(Qt.UserRole, scene_data)

        self.ui.tableWidget_scenesTable.setItem(0, 0, new_item_status)
        self.ui.tableWidget_scenesTable.setItem(0, 1, new_item_scene)
        self.ui.tableWidget_scenesTable.setItem(0, 2, new_item_note)

    def updateScenes(self):
        self.ui.tableWidget_scenesTable.clearContents()
        self.scene_list.clear()
        selected_episode = self.ui.listWidget_episodes.currentItem()
        if selected_episode is not None:
            scenes = get_scenes_list(
                selected_episode.text(),
                self.ui.comboBox_projName.currentText(),
                self.config,
            )
            for scene in scenes:
                if scene.render_exists:
                    status, color = "in process", QColor(130, 95, 193)
                else:
                    status, color = "ready to start", QColor(92, 113, 245)
                self.scene_list.append(SceneDisplayRecord(status, color, scene))
        self.filter_scenes()
        self.write_prj_state_to_config("episode")

    def updateAssets(self):
        self.ui.listWidget_assets.clear()
        icon_size = self.config.application.icon_size
        self.ui.listWidget_assets.setIconSize(QSize(icon_size, icon_size))
        selected_items = self.ui.treeWidget_assetFolders.selectedItems()
        selected_path = selected_items[0].data(0, Qt.UserRole) if selected_items else ""
        search_path = selected_path or getAssetPath(
            self.ui.comboBox_aTypes.currentText(),
            self.ui.comboBox_projName.currentText(),
            self.config,
        )
        self.asset_list[:] = getAssetsPathsList(search_path, self.config)
        self.filter_assets()

    def is_scene_path(self, path):
        return any(
            is_path_within(path, project.root / project.episode_path)
            for project in self.config.application.projects
        )

    def is_asset_path(self, path):
        return any(
            is_path_within(path, project.root / asset.relative_path)
            for project in self.config.application.projects
            for asset in project.asset_types
        )

    # actions
    def createScene(self):
        item = self._current_scene_data()
        if self.ui.tabWidget.currentIndex() != 1 or item is None:
            return
        index = self.ui.tableWidget_scenesTable.currentRow()
        created = jam_maya_scene.createRenderScene(
            item.name,
            item.animation_path,
            item.render_path,
            self.get_rs_file_path(),
        )
        if created:
            self.add_message_to_report(item.render_path, 0, "Created")
        self.updateScenes()
        if index >= 0:
            self.ui.tableWidget_scenesTable.selectRow(index)

    def open(self):
        data = self.get_current_assetdata_to_report()
        if data and os.path.isfile(data[1]):
            jam_maya_scene.openRenderScene(data[1])

    def updateScene(self):
        item = self._current_scene_data()
        if self.ui.tabWidget.currentIndex() != 1 or item is None:
            return
        if jam_maya_scene.updateRenderScene(item.name, item.animation_path, item.render_path):
            self.add_message_to_report(item.render_path, 0, "Updated")

    def publishElement(self):
        path = jam_maya_scene.get_current_scene_path()
        if not path:
            return
        if self.is_scene_path(path) and jam_maya_scene.publish_scene():
            self.add_message_to_report(path, 0, "Published")
        elif self.is_asset_path(path) and jam_maya_asset.publish_asset():
            self.add_message_to_report(path, 0, "Published")

    def importElement(self):
        data = self.get_current_assetdata_to_report()
        if data and self.is_asset_path(data[1]):
            jam_maya_asset.import_asset(data[1])

    def denoise(self):
        LOGGER.info("Denoising is unavailable in the community edition")

    def checkElement(self):
        jam_maya_scene.check_scene()

    def refreshAssets(self):
        self.ui.comboBox_aTypes.clear()
        self.ui.treeWidget_assetFolders.clear()
        self.ui.listWidget_assets.clear()
        self.updateAssetTypes()
        self.updateAssetTree()
        self.updateAssets()

    def refreshScenes(self):
        index = self.ui.listWidget_episodes.currentRow()
        self.updateEpisodeList()
        self.ui.listWidget_episodes.setCurrentRow(index)
        self.updateScenes()

    def goToAsset(self):
        self.go_to_asset()

    def addReport(self):
        self.showReportWindow()

    def addNote(self):
        self.showNoteWindow()

    def copyToClipboard(self):
        addToClipBoard(self.ui.lineEdit_fullPath.text())

    def click_on_asset(self):
        self.asset_path_to_outline()
        self.updateReportNote()

    def click_on_scene(self):
        self.scene_path_to_outline()
        self.updateReportNote()

    def filter_scenes(self):
        self.ui.tableWidget_scenesTable.clearContents()
        filter_text = self.ui.lineEdit_scenes_filter.text().strip().casefold()
        matches = []
        for display in self.scene_list:
            scene_name = display.scene.name
            numeric_parts = [
                "".join(character for character in part if character.isdigit())
                for part in scene_name.split("_")
            ]
            numeric_parts = [part for part in numeric_parts if part]
            candidates = {scene_name.casefold()}
            if numeric_parts:
                candidates.add("_".join(numeric_parts))
                candidates.add(" ".join(numeric_parts))
                normalized = [str(int(part)) for part in numeric_parts]
                candidates.add("_".join(normalized))
                candidates.add(" ".join(normalized))
            if any(candidate.startswith(filter_text) for candidate in candidates):
                matches.append(display)
        self.updateScenes_from_list(matches)

    def filter_assets(self):
        self.ui.listWidget_assets.clear()
        filter_text = self.ui.lineEdit_filter.text().strip().casefold()
        for asset in self.asset_list:
            if asset.name.casefold().startswith(filter_text):
                self.createAssetItem(asset)

    def get_object_outline_path(self, data):
        relative_path = os.path.splitext(os.path.relpath(data[1], self.get_current_project_path()))[
            0
        ]
        return "|".join([self.get_current_project_name(), relative_path.replace(os.sep, "|")])

    def get_current_assetdata_to_report(self):
        if self.ui.tabWidget.currentIndex() == 1:
            item = self._current_scene_data()
            return [item.name, item.render_path] if item is not None else []
        if self.ui.tabWidget.currentIndex() == 0:
            item = self.ui.listWidget_assets.currentItem()
            if item is not None:
                item_data = item.data(Qt.UserRole)
                return [item_data.name, item_data.path]
        return []

    def showReportWindow(self):
        if self.get_current_assetdata_to_report():
            self.report_window = ReportWindow("report", self)
            self.report_window.show()

    def showNoteWindow(self):
        if self.get_current_assetdata_to_report():
            self.report_window = ReportWindow("note", self)
            self.report_window.show()

    def set_current_state_assets(self):
        current_index = self.ui.comboBox_aTypes.findText(self.get_current_asset_type())
        self.ui.comboBox_aTypes.setCurrentIndex(max(0, current_index))

    def updateAllAssets(self):
        self.config.reload()
        self.updateAssetTypes()
        self.updateAssetTree()
        self.updateAssets()
        self.updateEpisodeList()
        self.initEpisode()
        self.updateScenes()
        self.set_current_state_assets()
        self.write_prj_state_to_config("project")

    def __init__(self, parent=None, config=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint)
        self.config = config or JamConfig.from_environment()
        self.asset_list = []
        self.scene_list = []
        self.ui = Ui_jam()
        self.ui.setupUi(self)
        self.report_window = None
        menu = self.menuBar()
        menu.setNativeMenuBar(False)

        self.setWindowIcon(_icon("icon_maya_jam_purple.png", self.config.icons_path))
        button_icons = (
            (self.ui.toolButton_newScene, "icon_maya_jam_purple.png"),
            (self.ui.toolButton_sCreate, "new_scene.png"),
            (self.ui.toolButton_update, "update.png"),
            (self.ui.toolButton_sUpdate, "update.png"),
            (self.ui.toolButton_publish, "publish.png"),
            (self.ui.toolButton_aPublish, "publish.png"),
            (self.ui.toolButton_sPublish, "publish.png"),
            (self.ui.toolButton_import, "import.png"),
            (self.ui.toolButton_aImport, "import.png"),
            (self.ui.toolButton_denoise, "denoise.png"),
            (self.ui.toolButton_statistics, "statistics.png"),
            (self.ui.toolButton_check, "check.png"),
            (self.ui.toolButton_aRefresh, "refresh.png"),
            (self.ui.toolButton_sRefresh, "refresh.png"),
            (self.ui.toolButton_goto, "goto.png"),
            (self.ui.toolButton_copyClipboard, "clipboard.png"),
            (self.ui.toolButton_addReport, "add_report.png"),
            (self.ui.toolButton_addNote, "add_note.png"),
        )
        for button, filename in button_icons:
            button.setIcon(_icon(filename, self.config.icons_path))

        commercial_controls = (
            self.ui.toolButton_denoise,
            self.ui.toolButton_statistics,
            self.ui.actionDenoise,
            self.ui.actionDenoise_2,
            self.ui.actionDenoise_3,
        )
        for control in commercial_controls:
            control.setEnabled(False)
            control.setToolTip("Available in the commercial edition")

        self.updateProject()
        self.updateAssetTypes()
        self.updateAssetTree()
        self.updateAssets()
        self.updateEpisodeList()
        self.initEpisode()
        self.updateScenes()

        # update all items when the project changes
        self.ui.comboBox_projName.currentIndexChanged.connect(self.updateAllAssets)

        # update asset items when the folder changes
        self.ui.treeWidget_assetFolders.clicked.connect(self.updateAssets)

        # update asset tree when the type changes
        self.ui.comboBox_aTypes.currentIndexChanged.connect(self.updateAssetTree)

        # update asset text block when a selection changes
        self.ui.listWidget_assets.clicked.connect(self.click_on_asset)

        # update scene text block when a selection changes
        self.ui.tableWidget_scenesTable.clicked.connect(self.click_on_scene)

        # update scenes items when the episode changes
        self.ui.listWidget_episodes.clicked.connect(self.updateScenes)

        # Open scenes and assets on a double-click.
        self.ui.tableWidget_scenesTable.doubleClicked.connect(self.open)
        self.ui.listWidget_assets.doubleClicked.connect(self.open)

        # filtering assets
        self.ui.lineEdit_filter.textChanged.connect(self.filter_assets)

        # filtering scenes
        self.ui.lineEdit_scenes_filter.textChanged.connect(self.filter_scenes)

        # attach functions to other UI events
        self.ui.toolButton_newScene.pressed.connect(self.createScene)
        self.ui.toolButton_sCreate.pressed.connect(self.createScene)
        self.ui.toolButton_update.pressed.connect(self.updateScene)
        self.ui.toolButton_sUpdate.pressed.connect(self.updateScene)
        self.ui.toolButton_publish.pressed.connect(self.publishElement)
        self.ui.toolButton_aPublish.pressed.connect(self.publishElement)
        self.ui.toolButton_sPublish.pressed.connect(self.publishElement)
        self.ui.toolButton_import.pressed.connect(self.importElement)
        self.ui.toolButton_aImport.pressed.connect(self.importElement)
        self.ui.toolButton_denoise.pressed.connect(self.denoise)
        self.ui.toolButton_check.pressed.connect(self.checkElement)
        self.ui.toolButton_aRefresh.pressed.connect(self.refreshAssets)
        self.ui.toolButton_sRefresh.pressed.connect(self.refreshScenes)
        self.ui.toolButton_goto.pressed.connect(self.goToAsset)
        self.ui.toolButton_copyClipboard.pressed.connect(self.copyToClipboard)
        self.ui.toolButton_addReport.pressed.connect(self.addReport)
        self.ui.toolButton_addNote.pressed.connect(self.addNote)
        # attach functions to menu bar
        self.ui.actionNewScene.triggered.connect(self.createScene)
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionUpdate.triggered.connect(self.updateScene)
        self.ui.actionPublish.triggered.connect(self.publishElement)
        self.ui.actionImport.triggered.connect(self.importElement)
        self.ui.actionCheck.triggered.connect(self.checkElement)
        self.ui.actionDenoise.triggered.connect(self.denoise)


def jam_asset_manager_run(config=None):
    """Create the Maya window with an optional injected :class:`JamConfig`."""
    maya_main_window_pointer = omui.MQtUtil.mainWindow()
    if maya_main_window_pointer is None:
        raise RuntimeError("Maya's main window is unavailable")
    maya_main_window = wrapInstance(int(maya_main_window_pointer), QWidget)
    jam_window = MainWindow(parent=maya_main_window, config=config)
    jam_window.show()
    return jam_window
