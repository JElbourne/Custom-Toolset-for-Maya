from maya import cmds

def place_joint_in_center():
    
    #selections = cmds.ls(typ="mesh", sl=True)
    
    sel = cmds.ls(sl=True, o=True)[0]
    sel_vtx = cmds.ls('{0}.vtx[:]'.format(sel), sl=True, fl=True)
    
    print sel
    print sel_vtx
    #print cmds.objectType(selections[0])
    
    xpos = ypos = zpos = 0
    for vtx in sel_vtx:
        vtx_pos = cmds.pointPosition(vtx, w=True)
        xpos += vtx_pos[0]
        ypos += vtx_pos[1]
        zpos += vtx_pos[2]
    
    xpos = xpos/len(sel_vtx)
    ypos = ypos/len(sel_vtx)
    zpos = zpos/len(sel_vtx)
    
    cmds.joint( p=(xpos, ypos, zpos) )
     
    
place_joint_in_center()