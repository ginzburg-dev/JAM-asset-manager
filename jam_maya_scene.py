import maya.cmds as cmds

dropboxDir = "c:/Users/ginzb/I4K Dropbox";
RSFile = "c:/Ginzburg/Production/Kids/Presets/RS/MG_RS_v02.ma";

def createRenderScene(name,rsfilename):
   if len(name.split(' ')) > 2:
        episode = name.split(' ')[0] + name.split(' ')[1];
        scene = name.split(' ')[2];
   else:
        episode = "MG" + name.split(' ')[0];
        scene = name.split(' ')[1];
   
   animationDir = dropboxDir + "/MG/episodes/" + episode + "/maya/animation/"
   renderDir = dropboxDir + "/MG/episodes/" + episode + "/render/"
   renderSceneDir = renderDir + episode + "_" + scene
   

   animFilePath = animationDir + episode + "_" + scene + ".ma";
   checkScene = renderDir + episode + "_" + scene + "/" + episode + "_" + scene + "_check_v01" + ".ma";
   renderScene = renderDir + episode + "_" + scene + "/" + episode + "_" + scene + ".ma";
   animRefName = "episodes/" + episode + "/render/" + episode + "_" + scene + "/" + episode + "_" + scene + "_check_v01" + ".ma";

   # create render directory
   cmds.sysFile( renderSceneDir, makeDir=True )# Windows
   # copy check_v01
   cmds.sysFile( animFilePath, copy=checkScene )# Windows
   # copy RS
   cmds.sysFile( rsfilename, copy=renderScene )# Windows
   # open renderScene
   cmds.file(new=True, force=True, bls=True)
   cmds.file( renderScene, open=True )


   #ref
   cmds.file(animRefName, reference=True, mergeNamespacesOnClash=True, namespace='anim');

def updateRenderScene(name,rsfilename):
   if len(name.split(' ')) > 2:
        episode = name.split(' ')[0] + name.split(' ')[1];
        scene = name.split(' ')[2];
   else:
        episode = "MG" + name.split(' ')[0];
        scene = name.split(' ')[1];
   
   animationDir = dropboxDir + "/MG/episodes/" + episode + "/maya/animation/"
   renderDir = dropboxDir + "/MG/episodes/" + episode + "/render/"
   renderSceneDir = renderDir + episode + "_" + scene
   

   animFilePath = animationDir + episode + "_" + scene + ".ma";
   checkScene = renderDir + episode + "_" + scene + "/" + episode + "_" + scene + "_check_v01" + ".ma";
   renderScene = renderDir + episode + "_" + scene + "/" + episode + "_" + scene + ".ma";
   animRefName = "episodes/" + episode + "/render/" + episode + "_" + scene + "/" + episode + "_" + scene + "_check_v01" + ".ma";

   # create render directory
   #cmds.sysFile( renderSceneDir, makeDir=True )# Windows
   # copy check_v01
   cmds.sysFile( animFilePath, copy=checkScene )# Windows
   # copy RS
   #cmds.sysFile( rsfilename, copy=renderScene )# Windows
   # open renderScene
   cmds.file(new=True, force=True, bls=True)
   cmds.file( renderScene, open=True )


   #ref
   #cmds.file(animRefName, reference=True, mergeNamespacesOnClash=True, namespace='anim');


result = cmds.promptDialog(
		title='Create Render Scene KIDS',
		message='Enter Name:',
		button=['OK', 'Cancel'],
		defaultButton='OK',
		cancelButton='Cancel',
		dismissString='Cancel')

if result == 'OK':
	text = cmds.promptDialog(query=True, text=True);
	if len(text.split(' ')) > 1:
	    createRenderScene(text,RSFile);
	else:
	    print "Wrong Scene Name";