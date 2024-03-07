import sys
JAM_path = '/Users/dmitryginzburg/Documents/Ginzburg/Github/JAM-asset-manager'
sys.path.append(JAM_path)

import sys
import os
import json
import shutil
from datetime import datetime
from functools import partial

from ui.ui_jam import Ui_jam
from ui.ui_report import Ui_report

from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QListWidgetItem, QTreeWidgetItem, QTableWidgetItem, QListWidgetItem, QAbstractItemView, QTextBrowser, QWidget, QAction
from PySide2.QtGui import QPixmap, QIcon, QCursor, QColor
from PySide2.QtCore import Qt, QSize, QRect, QModelIndex

# Asset Manager Configuration
json_config_path = JAM_path+'/config.json'
json_user_config_path = JAM_path+'/config.user.json'
json_asset_template = {
"assetName":"asset_name",
"assetType":"type",
"createdTime":"",
"messages": []
}

json_user_cfg_template = {
    "projectName": "",
    "currentAssetType": "", 
    "currentEpisode": ""
}

excluded_names  = ['.DS_Store']
allowed_extensions  = ['hdr','ma','mb']
icon_placeholder = 'icon_placeholder.jpg'
asset_icon_size = 200
projects_paths = [
    [
        'Kids', 
        '/Users/dmitryginzburg/UI_example', 
        'scenes/episodes'
    ],
    [
        'Flo-Flo', 
        '/Users/dmitryginzburg/UI_example', 
        'scenes/episodes'
    ],
    [
        'Fixies5', 
        '/Users/dmitryginzburg/UI_example', 
        'scenes/episodes',
        [
            [
                'Master Lights', 
                'assets/Master_Lights'
            ],
            [
                'Master Shots', 
                'assets/MasterShots'
            ],
            [
                'HDRI Library', 
                'assets/HDRI'
            ],
            [
                'Misc.', 
                'assets/Misc'
            ]
        ]
    ]
]

#current_project = 'Kids'
#current_asset_type = 'Master Lights'
#current_episode = 'MG049'

current_user_state = [
    'Fixies5',
    [
        'Kids',
        'Master Lights',
        'MG049'
    ],
    [
        'Flo-Flo',
        'Master Lights',
        'MG049'
    ],
    [
        'Fixies5',
        'Master Lights',
        'MG049'
    ]
]

# global variables
global_asset_list = []
global_scene_list = []

def readConfig():
    global excluded_names
    global allowed_extensions
    global icon_placeholder
    global asset_icon_size
    global current_user_state
    #global current_asset_type
    #global current_episode
    global projects_paths
    
    if os.path.exists(json_config_path):
        f = open(json_config_path)
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        # Iterating through the json
        # list

        excluded_names = data['excludedNames']
        allowed_extensions  = data['allowedExtensions']
        icon_placeholder = data['iconPlaceholder']
        asset_icon_size = data['iconSize']

        projects_paths.clear()
        
        for i in data['projects']:
            assets_paths = []
            for k in i['assets']:
                    assets_paths.append([k['assetType'],k['assetTypePath']])
            projects_paths.append([i['projectName'],i['projectPath'],i['episodePath'],assets_paths])

        
        #current_project = data['currentProject'] ##
        #current_asset_type = data['currentAssetType'] ##
        #current_episode = data['currentEpisode'] ##

        current_user_state[0] = data['currentProject']

        if os.path.exists(json_user_config_path):
            f_u = open(json_user_config_path)
            data_u = json.load(f_u)
            #current_project = data_u['currentProject'] ##
            #current_asset_type = data_u['currentAssetType'] ##
            #current_episode = data_u['currentEpisode'] ##
            current_user_state[0] = data_u['currentProject']
            current_user_state[1] = []
            for i in data_u['configs']:
                current_user_state[1].append([i['projectName'],i['currentAssetType'],i['currentEpisode']])
            f_u.close()
        print('PP: ',projects_paths)
        print('CURRENT_USER_STATE: ', current_user_state)

        # Closing file
        f.close()

def read_user_config():
        global current_user_state
        if os.path.exists(json_user_config_path):
            f_u = open(json_user_config_path)
            data_u = json.load(f_u)
            current_user_state[1] = []
            for i in data_u['configs']:
                current_user_state[1].append([i['projectName'],i['currentAssetType'],i['currentEpisode']])
            f_u.close()
        print('PP: ',projects_paths)
        print('CURRENT_USER_STATE: ', current_user_state)
        


def readJSON(path):
    data = []
    if os.path.exists(path):
        f = open(path)
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Closing file
        f.close()
    return data

def writeJSON(path, data):
    complete = True
    if os.path.exists(path):
        init_size = os.path.getsize(path)
        shutil.copyfile(path, path.replace('.json','.jsontmp'))
        current_size = os.path.getsize(path.replace('.json','.jsontmp'))
        if init_size != current_size:
            complete = False
    else:
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
    with open(path, 'w') as f:
        json.dump(data, f)
        f.close()

    if (complete)and(os.path.exists(path.replace('.json','.jsontmp'))):
        os.remove(path.replace('.json','.jsontmp'))


def getProjectPath(name):
    result = ''
    for i in projects_paths:
        if name == i[0]:
            result = i[1]
    return result

def getEpisodePath(name):
    result = ''
    for i in projects_paths:
        if name == i[0]:
            result = i[2]
    return result

def getAssetPath(name,current_project):
    result = ''
    for i in projects_paths:
        if current_project == i[0]:
            for k in i[3]:
                if name == k[0]:
                    result = getProjectPath(current_project) + '/'+ k[1]
                    if not os.path.isdir(result):
                        result = ''
    return result

def isThere(name,list):
    result = False
    for i in list:
        if i == name:
            result = True
    return result

def isAllowedExtension(name):
    result = False
    for i in allowed_extensions:
        if name.find('.'+i) != -1:
            result = True
    return result

def getExtension(name):
    result = ''
    for i in allowed_extensions:
        if name.find('.'+i) != -1:
            result = i
    return result

def getAssetsPathsList(path):
    #asset path structure [ 'name without .ext' , 'asste folder path' ,  'full path' ]
    result = []
    for path, subdirs, files in os.walk(path):
        for x in files:
            if x.endswith(tuple(allowed_extensions)) == True:
                element = os.path.join(path, x)
                result.append([x.replace('.'+getExtension(element),''),path,element])
    return result

def get_preview_path(item):
    #asset path structure [ 'name without .ext' , 'asste folder path' ,  'full path' ]
    return os.path.join(item[1], item[0]+'.jpg')

def load_project_structure(startpath, tree):
    for element in os.listdir(startpath):
        path_info = startpath + "/" + element
        if (not isThere(element,excluded_names)) and (os.path.isdir(path_info)):
            parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
            parent_itm.setData(0, Qt.UserRole, path_info)
            #print(path_info)
            if os.path.isdir(path_info):
                load_project_structure(path_info, parent_itm)
                parent_itm.setIcon(0, QIcon(JAM_path+'/icons/folder.png')) #ADD
            else:
                #parent_itm.setIcon(0, QIcon('assets/file.ico')). ADD
                ik = 0

def get_episodes_list(project_name):
    episode_path = getProjectPath(project_name) +"/" + getEpisodePath(project_name)
    result = []
    for element in os.listdir(episode_path):
        path_info = episode_path + "/" + element
        if (not isThere(element,excluded_names)) and (os.path.isdir(path_info)):
            result.append([os.path.basename(element), path_info])
    print(result)
    return result

def check_animscene_name(episode,name):
    result = False
    if len(name.split(episode+'_')) == 2:
        if (len(name.split(episode+'_')[1]) == 6) and (name.split(episode+'_')[1].endswith('.ma')):
            result = True

    return result

def get_scenes_list(episode,project_name):
    anim_path = getProjectPath(project_name) +"/" + getEpisodePath(project_name)+'/'+episode+'/maya/animation'
    render_path = getProjectPath(project_name) +"/" + getEpisodePath(project_name)+'/'+episode+'/render'
    anim_scenes = []
    render_scenes = []
    if os.path.exists(anim_path):
        for anim_item in os.listdir(anim_path):
            path_info = anim_path + "/" + anim_item
            render_meta_path = render_path + "/" + anim_item.replace('.'+getExtension(anim_item),'')+'/'+anim_item
            if (not isThere(anim_item,excluded_names)) and (os.path.isfile(path_info)) and (check_animscene_name(episode,anim_item)):
                anim_scenes.append([anim_item.replace('.'+getExtension(anim_item),''),path_info,render_meta_path,0])

        for render_item in os.listdir(render_path):
            path_info = render_path + "/" + render_item+'/'+render_item+'.ma'
            if (not isThere(path_info,excluded_names)) and (os.path.isfile(path_info)):
                render_scenes.append([render_item.replace('.'+getExtension(render_item),''),path_info])

        for i in anim_scenes:
            for k in render_scenes:
                if i[0] == k[0]:
                    i[3] = 1
                    i[2] = k[1]
                    break

    print(anim_scenes)
    return anim_scenes

class ReportWindow(QMainWindow):

    def cancel(self):
        self.close()

    def sendReportNote(self,parent,type):
        obj_data = parent.get_current_assetdata_to_report()
        print('DATA0_!!!!: ', obj_data)
        now = datetime.now() # current date and time
        hours = self.ui.spinBox_hours.value()
        text = self.ui.textEdit_maintext.toPlainText()
        path = obj_data[1].replace('.'+getExtension(obj_data[1]),'.json')
        print('DATA1_!!!!: ', text,path)
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        data = []
        report = {
            "type": type,
            "message": text,
            "user": "user",
            "createdTime": date_time,
            "hours": hours
        }
        if not os.path.isfile(path):
            data = json_asset_template
            data['messages'].clear()
        else:
            data = readJSON(path)
        print(data,obj_data)
        data['assetName'] = obj_data[0]
        data['assetType'] = getExtension(obj_data[1])
        if len(data['createdTime']) == 0:
            data['createdTime'] = date_time
        data['messages'].append(report)
        writeJSON(path,data)
        print('DATA_!!!!: ', data)
        parent.updateReportNote()
        self.close()


    def __init__(self,type,parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint)
        self.ui = Ui_report()
        self.ui.setupUi(self)
        obj_outline = parent.get_object_outline_path(parent.get_current_assetdata_to_report())
        out_report_widget = parent.ui.textBrowser_history
        self.ui.lineEdit.setText(obj_outline)
        if type == 'note':
            self.setWindowTitle("Create note")
            self.ui.spinBox_hours.setDisabled(True)
        self.ui.pushButton_cancel.pressed.connect(self.cancel)
        self.ui.pushButton_ok.pressed.connect(partial(self.sendReportNote, parent, type))

class MainWindow(QMainWindow):
    
    def getCurrentAssetsPaths(self):
        result = []
        current_project = self.ui.comboBox_projName.currentText()
        for i in projects_paths:
            if current_project == i[0]:
                result = i[3]
        return result
    
    def isAsset(self,name):
        result = False
        for k in self.getCurrentAssetsPaths():
            if  name.find(k[1]) != -1:
                result = True
        return result

    def updateReportNote(self):
        self.ui.textBrowser_history.clear()
        data = self.get_current_assetdata_to_report()
        path = data[1].replace('.'+getExtension(data[1]),'.json')
        if os.path.exists(path):
            obj_data = readJSON(path)
            if len(obj_data) != 0:
                if len(obj_data['messages']) != 0:
                    text = ''
                    for i in obj_data['messages']:
                        date = i['createdTime']
                        user = i['user']
                        hours = i['hours']
                        body_message = i['message'].split('\n')
                        if i['type'] == 'report':
                            header = '<p align="right" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color: #4D5CC1">Report&nbsp;&nbsp;'+date+'</p>'
                            header += '<p align="right" style=" font-style:italic; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color: #4D5CC1">'+user+'&nbsp;&nbsp;&nbsp;'+str(hours)+'h</p>'
                            message = ''
                            if len(body_message) > 1:
                                for k in body_message:
                                    if k != '':
                                        message += '<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color: #403B45">'+k+'</p>'
                                        message += '<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color: #403B45">&nbsp;</p>'
                            else:
                                message += '<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color: #403B45">'+body_message[0]+'</p>'
                            text += header + message
                        if i['type'] == 'note':
                            
                            header = '<p align="right" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color: #79A762">Note&nbsp;&nbsp;'+date+'</p>'
                            header += '<p align="right" style=" font-style:italic; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color: #79A762">'+user+'</p>'
                            message = ''
                            if len(body_message) > 1:
                                for k in body_message:
                                    if k != '':
                                        message += '<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#3B453D">'+k+'</p>'
                                        message += '<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color: #3B453D">&nbsp;</p>'
                            else:
                                message += '<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color: #3B453D">'+body_message[0]+'</p>'
                            text += header + message
            self.ui.textBrowser_history.setHtml(text)

    def write_prj_state_to_config(self,mode):
        # mode = {'project' , 'asset' , 'episode'}
        init_size = os.path.getsize(json_user_config_path)
        shutil.copyfile(json_user_config_path, json_user_config_path.replace('.json','.jsontmp'))
        current_size = os.path.getsize(json_user_config_path.replace('.json','.jsontmp'))
        f_u = open(json_user_config_path)
        data_u = json.load(f_u)
        if mode == 'project':
            data_u['currentProject'] = self.ui.comboBox_projName.currentText()
        global json_user_cfg_template
        json_user_cfg = json_user_cfg_template
        found = 0
        for i in data_u['configs']:
            if i['projectName'] == self.ui.comboBox_projName.currentText():
                if mode == 'asset':
                    i['currentAssetType'] = self.ui.comboBox_aTypes.currentText()
                if mode == 'episode':
                    if self.ui.listWidget_episodes.currentItem() != None:
                        i['currentEpisode'] = self.ui.listWidget_episodes.currentItem().text()
                    else:
                        i['currentEpisode'] = ''
                found = 1
        if found == 0:
            json_user_cfg['projectName'] = data_u['currentProject']
            json_user_cfg['currentAssetType'] = self.ui.comboBox_aTypes.currentText()
            if self.ui.listWidget_episodes.currentItem() != None:
                json_user_cfg['currentEpisode'] = self.ui.listWidget_episodes.currentItem().text()
            else:
                json_user_cfg['currentEpisode'] = ''

            data_u['configs'].append(json_user_cfg)

        if init_size == current_size:
            with open(json_user_config_path, 'w') as f:
                json.dump(data_u, f)
            f.close()
            os.remove(json_user_config_path.replace('.json','.jsontmp'))

        f_u.close()
        #print('Wrote to JSON: ', data_u['currentProject'], ' ', data_u['currentAssetType'], ' ', data_u['currentEpisode'])

    def get_current_project_path(self):
        return getProjectPath(self.ui.comboBox_projName.currentText())

    def asset_path_to_outline(self):
        item = self.ui.listWidget_assets.currentItem().data(Qt.UserRole)
        proj_name = self.ui.comboBox_projName.currentText()
        text = proj_name + item[1].replace(self.get_current_project_path(),'').replace('/','|').replace('\\','|') + '|' + item[0]
        self.ui.lineEdit_fullPath.setText(text)

    def scene_path_to_outline(self):
        if len(self.ui.tableWidget_scenesTable.selectedItems()) != 0:
            item = self.ui.tableWidget_scenesTable.selectedItems()[1].data(Qt.UserRole)
            proj_name = self.ui.comboBox_projName.currentText()
            text = proj_name + item[2].replace(self.get_current_project_path(),'').replace('/','|').replace('\\','|').replace('.ma','')
            self.ui.lineEdit_fullPath.setText(text)

    def go_to_asset(self):
        name = self.ui.lineEdit_fullPath.text()
        proj_name = ''
        element_name = ''
        dir_path = self.get_current_project_path() + '/'
        if len(name) != 0:
            splitted = name.split('|')
            if len(splitted) != 0:
                proj_name = splitted[0]
                element_name = splitted[len(splitted)-1]
            for i in range(1,len(splitted)-1):
                dir_path += splitted[i] + '/'
        print(proj_name,' ',element_name,' ',dir_path, ' ',self.isAsset(dir_path))

        if self.isAsset(dir_path):
            print('this is the asset')
            self.ui.tabWidget.setCurrentWidget(self.ui.tabWidget.findChild(QWidget, 'tab'))
            found_items_buff = self.ui.listWidget_assets.findItems(element_name,Qt.MatchFlag.MatchExactly)
            found_items = []
            for i in found_items_buff:
                path_tmp = i.data(Qt.UserRole)[2]
                if path_tmp.startswith(dir_path+element_name):
                    found_items.append(i)
            print(found_items)
            if len(found_items) != 0:
                for i in found_items:
                    print('TMP: ', dir_path+element_name+'.'+getExtension(i.data(Qt.UserRole)[2]),'   ',dir_path+element_name+'.'+getExtension(i.data(Qt.UserRole)[2]))
                    print('add: ', i.data(Qt.UserRole)[2])
                    if i.data(Qt.UserRole)[2] == dir_path+element_name+'.'+getExtension(i.data(Qt.UserRole)[2]):
                        print('FOUND: ', i.data(Qt.UserRole)[2])
                        self.ui.listWidget_assets.setCurrentItem(i)
                        self.ui.listWidget_assets.scrollToItem(i,QAbstractItemView.PositionAtTop)
                        # add FOCUS
            else:
                    print(dir_path[:-1],os.listdir(dir_path))
                    for i in os.listdir(dir_path):
                        path = dir_path+i
                        if (path.startswith(dir_path+element_name))and(isAllowedExtension(path)):
                            self.ui.listWidget_assets.clear()
                            if getExtension(i):
                                item = [element_name,dir_path[:-1],path]
                                self.ui.listWidget_assets.clear()
                                self.createAssetItem(item)
                                current_item = self.ui.listWidget_assets.findItems(element_name,Qt.MatchFlag.MatchExactly)
                                if len(current_item) != 0:
                                    self.ui.listWidget_assets.setCurrentItem(current_item[0])
        else:
            print('this is the scene')
            self.ui.tabWidget.setCurrentWidget(self.ui.tabWidget.findChild(QWidget, 'tab_2'))
            found_items_buff = self.ui.tableWidget_scenesTable.findItems(element_name,Qt.MatchFlag.MatchExactly)
            #print(found_items_buff[0].data(Qt.UserRole))
            found_items = []
            for i in found_items_buff:
                path_tmp = i.data(Qt.UserRole)[2]
                if path_tmp.startswith(dir_path+element_name):
                    found_items.append(i)
            print(found_items)
            if len(found_items) != 0:
                for i in found_items:
                    print('TMP: ', dir_path+element_name+'.'+getExtension(i.data(Qt.UserRole)[2]),'   ',dir_path+element_name+'.'+getExtension(i.data(Qt.UserRole)[2]))
                    print('add: ', i.data(Qt.UserRole)[2])
                    if i.data(Qt.UserRole)[2] == dir_path+element_name+'.'+getExtension(i.data(Qt.UserRole)[2]):
                        print('FOUND: ', i.data(Qt.UserRole)[2])
                        self.ui.tableWidget_scenesTable.setCurrentItem(i)
                        self.ui.tableWidget_scenesTable.scrollToItem(i,QAbstractItemView.PositionAtTop)
                        # add FOCUS
            else:
                    files_ = []
                    if not os.path.exists(dir_path):
                        files_.append(element_name+'.ma')
                    else:
                        files_ = os.listdir(dir_path)
                    print(dir_path[:-1],files_,os.path.exists(dir_path))
                    for i in files_:
                        path = dir_path+i
                        if (path.startswith(dir_path+element_name))and(isAllowedExtension(path)):
                            if getExtension(i):
                                self.ui.tableWidget_scenesTable.clearContents()
                                self.createSceneItem(name)
                                current_item = self.ui.tableWidget_scenesTable.findItems(element_name,Qt.MatchFlag.MatchExactly)
                                if len(current_item) != 0:
                                    for k in current_item:
                                        if k.data(Qt.UserRole)[2] == dir_path+element_name+'.'+getExtension(k.data(Qt.UserRole)[2]):
                                            self.ui.tableWidget_scenesTable.setCurrentItem(current_item[0])



    def updateProject(self):
        self.ui.comboBox_projName.clear()
        for i in projects_paths:
            self.ui.comboBox_projName.addItem(i[0])
        self.ui.comboBox_projName.setCurrentIndex(self.ui.comboBox_projName.findText(current_user_state[0]))

    def get_current_asset_type(self):
        result = ''
        for i in current_user_state[1]:
            if i[0] == self.ui.comboBox_projName.currentText():
                result = i[1]
        return result
    
    def get_current_episode(self):
        result = ''
        for i in current_user_state[1]:
            if i[0] == self.ui.comboBox_projName.currentText():
                result = i[2]
        return result
    
    def initEpisode(self):
        if len(self.ui.listWidget_episodes.findItems(self.get_current_episode(), Qt.MatchFlag.MatchExactly)) != 0:
            self.ui.listWidget_episodes.setCurrentItem(self.ui.listWidget_episodes.findItems(self.get_current_episode(), Qt.MatchFlag.MatchExactly)[0])
    
    def updateAssetTypes(self):
        self.ui.comboBox_aTypes.clear()
        atlist  =  []
        for atname in self.getCurrentAssetsPaths():
            atlist.append(atname[0])
        self.ui.comboBox_aTypes.addItems(atlist)
        self.ui.comboBox_aTypes.setCurrentIndex(self.ui.comboBox_aTypes.findText(self.get_current_asset_type()))

    def updateAssetTree(self):
        self.ui.treeWidget_assetFolders.clear()
        projectTreeWidget = self.ui.treeWidget_assetFolders
        path = getAssetPath(self.ui.comboBox_aTypes.currentText(),self.ui.comboBox_projName.currentText())
        parent_itm = QTreeWidgetItem(projectTreeWidget, ['[root]'])
        parent_itm.setIcon(0, QIcon(JAM_path+'/icons/base_01.png'))
        parent_itm.setData(0, Qt.UserRole, path)
        print('path:   ', path)
        if len(path) != 0:
            load_project_structure(path,parent_itm)
        self.ui.treeWidget_assetFolders.expandAll()
        self.updateAssets()
        self.write_prj_state_to_config('asset') # write current statement to json


    def updateEpisodeList(self):
        self.ui.listWidget_episodes.clear()
        list = get_episodes_list(self.ui.comboBox_projName.currentText())
        for i in list:
            listItem = QListWidgetItem(i[0])
            listItem.setData(Qt.UserRole,i[1])
            #new_item_status = QTableWidgetItem()
            #new_item_scene = QTableWidgetItem()
            #new_item_note = QTableWidgetItem()
            #new_item_scene.setData(Qt.UserRole,item)
            self.ui.listWidget_episodes.addItem(listItem)

    def getAssetDir(self):
        print(self.ui.treeWidget_assetFolders.currentItem().data(0, Qt.UserRole))
        #path = getAssetPath(self.ui.comboBox_aTypes.currentText(),self.ui.comboBox_projName.currentText())

    def createAssetItem(self,item):
        icon_path = ''
        if os.path.exists(get_preview_path(item)):
            icon_path = get_preview_path(item)
        else:
            icon_path = JAM_path+'/icons/'+icon_placeholder
        #scaled(QSize(200, 200)
        icoPixmap = QPixmap(icon_path)
        w = icoPixmap.width()
        h = icoPixmap.height()
        scaled = QPixmap()
        #scaled = icoPixmap.scaled(QSize(200,200), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        if w > h:
            dif = (w-h)/2
            scaled = icoPixmap.copy(QRect(dif,0,min(w,h),min(w,h)))
        if w <= h:
            dif = (h-w)/2
            scaled = icoPixmap.copy(QRect(0,dif,min(w,h),min(w,h)))
        #scaled.copy(QRect(0,0,10,10))
        icon = QIcon(scaled)
        new_item = QListWidgetItem(icon,item[0])
        new_item.setData(Qt.UserRole,item)
        self.ui.listWidget_assets.addItem(new_item)

    def updateScenes_from_list(self,list):
        if len(list) != 0:
            for i in enumerate(list):
                status = list[i[0]][0][0]
                color = list[i[0]][0][1] #get color
                new_item_status = QTableWidgetItem(status)
                new_item_status.setText(status)
                new_item_status.setBackground(color)
                new_item_scene = QTableWidgetItem(list[i[0]][1])
                new_item_note = QTableWidgetItem()
                new_item_scene.setData(Qt.UserRole,list[i[0]][2])

                self.ui.tableWidget_scenesTable.setItem(i[0],0,new_item_status)
                self.ui.tableWidget_scenesTable.setItem(i[0],1,new_item_scene)
                self.ui.tableWidget_scenesTable.setItem(i[0],2,new_item_note)

            self.ui.tableWidget_scenesTable.sortByColumn(1,Qt.SortOrder.AscendingOrder)

    def createSceneItem(self,name_am_path):
        proj_name = ''
        element_name = ''
        exist = 0
        dir_path = self.get_current_project_path() + '/'
        if len(name_am_path) != 0:
            splitted = name_am_path.split('|')
            if len(splitted) != 0:
                proj_name = splitted[0]
                element_name = splitted[len(splitted)-1]
            for i in range(1,len(splitted)-1):
                dir_path += splitted[i] + '/'
        print(proj_name,' ',element_name,' ',dir_path, ' ',self.isAsset(dir_path))

        if os.path.isfile(dir_path+element_name+'.ma'):
            exist = 1
            print('ex: ',exist)

        status = 'ready to start'
        color = QColor(114,183,245) #blue color
        if exist:
            status = 'in process'
            color = QColor(139,192,61) #green color
        new_item_status = QTableWidgetItem(status)
        new_item_status.setText(status)
        new_item_status.setBackground(color)
        new_item_scene = QTableWidgetItem(element_name)
        new_item_note = QTableWidgetItem()
        tmp = '/render/'+element_name+'/'
        list = [element_name,dir_path.replace(tmp,'/maya/animation/')+element_name+'.ma',dir_path+element_name+'.ma',exist]
        print(list)
        new_item_scene.setData(Qt.UserRole,list)

        self.ui.tableWidget_scenesTable.setItem(0,0,new_item_status)
        self.ui.tableWidget_scenesTable.setItem(0,1,new_item_scene)
        self.ui.tableWidget_scenesTable.setItem(0,2,new_item_note)

    def updateScenes(self):
        self.ui.tableWidget_scenesTable.clearContents()
        global global_scene_list # initialize globality
        global_scene_list.clear()
        getEpisodeSelected = self.ui.listWidget_episodes.currentItem()
        if getEpisodeSelected != None:
            episode = getEpisodeSelected.text()
            list = []
            print('EPISODE: ',episode)
            list = get_scenes_list(episode,self.ui.comboBox_projName.currentText())
            print('LIST: ',list)
            self.ui.tableWidget_scenesTable.setRowCount(len(list)) 
            for i in enumerate(list):
                status = 'ready to start'
                color = QColor(92,113,245) #ready to start color
                if list[i[0]][3] == 1:
                    status = 'in process'
                    color = QColor(130,95,193) #in progress color
                new_item_status = QTableWidgetItem(status)
                new_item_status.setText(status)
                new_item_status.setBackground(color)
                new_item_scene = QTableWidgetItem(list[i[0]][0])
                new_item_note = QTableWidgetItem()
                new_item_scene.setData(Qt.UserRole,list[i[0]])

                self.ui.tableWidget_scenesTable.setItem(i[0],0,new_item_status)
                self.ui.tableWidget_scenesTable.setItem(i[0],1,new_item_scene)
                self.ui.tableWidget_scenesTable.setItem(i[0],2,new_item_note)

                global_scene_list.append([[status,color],list[i[0]][0],list[i[0]]])

            self.ui.tableWidget_scenesTable.sortByColumn(1,Qt.SortOrder.AscendingOrder)
        self.filter_scenes()
        self.write_prj_state_to_config('episode') # write current statement to json

    def updateAssets(self):
        self.ui.listWidget_assets.clear()
        self.ui.listWidget_assets.setIconSize(QSize(asset_icon_size,asset_icon_size))

        # insert asset folder path when click
        asset_path = []
        getSelected = self.ui.treeWidget_assetFolders.selectedItems()
        item_data = ''

        if getSelected:
            baseNode = getSelected[0]
            qmIndex = self.ui.treeWidget_assetFolders.indexFromItem(baseNode)
            item_data = qmIndex.data(Qt.UserRole)
            #print(item_data)
        if len(item_data) !=  0:
            asset_path = getAssetsPathsList(item_data)
        else:
            asset_path = getAssetsPathsList(getAssetPath(self.ui.comboBox_aTypes.currentText(),self.ui.comboBox_projName.currentText()))
        #print(asset_path)

        #asset path structure [ 'name without .ext' , 'asste folder path' ,  'full path' ]
        global global_asset_list
        global_asset_list.clear()
        # clear global var
        for i in asset_path:
            global_asset_list.append(i) # send list of found assets to global var
            self.createAssetItem(i)
        
        self.filter_assets()

    # actions
    def createScene(self):
        print('create scene')
    def open(self):
        print('open')
    def updateScene(self):
        print('update scene')
    def publishElement(self):
        print('publish')
    def importElement(self):
        print('import')
    def denoise(self):
        print('denoise')
    def checkElement(self):
        print('check')

    def refreshAssets(self):
        print('refresh assets')

    def refreshScenes(self):
        print('refresh scenes')

    def goToAsset(self):
        self.go_to_asset()
        print('go to asset')

    def addReport(self):
        self.showReportWindow()
        print('add report')

    def addNote(self):
        self.showNoteWindow()
        print('add note')

    def copyToClipboard(self):
        print('copy to clipboard')

    def click_on_asset(self):
        self.asset_path_to_outline()
        self.updateReportNote()

    def click_on_scene(self):
        self.scene_path_to_outline()
        self.updateReportNote()

    def filter_scenes(self):
        self.ui.tableWidget_scenesTable.clearContents()
        print(self.ui.lineEdit_scenes_filter.text())
        items = []
        global global_scene_list
        print(global_scene_list)
        filter_text = self.ui.lineEdit_scenes_filter.text()
        for i in global_scene_list:
            sname = i[1]
            name = sname.split('_')
            print(name)
            numbers_name = ''.join(i for i in name[0] if i.isdigit())+' '+''.join(i for i in name[1] if i.isdigit())
            numbers_name_=numbers_name.replace(' ','_')
            int_name = str(int(''.join(i for i in name[0] if i.isdigit())))+' '+str(int(''.join(i for i in name[1] if i.isdigit())))
            int_name_=int_name.replace(' ','_')

            print(numbers_name)
            print(numbers_name_)
            print(int_name)
            print(int_name_)

            if (numbers_name.startswith(filter_text))or(int_name.startswith(filter_text))or(numbers_name_.startswith(filter_text))or(int_name_.startswith(filter_text)):
                print('catch ', i)
                items.append(i)
        #items_tmp = self.ui.listWidget_assets.findItems(self.ui.lineEdit_filter.text(),Qt.MatchFlag.MatchStartsWith)
        self.updateScenes_from_list(items)

        print('filtering scenes')

    def filter_assets(self):
        self.ui.listWidget_assets.clear()
        print(self.ui.lineEdit_filter.text())
        items = []
        global global_asset_list
        for i in global_asset_list:
            print(i)
            if i[0].startswith(self.ui.lineEdit_filter.text()):
                print('catch')
                items.append(i)
        #items_tmp = self.ui.listWidget_assets.findItems(self.ui.lineEdit_filter.text(),Qt.MatchFlag.MatchStartsWith)
        for i in items:
            self.createAssetItem(i)
        print('filtering assets')

    def asset_tree_clicked(self):
        gp = QCursor.pos()
        lp = self.ui.treeWidget_assetFolders.viewport().mapFromGlobal(gp)
        ix_ = self.ui.treeWidget_assetFolders.indexAt(lp)
        print('not')
        if ix_.isValid():
            print('ix_')

    def get_object_outline_path(self,data):
        proj_name = self.ui.comboBox_projName.currentText()
        text = proj_name + data[1].replace(self.get_current_project_path(),'').replace('/','|').replace('\\','|').replace('.'+getExtension(data[1]),'') + '|' + data[0]
        return text

    def get_current_assetdata_to_report(self):
        item = []
        asset_data = []
        if self.ui.tabWidget.currentIndex() == 1:
            if len(self.ui.tableWidget_scenesTable.selectedItems()) != 0:
                item = self.ui.tableWidget_scenesTable.selectedItems()[1].data(Qt.UserRole)
                asset_data = [item[0],item[2]]
        if self.ui.tabWidget.currentIndex() == 0:
            if len(self.ui.listWidget_assets.selectedItems()) != 0:
                item = self.ui.listWidget_assets.currentItem().data(Qt.UserRole)
                asset_data = [item[0],item[2]]
        return asset_data

    def showReportWindow(self):
        if len(self.get_current_assetdata_to_report()) != 0:
            report_window = ReportWindow('report',self)
            report_window.show()

    def showNoteWindow(self):
        if len(self.get_current_assetdata_to_report()) != 0:
            report_window = ReportWindow('note',self)
            report_window.show()

    def set_current_state_assets(self):
        self.ui.comboBox_aTypes.setCurrentIndex(self.ui.comboBox_aTypes.findText(self.get_current_asset_type()))

    def updateAllAssets(self):
        read_user_config()
        self.updateAssetTypes()
        self.updateAssetTree()
        self.updateAssets()
        self.updateEpisodeList()
        self.initEpisode()
        self.updateScenes()
        self.set_current_state_assets()
        self.write_prj_state_to_config('project')

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint)
        self.ui = Ui_jam()
        self.ui.setupUi(self)
        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        
        #self.setWindowTitle("JAM Asset Manager")
        self.setWindowIcon(QIcon(JAM_path+"/icons/icon_jam_purple.png"))
        
        # set icons
        self.ui.toolButton_newScene.setIcon(QIcon(JAM_path+"/icons/icon_jam_purple.png"))
        self.ui.toolButton_sCreate.setIcon(QIcon(JAM_path+"/icons/new_scene.png"))
        self.ui.toolButton_update.setIcon(QIcon(JAM_path+"/icons/update.png"))
        self.ui.toolButton_sUpdate.setIcon(QIcon(JAM_path+"/icons/update.png"))
        self.ui.toolButton_publish.setIcon(QIcon(JAM_path+"/icons/publish.png"))
        self.ui.toolButton_aPublish.setIcon(QIcon(JAM_path+"/icons/publish.png"))
        self.ui.toolButton_sPublish.setIcon(QIcon(JAM_path+"/icons/publish.png"))
        self.ui.toolButton_import.setIcon(QIcon(JAM_path+"/icons/import.png"))
        self.ui.toolButton_aImport.setIcon(QIcon(JAM_path+"/icons/import.png"))
        self.ui.toolButton_denoise.setIcon(QIcon(JAM_path+"/icons/denoise.png"))
        self.ui.toolButton_check.setIcon(QIcon(JAM_path+"/icons/check.png"))
        self.ui.toolButton_aRefresh.setIcon(QIcon(JAM_path+"/icons/refresh.png"))
        self.ui.toolButton_sRefresh.setIcon(QIcon(JAM_path+"/icons/refresh.png"))
        self.ui.toolButton_goto.setIcon(QIcon(JAM_path+"/icons/goto.png"))
        self.ui.toolButton_copyClipboard.setIcon(QIcon(JAM_path+"/icons/clipboard.png"))
        self.ui.toolButton_addReport.setIcon(QIcon(JAM_path+"/icons/add_report.png"))
        self.ui.toolButton_addNote.setIcon(QIcon(JAM_path+"/icons/add_note.png"))
        
        readConfig()
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

        # open scene when double klicked
        self.ui.tableWidget_scenesTable.doubleClicked.connect(self.open)

        # open asset when double klicked
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
        #self.ui.setStyleSheet(u"border: 1px solid #C4C4C3;")
        
        
if __name__ == "__main__":
    widget = MainWindow()
    widget.show()
