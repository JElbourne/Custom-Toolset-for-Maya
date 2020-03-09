from maya import cmds

def tween(percentage, obj=None, attrs=None, selection=True):
    
    # We must have either an object or allow selections
    if not obj and not selection:
        raise ValueError("No object given to tween")
      
    # If we dont have an object use the first selection
    if not obj:
        obj = cmds.ls(selection=True)[0]
        
    if not attrs:
        attrs = cmds.listAttr(obj, keyable=True)
    
    current_time = cmds.currentTime(q=True)
    
    for attr in attrs:
        # construct the full name of the attribuite with its object
        attr_full = "{0}.{1}".format(obj, attr)
        
        # Get the keyframes of the attribute on this object
        keyframes = cmds.keyframe(attr_full, q=True)
        
        if not keyframes:
            continue
        
        previous_keyframes = [frame for frame in keyframes if frame < current_time]
        later_keyframes = [frame for frame in keyframes if frame > current_time]
        
        if not previous_keyframes and not later_keyframes:
            continue
            
        previous_keyframe = max(previous_keyframes) if previous_keyframes else None
        next_keyframe = min(later_keyframes) if later_keyframes else None
        
        if not previous_keyframe or not next_keyframe:
            continue
        
        previous_value = cmds.getAttr(attr_full, time=previous_keyframe)
        next_value = cmds.getAttr(attr_full, time=next_keyframe)
        
        difference = next_value - previous_value
        weighted_diff = (difference * percentage)/ 100.0
        
        current_value = previous_value + weighted_diff
        
        cmds.setKeyframe(attr_full, time=current_time, value=current_value)


class TweenWindow(object):
    
    windowName = "TweenerWindow"
    
    def show(self):
        if cmds.window(self.windowName,q=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)
        self.build_ui()
        cmds.showWindow()
        
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
        
    def close(self, *args):
        cmds.deleteUI(self.windowName)