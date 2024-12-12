#fichier draw_handler.py
import logging

import bpy
from bpy.types import Context, Operator
from bpy.utils import register_class, unregister_class

# Configuration du logger pour les messages d'information et de débogage
logger = logging.getLogger(__name__)

# Variable globale pour stocker le gestionnaire de dessin 2D
draw_handle_2d = None

# Dictionnaire global pour contenir les dialogues (widgets), accessible par d'autres add-ons
dialogs = {}


def draw2d_cb():
    """
    Callback pour le dessin 2D des widgets dans le Viewport.
    Parcourt tous les widgets dans le dictionnaire "dialogs" et les dessine.
    """
    context = bpy.context
    for widget in dialogs.values():
        widget.draw(context)


class View3D_OT_widget_register_draw_cb(Operator):
    """
    Opérateur pour enregistrer le gestionnaire de dessin 2D.
    Ce gestionnaire permet de dessiner des widgets dans le Viewport Blender.
    """
    bl_idname = "view3d.widget_register_draw_cb"
    bl_label = "Register Draw Callback"

    def execute(self, context: Context):
        global draw_handle_2d

        # Vérifie si le gestionnaire de dessin est déjà enregistré
        if draw_handle_2d is None:
            draw_handle_2d = bpy.types.SpaceView3D.draw_handler_add(
                draw2d_cb, (), "WINDOW", "POST_PIXEL"
            )
            logger.info("Draw handler registered.")
        else:
            logger.warning("Draw handler is already registered.")

        return {"FINISHED"}


class View3D_OT_widget_unregister_draw_cb(Operator):
    """
    Opérateur pour désenregistrer le gestionnaire de dessin 2D.
    Cela permet de nettoyer les ressources et d'arrêter le dessin des widgets.
    """
    bl_idname = "view3d.widget_unregister_draw_cb"
    bl_label = "Unregister Draw Callback"

    def execute(self, context: Context):
        global draw_handle_2d

        # Vérifie si un gestionnaire de dessin est enregistré
        if draw_handle_2d is not None:
            bpy.types.SpaceView3D.draw_handler_remove(draw_handle_2d, "WINDOW")
            draw_handle_2d = None
            logger.info("Draw handler unregistered.")
        else:
            logger.warning("No draw handler to unregister.")

        return {"FINISHED"}


def register():
    """
    Enregistre les classes d'opérateurs et initialise les ressources nécessaires.
    """
    register_class(View3D_OT_widget_register_draw_cb)
    register_class(View3D_OT_widget_unregister_draw_cb)


def unregister():
    """
    Désenregistre les classes d'opérateurs et libère les ressources.
    """
    unregister_class(View3D_OT_widget_unregister_draw_cb)
    unregister_class(View3D_OT_widget_register_draw_cb)

# Note pour les développeurs :
# Le dictionnaire global "dialogs" peut être utilisé par d'autres add-ons pour ajouter des widgets personnalisés.
# Par exemple :
# from <nom_du_module> import dialogs
# dialogs["my_widget"] = MonWidget()
