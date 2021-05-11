from .pypresence import Presence
import bpy
from bpy.app.handlers import persistent
import time
import atexit
import sys

update_delay = 15.0

def main():
    client_id = '638415602167447553'

    global presence
    presence = Presence(client_id)

    global app_version
    app_version = 'Blender ' + bpy.app.version_string

    presence.connect()

    bpy.app.handlers.load_post.append(start_timer)
    bpy.app.handlers.render_init.append(render_started)
    bpy.app.handlers.render_complete.append(render_ended)
    bpy.app.handlers.render_cancel.append(render_ended)

    atexit.register(close)

    start_timer(None)

@persistent
def start_timer(dummy):
    if bpy.app.timers.is_registered(update):
        bpy.app.timers.unregister(update)

    bpy.app.timers.register(update)

@persistent
def render_started(dummy):
    if bpy.app.timers.is_registered(update):
        bpy.app.timers.unregister(update)
        
    start_time = int(round(time.time() * 1000))
    presence.update(large_image='blender_icon', large_text=app_version, details=get_project_path(), state='RENDERING:', start=start_time)

@persistent
def render_ended(dummy):
    bpy.app.timers.register(update)
    presence.update(large_image='blender_icon', large_text=app_version, details=get_project_path(), state=get_project_info())

def get_project_path():
    project_path = "None"
    if bpy.data.is_saved:
        if sys.platform == 'win32':
            project_path = str(bpy.data.filepath).split('\\')[-1]
        else:
            project_path = str(bpy.data.filepath).split('/')[-1]
    else:
        project_path = 'Project Not Saved'
    return project_path

def get_project_info():
    stats = bpy.context.scene.statistics(bpy.context.view_layer)
    stats_split = stats.split("|")
    verts = stats_split[2].strip().split(":")[1]
    faces = stats_split[3].strip().split(":")[1]

    project_info = "Verts: " + verts + " | " + "Faces: " + faces
    return project_info

def update():
    presence.update(large_image='blender_icon', large_text=app_version, details=get_project_path(), state=get_project_info())
    return update_delay

def close():
    presence.clear()
    presence.close()
