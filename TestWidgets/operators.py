import bpy
import widgets_lib  # Assurez-vous que widgets_lib est bien accessible

# Exemple d'opérateur
class WIDGETS_LIB_USER_OT_TestOperator(bpy.types.Operator):
    bl_idname = "wm.widgets_lib_test"
    bl_label = "Test Widgets Lib"

    def execute(self, context):
        # Exemple d'utilisation d'un widget
        widgets_lib.bl_ui_button("Mon Bouton", (50, 50), (100, 30), context=context)
        self.report({'INFO'}, "Test de Widgets Lib réussi")
        return {'FINISHED'}


class WIDGETS_LIB_USER_OT_ShowLabel(bpy.types.Operator):
    bl_idname = "wm.widgets_lib_show_label"
    bl_label = "Afficher un Label"

    def execute(self, context):
        widgets_lib.bl_ui_label("Mon Label", (150, 150), context=context)
        self.report({'INFO'}, "Label affiché")
        return {'FINISHED'}
