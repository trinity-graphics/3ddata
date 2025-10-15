import sys
import os
import bpy
import json

from typing import Any, Callable, Dict, Generator, List, Literal, Optional, Set, Tuple

IMPORT_FUNCTIONS: Dict[str, Callable] = {
    "obj": bpy.ops.import_scene.obj,
    "glb": bpy.ops.import_scene.gltf,
    "gltf": bpy.ops.import_scene.gltf,
    "usd": bpy.ops.import_scene.usd,
    "fbx": bpy.ops.import_scene.fbx,
    "stl": bpy.ops.import_mesh.stl,
    "usda": bpy.ops.import_scene.usda,
    "dae": bpy.ops.wm.collada_import,
    "ply": bpy.ops.import_mesh.ply,
    "abc": bpy.ops.wm.alembic_import,
    "blend": bpy.ops.wm.append,
}

def import_obj(filepath, file_ext):
    object_name = os.path.basename(filepath) # Get object name
    existing_objects = set(bpy.context.scene.objects) # Store the current objects in the scene
    IMPORT_FUNCTIONS[file_ext](filepath=filepath) # Import
    new_objects = set(bpy.context.scene.objects) - existing_objects # Determine the newly imported objects

    # Set the location and name for each new object
    for obj in new_objects:
        obj.name = object_name
        if obj.data:
            obj.data.name = object_name
    
    return object_name

def export_obj(filepath, export_triangle=True):
    bpy.ops.wm.obj_export(
        filepath=filepath,
        check_existing=True,
        filter_blender=False,
        filter_backup=False,
        filter_image=False,
        filter_movie=False,
        filter_python=False,
        filter_font=False,
        filter_sound=False,
        filter_text=False,
        filter_archive=False,
        filter_btx=False,
        filter_collada=False,
        filter_alembic=False,
        filter_usd=False,
        filter_obj=False,
        filter_volume=False,
        filter_folder=True,
        filter_blenlib=False,
        filemode=8,
        display_type='DEFAULT',
        sort_method='DEFAULT',
        export_animation=False,
        start_frame=-2147483648,
        end_frame=2147483647,
        forward_axis='X',
        up_axis='Z',
        global_scale=1.0,
        apply_modifiers=False,
        export_eval_mode='DAG_EVAL_VIEWPORT',
        export_selected_objects=True,
        export_uv=False,
        export_normals=False,
        export_colors=False,
        export_materials=False,
        export_pbr_extensions=False,
        path_mode='AUTO',
        export_triangulated_mesh=export_triangle,
        export_curves_as_nurbs=False,
        export_object_groups=False,
        export_material_groups=False,
        export_vertex_groups=False,
        export_smooth_groups=False,
        smooth_group_bitflags=False,
        filter_glob='*.obj;*.mtl'
    )


def main(argv):
    # Expected args: <src_obj> <dst_obj> <meta.json> <file_ext>
    if len(argv) < 4:
        print('Usage: blender --background --python blender_worker.py -- <src.obj> <dst.obj> <meta.json> <file_ext>')
        return 2

    src = argv[0]
    dst = argv[1]
    meta_out = argv[2]
    file_ext = argv[3]

    print(f'Worker: importing {src} and exporting to {dst}')

    # Clean the current scene: remove all objects
    if bpy is not None:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    # Import
    try:
        name = import_obj(src, file_ext)
    except Exception as e:
        print(f'Import failed: {e}')
        return 3

    # Export
    try:
        # Ensure destination directory exists
        export_obj(dst)
    except Exception as e:
        print(f'Export failed: {e}')
        return 4

    # Gather metadata from the current scene
    metadata = {
        'num_objects': 0,
        'num_vertices': 0,
        'num_edges': 0,
        'num_polygons': 0
    }

    if bpy is not None:
        # Count objects that have mesh data
        mesh_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
        metadata['num_objects'] = len(mesh_objs)
        verts = 0
        edges = 0
        polys = 0
        for o in mesh_objs:
            try:
                m = o.data
                verts += len(m.vertices)
                edges += len(m.edges)
                polys += len(m.polygons)
            except Exception:
                continue
        metadata['num_vertices'] = verts
        metadata['num_edges'] = edges
        metadata['num_polygons'] = polys

    # Write metadata JSON
    try:
        meta_dir = os.path.dirname(meta_out)
        os.makedirs(meta_dir, exist_ok=True)
        with open(meta_out, 'w') as f:
            json.dump(metadata, f)
    except Exception as e:
        print(f'Failed to write metadata {meta_out}: {e}')

    print('Worker: done')
    return 0


if __name__ == '__main__':
    # Blender passes args after '--' to the script via sys.argv
    try:
        idx = sys.argv.index('--')
        args = sys.argv[idx+1:]
    except ValueError:
        args = sys.argv[1:]
    rc = main(args)
    # When running inside Blender, sys.exit will return the code to the shell
    sys.exit(rc)