import maya.cmds as cmds
import maya.OpenMaya as om

    
class DisplayColourOverride(object):
    
    MAX_OVERRIDE_COLOURS = 32
    
    @classmethod
    def override_colour(cls, colour_index):
        if (colour_index >= cls.MAX_OVERRIDE_COLOURS or colour_index < 0):
            om.MGlobal.displayError("Colour index is out of range (must be between 0-31)")
            return False
        
        shapes = cls.shape_nodes()
        if not shapes:
            om.MGlobal.displayError("No shape Nodes selected")
            return False
        
        for shape in shapes:
            cmds.setAttr("{0}.overrideEnabled".format(shape), True)
            cmds.setAttr("{0}.overrideColor".format(shape), colour_index)
        
        return True
        
    @classmethod
    def use_defaults(cls):
        shapes = cls.shape_nodes()
        if not shapes:
            om.MGlobal.displayError("No shape Nodes selected")
            return False
        
        for shape in shapes:
            cmds.setAttr("{0}.overrideEnabled".format(shape), False)
            
        return True
        
    @classmethod
    def shape_nodes(cls):
        selection = cmds.ls(selection=True)
        if not selection:
            return None
        
        shapes = []
        for shape in selection:
            shapes.extend(cmds.listRelatives(shape, shapes=True))
            
        return shapes
    
class DisplayColourOverrideUI(object):
    
    
    WINDOW_NAME = "Jays Display Colour Override"
    COLOUR_PALETTE_CELL_WIDTH = 17
    FORM_OFFSET = 2
    
    colour_palette = None
    
    @classmethod
    def display(cls):
        cls.delete()
        
        main_window = cmds.window(cls.WINDOW_NAME,
                                title="Jay's Display Colour Override",
                                rtf=True,
                                sizeable=False)
                                
        main_layout = cmds.formLayout(parent=main_window)
        
        rows = 2
        columns = DisplayColourOverride.MAX_OVERRIDE_COLOURS / rows
        width = columns * cls.COLOUR_PALETTE_CELL_WIDTH
        height = rows * cls.COLOUR_PALETTE_CELL_WIDTH
        
        cls.colour_palette=cmds.palettePort(dimensions=(columns, rows),
                                            transparent=0,
                                            width = width,
                                            height = height,
                                            topDown=True,
                                            colorEditable=False,
                                            parent=main_layout)
                                            
        for index in range(1, DisplayColourOverride.MAX_OVERRIDE_COLOURS):
            colour_component=cmds.colorIndex(index, q=True)
            cmds.palettePort(cls.colour_palette,
                               edit=True,
                               rgbValue=(index, colour_component[0], colour_component[1], colour_component[2]))
        
        cmds.palettePort(cls.colour_palette,
                         edit=True,
                         rgbValue=(0, 0.6, 0.6, 0.6))
                         
        # Create the override and default buttons
        override_button = cmds.button(label="Override",
                                        command="DisplayColourOverrideUI.override()",
                                        parent=main_layout)
                                        
                                        
        default_button = cmds.button(label="Default",
                                        command="DisplayColourOverrideUI.default()",
                                        parent=main_layout)           
        
        
        # Layout the Colour Palette
        cmds.formLayout(main_layout, edit=True,
                         attachForm=(cls.colour_palette, "top", cls.FORM_OFFSET))
                         
        cmds.formLayout(main_layout, edit=True,
                         attachForm=(cls.colour_palette, "right", cls.FORM_OFFSET))
                         
        cmds.formLayout(main_layout, edit=True,
                         attachForm=(cls.colour_palette, "left", cls.FORM_OFFSET))
                         
        # Layout the override and default buttons
        cmds.formLayout(main_layout, edit=True,
                         attachControl=(override_button, "top", cls.FORM_OFFSET, cls.colour_palette))              
        cmds.formLayout(main_layout, edit=True,
                         attachForm=(override_button, "left", cls.FORM_OFFSET))
        cmds.formLayout(main_layout, edit=True,
                         attachPosition=(override_button, "right", 0, 50))

        cmds.formLayout(main_layout, edit=True,
                         attachOppositeControl=(default_button, "top", 0, override_button))
        cmds.formLayout(main_layout, edit=True,
                         attachControl=(default_button, "left", 0, override_button))
        cmds.formLayout(main_layout, edit=True,
                         attachForm=(default_button, "right", cls.FORM_OFFSET))
                         
        cmds.showWindow(main_window)
                         
         
        
    @classmethod
    def delete(cls):
        if cmds.window(cls.WINDOW_NAME, exists=True):
            cmds.deleteUI(cls.WINDOW_NAME, window=True)
        
    @classmethod
    def override(cls):
        colour_index = cmds.palettePort(cls.colour_palette, query=True, setCurCell=True)
        DisplayColourOverride.override_colour(colour_index)
        
    @classmethod
    def default(cls):
        DisplayColourOverride.use_defaults()
        
if __name__ == "__main__":
    DisplayColourOverrideUI.display()