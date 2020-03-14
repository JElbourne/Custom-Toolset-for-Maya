from maya import cmds
import maya.mel as mel

def align_joints():
    
    selections = cmds.ls(typ="joint", sl=True) or []
    print selections
    
    if not selections or len(selections) < 2:
        print("You must have two joints selected")
        return
    
    cmds.aimConstraint( selections[1], selections[0], skip=["x"] )
        
    rotx = cmds.getAttr(selections[0] + ".rx")
    roty = cmds.getAttr(selections[0] + ".ry")
    rotz = cmds.getAttr(selections[0] + ".rz")
    
    if cmds.listRelatives(selections[0], typ="aimConstraint"):
        cmds.delete(selections[0], cn=True)
    elif cmds.listRelatives(selections[1], typ="aimConstraint"):
        cmds.delete(selections[1], cn=True)
    
    cmds.makeIdentity(selections[0], apply=True, r=True)
    cmds.parent(selections[1], selections[0])
    
align_joints()