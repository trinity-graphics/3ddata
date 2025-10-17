import argparse
import glob
import os
import trimesh
import multiprocessing as mp
import polars as pl
import numpy as np


def analyze_mesh(file_path):
    """Load a mesh and extract geometric + connectivity statistics."""
    try:
        mesh = trimesh.load(file_path, force='mesh')
        if not isinstance(mesh, trimesh.Trimesh):
            return None  # skip if not a mesh

        # Vertices and faces
        num_vertices = len(mesh.vertices)
        num_faces = len(mesh.faces)

        # Edges and connectivity
        edges = mesh.edges_sorted
        edges_unique, edges_counts = np.unique(edges, axis=0, return_counts=True)

        num_internal_edges = np.sum(edges_counts == 2)
        num_boundary_edges = np.sum(edges_counts == 1)

        # Vertex connectivity (number of edges incident to each vertex)
        vertex_connectivity = np.bincount(edges_unique.flatten(), minlength=num_vertices)
        min_conn = int(vertex_connectivity.min())
        max_conn = int(vertex_connectivity.max())
        avg_conn = float(vertex_connectivity.mean())

        return {
            "filename": os.path.basename(file_path),
            "num_vertices": num_vertices,
            "num_faces": num_faces,
            "num_internal_edges": num_internal_edges,
            "num_boundary_edges": num_boundary_edges,
            "min_connectivity": min_conn,
            "max_connectivity": max_conn,
            "avg_connectivity": avg_conn,
            "file_path": file_path,
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
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
    os.make_dirs(output_dir, exist_ok=True)

    df = main(folder_path=args.folder_path, num_workers=args.jobs)

    if df is not None:
        print(df)
        df.write_csv(args.output_path)
