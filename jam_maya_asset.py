import maya.cmds as cmds
import os
import sys
import os
import shutil

def import_asset(path):
     result = False
     if os.path.isfile(path):
          cmds.file(path,mergeNamespacesOnClash=True,ra=True,namespace=":",i=True)
          result = True
     return result

def asset_check_message():
     result = True
     result_message =[]
     messages = []
     # checkers here
     #messages.append(check_camera_name())
     #messages.append(check_quality())
     text = ''
     for message in messages:
          if message[0] == 0:
               text += message[1]+'\n\n'
               result = False
     if result:
          result_message =[1,'']
     else:
          result_message =[0,text]

     return result_message

def publish_asset():
     check_message = asset_check_message()
     result = False
     if len(cmds.file(q=True, sn=True)) != 0:
          if check_message[0] == 0:
               cmds.confirmDialog(title= "Warning. Asset wasn't publish", message = check_message[1], button =['OK'])
          else:
               try:
                    cmds.file(save=True)
                    cmds.confirmDialog(title= "The publish was successful!", message = '', button =['OK'])
                    result = True
               except:
                    print("Publishing wasn't successful")
     return result