from maya import cmds
import os
import json
import pprint

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary')


def create_directory(directory=DIRECTORY):
    """
    Create the given directory if it doesnt exist already.
    
    Args:
        directory (str): The directory to create
    """
    if not os.path.exists(directory):
        os.mkdir(directory)
        

class ControllerLibrary(dict):
    
    def save(self, name, directory=DIRECTORY, screenshot=True, **info):
        
        create_directory(directory)
        
        path = os.path.join(directory, "{0}.ma".format(name))
        infoFile = os.path.join(directory, "{0}.json".format(name))
        
        info['name'] = name
        info['path'] = path
        
        cmds.file(rename=path)
        
        if cmds.ls(selection=True):
            cmds.file(force=True, type="mayaAscii", exportSelected=True)
        else:
            cmds.file(save=True, type="mayaAscii", force=True)
        
        if screenshot:
            info['screenshot'] = self.saveScreenshot(name, directory=directory)
        
        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)
            
        self[name] = info
 
 
    def find(self, directory=DIRECTORY):
        self.clear()
        
        info = {}
        if not os.path.exists(directory):
            return
            
        files = os.listdir(directory)
        mayaFiles = [f for f in files if f.endswith('.ma')]
        
        for mf in mayaFiles:
            name, ext = os.path.splitext(mf)
            path = os.path.join(directory, mf)
            
            infoFile = "{0}.json".format(name)
            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)
            
                with open(infoFile, 'r') as f:
                    info = json.load(f)
                    
            else:
                info = {}
                
            screenshot = "{0}.jpg".format(name)
            if screenshot in files:
                info['screenshot'] = os.path.join(directory, screenshot)
            
            info['name'] = name
            info['path'] = path
            
            self[name] = info

    
    def load(self, name):
        path = self[name]['path']
        
        cmds.file(path, i=True, usingNamespaces=False)
            
    def saveScreenshot(self, name, directory=DIRECTORY):
        path = os.path.join(directory, "{0}.jpg".format(name))
        
        cmds.viewFit()
        cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
        
        cmds.playblast(completeFilename=path,
                        forceOverwrite=True,
                        format="image",
                        width=200,
                        height=200,
                        showOrnaments=False,
                        startTime=1,
                        endTime=1,
                        viewer=False,)
        

        return path