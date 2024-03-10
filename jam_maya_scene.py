import maya.cmds as cmds
import os
import sys
import os
import shutil

def get_current_scene_path():
     return cmds.file(q=True, sn=True)

def check_quality():
     result = []
     width = cmds.getAttr("defaultResolution.width")
     height = cmds.getAttr("defaultResolution.height")
     if (width >= 1600)and(height>= 900):
          result = [1,'']
     else:
          result = [0,"The scene wasn't published. Please, change the quality to final."]
     return result

def check_camera_name():
     result = []
     name = os.path.basename(cmds.file(q=True, sn=True)).replace('.ma','').replace('.mb','')
     cameras = cmds.ls(type='camera')
     for camera_ in cameras:
          if cmds.getAttr(camera_+'.renderable'):
               if camera_.startswith(name):
                    result = [1,'']
               else:
                    result = [0,camera_+" is an incorrect camera name. Please change the camera name to match the scene name."]
                    cmds.warning( camera_, ' is an incorrect camera name. Please change the camera name to match the scene name.')
     return result

def scene_check_message():
     result = True
     result_message =[]
     messages = []
     messages.append(check_camera_name())
     messages.append(check_quality())
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

def createRenderScene(name,anim_filename,render_filename,rs_filename):
     fileCheckState = cmds.file(q=True, modified=True)
     current_scene_name = cmds.file(q=True, sn=True)
     if fileCheckState:
          dialog_message = cmds.confirmDialog(title= "Save Changes", message = 'Save changes to '+current_scene_name+'?', button =['Save',"Don't Save", "Cancel"])
          if dialog_message == 'Cancel':
               return
          if dialog_message == 'Save':
               cmds.file( save=True)
     anim_ref_name = render_filename.replace(name+'.ma',name+'_check_v01.ma')
     # create render directory
     os.makedirs(os.path.dirname(render_filename), exist_ok=True)
     # copy check_v01
     shutil.copy(anim_filename, render_filename.replace(name+'.ma',name+'_check_v01.ma'))
     # copy RS
     shutil.copy(rs_filename, render_filename)
     # open renderScene
     cmds.file(new=True, force=True, bls=True)
     cmds.file(render_filename, open=True )
     #ref
     cmds.file(anim_ref_name, reference=True, mergeNamespacesOnClash=True, namespace='anim');

def openRenderScene(path):
     fileCheckState = cmds.file(q=True, modified=True)
     current_scene_name = cmds.file(q=True, sn=True)
     if fileCheckState:
          dialog_message = cmds.confirmDialog(title= "Save Changes", message = 'Save changes to '+current_scene_name+'?', button =['Save',"Don't Save", "Cancel"])
          if dialog_message == 'Cancel':
               return
          if dialog_message == 'Save':
               cmds.file( save=True)
     cmds.file(path, o=True, force=True)

def updateRenderScene(name,anim_filename,render_filename):
     fileCheckState = cmds.file(q=True, modified=True)
     current_scene_name = cmds.file(q=True, sn=True)
     if fileCheckState:
          dialog_message = cmds.confirmDialog(title= "Save Changes", message = 'Save changes to '+current_scene_name+'?', button =['Save',"Don't Save", "Cancel"])
          if dialog_message == 'Cancel':
               return
          if dialog_message == 'Save':
               cmds.file( save=True)
     if os.path.isfile(render_filename):
          anim_ref_name = render_filename.replace(name+'.ma',name+'_check_v01.ma')
          shutil.copy(anim_filename, anim_ref_name)
          # open renderScene
          cmds.file(new=True, force=True, bls=True)
          cmds.file(render_filename, open=True )
     else:
          cmds.warning("The render scene is empty. Please create a scene to be able to update it")

def publish_scene():
     check_message = scene_check_message()
     result = False
     if len(cmds.file(q=True, sn=True)) != 0:
          if check_message[0] == 0:
               cmds.confirmDialog(title= "Warning: Scene wasn't publish", message = check_message[1], button =['OK'])
          else:
               try:
                    cmds.file(save=True)
                    cmds.confirmDialog(title= "The publish was successful!", message = '', button =['OK'])
                    result = True
               except:
                    print("Publishing wasn't successful")
     return result