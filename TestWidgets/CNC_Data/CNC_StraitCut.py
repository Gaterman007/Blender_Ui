import bpy
from .CNCDataPropertyGroup import CNCDataPropertyGroup

# Spécialisation pour les outils de type Straight Cut
class CNCStraitCutPropertyGroup(CNCDataPropertyGroup):
    # Redefine methodType in the derived class
    methodType: bpy.props.EnumProperty(
        name="Strait Cut Method",
        description="Type of straight cut",
        items=[
            ('RAMP', "Ramp", "Ramp cutting"),
            ('MULTIPASS', "Multi-pass", "Multi-pass cutting"),
            ('PLUNGE', "Plunge", "Plunge cutting")
        ],
        default='RAMP'
    )
    cut_width: bpy.props.FloatProperty(
        name="Cut Width",
        description="Width of the cut",
        default=5.0,
        unit='LENGTH'
    )