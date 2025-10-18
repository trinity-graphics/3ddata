import os
import json
import argparse
from glob import glob
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

FORMATS = [
    'abc', 'blend', 'dae', 'fbx', 'glb', 'gltf',
    'obj', 'ply', 'stl', 'usdz'
]

SOURCES = ['github']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process 3D files by filetype.")
    parser.add_argument("--cleaning_dir", type=str, required=True, help="Cleaning Directory")
    parser.add_argument("--status_path", type=str, required=True, help="Status JSON path")
    parser.add_argument("--format", type=str, default=None, help=f"Format (can be one of {FORMATS})")

    args = parser.parse_args()

    if args.format is not None:
        if args.format not in FORMATS:
            raise ValueError(f"args.format: {args.format} must be one of {FORMATS}")

    formats = [args.format] if args.format else FORMATS

    log = {}

    for fm in formats:
        fm_dir = os.path.join(args.cleaning_dir, fm)
        if not os.path.exists(fm_dir):
            continue

        for src in SOURCES:
            src_dir = os.path.join(fm_dir, src)
            if not os.path.exists(src_dir):
                continue

            print(f"\n🔍 Checking cleaning status for format '{fm}', source: '{src}'")

            file_paths = glob(os.path.join(src_dir, '*', '*.obj'))
            if not file_paths:
                print(f"⚠️ No obj files found for {fm}/{src}")
                continue

            log[f"{fm}/{src}"] = len(file_paths)

            # Save results
            with open(args.status_path, 'w') as file:
                json.dump(log, file, indent=4)

            print(f"✅ Saved log to: {args.status_path}")
            print(f"   Summary: {log}")
