import bpy
import gpu
import os

from .bl_ui_widget import BL_UI_Widget
from .bl_ui_image import BL_UI_Image
from .bl_ui_label import BL_UI_Label
from gpu_extras.batch import batch_for_shader
from .Icons.SVG_Icon import SVG_Icon, get_SVG_Icon
from .Icons.Texture import Textures

class BL_UI_Button(BL_UI_Label):
    STATE_NORMAL = 0
    STATE_PRESSED = 1
    STATE_HOVER = 2

    def __init__(self, *args , **kwargs):
        """
        Initialisation du bouton avec position, dimensions et texte.
        """
        self.texture = None
        self.__image_size = None
        
        self.cropTop = 0.0;
        self.cropBottom = 1.0;
        self.cropLeft = 0.0;
        self.cropRight = 1.0;

        super().__init__( *args , **kwargs)
        self._text = kwargs.get("text", args[4] if len(args) > 4 else "button")
        self.className = "Button"
        self._text_color = (1.0, 1.0, 1.0, 1.0)  # Couleur du texte
        self._hover_bg_color = (0.5, 0.5, 0.5, 1.0)  # Couleur arrière-plan au survol
        self._select_bg_color = (0.7, 0.7, 0.7, 1.0)  # Couleur arrière-plan à la sélection
        self._setState(self.STATE_NORMAL)
        
        self.__opClass = None  # Classe d'opérateur pour l'appel dynamique
        self.index = None  # Paramètre d'index pour l'opérateur
        self.type = None  # Paramètre de type pour l'opérateur

        self._clicFunct = None  # Fonction callback pour clic
        self._FunctData = None  # Données pour la fonction callback        
      
    def _setState(self,state):
        self.__state = state
      
    @property
    def hover_bg_color(self):
        """Retourne la couleur d'arrière-plan au survol."""
        return self._hover_bg_color

    @hover_bg_color.setter
    def hover_bg_color(self, value):
        """Définit la couleur d'arrière-plan au survol et redessine si nécessaire."""
        if value != self._hover_bg_color:
            bpy.context.region.tag_redraw()  # Redessiner la région
        self._hover_bg_color = value

    @property
    def select_bg_color(self):
        """Retourne la couleur d'arrière-plan à la sélection."""
        return self._select_bg_color

    @select_bg_color.setter
    def select_bg_color(self, value):
        """Définit la couleur d'arrière-plan à la sélection et redessine si nécessaire."""
        if value != self._select_bg_color:
            bpy.context.region.tag_redraw()  # Redessiner la région
        self._select_bg_color = value

    def set_image(self, rel_filename):
        svg_filename = rel_filename
        svg_filename += '.svg'
        print(BL_UI_Image.svg_path)
        print(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"\\SVG_Files")
        svg_filepath = os.path.join(BL_UI_Image.svg_path, rel_filename + '.svg')
        png_filepath = os.path.join(BL_UI_Image.svg_path, rel_filename + '.png')
        print(svg_filepath)
        fileExist = os.path.exists(svg_filepath)
        if fileExist:    # fichier svg exist
            if self.texture is not None:
                self.texture = None
            self.texture = Textures(self.width, self.height)
            self.texture.load_SVG(svg_filepath)
            # cree l image a partir du fichier svg
        else:
            fileExist = os.path.exists(os.path.join(BL_UI_Image.svg_path, rel_filename + '.png'))
            if fileExist:    # fichier png exist
                if self.texture is not None:
                    self.texture = None
                self.texture = Textures(self.width, self.height)
                self.texture.load_PNG(png_filepath)
            else:
                if self.texture is not None:
                    self.texture = None

    def set_crop(self,top,bottom,left,right):
        self.cropTop = top;
        self.cropBottom = bottom;
        self.cropLeft = left;
        self.cropRight = right;
        self.batch()

    def batch(self):     
        super().batch()
        off_x = 2
        off_y = 2
        if self.__image_size is None:
            self.__image_size = (self.width, self.height)
        sx, sy = self.__image_size

        if bpy.app.version < (4, 0, 0):
            # Utilise un shader pour les textures 2D
            self.shader_img = gpu.shader.from_builtin("2D_IMAGE")
        else:
            self.shader_img = gpu.shader.from_builtin("IMAGE")

        # Définition des vertices pour un rectangle (4 points pour afficher l'image)
        self.vertices = [
            ( 0 + off_x,  0 + off_y),  # coin inférieur gauche
            (sx - off_x,  0 + off_y),  # coin inférieur droit
            (sx - off_x, sy - off_y),  # coin supérieur droit
            ( 0 + off_x, sy - off_y),  # coin supérieur gauche
        ]

        # Définition des coordonnées UV pour l'image (mapping de la texture)
        self.uv_coords = [
            (self.cropLeft, self.cropTop),  # Coin inférieur gauche
            (self.cropRight, self.cropTop),  # Coin inférieur droit
            (self.cropRight, self.cropBottom),  # Coin supérieur droit
            (self.cropLeft, self.cropBottom),  # Coin supérieur gauche
        ]

        # Indices des sommets pour former le rectangle
        self.indices = [(0, 1, 2), (2, 3, 0)]

        # Création du batch pour le dessin du rectangle avec texture
        self.batch_image = batch_for_shader(
            self.shader_img, 'TRIS', {"pos": self.vertices, "texCoord": self.uv_coords}, indices=self.indices
        )

    def draw(self,context):
        if not self._is_visible:
            return

        if self.texture is not None:
            BL_UI_Widget.draw(self,context)
            # draw image
            gpu.state.blend_set("ALPHA")
            self.drawStartShader(self.shader_img,context)
            self.texture.draw_texture(self.shader_img)
            self.batch_image.draw(self.shader_img) 
            self.drawEndShader(self.shader_img,context) 
            gpu.state.blend_set("NONE")
        else:
            super().draw(context)

    def setOpClass(self, opClass, index, type):
        """
        Définit la classe d'opérateur à appeler lors du clic.
        Définit l'index à passer à l'opérateur lors du clic.
        Définit le type à passer à l'opérateur lors du clic.
        :param opClass: String sous la forme "module.operateur".
        """
        self.__opClass = opClass
        self.index = index
        self.type = type

    def setMouseClicCallBack(self, funct, data):
        """
        Définit une fonction callback pour l'événement de clic.
        :param funct: Fonction callback à appeler.
        :param data: Données à passer à la fonction callback.
        """
        self._clicFunct = funct
        self._FunctData = data

    def get_bg_color(self):
        """
        Définit la couleur d'arrière-plan en fonction de l'état actuel (survol, sélection, normal).
        """
        if self.__state == self.STATE_PRESSED:
            color = self._select_bg_color
        elif self.__state == self.STATE_HOVER:
            color = self._hover_bg_color
        else:
            color = self._bg_color
        return color
        
    def is_in_rect(self, x, y):
        return BL_UI_Widget.is_in_rect(self,x, y)

    def mouse_down(self, x, y, context):
        """
        Gère l'événement de clic de souris.
        :param x: Position x de la souris.
        :param y: Position y de la souris.
        """
        if self.is_in_rect(x, y):
            self._setState(self.STATE_PRESSED)
            return {"RUNNING_MODAL"}, True
        return {"RUNNING_MODAL"}, False

    def mouse_move(self, x, y, context):
        """
        Gère l'événement de mouvement de souris.
        :param x: Position x de la souris.
        :param y: Position y de la souris.
        """
        if self.is_in_rect(x, y):
            if self.__state != self.STATE_PRESSED:
                self._setState(self.STATE_HOVER)
        else:
            self._setState(self.STATE_NORMAL)
        return {"RUNNING_MODAL"}, False

    def mouse_up(self, x, y, context):
        """
        Gère l'événement de relâchement de la souris.
        :param x: Position x de la souris.
        :param y: Position y de la souris.
        """
        result = ({"RUNNING_MODAL"},False)
        if self.is_in_rect(x, y) and self.__state == self.STATE_PRESSED:
            if self.__opClass is not None:
                family, operator = self.__opClass.split(".")
                try:
                    # Appeler l'opérateur en utilisant `bpy.ops` dynamiquement
                    if self.type is not None:
                        resDelete = getattr(bpy.ops, family).__getattr__(operator)(type = self.type,index= self.index)
                    else:
                        resDelete = getattr(bpy.ops, family).__getattr__(operator)(index= self.index)
                    result = (resDelete,True)
                except AttributeError as e:
                    print(f"Erreur d'appel d'opérateur: {e}")                    
            else:
                if self._clicFunct is not None:
                    result = self._clicFunct(self._FunctData,context)
            self._setState(self.STATE_HOVER)
        else:
            self._setState(self.STATE_NORMAL)
        return result