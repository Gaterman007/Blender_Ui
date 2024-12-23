import bpy
from .CNCDataPropertyGroup import CNCDataPropertyGroup

# Spécialisation pour les outils de type Plunge
class CNCPlungePropertyGroup(CNCDataPropertyGroup):
    # Redefine methodType in the derived class
    methodType: bpy.props.EnumProperty(
        name="Plunge Method",
        description="Type of plunge method",
        items=[
            ('DOWN', "Down", "Plunge straight down"),
            ('STEP', "Step", "Step plunge"),
            ('SPIRAL', "Spiral", "Spiral plunge")
        ],
        default='DOWN'
    )
    spiral_overlap: bpy.props.FloatProperty(
        name="Spiral Overlap",
        description="Overlap percentage for spiral plunge",
        default=50.0,
        subtype='PERCENTAGE'
    )
    hole_size: bpy.props.FloatProperty(
        name="Hole Size",
        description="Size of the hole",
        default=10.0,
        unit='LENGTH'
    )
    location: bpy.props.FloatVectorProperty(
        name="Location",
        description="Position 3D du plunge",
        default=(0.0, 0.0, 0.0),
        subtype='XYZ'
    )    
    