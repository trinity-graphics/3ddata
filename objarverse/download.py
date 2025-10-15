import pandas as pd
import os
import argparse

from glob import glob
from tqdm import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process 3D files by filetype.")
    parser.add_argument("--split_dir", type=str, required=True, help="Directory to save processed files")
    parser.add_argument("--savedir", type=str, required=True, help="Directory to save processed files")
    parser.add_argument("--filetype", type=str, required=True, help="Filetype to process")
    parser.add_argument("--chunk", type=int, required=True, help="Chunk index to process (required)")
    parser.add_argument("--source", type=str, required=True, choices=['github', 'thingiverse', 'smithsonian', 'sketchfab'], help="Source of the data to process")
    args = parser.parse_args()

    filetype = args.filetype.lower()

    objarverse_folder = args.split_dir

    save_dir = os.path.join(args.savedir, 'objarverse_raw', filetype, args.source)
    os.makedirs(save_dir, exist_ok=True)

    chunk_files = glob(os.path.join(objarverse_folder, filetype, "*.csv"))
    number_of_chunks = len(chunk_files)
    print(f"Number of chunks for filetype '{filetype}': {number_of_chunks}")

    chunk_save_dir = os.path.join(save_dir, f"chunk_{args.chunk}")
    
    os.makedirs(chunk_save_dir, exist_ok=True)
    print(f"Chunk save directory created: {chunk_save_dir}")

    chunk_file_path = os.path.join(objarverse_folder, filetype, f"{args.chunk}.csv")
    chunk_df = pd.read_csv(chunk_file_path)
    if chunk_df.empty:
        print(f"Chunk {args.chunk} is empty, skipping...")
        exit(0)
    print(f"Processing chunk {args.chunk} with {len(chunk_df)} entries...")

    if args.source == 'github':
        pass
    else:
        raise ValueError(f"Unsupported source: {args.source}. Supported sources are: github, thingiverse, smithsonian, sketchfab.")

    urls = sorted(chunk_df[chunk_df['source'] == args.source]['fileIdentifier'].unique().tolist())

    logs = []
    log_file = os.path.join(chunk_save_dir, 'download_log.txt')

    for idx, url in enumerate(tqdm(urls, desc="Downloading files", unit="file")):

        filename = url.split("/")[-1]
        if '?' in filename:
            filename = filename.split('?')[0]

        save_path = os.path.join(chunk_save_dir, filename)

        if os.path.exists(save_path):
            continue

        if args.source == 'github':
            raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

            try:
                os.system(f'curl -s "{raw_url}" -o "{save_path}"')
            except Exception as e:
                logs.append(f"Error downloading {url}: {e}")
                continue
    
    # Save logs to file
    with open(log_file, 'w') as f:
        for log in logs:
            f.write(log + '\n')