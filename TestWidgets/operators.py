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
            self.toolbar_button = widgets_lib.BL_UI_Button(0, 10, panel_height - 4, panel_height - 4)
#            self.button = widgets_lib.BL_UI_Button(panel_x, panel_y - (2 *  panel_height), panel_height, panel_height)
            self.button = widgets_lib.BL_UI_Button(0, 0, panel_height, panel_height)
            self.button.set_image("action")
            self.dialog = True
            self.toolbar_panneau.bg_color = (0.0, 0.0, 0.0, 0.2)

            # Ajouter le panneau au dictionnaire dialogs pour qu'il soit dessiné
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



class WIDGETS_LIB_USER_OT_ShowLabel(bpy.types.Operator):
    bl_idname = "wm.widgets_lib_show_label"
    bl_label = "Afficher un Label"

    def execute(self, context):
        widgets_lib.bl_ui_label("Mon Label", (150, 150), context=context)
        self.report({'INFO'}, "Label affiché")
        return {'FINISHED'}
