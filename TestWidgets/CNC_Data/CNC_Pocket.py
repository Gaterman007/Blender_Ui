import bpy
from .CNCDataPropertyGroup import CNCDataPropertyGroup

# Spécialisation pour les outils de type Pocket
class CNCPocketPropertyGroup(CNCDataPropertyGroup):
    # Redefine methodType in the derived class
    methodType: bpy.props.EnumProperty(
        name="Pocket Method",
        description="Type of Pocket method",
        items=[
            ('CENTER', "Center", "Pocket from the center out"),
            ('INTERIOR', "Interior", "Interior pocketing"),
            ('EXTERIOR', "Exterior", "Exterior pocketing")
        ],
        default='CENTER'
    )
    spiral_step: bpy.props.FloatProperty(
        name="Spiral Step",
        description="Step size for spiral pocketing",
        default=1.0,
        unit='LENGTH'
    )
    hole_size: bpy.props.FloatProperty(
        name="Hole Size",
        description="Size of the pocket or hole",
        default=10.0,
        unit='LENGTH'
    )
