import maya.cmds as cmds
import maya.api.OpenMaya as om2

class DisplayColorOverride(object):
    """
    class modifying the draw overrides of selected objects
    """
    
    MAX_OVERRIDE_COLORS = 32
    
    @classmethod
    def override_color(cls, color_index):
        """ Enable and change color in override color """
        if color_index >= cls.MAX_OVERRIDE_COLORS or color_index < 0:
            om2.MGlobal.displayError("color index out of range (must between 0-31)")
            return False
            
        shapes = cls.shape_nodes()
        if not shapes:
            om2.MGlobal.displayError("No shape nodes selected")
            return False
        
        for shape in shapes:
            cmds.setAttr("{0}.overrideEnabled".format(shape), True)
            cmds.setAttr("{0}.overrideColor".format(shape), color_index)
            
        return True
        
    @classmethod
    def use_default_color(cls):
        """ disabled override color """
        shapes = cls.shape_nodes()
        if not shapes:
            om2.MGlobal.displayError("No shape nodes selected")
            return False
    
        for shape in shapes:
            cmds.setAttr("{0}.overrideEnabled".format(shape), False)
        
        return True
    
    @classmethod
    def shape_nodes(cls):
        """ getting the shape nodes """
        selection = cmds.ls(selection=True)
        if not selection:
            return None
            
        shape = []
        
        for node in selection:
            shape.extend(cmds.listRelatives(node, shapes=True))
        return shape

class DisplayColorOverridesUI(object):
    """
    Create GUI for manipulate override color for selected method
    """
    
    WINDOW_NAME = "displayoverridecolor"
    
    COLOR_PALETTE_CELL_WIDTH = 20
    
    FORM_OFFSET = 2
    
    color_palette = None
    
    @classmethod
    def display(cls):
        cls.delete()
        
        main_window = cmds.window(cls.WINDOW_NAME, title="Display Override Color", rtf=True, sizeable=False)
        main_layout = cmds.formLayout(parent=main_window)
        
        rows = 2
        column = DisplayColorOverride.MAX_OVERRIDE_COLORS / rows
        width = column * cls.COLOR_PALETTE_CELL_WIDTH
        height = rows * cls.COLOR_PALETTE_CELL_WIDTH
        
        cls.color_palette = cmds.palettePort(dimensions=(column, rows),
                                            transparent=0,
                                            width=width,
                                            height=height,
                                            topDown=True,
                                            colorEditable=False,
                                            parent=main_layout)
        
        for index in range(1, DisplayColorOverride.MAX_OVERRIDE_COLORS):
            color_component = cmds.colorIndex(index, query=True)
            cmds.palettePort(cls.color_palette,
                            edit=True,
                            rgb=(index, color_component[0], color_component[1], color_component[2]))
    
        cmds.palettePort(cls.color_palette,
                        edit=True,
                        rgb=(0, 0.6, 0.6, 0.6))
        
        # create override and default button
        override_button = cmds.button(label="Override", command="DisplayColorOverridesUI.override()" , parent=main_layout)
        default_button = cmds.button(label="Default", command="DisplayColorOverridesUI.default()", parent=main_layout)
        
        # layout the color palette
        cmds.formLayout(main_layout, edit=True,
                        attachForm=(cls.color_palette, "top", cls.FORM_OFFSET))
        cmds.formLayout(main_layout, edit=True,
                        attachForm=(cls.color_palette, "left", cls.FORM_OFFSET))
        cmds.formLayout(main_layout, edit=True,
                        attachForm=(cls.color_palette, "right", cls.FORM_OFFSET))
                        
        # layout override button
        cmds.formLayout(main_layout, edit=True,
                        attachControl=(override_button, "top", cls.FORM_OFFSET, cls.color_palette))
        cmds.formLayout(main_layout, edit=True,
                        attachForm=(override_button, "left", cls.FORM_OFFSET))
        cmds.formLayout(main_layout, edit=True,
                        attachPosition=(override_button, "right", 0, 50))
                        
        # layout default button
        cmds.formLayout(main_layout, edit=True,
                        attachOppositeControl=(default_button, "top", 0, override_button))
        cmds.formLayout(main_layout, edit=True,
                        attachControl=(default_button, "left", cls.FORM_OFFSET, override_button))
        cmds.formLayout(main_layout, edit=True,
                        attachForm=(default_button, "right", cls.FORM_OFFSET))
        
        cmds.showWindow(main_window)
    
    @classmethod
    def delete(cls):
        if cmds.window(cls.WINDOW_NAME, exists=True):
            cmds.deleteUI(cls.WINDOW_NAME, window=True)
    
    @classmethod
    def override(cls):
        color_index = cmds.palettePort(cls.color_palette, query=True, setCurCell=True)
        DisplayColorOverride.override_color(color_index)
    
    @classmethod
    def default(cls):
        DisplayColorOverride.use_default_color()
    

cmds.evalDeferred("DisplayColorOverridesUI.display()")