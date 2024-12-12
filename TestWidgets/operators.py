import bpy
import widgets_lib  # Assurez-vous que widgets_lib est bien accessible

# Exemple d'opérateur
class WIDGETS_LIB_USER_OT_TestOperator(bpy.types.Operator):
    bl_idname = "wm.widgets_lib_test"
    bl_label = "Test Widgets Lib Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Test Widgets"
    

    def execute(self, context):
        # Initialisation des dimensions et position du panneau
        panel_width = 300
        panel_height = 38
        panel_x = (context.region.width // 2) - (panel_width // 2)
        panel_y = (context.region.height // 2) - (panel_height // 2) + 400

        # Créer le panneau draggable
        toolbar_panel = widgets_lib.BL_UI_Drag_Panel(panel_x, panel_y, panel_width, panel_height)
        toolbar_panel.bg_color = (0.0, 0.0, 0.0, 0.2)
#        widgets_lib.bl_ui_button("Mon Bouton", (50, 50), (100, 30), context=context)
        self.report({'INFO'}, "Test de Widgets Lib réussi")
        return {'FINISHED'}


class WIDGETS_LIB_USER_OT_ShowLabel(bpy.types.Operator):
    bl_idname = "wm.widgets_lib_show_label"
    bl_label = "Afficher un Label"

    def execute(self, context):
        widgets_lib.bl_ui_label("Mon Label", (150, 150), context=context)
        self.report({'INFO'}, "Label affiché")
        return {'FINISHED'}
