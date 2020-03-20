import maya.api.OpenMaya as om

import maya.cmds as cmds


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


class JaysWatchTimeNode(om.MPxNode):

    TYPE_NAME = "jaysWatchTime"
    TYPE_ID = om.MTypeId(0x0007F7F9)
    
    frame_time = None
    
    curr_sec_hand = None
    curr_min_hand = None
    curr_hour_hand = None
    
    new_sec_hand = None
    new_min_hand = None
    new_hour_hand = None
    
    man_min_hand = None
    man_hour_hand = None

    def __init__(self):
        super(JaysWatchTimeNode, self).__init__()

    def compute(self, plug, data):
        if plug == JaysWatchTimeNode.new_sec_hand:
            frame = data.inputValue(JaysWatchTimeNode.frame_time).asDouble()
            curr_sec_rot = data.inputValue(JaysWatchTimeNode.curr_sec_hand).asDouble()
            
            sec_rotation = 0.0
            
            if not frame <= 1:
                seconds = frame / 24.0
                if (seconds % 1) == 0:
                    sec_rotation = (-6 * seconds) * 0.01745
                else:
                    sec_rotation = curr_sec_rot
            
            new_sec_rot = data.outputValue(JaysWatchTimeNode.new_sec_hand)
            new_sec_rot.setDouble(sec_rotation)
            
            data.setClean(plug)
            
        elif plug == JaysWatchTimeNode.new_min_hand:
            frame = data.inputValue(JaysWatchTimeNode.frame_time).asDouble()
            curr_min_rot = data.inputValue(JaysWatchTimeNode.curr_min_hand).asDouble()
            man_min_rot = data.inputValue(JaysWatchTimeNode.man_min_hand).asDouble()
            manual_min_offset = man_min_rot * 0.01745
            
            if frame <= 1:
                min_rotation = 0.0 - manual_min_offset
            else:
                seconds = frame / 24.0
                
                if (seconds % 60) == 0:
                    min_rotation = ((-6.0 * (seconds/60)) * 0.01745) - manual_min_offset
                else:
                    min_rotation = curr_min_rot
            
            new_min_rot = data.outputValue(JaysWatchTimeNode.new_min_hand)
            new_min_rot.setDouble(min_rotation)
            
            data.setClean(plug)
            
        elif plug == JaysWatchTimeNode.new_hour_hand:
            frame = data.inputValue(JaysWatchTimeNode.frame_time).asDouble()
            curr_hour_rot = data.inputValue(JaysWatchTimeNode.curr_hour_hand).asDouble()
            man_hour_rot = data.inputValue(JaysWatchTimeNode.man_hour_hand).asDouble()
            manual_offset = man_hour_rot * 0.01745
            
            if frame <= 1:
                hour_rotation = 0.0 - manual_offset
            else:
                seconds = frame / 24.0
                
                if (seconds % 3600) == 0:
                    hour_rotation = ((-30.0 * (seconds/3600)) * 0.01745) - manual_offset
                else:
                    hour_rotation = curr_hour_rot
                        
            new_hour_rot = data.outputValue(JaysWatchTimeNode.new_hour_hand)
            new_hour_rot.setDouble(hour_rotation)
            
            data.setClean(plug)


    @classmethod
    def creator(cls):
        return JaysWatchTimeNode()

    @classmethod
    def initialize(cls):
        unit_attr = om.MFnUnitAttribute()
        numeric_attr = om.MFnNumericAttribute()
        
        cls.frame_time = numeric_attr.create("time", "tm", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable= True
        numeric_attr.readable = False
        
        cls.curr_sec_hand = unit_attr.create("curr_sec_rotation", "csr", om.MFnUnitAttribute.kAngle, 0.0)
        unit_attr.keyable= True
        unit_attr.readable = False
        
        cls.curr_min_hand = unit_attr.create("curr_min_rotation", "cmr", om.MFnUnitAttribute.kAngle, 0.0)
        unit_attr.keyable= True
        unit_attr.readable = False
        
        cls.curr_hour_hand = unit_attr.create("curr_hour_rotation", "chr", om.MFnUnitAttribute.kAngle, 0.0)
        unit_attr.keyable= True
        unit_attr.readable = False
        
        cls.man_min_hand = numeric_attr.create("man_min_rotation", "mmr", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable= True
        numeric_attr.readable = False
        
        cls.man_hour_hand = numeric_attr.create("man_hour_rotation", "mhr", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable= True
        numeric_attr.readable = False
        
        cls.new_sec_hand = unit_attr.create("new_sec_rot", "nsr", om.MFnUnitAttribute.kAngle, 0.0)
        cls.new_min_hand = unit_attr.create("new_min_rot", "nmr", om.MFnUnitAttribute.kAngle, 0.0)
        cls.new_hour_hand = unit_attr.create("new_hour_rot", "nhr", om.MFnUnitAttribute.kAngle, 0.0)
        
        cls.addAttribute(cls.frame_time)
        cls.addAttribute(cls.curr_sec_hand)
        cls.addAttribute(cls.curr_min_hand)
        cls.addAttribute(cls.curr_hour_hand)
        cls.addAttribute(cls.new_sec_hand)
        cls.addAttribute(cls.new_min_hand)
        cls.addAttribute(cls.new_hour_hand)
        cls.addAttribute(cls.man_min_hand)
        cls.addAttribute(cls.man_hour_hand)
        
        cls.attributeAffects(cls.frame_time, cls.new_sec_hand)
        cls.attributeAffects(cls.frame_time, cls.new_min_hand)
        cls.attributeAffects(cls.frame_time, cls.new_hour_hand)
        
        cls.attributeAffects(cls.curr_sec_hand, cls.new_sec_hand)
        cls.attributeAffects(cls.curr_min_hand, cls.new_min_hand)
        cls.attributeAffects(cls.curr_hour_hand, cls.new_hour_hand)
        
        cls.attributeAffects(cls.man_min_hand, cls.new_min_hand)
        cls.attributeAffects(cls.man_hour_hand, cls.new_hour_hand)


def initializePlugin(plugin):
    """
    Entry point for a plugin.
    """
    vendor = "Jay Elbourne"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode(JaysWatchTimeNode.TYPE_NAME,              
                               JaysWatchTimeNode.TYPE_ID,                
                               JaysWatchTimeNode.creator,                
                               JaysWatchTimeNode.initialize,             
                               om.MPxNode.kDependNode)             
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(JaysWatchTimeNode.TYPE_NAME))

def uninitializePlugin(plugin):
    """
    Exit point for a plugin.
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode(JaysWatchTimeNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to unregister node: {0}".format(JaysWatchTimeNode.TYPE_NAME))


if __name__ == "__main__":
    """
    For Development Only
    """

    # Any code required before unloading the plug-in (e.g. creating a new scene)
    #cmds.file(new=True, force=True)

    # Reload the plugin
    plugin_name = "jays_watch_time_node.py"

    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))


    # Any setup code to help speed up testing (e.g. loading a test scene)
    #cmds.evalDeferred('cmds.createNode("jaysWatchTime")')
