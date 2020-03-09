from maya import cmds

from PySide2 import QtWidgets, QtCore, QtGui

from JGeneral.JQTDialog import JDialogUI
from JRigging.JAutoFootRoll import auto_foot_roll


class AutoFootRollUI(JDialogUI):
    """ The AutoFootRollUI is a dialog that lets us auto generate a foot roll rig from existing foot joints """

    def __init__(self):
        self.WINDOW_TITLE = "Auto Foot Roll UI"
        super(AutoFootRollUI, self).__init__()
        
        # The library variable points to an instance of our controller library
        self.footRoll = auto_foot_roll.FootRoll()
        
        # Every time we create a new instancve,
        # we will automatically build our UI and populate it
        self.build_ui()
        
    def build_ui(self):
        """ This method build out the UI """
        
        # This is the master layout
        layout = QtWidgets.QVBoxLayout(self)
        
        # This is the child Horizontal widget for the Save functionality
        ikWidget = QtWidgets.QWidget()
        ikLayout = QtWidgets.QHBoxLayout(ikWidget)
        layout.addWidget(ikWidget)
        
        self.ikNameField = QtWidgets.QLabel(text=self.footRoll.get_ik_display_name())
        ikLayout.addWidget(self.ikNameField)
        
        ikBtn = QtWidgets.QPushButton("Select IK Handle")
        ikBtn.clicked.connect(self.run_assign_ik)
        ikLayout.addWidget(ikBtn)

        # This is the child widget that holds all our action buttons
        btnsWidget = QtWidgets.QWidget()
        btnsLayout = QtWidgets.QHBoxLayout(btnsWidget)
        layout.addWidget(btnsWidget)
        
        executeCloseBtn = QtWidgets.QPushButton("Execute and Close")
        executeCloseBtn.clicked.connect(self.close)
        btnsLayout.addWidget(executeCloseBtn)
        
        executeBtn = QtWidgets.QPushButton("Execute")
        executeBtn.clicked.connect(self.run_auto_foot_roll)
        btnsLayout.addWidget(executeBtn)
        
        closeBtn = QtWidgets.QPushButton("Close")
        closeBtn.clicked.connect(self.close)
        btnsLayout.addWidget(closeBtn)
    
    def run_assign_ik(self):
        ik_name, message = self.footRoll.assign_ik()
        print ik_name
        print message
        self.ikNameField.setText(ik_name)
        
    def run_auto_foot_roll(self):
        pass
        


def show_ui(*args):
    """ This shows and returns a handle to the UI """
    #global auto_foot_roll_ui
    # try:
    #     auto_foot_roll_ui.close()
    #     auto_foot_roll_ui.deleteLater()
    # except:
    #     pass
    
    # auto_foot_roll_ui = AutoFootRollUI()
    # auto_foot_roll_ui.show(dockable=True)
    # auto_foot_roll_ui.activateWindow
    
    AutoFootRollUI.display()

    
    
if __name__ == "__main__":
    show_ui()