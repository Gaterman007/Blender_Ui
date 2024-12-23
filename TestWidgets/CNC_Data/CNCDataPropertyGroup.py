import bpy

# Define a property group for storing CNC data
class CNCDataPropertyGroup(bpy.types.PropertyGroup):
    drillBitName: bpy.props.StringProperty(
        name="Drill Bit Name",
        description="Name of the drill bit"
    )
    drillBitUnits: bpy.props.EnumProperty(
        name="Units",
        description="Units of measurement for the drill bit",
        items=[
            ('MM', "Millimeters", "Use millimeters"),
            ('INCH', "Inches", "Use inches")
        ],
        default='MM'
    )
    methodType: bpy.props.EnumProperty(
        name="Method Type",
        description="Type of machining method (e.g., plunge, pocket)",
        items=[
            ('PLUNGE', "Plunge", "Plunge machining method"),
            ('POCKET', "Pocket", "Pocket machining method"),
            # Add other methods if needed
        ],
        default='PLUNGE'
    )
    depth: bpy.props.FloatProperty(
        name="Depth",
        description="Depth of cut",
        default=10.0,
        unit='LENGTH'
    )
    feedrate: bpy.props.FloatProperty(
        name="Feed Rate",
        description="Feed rate of the tool",
        default=1.0,
        unit='VELOCITY'
    )
    multipass: bpy.props.BoolProperty(
        name="Multi-pass",
        description="Whether to use multiple passes for cutting",
        default=False
    )
    depthStep: bpy.props.FloatProperty(
        name="Depth Step",
        description="Depth step per pass",
        default=2.0,
        unit='LENGTH'
    )
    overlapPercent: bpy.props.FloatProperty(
        name="Overlap Percentage",
        description="Percentage of overlap between passes",
        default=50.0,
        subtype='PERCENTAGE'
    )
