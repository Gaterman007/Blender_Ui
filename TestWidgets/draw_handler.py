import logging
import bpy
from bpy.types import Context, Operator
from bpy.utils import register_class, unregister_class

# Configuration du logger pour les messages d'information et de débogage
logger = logging.getLogger(__name__)

# Variable globale pour stocker le gestionnaire de dessin 3D
draw_handle_3d = None

# Dictionnaire global pour contenir les dialogues (widgets), accessible par d'autres add-ons
cnc_data = {}

def draw3d_cb():
    """
    Callback pour le dessin 3D des widgets dans le Viewport.
    Parcourt tous les widgets dans le dictionnaire "dialogs" et les dessine dans l'espace 3D.
    """
    context = bpy.context
    region = context.region
    region_3d = context.space_data.region_3d
    
    # Active la matrice de transformation de la vue 3D
    # Exemple de transformation : placer un cnc data à une position donnée dans l'espace 3D
    for data in cnc_data.values():
        data.draw_3d(context, region, region_3d)

class View3D_OT_CNC_data_register_draw_cb(Operator):
    """
    Opérateur pour enregistrer le gestionnaire de dessin 3D.
    Ce gestionnaire permet de dessiner des widgets dans le Viewport 3D de Blender.
    """
    bl_idname = "view3d.cnc_data_register_draw_cb"
    bl_label = "Register Draw Callback 3D"

    def execute(self, context: Context):
        global draw_handle_3d

        # Vérifie si le gestionnaire de dessin est déjà enregistré
        if draw_handle_3d is None:
            draw_handle_3d = bpy.types.SpaceView3D.draw_handler_add(
                draw3d_cb, (), "WINDOW", "POST_VIEW"  # Passer à "POST_VIEW" pour un dessin en 3D
            )
            logger.info("Draw handler registered for 3D.")
        else:
            logger.warning("Draw handler is already registered.")

        return {"FINISHED"}

class View3D_OT_CNC_data_unregister_draw_cb(Operator):
    """
    Opérateur pour désenregistrer le gestionnaire de dessin 3D.
    Cela permet de nettoyer les ressources et d'arrêter le dessin des widgets.
    """
    bl_idname = "view3d.cnc_data_unregister_draw_cb"
    bl_label = "Unregister Draw Callback 3D"

    def execute(self, context: Context):
        global draw_handle_3d

        # Vérifie si un gestionnaire de dessin est enregistré
        if draw_handle_3d is not None:
            bpy.types.SpaceView3D.draw_handler_remove(draw_handle_3d, "WINDOW")
            draw_handle_3d = None
            logger.info("Draw handler unregistered.")
        else:
            logger.warning("No draw handler to unregister.")

        return {"FINISHED"}

def register():
    """
    Enregistre les classes d'opérateurs et initialise les ressources nécessaires.
    """
    register_class(View3D_OT_CNC_data_register_draw_cb)
    register_class(View3D_OT_CNC_data_unregister_draw_cb)

def unregister():
    """
    Désenregistre les classes d'opérateurs et libère les ressources.
    """
    unregister_class(View3D_OT_CNC_data_unregister_draw_cb)
    unregister_class(View3D_OT_CNC_data_register_draw_cb)
