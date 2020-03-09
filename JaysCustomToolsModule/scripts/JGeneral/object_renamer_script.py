from maya import cmds

SUFFIXES = {
    "mesh": "geo",
    "joint": "jnt",
    "ambientLight": "lgt",
    "camera": None,
}

DEFAULT_SUFFIX = "grp"

def rename_objects(selection=False):
    """
    This function will rename any object to have the correct suffix
    
    Args:
        selection: Whether or not we use the current selection
    
    Returns:
        A list fo all the objects we operated on
    """
    objects = cmds.ls(sl=selection, dag=True, long=True)

    # This function cannot run if there is no selection and no objects
    if selection and not objects:
        raise RuntimeError("You dont have anything selected.")
        
    objects.sort(key=len, reverse=True)

    for obj in objects:
        short_name = obj.split("|")[-1]
        
        children = cmds.listRelatives(obj, children=True, fullPath=True) or []
        
        if len(children) == 1:
            child = children[0]
            obj_type = cmds.objectType(child)
        else:
            obj_type = cmds.objectType(obj)
        
           
        suffix = SUFFIXES.get(obj_type, DEFAULT_SUFFIX)
        
        if not suffix:
            continue

        if obj.endswith('_'+suffix):
            continue
        
        new_name = "{0}_{1}".format(short_name, suffix)
        
        cmds.rename(obj, new_name)
        
        index = objects.index(obj)
        
        objects[index] = obj.replace(short_name, new_name)

    return objects
