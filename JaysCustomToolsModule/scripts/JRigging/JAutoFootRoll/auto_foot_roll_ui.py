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
        
        
        ikTitle = QtWidgets.QLabel(text="1. Start by selecting IK Handle at ankle")
        ikTitle.setStyleSheet("color: black;background-color: grey;")
        ikTitle.setMargin(6)
        ikTitle.setFixedHeight(25)
        layout.addWidget(ikTitle)
        
        self.ikError = QtWidgets.QLabel(text="")
        self.ikError.setStyleSheet("color: white;background-color: red;")
        self.ikError.setMargin(6)
        self.ikError.setFixedHeight(25)
        self.ikError.hide()
        layout.addWidget(self.ikError)
        
        ikWidget = QtWidgets.QWidget()
        ikLayout = QtWidgets.QHBoxLayout(ikWidget)
        ikWidget.setMaximumHeight(40)
        layout.addWidget(ikWidget)

        self.ikNameField = QtWidgets.QLabel(text=self.footRoll.get_ik_display_name())
        self.ikNameField.setStyleSheet("color: grey;background-color: black;")
        self.ikNameField.setMargin(8)
        self.ikNameField.setFixedHeight(26)
        ikLayout.addWidget(self.ikNameField)
        
        ikBtn = QtWidgets.QPushButton("Select IK Handle")
        ikBtn.clicked.connect(self.run_assign_ik)
        ikBtn.setFixedHeight(26)
        ikLayout.addWidget(ikBtn)
        
        jointsTitle = QtWidgets.QLabel(text="2. Next, select all three foot joints")
        jointsTitle.setStyleSheet("color: black;background-color: grey;")
        jointsTitle.setMargin(6)
        jointsTitle.setFixedHeight(25)
        layout.addWidget(jointsTitle)

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
        print message
        if message.strip():
            self.ikError.setText(message)
            self.ikError.show()
        else:
            self.ikError.setText(" ")
            self.ikError.hide()

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