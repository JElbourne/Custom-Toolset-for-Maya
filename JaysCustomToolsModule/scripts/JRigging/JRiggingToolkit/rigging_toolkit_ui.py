from maya import cmds

from PySide2 import QtWidgets, QtCore, QtGui

from JGeneral.JQTDialog import JDialogUI
from JRigging.JRiggingToolkit import place_joint_in_center_tool
from JRigging.JRiggingToolkit import align_joints_tool


class RiggingToolkitUI(JDialogUI):
    """ The AutoFootRollUI is a dialog that lets us auto generate a foot roll rig from existing foot joints """

    def __init__(self):
        self.WINDOW_TITLE = "Jays Rigging Toolkit"
        super(RiggingToolkitUI, self).__init__()        
        # Every time we create a new instancve,
        # we will automatically build our UI and populate it
        self.build_ui()
        
    def build_ui(self):
        """ This method build out the UI """
        
        # This is the master layout
        layout = QtWidgets.QVBoxLayout(self)
        
        
        utilTitle = QtWidgets.QLabel(text="Helpers for placing joins on a rig")
        utilTitle.setStyleSheet("color: black;background-color: grey;")
        utilTitle.setMargin(6)
        utilTitle.setFixedHeight(25)
        layout.addWidget(utilTitle)
 
        buttonsWidget = QtWidgets.QWidget()
        buttonsLayout = QtWidgets.QVBoxLayout(buttonsWidget)
        layout.addWidget(buttonsWidget)
        
        pjBtn = QtWidgets.QPushButton("Place Joint in Center of Edgeloop")
        pjBtn.clicked.connect(self.run_place_joint)
        pjBtn.setFixedHeight(26)
        buttonsLayout.addWidget(pjBtn)
        
        ajBtn = QtWidgets.QPushButton("Align Joint and Parent")
        ajBtn.clicked.connect(self.run_align_joints)
        ajBtn.setFixedHeight(26)
        buttonsLayout.addWidget(ajBtn)

    
    def run_place_joint(self):
        place_joint_in_center_tool.place_joint_in_center()
        
    def run_align_joints(self):
        align_joints_tool.align_joints()
        

def show_ui(*args):
    """ This shows and returns a handle to the UI """
    
    RiggingToolkitUI.display()

    
    
if __name__ == "__main__":
    show_ui()