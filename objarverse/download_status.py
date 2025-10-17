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


def check_file_status(file_path):
    """Check content of one file and return a status key."""
    try:
        with open(file_path, 'r', errors='ignore') as file:
            content = file.read()
            if '404' in content:
                return '404'
            elif 'Access has been restricted' in content:
                return 'limit'
            else:
                return 'success'
    except Exception:
        # Treat unreadable or binary files as 'success'
        return 'success'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process 3D files by filetype.")
    parser.add_argument("--download_dir", type=str, required=True, help="Download Directory")
    parser.add_argument("--status_dir", type=str, required=True, help="Status Directory")
    parser.add_argument("--jobs", type=int, required=True, help="# Jobs")
    parser.add_argument("--format", type=str, default=None, help=f"Format (can be one of {FORMATS})")

    args = parser.parse_args()
    os.makedirs(args.status_dir, exist_ok=True)

    if args.format is not None:
        if args.format not in FORMATS:
            raise ValueError(f"args.format: {args.format} must be one of {FORMATS}")

    formats = [args.format] if args.format else FORMATS

    for fm in formats:
        fm_dir = os.path.join(args.download_dir, fm)
        if not os.path.exists(fm_dir):
            continue

        for src in SOURCES:
            src_dir = os.path.join(fm_dir, src)
            if not os.path.exists(src_dir):
                continue

            print(f"\n🔍 Checking download status for format '{fm}', source: '{src}'")

            file_paths = glob(os.path.join(src_dir, '*', f'*.{fm}'))
            if not file_paths:
                print(f"⚠️ No files found for {fm}/{src}")
                continue

            log = {'success': 0, '404': 0, 'limit': 0, 'total': len(file_paths)}

            # Use multiprocessing
            num_workers = max(1, min(cpu_count() - 1, args.jobs))
            with Pool(num_workers) as pool:
                for result in tqdm(pool.imap_unordered(check_file_status, file_paths), total=len(file_paths), desc=f"{fm}/{src}", ncols=100):
                    log[result] += 1

            # Save results
            log_path = os.path.join(args.status_dir, f'status_{fm}_{src}.json')
            with open(log_path, 'w') as file:
                json.dump(log, file, indent=4)

            print(f"✅ Saved log to: {log_path}")
            print(f"   Summary: {log}")
