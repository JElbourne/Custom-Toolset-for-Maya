from maya import cmds

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

class JDialogUI(QtWidgets.QDialog):
    """ The ControllerLibraryUI is a dialog that lets us save and import controllers """
    
    WINDOW_TITLE = "JDialog UI"
    
    dlg_instance = None
    
    @classmethod
    def display(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = cls()
            
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activeWindow()
    
    @classmethod
    def maya_main_window(cls):
        """
        Return the Maya main window widget as a Python object
        """
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
    
    
    def __init__(self):
        super(JDialogUI, self).__init__(self.maya_main_window())
                
        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)