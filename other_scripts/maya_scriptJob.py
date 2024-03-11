import maya.cmds as cmds

def mayaSceneOpened():
    print("Scene has been loaded")

job_scene_opened = cmds.scriptJob(runOnce = True, e=('SceneOpened', mayaSceneOpened))
