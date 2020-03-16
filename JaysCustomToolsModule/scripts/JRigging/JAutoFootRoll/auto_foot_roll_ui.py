from maya import cmds

from PySide2 import QtWidgets, QtCore, QtGui

from JGeneral.JQTDialog import JDialogUI
from JRigging.JAutoFootRoll import auto_foot_roll
reload(auto_foot_roll)


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
        
        instructions = QtWidgets.QLabel(text="1. Start by selecting IK Handle at ankle")
        instructions.setStyleSheet("color: black;background-color: grey;")
        instructions.setMargin(6)
        instructions.setFixedHeight(25)
        layout.addWidget(instructions)
        
        jntsTitle = QtWidgets.QLabel(text="2. Next, select select the ankle joint")
        jntsTitle.setStyleSheet("color: black;background-color: grey;")
        jntsTitle.setMargin(6)
        jntsTitle.setFixedHeight(25)
        layout.addWidget(jntsTitle)
        
        self.selError = QtWidgets.QLabel(text="")
        self.selError.setStyleSheet("color: white;background-color: red;")
        self.selError.setMargin(6)
        self.selError.setFixedHeight(24)
        self.selError.hide()
        layout.addWidget(self.selError)
        
        legWidget = QtWidgets.QWidget()
        legLayout = QtWidgets.QHBoxLayout(legWidget)
        legWidget.setMaximumHeight(36)
        layout.addWidget(legWidget)

        legLabelField = QtWidgets.QLabel(text="Leg Joint: ")
        legLabelField.setStyleSheet("color: white;background-color: none;")
        legLabelField.setMargin(4)
        legLabelField.setFixedHeight(26)
        legLayout.addWidget(legLabelField)
        
        self.legNameField = QtWidgets.QLabel(text=self.footRoll.get_leg_display_name())
        self.legNameField.setStyleSheet("color: white;background-color: #999999;")
        self.legNameField.setMargin(4)
        self.legNameField.setFixedHeight(26)
        legLayout.addWidget(self.legNameField)
        
        kneeWidget = QtWidgets.QWidget()
        kneeLayout = QtWidgets.QHBoxLayout(kneeWidget)
        kneeWidget.setMaximumHeight(36)
        layout.addWidget(kneeWidget)

        kneeLabelField = QtWidgets.QLabel(text="Knee Joint: ")
        kneeLabelField.setStyleSheet("color: white;background-color: none;")
        kneeLabelField.setMargin(4)
        kneeLabelField.setFixedHeight(26)
        kneeLayout.addWidget(kneeLabelField)
        
        self.kneeNameField = QtWidgets.QLabel(text=self.footRoll.get_knee_display_name())
        self.kneeNameField.setStyleSheet("color: white;background-color: #999999;")
        self.kneeNameField.setMargin(4)
        self.kneeNameField.setFixedHeight(26)
        kneeLayout.addWidget(self.kneeNameField)
        
        
        ankleWidget = QtWidgets.QWidget()
        ankleLayout = QtWidgets.QHBoxLayout(ankleWidget)
        ankleWidget.setMaximumHeight(30)
        layout.addWidget(ankleWidget)
        
        ankleLabelField = QtWidgets.QLabel(text="Ankle Joint: ")
        ankleLabelField.setStyleSheet("color: white;background-color: none; text-align:right")
        ankleLabelField.setMargin(8)
        ankleLabelField.setFixedHeight(26)
        ankleLayout.addWidget(ankleLabelField)
        
        self.ankleNameField = QtWidgets.QLabel(text=self.footRoll.get_ankle_display_name())
        self.ankleNameField.setStyleSheet("color: grey;background-color: black;")
        self.ankleNameField.setMargin(8)
        self.ankleNameField.setFixedHeight(26)
        ankleLayout.addWidget(self.ankleNameField)
        
        footballWidget = QtWidgets.QWidget()
        footballLayout = QtWidgets.QHBoxLayout(footballWidget)
        footballWidget.setMaximumHeight(30)
        layout.addWidget(footballWidget)
        
        footballLabelField = QtWidgets.QLabel(text="Foot Ball Joint: ")
        footballLabelField.setStyleSheet("color: white;background-color: none;")
        footballLabelField.setMargin(8)
        footballLabelField.setFixedHeight(26)
        footballLayout.addWidget(footballLabelField)
        
        self.footballNameField = QtWidgets.QLabel(text=self.footRoll.get_ball_display_name())
        self.footballNameField.setStyleSheet("color: grey;background-color: black;")
        self.footballNameField.setMargin(8)
        self.footballNameField.setFixedHeight(26)
        footballLayout.addWidget(self.footballNameField)
        
        footToeWidget = QtWidgets.QWidget()
        footToeLayout = QtWidgets.QHBoxLayout(footToeWidget)
        footToeWidget.setMaximumHeight(30)
        layout.addWidget(footToeWidget)
        
        footToeLabelField = QtWidgets.QLabel(text="Foot Toe Joint: ")
        footToeLabelField.setStyleSheet("color: white;background-color: none;")
        footToeLabelField.setMargin(8)
        footToeLabelField.setFixedHeight(26)
        footToeLayout.addWidget(footToeLabelField)
        
        self.footToeNameField = QtWidgets.QLabel(text=self.footRoll.get_toe_display_name())
        self.footToeNameField.setStyleSheet("color: grey;background-color: black;")
        self.footToeNameField.setMargin(8)
        self.footToeNameField.setFixedHeight(26)
        footToeLayout.addWidget(self.footToeNameField)
        
        selbtnsWidget = QtWidgets.QWidget()
        selbtnsLayout = QtWidgets.QHBoxLayout(selbtnsWidget)
        layout.addWidget(selbtnsWidget)
        
                                
        clearBtn = QtWidgets.QPushButton("Clear")
        clearBtn.clicked.connect(self.run_clear_joints)
        clearBtn.setFixedHeight(26)
        selbtnsLayout.addWidget(clearBtn)
        
        jntsBtn = QtWidgets.QPushButton("Select Upper Leg Joint")
        jntsBtn.clicked.connect(self.run_assign_joints)
        jntsBtn.setFixedHeight(26)
        selbtnsLayout.addWidget(jntsBtn)
                
        # This is the child widget that holds all our action buttons
        btnsWidget = QtWidgets.QWidget()
        btnsLayout = QtWidgets.QHBoxLayout(btnsWidget)
        layout.addWidget(btnsWidget)
        
        executeCloseBtn = QtWidgets.QPushButton("Execute and Close")
        executeCloseBtn.clicked.connect(lambda: self.run_auto_foot_roll(close=True))
        btnsLayout.addWidget(executeCloseBtn)
        
        executeBtn = QtWidgets.QPushButton("Execute")
        executeBtn.clicked.connect(self.run_auto_foot_roll)
        btnsLayout.addWidget(executeBtn)
        
        closeBtn = QtWidgets.QPushButton("Close")
        closeBtn.clicked.connect(self.close)
        btnsLayout.addWidget(closeBtn)
    
    def run_clear_joints(self):
        leg_name, knee_name, ankle_name, ball_name, toe_name, message = self.footRoll.clear_joints()
        self.set_message(message)

        self.legNameField.setText(leg_name)
        self.kneeNameField.setText(knee_name)
        self.ankleNameField.setText(ankle_name)
        self.footballNameField.setText(ball_name)
        self.footToeNameField.setText(toe_name)
    
    def run_assign_joints(self):
        leg_name, knee_name, ankle_name, ball_name, toe_name, message = self.footRoll.assign_joints()
        self.set_message(message)

        self.legNameField.setText(leg_name)
        self.kneeNameField.setText(knee_name)
        self.ankleNameField.setText(ankle_name)
        self.footballNameField.setText(ball_name)
        self.footToeNameField.setText(toe_name)
        
    def run_auto_foot_roll(self, close=False):
        message = self.footRoll.create_footroll() 
        if close:
            self.close()
        
    def set_message(self, message):
        if message.strip():
            self.selError.setText(message)
            self.selError.show()
        else:
            self.selError.setText(" ")
            self.selError.hide()
        


def show_ui(*args):
    """ This shows and returns a handle to the UI """   
    AutoFootRollUI.display()

    
if __name__ == "__main__":
    show_ui()