from tweener_ui_script import tween

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
        
        