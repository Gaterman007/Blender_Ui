# __init__.py

bl_info = {
    "name": "Widgets Library",
    "description": "Une bibliothèque de widgets personnalisés pour Blender",
    "author": "Gaétan Noiseux",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),  # Changez selon la version minimale de Blender supportée
    "location": "View3D > Tools",
    "warning": "",  # Laissez vide si pas de problème connu
    "category": "Development",
}

# Métadonnées du package
__version__ = "1.0.0"
__author__ = "Gaétan Noiseux"
__license__ = "MIT"
__description__ = "Une bibliothèque de widgets personnalisés pour Blender"

# Importation des modules nécessaires
from .draw_handler import draw2d_cb
from .widgets import (
    bl_ui_button,
    bl_ui_checkbox,
    bl_ui_drag_panel,
    bl_ui_dropdown,
    bl_ui_image,
    bl_ui_label,
    bl_ui_slider,
    bl_ui_textbox,
    bl_ui_toolbar,
    bl_ui_up_down,
    bl_ui_widget,
)

from .widgets.Icons import (
    SVG_Icon,
    Texture,
)

# Exposition des interfaces principales
__all__ = [
    "draw2d_cb",
    "bl_ui_button",
    "bl_ui_checkbox",
    "bl_ui_drag_panel",
    "bl_ui_dropdown",
    "bl_ui_image",
    "bl_ui_label",
    "bl_ui_slider",
    "bl_ui_textbox",
    "bl_ui_toolbar",
    "bl_ui_up_down",
    "bl_ui_widget",
    "SVG_Icon",
    "Texture",
]


def register():
    print("Widgets Library est activé.")

def unregister():
    print("Widgets Library est désactivé.")

#widgets_lib/
#├── __init__.py               # Point d'entrée principal pour l'importation
#├── draw_handler.py           # Gestion des dessins dans le viewport
#├── SVG_Files/                # Contient les fichiers SVG
#│   ├── action.svg            # fichiers svg
#│   ├── ... (les fichiers SVG)
#├── widget/                   # Répertoire pour les widgets
#│   ├── __init__.py           # Initialisation pour importer tous les widgets
#│   ├── bl_ui_button.py       # widget bouton
#│   ├── bl_ui_checkbox.py     # widget checkbox
#│   ├── bl_ui_drag_panel.py   # widget dragpanel
#│   ├── bl_ui_dropdown.py     # widget dropdown
#│   ├── bl_ui_image.py        # widget image
#│   ├── bl_ui_label.py        # widget label
#│   ├── bl_ui_slider.py       # widget slider
#│   ├── bl_ui_textbox.py      # widget textbox
#│   ├── bl_ui_toolbar.py      # widget toolbar
#│   ├── bl_ui_up_down.py      # widget up down
#│   ├── bl_ui_widget.py       # widget de base
#│   └── Icons/                # Répertoire pour la gestion des icônes
#│       ├── __init__.py       # Initialisation pour la gestion des icônes
#│       ├── ImagesCls.py      # 
#│       ├── Matrices.py       # 
#│       ├── SVG_Element.py    # 
#│       ├── SVG_Icon.py       # 
#│       ├── Texture.py        # Créer des textures depuis des SVG

