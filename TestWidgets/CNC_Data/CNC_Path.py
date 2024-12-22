import bpy
from .CNCDataPropertyGroup import CNCDataPropertyGroup

class CNCPathProperty(CNCDataPropertyGroup):
    start_point: bpy.props.FloatVectorProperty(
        name="Start Point",
        description="Starting point of the toolpath",
        subtype='XYZ',
        default=(0.0, 0.0, 0.0)
    )
    end_point: bpy.props.FloatVectorProperty(
        name="End Point",
        description="End point of the toolpath",
        subtype='XYZ',
        default=(1.0, 1.0, 1.0)
    )
