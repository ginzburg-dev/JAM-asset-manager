import maya.cmds as cmds

path = '/Users/dmitryginzburg/Documents/Ginzburg/Github/JAM-asset-manager/example/Fixies5/scenes/episodes/ep260/maya/animation/'
rpath = '/Users/dmitryginzburg/Documents/Ginzburg/Github/JAM-asset-manager/example/Fixies5/scenes/episodes/ep260/render/'
pref = 'ep260_'
s = 1
e = 49
import sys
import os
import shutil
import random
rand = random.randrange(2)
print(rand)
os.makedirs(os.path.dirname(path), exist_ok=True)
for i in range(s,e):
    name = path+pref+'%03d' % (i*10)+'.ma'
    shutil.copy('/Users/dmitryginzburg/Documents/Ginzburg/Github/JAM-asset-manager/example/Fixies5/scenes/episodes/ep257/maya/animation/ep257_010.ma', name)
    print(name)

os.makedirs(os.path.dirname(path), exist_ok=True)
for i in range(s,e):
    if random.randrange(2) == 1:
        rname = rpath+pref+'%03d' % (i*10)
        os.makedirs(os.path.dirname(rname+'/'), exist_ok=True)
        name = rname+'/'+pref+'%03d' % (i*10)+'.ma'
        print(rname)
        shutil.copy('/Users/dmitryginzburg/Documents/Ginzburg/Github/JAM-asset-manager/example/Fixies5/scenes/episodes/ep257/maya/animation/ep257_010.ma', name)
        
import os
import os.path
json_path = '/Users/dmitryginzburg/Documents/Ginzburg/Github/JAM-asset-manager/example/Fixies5/scenes/episodes/'

for dirpath, dirnames, filenames in os.walk(json_path):
    for filename in [f for f in filenames if f.endswith(".json")]:
        print(os.path.join(dirpath, filename))
        os.remove(os.path.join(dirpath, filename))
        
