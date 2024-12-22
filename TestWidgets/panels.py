import bpy

class WIDGETS_LIB_USER_PT_TestPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_cnc_panel"
    bl_label = "CNC Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Development"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.cnc_main_toolbar", text="CNC ToolBar")
