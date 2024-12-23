import bpy
import widgets_lib  # Assurez-vous que widgets_lib est bien accessible

from widgets_lib.draw_handler import dialogs
from widgets_lib.draw_handler import draw_handle_2d
from .draw_handler import draw_handle_3d
from .modal_manager import ModalManager

from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_origin_3d


class CNC_TOOLS_OT_BaseOperator(bpy.types.Operator):
    """Classe de base pour les opérateurs CNC Tools"""    

    bl_idname = "cnc_tools.base_operator"
    bl_label = "CNC Tools Base Operator"

    def createDialog(self,context, event):
        """
        Méthode appelée pour créer les dialogues ou panneaux personnalisés.
        Cette méthode doit être redéfinie dans les sous-classes.
        """        
        pass
        
    def removeDialog(self):
        """
        Méthode appelée pour supprimer les dialogues ou panneaux personnalisés.
        Cette méthode doit être redéfinie dans les sous-classes.
        """
        pass

    def invoke(self, context, event):
        """
        Démarre l'opérateur en mode modal. Ajoute l'opérateur à la gestion modale.
        """
        ModalManager.add_modal(self)
        context.window_manager.modal_handler_add(self)
        self.createDialog(context, event)  # Appelle la méthode de création de dialogue
        return {'RUNNING_MODAL'}

    def mouseIsOnWindow(self, context,event):
        # Obtenir les coordonnées globales de la souris
        mouse_x, mouse_y = event.mouse_x, event.mouse_y
        regionFound = False
        # Parcourir toutes les zones de l'écran
        for area in context.window.screen.areas:
            # Vérifier si la souris est dans cette zone
            if area.x <= mouse_x <= area.x + area.width and area.y <= mouse_y <= area.y + area.height:
                # Parcourir toutes les régions de cette zone
                for region in area.regions:
                    self.report({'INFO'}, f"Verirfier Area: {area.type}, Region: {region.type}")
                    # Vérifier si la souris est dans cette région
                    if (region.x <= mouse_x <= region.x + region.width and
                            region.y <= mouse_y <= region.y + region.height):
                        self.report({'INFO'}, f"Souris dans Area: {area.type}, Region: {region.type}")
                        if area.type == "VIEW_3D" and region.type == "WINDOW":
                            regionFound = True
                        break
        return regionFound

    def modal(self, context, event):
        """
        Gère les événements en mode modal.
        """
        retValue = {'PASS_THROUGH'}
        if ModalManager.is_last(self):
            if event.type in {'ESC'} and ModalManager.is_last(self):  # Permet de quitter avec ESC
                self.removeDialog()
                return ModalManager.cancel_last_modal()

            if event.type == 'RIGHTMOUSE':
                if event.value == 'PRESS':
                    self.rightMouseDown = True
                elif self.rightMouseDown and event.value == 'RELEASE':
                    self.removeDialog()
                    return ModalManager.cancel_last_modal(True)
        return retValue
        
# Exemple d'opérateur
class CNCTOOLBAR_OT_Operator(CNC_TOOLS_OT_BaseOperator):
    bl_idname = "cnc_tools.main_toolbar"
    bl_label = "CNC Widgets Toolbar"
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
            self.selectButton = widgets_lib.BL_UI_Button(panel_height * 0, 0, panel_height - 4, panel_height - 4, image = "greasepencil")
            self.button       = widgets_lib.BL_UI_Button(panel_height * 1, 0, panel_height - 4, panel_height - 4, image = "action")
            self.button.setMouseClicCallBack("cnc_tools.cnc_add_plunge",'INVOKE_DEFAULT')
            self.dialog = True
            self.toolbar_panneau.bg_color = (0.0, 0.0, 0.0, 0.2)

            # Ajouter le panneau au dictionnaire dialogs pour qu'il soit dessiné
            self.toolbar_panneau.add_widget(self.selectButton)
            self.toolbar_panneau.add_widget(self.button)
            dialogs["drag_panel"] = self.toolbar_panneau
            # Vérifier si le gestionnaire de dessin est actif, sinon, l'enregistrer
            if draw_handle_2d is None:
                bpy.ops.view3d.widget_register_draw_cb()
            if draw_handle_3d is None:
                bpy.ops.view3d.cnc_data_register_draw_cb()

    def removeDialog(self):
        if self.dialog:
            del dialogs["drag_panel"]
            self.toolbar_panneau.eraseChilds()
            del self.toolbar_panneau
            bpy.context.region.tag_redraw()

    
    def invoke(self, context, event):
        self.dialog = False
        return super().invoke(context, event)
        
    def modal(self, context, event):
        retValue = super().modal(context, event)
        if retValue != {'RUNNING_MODAL'} and retValue != {'PASS_THROUGH'}:
            return retValue
            
        for widget in dialogs.values():
            retValue, handled = widget.handle_event(context,event)
            if handled:
                break
        if retValue != {'RUNNING_MODAL'} and retValue != {'PASS_THROUGH'}:
            self.removeDialog()
            
        return retValue


# Exemple d'opérateur

class CNC_TOOLS_OT_cnc_add_plunge(CNC_TOOLS_OT_BaseOperator):
    bl_idname = "cnc_tools.cnc_add_plunge"
    bl_label = "additionner un plunge"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Development"
    
    def invoke(self, context, event):
        self.dialog = False
        return super().invoke(context, event)

    def modal(self, context, event):
        retValue = super().modal(context, event)
        if retValue != {'RUNNING_MODAL'} and retValue != {'PASS_THROUGH'}:
            return retValue

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            if self.mouseIsOnWindow(context, event):
                # Clic gauche pour ajouter un CNCPlungePropertyGroup
                # Récupère la position 3D sous la souris
                # Récupération des informations nécessaires pour le raycasting
                region = context.region
                region_data = context.space_data.region_3d
                coord = (event.mouse_region_x, event.mouse_region_y)
                
                # Calcul du vecteur de vue et de l'origine du rayon
                view_vector = region_2d_to_vector_3d(region, region_data, coord)
                ray_origin = region_2d_to_origin_3d(region, region_data, coord)
                ray_target = ray_origin + (view_vector * 1000)  # Une longue distance pour le raycasting
                
                # Obtenir le depsgraph requis pour ray_cast
                depsgraph = context.evaluated_depsgraph_get()
                
                # Effectuer le raycasting
                hit, location, normal, face_index, obj, matrix = context.scene.ray_cast(depsgraph, ray_origin, view_vector)
                
                if hit:
                    print(f"Ray hit at {location}")

                retValue = {'RUNNING_MODAL'}

        return retValue

operators_cls = [
    CNC_TOOLS_OT_cnc_add_plunge,
    CNCTOOLBAR_OT_Operator
]
