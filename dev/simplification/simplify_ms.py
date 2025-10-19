import pymeshlab as ml

def simplify(input_path, output_path, ratio):
    ms = ml.MeshSet()
    ms.load_new_mesh(input_path)
    initial_faces = ms.current_mesh().face_number()
    target_faces = max(1, int(initial_faces * ratio))
    # Quadratic Edge Collapse Decimation
    ms.apply_filter('meshing_decimation_quadric_edge_collapse',
        targetfacenum=target_faces,
        preservenormal=True,
        # preservetopology=True,
        # preserveboundary=True,
        # planarquadric=False,
        # qualitythr=1.0
    )
    print("Meshes in set:", ms.mesh_number())
    for i in range(ms.mesh_number()):
        m = ms.mesh(i)
        print(f"Mesh {i}: {m.face_number()} faces")
    
    ms.save_current_mesh(
        output_path,
        save_vertex_color=False,
        save_vertex_normal=False,
        save_face_color=False,
        save_wedge_texcoord=False,
        save_wedge_normal=False,
        # save_polygonal=False
        )
    print(f"Saved simplified mesh to {output_path}. Faces: {target_faces} (from {initial_faces})")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simplify 3D mesh using PyMeshLab.")
    parser.add_argument("--input", help="Input mesh file path")
    parser.add_argument("--output", help="Output simplified mesh file path")
    parser.add_argument("--ratio", type=float, default=0.5, help="Simplification ratio (0 < ratio <= 1)")
    args = parser.parse_args()

    if not (0 < args.ratio <= 1):
        raise ValueError("Ratio must be between 0 and 1.")

    simplify(args.input, args.output, args.ratio)