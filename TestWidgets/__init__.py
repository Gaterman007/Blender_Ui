bl_info = {
    "name": "CNC Tools",
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

from .draw_handler import register as register_draw_handler_3d
from .draw_handler import unregister as unregister_draw_handler_3d


# Importer les classes depuis les fichiers séparés
from .operators import operators_cls    
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
        "cnc_tools.main_toolbar",  # Remplacez par l'ID de votre opérateur
        text="CNC Toolbar",  # Le texte visible dans le menu
        icon='MESH_CUBE'  # Icône de l'élément
    )

def register():
    register_draw_handler()  # Appelle la fonction register de widgets_lib.draw_handler
    register_draw_handler_3d()  # Appelle la fonction register de draw_handler_3d
    
    # Define a property group for storing CNC data
    for cls in classes:
        bpy.utils.register_class(cls)

    for cls in operators_cls:
        print(cls)
        bpy.utils.register_class(cls)
    
    bpy.utils.register_class(WIDGETS_LIB_USER_PT_TestPanel)

    # Enregistrer l'ajout au menu
    bpy.types.VIEW3D_MT_add.append(menu_func_add)
    
def unregister():
    unregister_draw_handler()  # Appelle la fonction register de widgets_lib.draw_handler
    unregister_draw_handler_3d()  # Appelle la fonction register de draw_handler_3d
    bpy.utils.unregister_class(WIDGETS_LIB_USER_PT_TestPanel)

    for cls in operators_cls:
        bpy.utils.unregister_class(cls)

    for cls in classes:
        bpy.utils.unregister_class(cls)
    

    # Supprimer l'ajout au menu
    bpy.types.VIEW3D_MT_add.remove(menu_func_add)

    
if __name__ == "__main__":
    register()

#
#
# Commun 
#   Method Type
#   Depth
#   Feed Rate
#   Multiple Pass
#       Depth Step
#   Drill Bit Name
#       drillBit.Cut_Diameter
#       drillBit.units
#   overlapPercent
#
# PlungeTool
#   Method Type
#       Down
#       Step
#       Spiral
#   Spiral overlap
#   Hole Size
#
# PocketTool
#   Method Type
#       Centrer
#       Interieur
#       Exterieur
#   Spiral Step
#   Hole Size
#   
#
# StraitCutTool
#   Method Type
#       Ramp
#       Multipass
#       Plunge
#  cutwidth = 5.3