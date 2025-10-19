import os
import sys
import shutil
import json
import argparse

import open3d as o3d
import numpy as np

from glob import glob
from tqdm import tqdm

def keep_vert_face(mesh):
    if not isinstance(mesh, o3d.geometry.TriangleMesh):
        raise TypeError("Input mesh must be an instance of o3d.geometry.TriangleMesh")

    vertices, triangles = np.asarray(mesh.vertices), np.asarray(mesh.triangles)

    if len(vertices) == 0 or len(triangles) == 0:
        raise ValueError("Mesh must contain vertices and triangles")
    
    # Create a new mesh with only vertices and triangles
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)

    return mesh

def transpose_z_up(mesh):
    if not isinstance(mesh, o3d.geometry.TriangleMesh):
        raise TypeError("Input mesh must be an instance of o3d.geometry.TriangleMesh")

    vertices = np.asarray(mesh.vertices)
    vertices = vertices[:, [2, 0, 1]]
    mesh.vertices = o3d.utility.Vector3dVector(vertices)

    return mesh

def center_vertex(mesh):
    if not isinstance(mesh, o3d.geometry.TriangleMesh):
        raise TypeError("Input mesh must be an instance of o3d.geometry.TriangleMesh")

    vertices = np.asarray(mesh.vertices)
    
    vert_min = vertices.min(axis=0)
    vert_max = vertices.max(axis=0)
    vert_center = 0.5 * (vert_min + vert_max)
    mesh.vertices = o3d.utility.Vector3dVector(vertices - vert_center)

    return mesh

def normalize_mesh_scale(mesh, scale=0.5):
    if not isinstance(mesh, o3d.geometry.TriangleMesh):
        raise TypeError("Input mesh must be an instance of o3d.geometry.TriangleMesh")

    vertices = np.asarray(mesh.vertices)
    
    vert_min = vertices.min(axis=0)
    vert_max = vertices.max(axis=0)
    extents = (vert_max - vert_min).max()
    mesh.vertices = o3d.utility.Vector3dVector(2.0 * scale * vertices / (extents + 1e-6))

    return mesh

def import_tria_obj(file_path, backend='open3d'):
    if backend == 'open3d':
        mesh = o3d.io.read_triangle_mesh(file_path)
        if not mesh.is_empty():
            return mesh
        else:
            return None

def export_tria_obj(mesh, file_path):
    if mesh.is_empty():
        raise ValueError("Cannot export an empty mesh.")
    o3d.io.write_triangle_mesh(
        file_path, 
        mesh, 
        write_ascii=True,
        write_triangle_uvs=False, 
        write_vertex_normals=False,
        write_vertex_colors=False,
    )

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="input_dir")
    parser.add_argument("--output_dir", required=True, help="output_dir")
    parser.add_argument("--reset", action='store_true', help='hard reset')

    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        raise FileNotFoundError(f"Data path not found: {args.input_dir}")
    file_paths = glob(f'{args.input_dir}/*.obj')
    total_files = len(file_paths)
    print(f'Number of files: {total_files}')

    os.makedirs(args.output_dir, exist_ok=True)

    check_dct_path = os.path.join(args.output_dir, 'clean.json')
    check_dct = {
        'reading_mesh' : [],
        'merge_close_vertices': [],
        'remove_duplicated_triangles': [],
        'remove_duplicated_vertices': [],
        'remove_unreferenced_vertices': [],
        'remove_degenerate_triangles': [],
        'remove_non_manifold_edges': [],
        'transpose_z_up': [],
        'vertex_centering': [],
        'normalize_vertices_scale': [],
        'kiui_mesh_clean': [],
        'is_edge_manifold': [],
        'is_vertex_manifold': [],
        'export': []
    }

    for file in tqdm(file_paths, desc='Cleaning files', unit='file'):
        output_path = os.path.join(args.output_dir, os.path.basename(file))
        if os.path.exists(output_path):
            continue
        try:
            mesh = import_tria_obj(file)
            if mesh is None:
                continue
            mesh = keep_vert_face(mesh)
        except Exception as e:
            check_dct['reading_mesh'].append({'file': file, 'error': str(e)})
            continue
        try:
            mesh = mesh.merge_close_vertices(1e-8) #1e-8
        except Exception as e:
            check_dct['merge_close_vertices'].append({'file': file, 'error': str(e)})
            continue
        try:
            mesh = mesh.remove_duplicated_triangles()
        except Exception as e:
            check_dct['remove_duplicated_triangles'].append({'file': file, 'error': str(e)})
            continue
        try:
            mesh = mesh.remove_duplicated_vertices()
        except Exception as e:
            check_dct['remove_duplicated_vertices'].append({'file': file, 'error': str(e)})
            continue
        try:
            mesh = mesh.remove_unreferenced_vertices()
        except Exception as e:
            check_dct['remove_unreferenced_vertices'].append({'file': file, 'error': str(e)})
            continue
        try:
            mesh = mesh.remove_degenerate_triangles()
        except Exception as e:
            check_dct['remove_degenerate_triangles'].append({'file': file, 'error': str(e)})
            continue
        try:
            mesh = mesh.remove_non_manifold_edges()
        except Exception as e:
            check_dct['remove_non_manifold_edges'].append({'file': file, 'error': str(e)})
            continue
        try:
            mesh = transpose_z_up(mesh)
        except Exception as e:
            check_dct['transpose_z_up'].append({'file': file, 'error': str(e)})
            continue
        try:
            mesh = center_vertex(mesh)
        except Exception as e:
            check_dct['vertex_centering'].append({'file': file, 'error': str(e)})
            continue
        try:
            mesh = normalize_mesh_scale(mesh, 0.5)
        except Exception as e:
            check_dct['normalize_vertices_scale'].append({'file': file, 'error': str(e)})
            continue
        try:
            export_tria_obj(mesh, output_path)
        except Exception as e:
            check_dct['export'].append({'file': file, 'error': str(e)})
            continue
    
    with open(check_dct_path, 'w') as f:
        json.dump(check_dct, f, indent=4)