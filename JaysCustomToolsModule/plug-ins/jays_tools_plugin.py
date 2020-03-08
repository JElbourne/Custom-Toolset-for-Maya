import maya.api.OpenMaya as om

import maya.cmds as cmds
import pymel.core as pm

# Tools Imports
import conLibrary.library_ui as clt
import colour_overrides_tool as cot
import retime_tool as rtt

MENU_OBJ = "JaysToolsMenu"
MENU_LABEL = "Jays Custom Tools"

MAIN_WINDOW = pm.language.melGlobals['gMainWindow']

g_con_lib_ui = None


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass
        
  
def colour_override_show():
    cot.DisplayColourOverrideUI.display()
    

def unload_menu_item():
    if pm.menu(MENU_OBJ, label=MENU_LABEL, exists=True, parent=MAIN_WINDOW):
        pm.deleteUI(pm.menu(MENU_OBJ, e=True, deleteAllItems=True))
        

def load_menu_item():
    
    unload_menu_item()

    custom_tools_menu = pm.menu(MENU_OBJ, label=MENU_LABEL, parent=MAIN_WINDOW, tearOff=True)

    pm.menuItem(label="Rigging", divider=True,)
    pm.menuItem(label="Auto Foot Roll Tool", command="print 'Auto Foot Rig'")
    pm.menuItem(label="Controllers Library", command="clt.show_ui()")

    pm.menuItem(label="Animation", divider=True )
    pm.menuItem(label="Retiming Tool", command="rtt.show_ui()")
    
    pm.menuItem( label="Utilities", divider=True )
    pm.menuItem(label="Colour Override", command="colour_override_show()")
        

def initializePlugin(plugin):
    """
    Entry point for a plugin. It is called once -- immediately after the plugin is loaded.
    This function registers all of the commands, nodes, contexts, etc... associated with the plugin.

    It is required by all plugins.

    :param plugin: MObject used to register the plugin using an MFnPlugin function set
    """
    vendor = "Jay Elbourne"
    version = "1.0.0"

    om.MFnPlugin(plugin, vendor, version)
    load_menu_item()

def uninitializePlugin(plugin):
    """
    Exit point for a plugin. It is called once -- when the plugin is unloaded.
    This function de-registers everything that was registered in the initializePlugin function.

    It is required by all plugins.

    :param plugin: MObject used to de-register the plugin using an MFnPlugin function set
    """
    unload_menu_item()


if __name__ == "__main__":
    """
    For Development Only

    Specialized code that can be executed through the script editor to speed up the development process.

    For example: scene cleanup, reloading the plugin, loading a test scene
    """

    # Any code required before unloading the plug-in (e.g. creating a new scene)


    # Reload the plugin
    plugin_name = "jays_tools_plugin.py"
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))


    # Any setup code to help speed up testing (e.g. loading a test scene)
