from tweener_ui_script import tween
from gear_creator_script import Gear

from maya import cmds

class BaseWindow(object):
    
    windowName = "JaysToolsWindow"
    
    def show(self):
        if cmds.window(self.windowName,q=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)
        self.build_ui()
        cmds.showWindow()
        
    def build_ui(self):
        pass
        
    def reset(self, *args):
        pass
        
    def close(self, *args):
        cmds.deleteUI(self.windowName)

class TweenerUI(BaseWindow):
    
    windowName = "TweenerUI"
    
    def build_ui(self):
        column = cmds.columnLayout()
        
        cmds.text(label="Use this slider to set the tween amount")
        
        row = cmds.rowLayout(numberOfColumns=2)
        
        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)
        
        cmds.button(label="Reset Slider", command=self.reset)
        
        cmds.setParent(column)
        cmds.button(label="Close Window", command=self.close)
        
        
    def reset(self, *args):
        cmds.floatSlider(self.slider, e=True, value=50)
        
class GearUI(BaseWindow):
    
    windowName = "GearMaker"
    
    def __init__(self):
        self.gear = None
    
    def build_ui(self):
        
        column = cmds.columnLayout()
        cmds.text(label="Use the slider to modify the Gear")
        
        row = cmds.rowLayout(numberOfColumns=4)
        
        self.label = cmds.label = cmds.text(label="10")
        self.slider = cmds.intSlider(min=5, max=30, value=10, step=1, dragCommand=self.modifyGear)
        
        cmds.button(label="Make Gear", command=self.makeGear)
        
        cmds.button(label="Reset", command=self.reset)
        
        cmds.setParent(column)
        cmds.button(label="Close Window", command=self.close)
    
    def makeGear(self, *args):
        teeth = cmds.intSlider(self.slider, q=True, value=True)
        
        self.gear = Gear()
        self.gear.create_gear(teeth=teeth)
    
    def modifyGear(self, teeth):
        if self.gear:
            self.gear.change_teeth(teeth)
         
        cmds.text(self.label, e=True, label=teeth)
    
    def reset(self, *args):
        self.gear = None
        cmds.intSlider(self.slider, e=True, value=10)
        cmds.text(self.label, e=True, label=10)
        