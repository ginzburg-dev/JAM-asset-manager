# This Python file uses the following encoding: utf-8
import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QListWidgetItem, QTreeWidgetItem
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize, QRect

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow


# Asset Manager Configuration
excluded_names  = ['.DS_Store']
allowed_extensions  = ['hdr','ma','mb']
icon_placeholder = 'icon_placeholder.jpg'
#projects = ['Kids','Flo-Flo','Fixies5']
projects_paths = [['Kids', '/Users/dmitryginzburg/UI_example/examplePRJ'],
['Flo-Flo', '/Users/dmitryginzburg/UI_example/examplePRJ'],
['Fixies5', '/Users/dmitryginzburg/UI_example/examplePRJ']]
assets_paths = [['Master Lights', 'MasterLights'],
['Master Shots', 'MasterShots'],
['HDRI Library', 'HDRI'],
['Misc.', 'Misc']]
current_project = 'Fixies5'
current_asset_type = 'Master Lights'
asset_icon_size = 200

def getProjectPath(name):
    result = ''
    for i in projects_paths:
        if name == i[0]:
            result = i[1]
    return result




def getAssetPath(name,current_project):
    result = ''
    for i in assets_paths:
        if name == i[0]:
            result = getProjectPath(current_project) + '/'+ i[1]
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
    result = []
    shpfiles = []
    for path, subdirs, files in os.walk(path):
        for x in files:
            if x.endswith(tuple(allowed_extensions)) == True:
                element = os.path.join(path, x)
                #asset path structure [ 'name without .ext' , 'asste folder path' ,  'full path' ]
                result.append([x.split('.'+getExtension(element))[0],path,element])

    '''
    for element in os.listdir(path):
        file_path = path + '/'+element
        if (os.path.isfile(file_path))and(isAllowedExtension(element)):
            result.append([element.split('.'+getExtension(element))[0],file_path])
    '''
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
                #parent_itm.setIcon(0, QIcon('assets/folder.ico')) ADD
            else:
                #parent_itm.setIcon(0, QIcon('assets/file.ico')). ADD
                ik = 0


def createScene():
    return
def updateScene():
    return
def publishScene():
    return
def getAssetTree():
    return


class MainWindow(QMainWindow):

    def get_current_project_path(self):
        return getProjectPath(self.ui.comboBox_projName.currentText())

    def asset_path_to_outline(self):
        item = self.ui.listWidget_assets.currentItem().data(Qt.UserRole)
        proj_name = self.ui.comboBox_projName.currentText()
        text = proj_name + item[1].replace(self.get_current_project_path(),'').replace('/','|').replace('\\','|') + '|' + item[0]
        self.ui.lineEdit_fullPath.setText(text)

    def updateProject(self):
        self.ui.comboBox_projName.clear()
        for i in projects_paths:
            self.ui.comboBox_projName.addItem(i[0])
        self.ui.comboBox_projName.setCurrentIndex(self.ui.comboBox_projName.findText(current_project))

    def updateAssetTypes(self):
        self.ui.comboBox_aTypes.clear()
        atlist  =  []
        for atname in assets_paths:
            atlist.append(atname[0])
        self.ui.comboBox_aTypes.addItems(atlist)
        self.ui.comboBox_aTypes.setCurrentIndex(self.ui.comboBox_aTypes.findText(current_asset_type))

    def updateAssetTree(self):
        self.ui.treeWidget_assetFolders.clear()
        projectTreeWidget = self.ui.treeWidget_assetFolders
        path = getAssetPath(self.ui.comboBox_aTypes.currentText(),self.ui.comboBox_projName.currentText())
        if len(path) != 0:
            load_project_structure(path,projectTreeWidget)
        self.updateAssets()

    def getAssetDir(self):
        print(self.ui.treeWidget_assetFolders.currentItem().data(0, Qt.UserRole))
        #path = getAssetPath(self.ui.comboBox_aTypes.currentText(),self.ui.comboBox_projName.currentText())

    def createAssetItem(self,item):
        icon_path = ''
        if os.path.exists(get_preview_path(item)):
            icon_path = get_preview_path(item)
        else:
            icon_path = icon_placeholder
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
        print(asset_path)

        #asset path structure [ 'name without .ext' , 'asste folder path' ,  'full path' ]
        for i in asset_path:
            self.createAssetItem(i)

        '''
        self.ui.listWidget_assets.addItem(QListWidgetItem(QIcon("img01.hdr"),"Bounty Island"))
        self.ui.listWidget_assets.addItem(QListWidgetItem(QIcon("img02.jpeg"),"Bounty Island"))
        self.ui.listWidget_assets.addItem(QListWidgetItem(QIcon("img03.jpeg"),"Bounty Island"))
        self.ui.listWidget_assets.addItem(QListWidgetItem(QIcon("img04.jpeg"),"Bounty Island"))
        self.ui.listWidget_assets.addItem(QListWidgetItem(QIcon("img05.jpeg"),"Bounty Island"))
        self.ui.listWidget_assets.addItem(QListWidgetItem(QIcon("img06.jpeg"),"Bounty Island"))
        self.ui.listWidget_assets.addItem(QListWidgetItem(QIcon("img07.jpeg"),"Bounty Island"))
        self.ui.listWidget_assets.addItem(QListWidgetItem(QIcon("img08.jpeg"),"Bounty Island"))
        '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        menu = self.menuBar()
        menu.setNativeMenuBar(False)

        self.updateProject()
        self.updateAssetTypes()
        self.updateAssetTree()
        self.updateAssets()



        # update asset items when the folder changes
        self.ui.treeWidget_assetFolders.clicked.connect(self.updateAssets)

        # update asset tree when the type changes
        self.ui.comboBox_aTypes.currentIndexChanged.connect(self.updateAssetTree)

        # update asset text block when a selection changes
        self.ui.listWidget_assets.clicked.connect(self.asset_path_to_outline)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
