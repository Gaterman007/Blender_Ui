bl_info = {
    "name": "CNC data with Widgets Test",
    "description": "Addon pour CNC utilisant Widgets Lib",
    "author": "Gaétan Noiseux",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Tools",
    "category": "Development",
}

import bpy
import sys
import os

# Ajouter widgets_lib au sys.path si nécessaire
ADDON_NAME = "widgets_lib"
addon_path = os.path.join(bpy.utils.user_resource('SCRIPTS'), "addons", ADDON_NAME)
if addon_path not in sys.path:
    sys.path.append(addon_path)

try:
    import widgets_lib
except ImportError:
    print(f"Erreur : Impossible de charger '{ADDON_NAME}'. Assurez-vous qu'il est installé et activé.")


from widgets_lib.draw_handler import register as register_draw_handler
from widgets_lib.draw_handler import unregister as unregister_draw_handler

# Importer les classes depuis les fichiers séparés
from .operators import CNCTOOLBAR_OT_Operator
from .panels import WIDGETS_LIB_USER_PT_TestPanel

from .CNC_Data.CNCDataPropertyGroup import CNCDataPropertyGroup
from .CNC_Data.CNC_Path import CNCPathProperty
from .CNC_Data.CNC_Plunge import CNCPlungePropertyGroup
from .CNC_Data.CNC_Pocket import CNCPocketPropertyGroup
from .CNC_Data.CNC_StraitCut import CNCStraitCutPropertyGroup


classes = [
    CNCDataPropertyGroup,
    CNCPlungePropertyGroup,
    CNCPathProperty,
    CNCPocketPropertyGroup,
    CNCStraitCutPropertyGroup
]


def menu_func_add(self, context):
    self.layout.operator(
        "wm.widgets_lib_test",  # Remplacez par l'ID de votre opérateur
        text="CNC Toolbar",  # Le texte visible dans le menu
        icon='MESH_CUBE'  # Icône de l'élément
    )

def register():
    register_draw_handler()  # Appelle la fonction register de widgets_lib.draw_handler
    
    # Define a property group for storing CNC data
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.utils.register_class(CNCTOOLBAR_OT_Operator)
    bpy.utils.register_class(WIDGETS_LIB_USER_PT_TestPanel)

    # Enregistrer l'ajout au menu
    bpy.types.VIEW3D_MT_add.append(menu_func_add)
    
def unregister():
    unregister_draw_handler()  # Appelle la fonction register de widgets_lib.draw_handler
    bpy.utils.unregister_class(WIDGETS_LIB_USER_PT_TestPanel)
    bpy.utils.unregister_class(CNCTOOLBAR_OT_Operator)

    for cls in classes:
        bpy.utils.unregister_class(cls)
    

    # Supprimer l'ajout au menu
    bpy.types.VIEW3D_MT_add.remove(menu_func_add)

    
if __name__ == "__main__":
    register()
