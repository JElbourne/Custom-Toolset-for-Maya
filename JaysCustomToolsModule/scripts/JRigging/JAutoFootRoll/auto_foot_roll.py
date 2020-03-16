from maya import cmds
import maya.OpenMaya as om

import pymel.core as pm


class FootRoll(object):
    SIDE = "l"
    FC_NAME_OVERRIDE = None
    FOOT_WIDTH = 5
    HEEL_OFFSET = 2
    GRND_HGT_OFFSET = 0
    
    foot_controller = None
    knee_polevector = None
    leg_ik = None
    ball_ik = None
    toe_ik = None
    leg_bone = None
    knee_bone = None
    ankle_bone = None
    foot_ball_bone = None
    foot_toe_bone = None

    
    def __init__(self, side="L", foot_width=5, heel_offset=2, grnd_hgt_offset=0, fc_name_override=None):
        self.SIDE = side
        self.FC_NAME_OVERRIDE = fc_name_override
        self.FOOT_WIDTH = foot_width
        self.HEEL_OFFSET = heel_offset
        self.GRND_HGT_OFFSET = grnd_hgt_offset
    
    def assign_ik(self):
        message = ""
        sel = cmds.ls(type="ikHandle", selection=True) or []
        if not sel:
            self.ik_handle = None
            message = "You must select one ikHandle."
            om.MGlobal.displayError(message)
        elif len(sel) > 1:
            self.ik_handle = None
            message = "Too many selections. Select only one ikHandle."
            om.MGlobal.displayError(message)
        else:
            self.ik_handle = sel[0]
        
        return (self.get_ik_display_name(), message)
    
    def assign_joints(self):
        message = ""
        leg_joint = cmds.ls(type="joint", selection=True) or []
        
        if not leg_joint:
            self.leg_bone = None
            self.knee_bone = None
            self.ankle_bone = None
            self.foot_ball_bone = None
            self.foot_toe_bone = None
            message = "You must select: one Leg Joint"
            om.MGlobal.displayError(message)
        elif len(leg_joint) > 1:
            self.leg_bone = None
            self.knee_bone = None
            self.ankle_bone = None
            self.foot_ball_bone = None
            self.foot_toe_bone = None
            message = "Too many selections. Select only one Leg Joint."
            om.MGlobal.displayError(message)
        else:
            self.leg_bone = leg_joint[0]
            knee_joint = cmds.listRelatives(leg_joint[0], children=True, path=True) or []
            if not knee_joint:
                self.knee_bone = None
                self.ankle_bone = None
                self.foot_ball_bone = None
                self.foot_toe_bone = None
                message += "The leg joint selected does not have required knee joint in hierarchy"
                om.MGlobal.displayError(message)
            else:
                self.knee_bone = knee_joint[0]
                ankle_joint = cmds.listRelatives(knee_joint[0], children=True, path=True) or []
                if not ankle_joint:
                    self.ankle_bone = None
                    self.foot_ball_bone = None
                    self.foot_toe_bone = None
                    message += "The leg joint selected does not have required ankle joint in hierarchy"
                    om.MGlobal.displayError(message)
                else:
                    self.ankle_bone = ankle_joint[0]
                    ball_joint = cmds.listRelatives(ankle_joint[0], children=True, path=True) or []
                    print ball_joint
                    if not ball_joint:
                        self.foot_ball_bone = None
                        self.foot_toe_bone = None
                        message += "The leg joint selected does not have required ball joint in hierarchy"
                        om.MGlobal.displayError(message)
                    else:
                        self.foot_ball_bone = ball_joint[0]
                        toe_joint = cmds.listRelatives(ball_joint[0], children=True, path=True) or []
                        if not toe_joint:
                            self.foot_toe_bone = None
                            message += "The leg joint selected does not have required ball joint in hierarchy"
                            om.MGlobal.displayError(message)
                        else:
                            self.foot_toe_bone = toe_joint[0]
                    
        
        return (self.get_leg_display_name(),
                self.get_knee_display_name(),
                self.get_ankle_display_name(),
                self.get_ball_display_name(),
                self.get_toe_display_name(),
                message)
 
        
    def clear_joints(self):
        message = ""
        self.leg_bone = None
        self.knee_bone = None
        self.ankle_bone = None
        self.foot_ball_bone = None
        self.foot_toe_bone = None
        return (self.get_leg_display_name(),
                self.get_knee_display_name(),
                self.get_ankle_display_name(),
                self.get_ball_display_name(),
                self.get_toe_display_name(),
                message)
        
    def get_leg_display_name(self):
        return self.leg_bone if self.leg_bone else "no leg joint assigned"
            
    def get_knee_display_name(self):
        return self.knee_bone if self.knee_bone else "no knee joint assigned"
           
    def get_ankle_display_name(self):
        return self.ankle_bone if self.ankle_bone else "no ankle joint assigned"
    
    def get_ball_display_name(self):
        return self.foot_ball_bone if self.foot_ball_bone else "no ball joint assigned"
    
    def get_toe_display_name(self):
        return self.foot_toe_bone if self.foot_toe_bone else "no toe joint assigned"
        
    def create_foot_controller(self):
        foot_ctrl_name = self.FC_NAME_OVERRIDE if self.FC_NAME_OVERRIDE else "foot_CTRL"
        scale = self.FOOT_WIDTH * 0.8

        coords = cmds.xform( self.leg_ik, query=True, translation=True, worldSpace=True )
        ctrl = cmds.circle(name="{0}_{1}".format(foot_ctrl_name, self.SIDE), normal=(0,1,0))
        self.foot_controller = ctrl[0]
        
        cmds.setAttr("{0}.translate".format(ctrl[0]), coords[0], self.GRND_HGT_OFFSET, coords[2])
        cmds.setAttr("{0}.scale".format(ctrl[0]), scale, scale, scale)
        cmds.makeIdentity(self.foot_controller, apply=True )
        cmds.move(coords[0], coords[1], coords[2],
                    "{0}.scalePivot".format(self.foot_controller),
                    "{0}.rotatePivot".format(self.foot_controller),
                    absolute=True)
    
    def create_poleVector(self):
        pv_name = "{0}_{1}".format("leg_PV", self.SIDE)
        scale = self.FOOT_WIDTH * 0.4
        
        coords = cmds.xform( self.knee_bone, query=True, translation=True, worldSpace=True )
        ctrl = cmds.circle(name=pv_name, normal=(0,0,1), degree=1, sections=3)
        self.knee_polevector = ctrl[0]
        print coords
        cmds.setAttr("{0}.translate".format(ctrl[0]), coords[0], coords[1], coords[2]+12)
        cmds.setAttr("{0}.scale".format(ctrl[0]), scale, scale, scale)
        cmds.makeIdentity(self.knee_polevector, apply=True )
        cmds.poleVectorConstraint( self.knee_polevector, self.leg_ik )
        
    def create_ik_handles(self):
        self.leg_ik = cmds.ikHandle(name="leg_IK_HDL_{0}".format(self.SIDE), sj=self.leg_bone, ee=self.ankle_bone, sol="ikRPsolver")[0]
        self.ball_ik = cmds.ikHandle(name="ball_IK_HDL_{0}".format(self.SIDE), sj=self.ankle_bone, ee=self.foot_ball_bone, sol="ikSCsolver")[0]
        self.toe_ik = cmds.ikHandle(name="toe_IK_HDL_{0}".format(self.SIDE), sj=self.foot_ball_bone, ee=self.foot_toe_bone, sol="ikSCsolver")[0]

    def check_for_all_joints(self):
        message = ""
        if (not self.leg_bone or
            not self.knee_bone or
            not self.ankle_bone or
            not self.foot_ball_bone or
            not self.foot_toe_bone):
            message = "Missing a required bone."
        
        return message
    
    
    def create_locators(self):
        ankle_coords = cmds.xform( self.ankle_bone, query=True, translation=True, worldSpace=True )
        ball_coords = cmds.xform( self.foot_ball_bone, query=True, translation=True, worldSpace=True )
        toe_coords = cmds.xform( self.foot_toe_bone, query=True, translation=True, worldSpace=True )

        self.toe_loc = cmds.spaceLocator(absolute=True, name="toe_LOC_{0}".format(self.SIDE), position=[toe_coords[0],toe_coords[1],toe_coords[2]])[0]
        cmds.move(toe_coords[0], toe_coords[1], toe_coords[2], "{0}.scalePivot".format(self.toe_loc), "{0}.rotatePivot".format(self.toe_loc), absolute=True)
        
        self.ball_loc = cmds.spaceLocator(absolute=True, name="ball_LOC_{0}".format(self.SIDE), position=[ball_coords[0],ball_coords[1],ball_coords[2]])[0]
        cmds.move(ball_coords[0], ball_coords[1], ball_coords[2], "{0}.scalePivot".format(self.ball_loc), "{0}.rotatePivot".format(self.ball_loc), absolute=True)

        self.heel_loc = cmds.spaceLocator(absolute=True, name="heel_LOC_{0}".format(self.SIDE), position=[ankle_coords[0],0,ankle_coords[2]-self.HEEL_OFFSET])[0]
        cmds.move(ankle_coords[0], 0, ankle_coords[2]-self.HEEL_OFFSET, "{0}.scalePivot".format(self.heel_loc), "{0}.rotatePivot".format(self.heel_loc), absolute=True)

    def parent_objects(self): 
        cmds.parent(self.heel_loc, self.foot_controller)
        cmds.parent(self.toe_loc, self.toe_ik, self.heel_loc)
        cmds.parent(self.leg_ik, self.ball_ik, self.ball_loc)
        cmds.parent(self.ball_loc, self.toe_loc)

       
    def create_footroll(self):
        message = self.check_for_all_joints()
        if message:
            return message 
            
        self.create_ik_handles()
        
        self.create_foot_controller()
        self.create_poleVector()
        
        self.create_locators()
        self.parent_objects()
        
        return message
        
