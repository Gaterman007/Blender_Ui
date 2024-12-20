import bpy
import os
import gpu

from .bl_ui_widget import BL_UI_Widget
from gpu_extras.batch import batch_for_shader
from .Icons.SVG_Icon import SVG_Icon, get_SVG_Icon
from .Icons.Texture import Textures

class BL_UI_Image(BL_UI_Widget):

    # Ajouter 'widgets\SVG_Files' au répertoire parent
    svg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'SVG_Files')

    def __init__(self, *args , **kwargs):
#         x, y, width = 80, height = 40, color = (0.0,0.0,0.0,0.0)
        self.__state = 0
        self.__image = None
        self.__image_size = None
        super().__init__( *args , **kwargs)
        self.__image_size = (self.width, self.height)
        self.texture = Textures(self.width, self.height)


    def __del__(self):
        if self.texture is not None:
            self.texture = None
        
    def set_image_size(self, image_size):
        self.__image_size = image_size
        self.batch()
        
    def check_image_exists(self):
        # it's possible image was removed and doesn't exist.
        try:
            self.__image
            self.__image.filepath
        except Exception as e:
            self.__image = None
        return None

    def set_image(self, rel_filename):
        #"\Icons\SVG_File"
        # first try to access the image, for cases where it can get removed

        self.check_image_exists()
        imgname = f".{rel_filename}"
        self.__image = bpy.data.images.get(imgname)
        if self.__image is None:  # image n'est pas deja definie
            svg_filename = rel_filename
            svg_filename += '.svg'
            svg_filepath = os.path.join(BL_UI_Image.svg_path, rel_filename + '.svg')
            png_filepath = os.path.join(BL_UI_Image.svg_path, rel_filename + '.png')
            fileExist = os.path.exists(svg_filepath)
            if fileExist:    # fichier svg exist
                self.texture.load_SVG(svg_filepath)
                # cree l image a partir du fichier svg
            else:
                fileExist = os.path.exists(os.path.join(BL_UI_Image.svg_path, rel_filename + '.png'))
                if fileExist:    # fichier png exist
                    self.texture.load_PNG(png_filepath)
        else:
            self.texture.set_textureData(self.__image.size[0],self.__image.size[1],self.__image.pixels)
            bpy.data.images.remove(self.__image)
            self.__image = None
            
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
            (0, 0),  # Coin inférieur gauche
            (1, 0),  # Coin inférieur droit
            (1, 1),  # Coin supérieur droit
            (0, 1),  # Coin supérieur gauche
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
            # draw image
            gpu.state.blend_set("ALPHA")
            self.drawStartShader(self.shader_img,context)
            self.texture.draw_texture(self.shader_img)
            self.batch_image.draw(self.shader_img) 
            self.drawEndShader(self.shader_img,context) 
            gpu.state.blend_set("NONE")

    def is_in_rect(self, x, y):
        return False
