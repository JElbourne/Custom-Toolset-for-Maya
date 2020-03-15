from maya import cmds
import maya.OpenMaya as om

import pymel.core as pm


class FootRoll(object):
    SIDE = "l"
    NAME_OVERRIDE = None
    FOOT_WIDTH = 5
    ANKLE_OFFSET = 3
    GRND_HGT_OFFSET = 0
    
    controller = None
    ik_handle = None
    ankle_bone = None
    foot_ball_bone = None
    foot_toe_bone = None
    
    def __init__(self, side="l", foot_width=5, ankle_offset=3, grnd_hgt_offset=0, name_override=None):
        self.SIDE = side
        self.NAME_OVERRIDE = name_override
        self.FOOT_WIDTH = foot_width
        self.ANKLE_OFFSET = ankle_offset
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
        ankle_joint = cmds.ls(type="joint", selection=True) or []
        
        if not ankle_joint:
            self.ankle_bone = None
            self.foot_ball_bone = None
            self.foot_toe_bone = None
            message = "You must select: one Ankle Joint"
            om.MGlobal.displayError(message)
        elif len(ankle_joint) > 1:
            self.ankle_bone = None
            self.foot_ball_bone = None
            self.foot_toe_bone = None
            message = "Too many selections. Select only one Ankle Joint."
            om.MGlobal.displayError(message)
        else:
            self.ankle_bone = ankle_joint[0]
            ball_joint = cmds.listRelatives(ankle_joint[0], children=True, path=True) or []
            print ball_joint
            if not ball_joint:
                self.foot_ball_bone = None
                self.foot_toe_bone = None
                message += "The ankle joint selected does not have required ball joint in hierarchy"
                om.MGlobal.displayError(message)
            else:
                self.foot_ball_bone = ball_joint[0]
                toe_joint = cmds.listRelatives(ball_joint[0], children=True, path=True) or []
                print toe_joint
                if not toe_joint:
                    self.foot_toe_bone = None
                    message += "The ankle joint selected does not have required ball joint in hierarchy"
                    om.MGlobal.displayError(message)
                else:
                    self.foot_toe_bone = toe_joint[0]
        
        return (self.get_ankle_display_name(),
                self.get_ball_display_name(),
                self.get_toe_display_name(),
                message)
     
    def get_ik_display_name(self):
        """
        A function to get the display name, for UI purposes, of the IK Handle being used in the foot roll.
        
        Returns (str):
            Name of IK handle that is set or a default string.
        """
        return self.ik_handle if self.ik_handle else "no ik assigned"
           
    def get_ankle_display_name(self):
        """
        A function to get the display name, for UI purposes, of the Ankle Joint being used in the foot roll.
        
        Returns (str):
            Name of Ankle Joint that is set or a default string.
        """
        return self.ankle_bone if self.ankle_bone else "no ankle joint assigned"
    
    def get_ball_display_name(self):
        """
        A function to get the display name, for UI purposes, of the Foot Ball Joint being used in the foot roll.
        
        Returns (str):
            Name of Foot Ball Joint that is set or a default string.
        """
        return self.foot_ball_bone if self.foot_ball_bone else "no ball joint assigned"
    
    def get_toe_display_name(self):
        """
        A function to get the display name, for UI purposes, of the Foot Toe Joint being used in the foot roll.
        
        Returns (str):
            Name of Foot Toe Joint that is set or a default string.
        """
        return self.foot_toe_bone if self.foot_toe_bone else "no toe joint assigned"
        
    def create_controller(self):
        ctrl_name = self.NAME_OVERRIDE if self.NAME_OVERRIDE else "foot_ctrl"
        scale = self.FOOT_WIDTH * 1.25
        
        xCoord = cmds.getAttr("{0}.translateX".format(self.ik_handle)) if self.ik_handle else 0
        zCoord = cmds.getAttr("{0}.translateZ".format(self.ik_handle)) if self.ik_handle else 0
        ctrl = cmds.circle(name="{0}_{1}".format(ctrl_name, self.SIDE), normal=(0,1,0))
        
        cmds.setAttr("{0}.translate".format(ctrl[0]), xCoord, self.GRND_HGT_OFFSET, zCoord)
        cmds.setAttr("{0}.scale".format(ctrl[0]), scale, scale, scale)
    
    
    def create_footroll(self):
        message = ""
        return message
        
