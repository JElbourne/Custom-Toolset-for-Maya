from maya import cmds


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