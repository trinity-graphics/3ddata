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

    save_dir = os.path.join(args.dst_dir, f'{os.path.basename(args.input_path)}')
    os.makedirs(save_dir, exist_ok=True)

    df = pl.read_csv(args.input_path)

    

    file_paths = df.get_column('file_path').to_arrow().to_numpy()

    def copy_file(src_path):
        dst_path = os.path.join(save_dir, os.path.basename(src_path))
        try:
            shutil.copy2(src_path, dst_path)
            return True
        except Exception as e:
            return f"Error copying {src_path}: {e}"

    with Pool(cpu_count()) as pool:
        results = list(tqdm(pool.imap_unordered(copy_file, file_paths), total=len(file_paths), desc="Copying files"))

    errors = [r for r in results if r is not True]
    if errors:
        print("Some errors occurred during copying:")
        for err in errors:
            print(err)