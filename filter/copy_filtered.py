from tqdm import tqdm

from multiprocessing import Pool, cpu_count

import os
import argparse
import polars as pl
import shutil


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Filter 3D mesh dataset based on predefined criteria.")
    parser.add_argument("--input_path", type=str, help="Path to the input cvs containing mesh metadata.")
    parser.add_argument("--dst_dir", type=str, help="Path to the destination directory.")
    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        raise ValueError(f'{args.input_path} does not exists')
    
    filename = os.path.basename(args.input_path)
    if 'csv' not in filename:
        raise ValueError(f'{args.input_path} is not a CSV file')

    save_dir = os.path.join(args.dst_dir, f"{filename.replace('csv', '')}")
    os.makedirs(save_dir, exist_ok=True)

    df = pl.read_csv(args.input_path)

    file_paths = df['file_path'].to_list()

    def copy_file(src_path):
        base = os.path.basename(src_path)
        dst_path = os.path.join(save_dir, base)
        try:
            if not os.path.exists(src_path):
                return ('error', src_path, 'source not found')

            # If destination exists, append a numeric suffix before the extension
            if os.path.exists(dst_path):
                name, ext = os.path.splitext(base)
                i = 1
                while True:
                    candidate = os.path.join(save_dir, f"{name}_{i}{ext}")
                    if not os.path.exists(candidate):
                        dst_path = candidate
                        break
                    i += 1

            shutil.copy2(src_path, dst_path)
            return ('copied', src_path, dst_path)
        except Exception as e:
            return ('error', src_path, str(e))

    with Pool(cpu_count()) as pool:
        results = list(tqdm(pool.imap_unordered(copy_file, file_paths), total=len(file_paths), desc="Copying files"))

    # summarize results
    copied = [r for r in results if isinstance(r, tuple) and r[0] == 'copied']
    errors = [r for r in results if isinstance(r, tuple) and r[0] == 'error']
    print(f"Copied: {len(copied)} files")
    if errors:
        print("Some errors occurred during copying:")
        for err in errors:
            print(err)