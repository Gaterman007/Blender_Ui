import bpy
import widgets_lib  # Assurez-vous que widgets_lib est bien accessible

from widgets_lib.draw_handler import dialogs
from widgets_lib.draw_handler import draw_handle_2d

# Exemple d'opérateur
class WIDGETS_LIB_USER_OT_TestOperator(bpy.types.Operator):
    bl_idname = "wm.widgets_lib_test"
    bl_label = "Test Widgets Lib Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Development"
    
    def createDialog(self,context, event):

        if not self.dialog:
            panel_width = 300
            panel_height = 38
            panel_x = (context.region.width // 2) - (panel_width // 2)
            panel_y = (context.region.height // 2) - (panel_height // 2) + 400

            # Créer le panneau draggable
            self.toolbar_panneau = widgets_lib.BL_UI_Drag_Panel(panel_x, panel_y, panel_width, panel_height)
            self.selectButton = widgets_lib.BL_UI_Button(panel_height * 0, 0, panel_height - 4, panel_height - 4)
            self.button       = widgets_lib.BL_UI_Button(panel_height * 1, 0, panel_height - 4, panel_height - 4)
            self.selectButton.set_image("greasepencil")
            self.button.set_image("action")
            self.dialog = True
            self.toolbar_panneau.bg_color = (0.0, 0.0, 0.0, 0.2)

            # Ajouter le panneau au dictionnaire dialogs pour qu'il soit dessiné
            self.toolbar_panneau.add_widget(self.selectButton)
            self.toolbar_panneau.add_widget(self.button)
            dialogs["drag_panel"] = self.toolbar_panneau
#            dialogs["button_test"] = self.button
            # Vérifier si le gestionnaire de dessin est actif, sinon, l'enregistrer
            if draw_handle_2d is None:
                bpy.ops.view3d.widget_register_draw_cb()

    def removeDialog(self):
        if self.dialog:
            del dialogs["drag_panel"]
#            del dialogs["button_test"]
            self.toolbar_panneau.eraseChilds()
#            self.button.eraseChilds()
            del self.toolbar_panneau
#            del self.button
            bpy.context.region.tag_redraw()

    
    def invoke(self, context, event):
        self.dialog = False
        self.createDialog(context,event)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
        
    def modal(self, context, event):
        retValue = {'RUNNING_MODAL'}
        
        if event.type in {'ESC'}:  # Permet de quitter avec ESC
            self.removeDialog()
            return {'CANCELLED'}

        if event.type == 'RIGHTMOUSE':
            if event.value == 'PRESS':
                self.rightMouseDown = True
            elif self.rightMouseDown and event.value == 'RELEASE':
                self.removeDialog()
                return {'FINISHED'}
        
        retValue = {'PASS_THROUGH'}
        for widget in dialogs.values():
            retValue, handled = widget.handle_event(context,event)
            if handled:
                break
        if retValue != {'RUNNING_MODAL'} and retValue != {'PASS_THROUGH'}:
            self.removeDialog()
            
        return retValue


# Define a property group for storing CNC data  PathObj
class CNCDataPropertyGroup(bpy.types.PropertyGroup):
    drillBitName: bpy.props.StringProperty(
        name="Drill Bit Name",
        description="Name of the drill bit"
    )
    drillBitUnits: bpy.props.EnumProperty(
        name="Units",
        description="Units of measurement for the drill bit",
        items=[
            ('MM', "Millimeters", "Use millimeters"),
            ('INCH', "Inches", "Use inches")
        ],
        default='MM'
    )
    methodType: bpy.props.StringProperty(
        name="Method Type",
        description="Type of machining method (e.g., plunge, pocket)"
    )
    depth: bpy.props.FloatProperty(
        name="Depth",
        description="Depth of cut",
        default=10.0,
        unit='LENGTH'
    )
    feedrate: bpy.props.FloatProperty(
        name="Feed Rate",
        description="Feed rate of the tool",
        default=1.0,
        unit='VELOCITY'
    )
    multipass: bpy.props.BoolProperty(
        name="Multi-pass",
        description="Whether to use multiple passes for cutting",
        default=False
    )
    depthStep: bpy.props.FloatProperty(
        name="Depth Step",
        description="Depth step per pass",
        default=2.0,
        unit='LENGTH'
    )
    overlapPercent: bpy.props.FloatProperty(
        name="Overlap Percentage",
        description="Percentage of overlap between passes",
        default=50.0,
        subtype='PERCENTAGE'
    )

# Spécialisation pour les outils de type Plunge
class CNCPlungePropertyGroup(CNCDataPropertyGroup):
    plunge_method: bpy.props.EnumProperty(
        name="Plunge Method",
        description="Type of plunge method",
        items=[
            ('DOWN', "Down", "Plunge straight down"),
            ('STEP', "Step", "Step plunge"),
            ('SPIRAL', "Spiral", "Spiral plunge")
        ],
        default='DOWN'
    )
    spiral_overlap: bpy.props.FloatProperty(
        name="Spiral Overlap",
        description="Overlap percentage for spiral plunge",
        default=50.0,
        subtype='PERCENTAGE'
    )
    hole_size: bpy.props.FloatProperty(
        name="Hole Size",
        description="Size of the hole",
        default=10.0,
        unit='LENGTH'
    )

class CNCPathProperty(CNCDataPropertyGroup):
    start_point: bpy.props.FloatVectorProperty(
        name="Start Point",
        description="Starting point of the toolpath",
        subtype='XYZ',
        default=(0.0, 0.0, 0.0)
    )
    end_point: bpy.props.FloatVectorProperty(
        name="End Point",
        description="End point of the toolpath",
        subtype='XYZ',
        default=(1.0, 1.0, 1.0)
    )

# Spécialisation pour les outils de type Pocket
class CNCPocketPropertyGroup(CNCDataPropertyGroup):
    pocket_method: bpy.props.EnumProperty(
        name="Pocket Method",
        description="Type of pocketing",
        items=[
            ('CENTER', "Center", "Pocket from the center out"),
            ('INTERIOR', "Interior", "Interior pocketing"),
            ('EXTERIOR', "Exterior", "Exterior pocketing")
        ],
        default='CENTER'
    )
    spiral_step: bpy.props.FloatProperty(
        name="Spiral Step",
        description="Step size for spiral pocketing",
        default=1.0,
        unit='LENGTH'
    )
    hole_size: bpy.props.FloatProperty(
        name="Hole Size",
        description="Size of the pocket or hole",
        default=10.0,
        unit='LENGTH'
    )

# Spécialisation pour les outils de type Straight Cut
class CNCStraitCutPropertyGroup(CNCDataPropertyGroup):
    cut_method: bpy.props.EnumProperty(
        name="Cut Method",
        description="Type of straight cut",
        items=[
            ('RAMP', "Ramp", "Ramp cutting"),
            ('MULTIPASS', "Multi-pass", "Multi-pass cutting"),
            ('PLUNGE', "Plunge", "Plunge cutting")
        ],
        default='RAMP'
    )
    cut_width: bpy.props.FloatProperty(
        name="Cut Width",
        description="Width of the cut",
        default=5.0,
        unit='LENGTH'
    )


class WIDGETS_LIB_USER_OT_ShowLabel(bpy.types.Operator):
    bl_idname = "wm.widgets_lib_show_label"
    bl_label = "Afficher un Label"

    def execute(self, context):
        widgets_lib.bl_ui_label("Mon Label", (150, 150), context=context)
        self.report({'INFO'}, "Label affiché")
        return {'FINISHED'}
