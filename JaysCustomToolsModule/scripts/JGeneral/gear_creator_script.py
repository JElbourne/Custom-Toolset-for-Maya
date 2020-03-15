from maya import cmds
import reusable_ui

class Gear(object):
    """
    This is a Gear object that lets us create and modify a gear.
    """
    
    def __init__(self):
        self.transform = None
        self.constructor = None
        self.gearextrude = None

    def create_gear(self, teeth=10, length=0.3):
        """
        This function will create a gear with the given perameters.
        
        Args:
            teeth: The number of teeth to create
            length: The length of the teeth
        """
        
        #print("Creating Gear: {0} Teeth and {1} Length".format(teeth, length))
        
        # Teeth are on alternate faces so we will span x 2
        spans = teeth *2
        
        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis=spans)
        
        side_faces = range(spans*2, spans*3, 2)
        
        cmds.select(clear=True)
        
        for face in side_faces:
            cmds.select("{0}.f[{1}]".format(self.transform, face), add=True)
            
        self.gearextrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
        

        
    def change_teeth(self, teeth=10, length=0.3):
        """
        This function will change an existing gear with the given perameters.
        
        Args:
            teeth: The number of teeth to create
            length: The length of the teeth
        """
        spans = teeth*2
        
        cmds.polyPipe(self.constructor, edit=True, subdivisionsAxis=spans)
        
        side_faces = range(spans*2, spans*3, 2)
        face_names =[]
        
        for face in side_faces:
            face_name = "f[{}]".format(face)
            face_names.append(face_name)
        
        cmds.setAttr("{0}.inputComponents".format(self.gearextrude), len(face_names), *face_names, type="componentList")
        cmds.polyExtrudeFacet(self.gearextrude, edit=True, localTranslateZ=length)

    
class GearUI(reusable_ui.BaseWindow):
    
    windowName = "GearMaker"
    
    def __init__(self):
        self.gear = None
    
    def build_ui(self):
        
        column = cmds.columnLayout()
        cmds.text(label="Use the slider to modify the Gear")
        
        row = cmds.rowLayout(numberOfColumns=4)
        
        self.label = cmds.label = cmds.text(label="10")
        self.slider = cmds.intSlider(min=5, max=30, value=10, step=1, dragCommand=self.modifyGear)
        
        cmds.button(label="Make Gear", command=self.makeGear)
        
        cmds.button(label="Reset", command=self.reset)
        
        cmds.setParent(column)
        cmds.button(label="Close Window", command=self.close)
    
    def makeGear(self, *args):
        teeth = cmds.intSlider(self.slider, q=True, value=True)
        
        self.gear = Gear()
        self.gear.create_gear(teeth=teeth)
    
    def modifyGear(self, teeth):
        if self.gear:
            self.gear.change_teeth(teeth)
         
        cmds.text(self.label, e=True, label=teeth)
    
    def reset(self, *args):
        self.gear = None
        cmds.intSlider(self.slider, e=True, value=10)
        cmds.text(self.label, e=True, label=10)

gear_ui = None

def displayGearUi(*args):
    global gear_ui
    gear_ui = GearUI()
    gear_ui.show()