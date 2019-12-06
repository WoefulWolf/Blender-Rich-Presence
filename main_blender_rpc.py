from .pypresence import Presence
import bpy
from bpy.app.handlers import persistent
import time
import atexit

update_delay = 15.0

def main():
    client_id = '638415602167447553'

    global presence
    presence = Presence(client_id)

    global app_version
    app_version = 'Blender ' + bpy.app.version_string

    presence.connect()

    bpy.app.handlers.load_post.append(start_timer)
    bpy.app.handlers.render_pre.append(render_started)
    bpy.app.handlers.render_post.append(render_ended)

    atexit.register(close)

    start_timer(None)

@persistent
def start_timer(dummy):
    if bpy.app.timers.is_registered(update):
        bpy.app.timers.unregister(update)

    bpy.app.timers.register(update)

@persistent
def render_started(dummy):
    print('render started')
    if bpy.app.timers.is_registered(update):
        bpy.app.timers.unregister(update)
        
    start_time = int(round(time.time() * 1000))
    presence.update(large_image='blender_icon', large_text=app_version, details=project_path, state='RENDERING:', start=start_time)

@persistent
def render_ended(dummy):
    print('render ended')
    bpy.app.timers.register(update)
    presence.update(large_image='blender_icon', large_text=app_version, details=project_path, state=project_info)

def update():

    global project_path
    if bpy.data.is_saved:
        project_path = str(bpy.data.filepath).split('\\')[-1]
    else:
        project_path = 'Project Not Saved'

    total_verts = 0
    total_faces = 0
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            total_verts += len(obj.data.vertices)
            total_faces += len(obj.data.polygons)

    global project_info
    project_info = 'Verts: ' + str(total_verts) + ' | Faces: ' + str(total_faces)

    presence.update(large_image='blender_icon', large_text=app_version, details=project_path, state=project_info)


    return update_delay

def close():
    presence.clear()
    presence.close()
