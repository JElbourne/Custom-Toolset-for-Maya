import traceback

import maya.OpenMaya as om
import maya.OpenMayaUI as omui

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

# MY Python Modules
from JGeneral.JQTDialog import JDialogUI
from JAnimation.RetimingTool.retime_tool import BourneRetimingUtils


class BourneRetimingUtilsUI(JDialogUI):
   
    ABSOLUTE_BUTTON_WIDTH = 50
    RELATIVE_BUTTON_WIDTH = 64
    
    RETIMING_PROPERTY_NAME = "retiming_data"

    def __init__(self):
        self.WINDOW_TITLE = "Jay Retiming Tool"
        super(BourneRetimingUtilsUI, self).__init__()
            
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
    def create_widgets(self):
        self.absolute_buttons = []
        for i in range(1, 7):
            btn = QtWidgets.QPushButton("{0}f".format(i))
            btn.setFixedWidth(self.ABSOLUTE_BUTTON_WIDTH)
            btn.setProperty(self.RETIMING_PROPERTY_NAME, [i, False])
            self.absolute_buttons.append(btn)
            
        self.relative_buttons = []
        for i in [-2,-1,1,2]:
            btn = QtWidgets.QPushButton("{0}f".format(i))
            btn.setFixedWidth(self.RELATIVE_BUTTON_WIDTH)
            btn.setProperty(self.RETIMING_PROPERTY_NAME, [i, True])
            self.relative_buttons.append(btn)
            
        self.move_to_next_cb = QtWidgets.QCheckBox("Move to Next KeyFrame")
            
    def create_layouts(self):
        absolute_retiming_layout = QtWidgets.QHBoxLayout()
        absolute_retiming_layout.setSpacing(2)
        for btn in self.absolute_buttons:
            absolute_retiming_layout.addWidget(btn)
            
        relative_retiming_layout = QtWidgets.QHBoxLayout()
        relative_retiming_layout.setSpacing(2)
        for btn in self.relative_buttons:
            relative_retiming_layout.addWidget(btn)
            if relative_retiming_layout.count() == 2:
                relative_retiming_layout.addStretch()
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        main_layout.addLayout(absolute_retiming_layout)
        main_layout.addLayout(relative_retiming_layout)
        main_layout.addWidget(self.move_to_next_cb)
        
    def create_connections(self):
        for btn in self.absolute_buttons:
            btn.clicked.connect(self.retime)
            
        for btn in self.relative_buttons:
            btn.clicked.connect(self.retime)
            
    def retime(self):
        btn = self.sender()
        if btn:
            retiming_data = btn.property(self.RETIMING_PROPERTY_NAME)
            move_to_next = self.move_to_next_cb.isChecked()
            
            cmds.undoInfo(openChunk=True)
            ## Make sure to alsways use a Try/except block when using Undo chunks so you can always
            ## Ensure the Undo chunck was CLOSED!
            try:
                BourneRetimingUtils.retime_keys(retiming_data[0], retiming_data[1], move_to_next)
            except:
                traceback.print_exc()
                om.MGlobal.displayError("Retime error occured. See script editor for details.")
            cmds.undoInfo(closeChunk=True)


retiming_ui = None


def show_ui(*args):
    """
    This shows and returns a handle to the UI
    
    Returns:
        QDialog
    """
    global retiming_ui
    
    try:
        retiming_ui.close()
        retiming_ui.deleteLater()
    except:
        pass
        
    retiming_ui = BourneRetimingUtilsUI()
    retiming_ui.show()
    return retiming_ui



if __name__ == "__main__":
    
    
    try:
        retiming_ui.close()
        retiming_ui.deleteLater()
    except:
        pass
        
    retiming_ui = BourneRetimingUtilsUI()
    retiming_ui.show()