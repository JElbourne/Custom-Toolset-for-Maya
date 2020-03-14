from maya import cmds

def place_joint_in_center():
    
    selections = cmds.ls(sl=True, o=True) or []
    print selections
    if not selections or len(selections[0]) < 2 :
        print("You must have an edgeloop selected")
        return
        
    sel_vtx = cmds.ls('{0}.vtx[:]'.format(selections[0]), sl=True, fl=True)
    
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