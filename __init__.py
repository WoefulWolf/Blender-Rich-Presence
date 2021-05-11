bl_info = {
    "name": "Discord Rich Presence for Blender",
    "author": "Woeful_Wolf",
    "version": (0, 3, 0),
    "blender": (2, 80, 0),
    "location": "None",
    "description": "Discord Rich Presence for Blender",
    "category": "System"}

import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty

from . import main_blender_rpc

class blender_rpc(bpy.types.Operator):
    '''Discord Rich Presence for Blender'''
    bl_idname = "system.blender_rpc"
    bl_label = "Blender RPC"
    bl_options = {'PRESET'}

    main_blender_rpc.main()

def register():
    bpy.utils.register_class(blender_rpc)

def unregister():
    bpy.utils.unregister_class(blender_rpc)


if __name__ == '__main__':
    register()