import os
import sys
import argparse

from utils.io import import_tria_obj, export_tria_obj
from glob import glob
from tqdm import tqdm

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

def process_file(file_path, output_path):

    try:
        mesh = import_tria_obj(file_path)
        if mesh is None:
            return f'Skipped {file_path}: Mesh is empty or could not be loaded.'
        export_tria_obj(mesh, output_path)
        return f'Processed {file_path} -> {output_path}'
    except Exception as e:
        return f'Error processing {file_path}: {e}'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="input_dir")
    parser.add_argument("--output_dir", required=True, help="output_dir")
    
    file_paths = glob(f'{args.input_dir}/*.glb')
    total_files = len(file_paths)
    print(f'Number of files: {total_files}')

    os.makedirs(args.output_dir, exist_ok=True)
    
    log_file = os.path.join(args.output_dir, 'log.txt')
    if os.path.exists(log_file):
        os.remove(log_file)

    with open(log_file, 'w') as log_f:
        log_f.write(f'Processing {total_files} files...\n')

    results = []
    for file_path in tqdm(file_paths):
        output_filename = os.path.basename(file_path).replace('.glb', '.obj')
        output_path = os.path.join(args.output_dir, output_filename)
        result = process_file(file_path, output_path)
        results.append(result)
    
    with open(log_file, 'a') as log_f:
        for result in results:
            log_f.write(result + '\n')

    # --- Final message ---
    print('All files processed.')