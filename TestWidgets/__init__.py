bl_info = {
    "name": "Widgets Lib Test",
    "description": "Un exemple de Addon utilisant Widgets Lib",
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

# Importer les classes depuis les fichiers séparés
from .operators import WIDGETS_LIB_USER_OT_TestOperator, WIDGETS_LIB_USER_OT_ShowLabel
from .panels import WIDGETS_LIB_USER_PT_TestPanel


def register():
    bpy.utils.register_class(WIDGETS_LIB_USER_OT_TestOperator)
    bpy.utils.register_class(WIDGETS_LIB_USER_OT_ShowLabel)
    bpy.utils.register_class(WIDGETS_LIB_USER_PT_TestPanel)


def unregister():
    bpy.utils.unregister_class(WIDGETS_LIB_USER_OT_TestOperator)
    bpy.utils.unregister_class(WIDGETS_LIB_USER_OT_ShowLabel)
    bpy.utils.unregister_class(WIDGETS_LIB_USER_PT_TestPanel)


if __name__ == "__main__":
    register()
