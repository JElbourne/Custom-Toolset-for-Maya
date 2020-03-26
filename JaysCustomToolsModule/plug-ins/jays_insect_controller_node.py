import maya.api.OpenMaya as om

import maya.cmds as cmds


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


class JaysInsectNode(om.MPxNode):

    # Class Variables
    TYPE_NAME = "jaysInsectNode"
    TYPE_ID = om.MTypeId(0x0007F7F8)
    
    # Class Plug Variable
    frame_time = None
    controller_translate = None
    mct_X = None
    mct_Y = None
    mct_Z = None
    
    plant_foot_out = None
    step_forward_out = None
    translateX = None
    translateZ = None
    rotateY = None
    
    # Instance variables
    old_location = om.MVector(0, 0, 0)
    total_travel = 0.0
    plant_foot = 1.0
    speed = 0.0


    def __init__(self):
        super(JaysInsectNode, self).__init__()
        self.total_travel = 0.0
        self.plant_foot = 1.0
        self.speed = 0.0
    
    def stepTransform(self, data):
        frame = data.inputValue(JaysInsectNode.frame_time).asDouble()
        cX = data.inputValue(JaysInsectNode.mct_X).asDouble()
        cY = data.inputValue(JaysInsectNode.mct_Y).asDouble()
        cZ = data.inputValue(JaysInsectNode.mct_Z).asDouble()
        location = om.MVector(cX, cY, cZ)
        
        if frame == 0:
            self.old_location = location
            self.total_travel = 0.0
            self.plant_foot = 1.0
            self.speed = 0.0
            
        vector_traveled = location - self.old_location
        self.speed = om.MVector(vector_traveled).length()
        self.total_travel += self.speed
        
        self.old_location = location
        
        new_step_forward = data.outputValue(JaysInsectNode.step_forward_out)
        new_step_forward.setDouble(self.total_travel)
        
        return True           
            
    def plantFootUpdate(self, data):
        if self.speed <= 0 and self.plant_foot > 0:
            self.plant_foot = max(0, self.plant_foot - 0.1)
        elif self.speed > 0 and self.plant_foot < 1:
            self.plant_foot = min(1, self.plant_foot + 0.1)
            
        new_plant_foot = data.outputValue(JaysInsectNode.plant_foot_out)
        new_plant_foot.setDouble(self.plant_foot)
        
        return True
        
    def compute(self, plug, data):
        if plug == JaysInsectNode.step_forward_out:
            if self.stepTransform(data):
                data.setClean(plug)

        if plug == JaysInsectNode.plant_foot_out:
            if self.plantFootUpdate(data):
                data.setClean(plug)


    @classmethod
    def creator(cls):
        return JaysInsectNode()

    @classmethod
    def initialize(cls):
        unit_attr = om.MFnUnitAttribute()
        numeric_attr = om.MFnNumericAttribute()
        compound_attr = om.MFnCompoundAttribute()
        
        cls.frame_time = numeric_attr.create("time", "tm", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable= True
        numeric_attr.readable = False
        
        # This is a compount attribute of 3 values for the input Controller Translate
        cls.controller_translate = compound_attr.create("controllerTranslate", 'ct')
        cls.mct_X = unit_attr.create("controllerTranlateX", "ctX", om.MFnUnitAttribute.kDistance, 0.0)
        unit_attr.keyable= True
        unit_attr.readable = False
        compound_attr.addChild(cls.mct_X)
        cls.mct_Y = unit_attr.create("controllerTranlateY", "ctY", om.MFnUnitAttribute.kDistance, 0.0)
        unit_attr.keyable= True
        unit_attr.readable = False
        compound_attr.addChild(cls.mct_Y)
        cls.mct_Z = unit_attr.create("controllerTranlateZ", "ctZ", om.MFnUnitAttribute.kDistance, 0.0)
        unit_attr.keyable= True
        unit_attr.readable = False
        compound_attr.addChild(cls.mct_Z)
            
        # Output plugs
        cls.plant_foot_out = numeric_attr.create("PlantFootOut", "pfo", om.MFnNumericData.kDouble, 0.0)
        cls.step_forward_out = numeric_attr.create("StepsForward", "sf", om.MFnNumericData.kDouble, 0.0)
        cls.translateX = numeric_attr.create("TranslateX", "tx", om.MFnNumericData.kDouble, 0.0)
        cls.translateZ = numeric_attr.create("TranslateZ", "tz", om.MFnNumericData.kDouble, 0.0)  
        cls.rotateY = unit_attr.create("RotateY", "ry", om.MFnUnitAttribute.kAngle, 0.0)
        
        
        cls.addAttribute(cls.frame_time)
        cls.addAttribute(cls.controller_translate)
        cls.addAttribute(cls.plant_foot_out)
        cls.addAttribute(cls.step_forward_out)
        cls.addAttribute(cls.translateX)
        cls.addAttribute(cls.translateZ)
        cls.addAttribute(cls.rotateY)
        
        cls.attributeAffects(cls.frame_time, cls.plant_foot_out)
        cls.attributeAffects(cls.mct_X, cls.step_forward_out)
        cls.attributeAffects(cls.mct_Y, cls.step_forward_out)
        cls.attributeAffects(cls.mct_Z, cls.step_forward_out)


def initializePlugin(plugin):
    """
    Entry point for a plugin.
    """
    vendor = "Jay Elbourne"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode(JaysInsectNode.TYPE_NAME,              
                               JaysInsectNode.TYPE_ID,                
                               JaysInsectNode.creator,                
                               JaysInsectNode.initialize,             
                               om.MPxNode.kDependNode)             
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(JaysInsectNode.TYPE_NAME))

def uninitializePlugin(plugin):
    """
    Exit point for a plugin.
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode(JaysInsectNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to unregister node: {0}".format(JaysInsectNode.TYPE_NAME))


if __name__ == "__main__":
    """
    For Development Only
    """

    # Any code required before unloading the plug-in (e.g. creating a new scene)
    #cmds.file(new=True, force=True)

    # Reload the plugin
    plugin_name = "jays_insect_controller_node.py"

    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))


    # Any setup code to help speed up testing (e.g. loading a test scene)
    #cmds.evalDeferred('cmds.createNode("jaysInsectNode")')
