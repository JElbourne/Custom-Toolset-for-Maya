from maya import cmds
import maya.mel as mel

def align_joints():
    
    selections = cmds.ls(typ="joint", sl=True)
    
    print selections[0]
    
    if not selections or len(selections) < 2:
        raise TypeError("You must have two joints selected")
    
    cmds.aimConstraint( selections[1], selections[0], skip=["x"] )
    constrains = cmds.listRelatives(selections[0], typ="aimConstraint")
    cmds.delete(selections[0], cn=True)
    
    mel.eval("CBdeleteConnection " + selections[0] + ".rx")
    mel.eval("CBdeleteConnection " + selections[0] + ".ry")
    mel.eval("CBdeleteConnection " + selections[0] + ".rz")  
    
    cmds.makeIdentity(selections[0], apply=True, r=True)
    cmds.parent(selections[1], selections[0])
    
align_joints()