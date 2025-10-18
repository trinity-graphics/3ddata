import argparse
import glob
import os
import trimesh
import multiprocessing as mp
import polars as pl
import numpy as np


def analyze_mesh(file_path):
    """Analyze a single mesh file for geometric and connectivity stats."""
    try:
        mesh = trimesh.load(file_path, force='mesh')
        if not isinstance(mesh, trimesh.Trimesh):
            return None  # skip non-mesh containers

        # --- Basic properties ---
        num_vertices = len(mesh.vertices)
        num_faces = len(mesh.faces)

        # --- Edges and connectivity ---
        edges = mesh.edges_sorted
        edges_unique, edges_counts = np.unique(edges, axis=0, return_counts=True)
        num_internal_edges = np.sum(edges_counts == 2)
        num_boundary_edges = np.sum(edges_counts == 1)

        # --- Vertex connectivity ---
        vertex_connectivity = np.bincount(edges_unique.flatten(), minlength=num_vertices)
        min_conn = int(vertex_connectivity.min())
        max_conn = int(vertex_connectivity.max())
        avg_conn = float(vertex_connectivity.mean())

        # --- Strongly connected components (disconnected parts) ---
        components = mesh.split(only_watertight=False)
        num_components = len(components)

        # Get size info for smallest and largest components
        if num_components > 0:
            component_sizes = [(len(c.vertices), len(c.faces)) for c in components]
            sorted_components = sorted(component_sizes, key=lambda x: x[0])  # sort by vertex count
            smallest_v, smallest_f = sorted_components[0]
            largest_v, largest_f = sorted_components[-1]
        else:
            smallest_v = smallest_f = largest_v = largest_f = 0

        # --- Geometry ---
        volume = float(mesh.volume) if mesh.is_volume else 0.0
        area = float(mesh.area)

        return {
            "filename": os.path.basename(file_path),
            "num_vertices": num_vertices,
            "num_faces": num_faces,
            "num_internal_edges": num_internal_edges,
            "num_boundary_edges": num_boundary_edges,
            "min_connectivity": min_conn,
            "max_connectivity": max_conn,
            "avg_connectivity": avg_conn,
            "num_components": num_components,
            "smallest_component_vertices": smallest_v,
            "smallest_component_faces": smallest_f,
            "largest_component_vertices": largest_v,
            "largest_component_faces": largest_f,
            "mesh_volume": volume,
            "mesh_area": area,
            "file_path": file_path,
        }

    except Exception as e:
        print(f"[Error] {file_path}: {e}")
        return None


def main(folder_path, num_workers=None):
    # Query all .obj files
    obj_files = glob.glob(os.path.join(folder_path, "*.obj"))
    if not obj_files:
        print("No .obj files found.")
        return None

    # Parallel processing
    with mp.Pool(processes=num_workers or mp.cpu_count()) as pool:
        results = pool.map(analyze_mesh, obj_files)

    # Filter out None results
    results = [r for r in results if r is not None]

    # Create Polars DataFrame
    df = pl.DataFrame(results)
    return df


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", required=True, type=str, help="folder_path")
    parser.add_argument("--output_path", required=True, type=str, help="output_path")
    parser.add_argument("--jobs", default=4, help="# Jobs")
    
    args = parser.parse_args()

    if not os.path.exists(args.folder_path):
        raise ValueError(f"{args.folder_path} does not exist")
    
    output_dir = os.path.dirname(args.output_path)
    os.makedirs(output_dir, exist_ok=True)

    df = main(folder_path=args.folder_path, num_workers=args.jobs)

    if df is not None:
        # print(df)
        df.write_csv(args.output_path)
