import bpy

class WIDGETS_LIB_USER_PT_TestPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_widgets_lib_test"
    bl_label = "Widgets Lib Test"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.widgets_lib_test", text="Test Widgets Lib")
        layout.operator("wm.widgets_lib_show_label", text="Afficher Label")
