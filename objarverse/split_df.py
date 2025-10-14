import objaverse.xl as oxl
import json
import pandas as pd
import polars as pl
import os
import argparse

from tqdm import tqdm

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--download_dir", default="~/.objaverse", help="download_dir")
    parser.add_argument("--save_dir", required=True, help="save_dir")

    args = parser.parse_args()

    # Download the annotations
    annotations = oxl.get_annotations(download_dir=args.download_dir)

    # Convert to Polars DataFrame
    pl_df = pl.from_pandas(annotations)

    # Get unique file types
    file_types = annotations["fileType"].unique()

    # Get unique file types
    file_types = pl_df["fileType"].unique().to_list()

    # For each file type, filter and split into chunks
    for file_type in tqdm(file_types):
        filtered_df = pl_df.filter(pl.col("fileType") == file_type)
        out_dir = os.path.join(f"{args.save_dir}", f"{file_type}")
        os.makedirs(out_dir, exist_ok=True)

        n_rows = filtered_df.height
        for i, chunk_start in enumerate(range(0, n_rows, 2000)):
            chunk_df = filtered_df.slice(chunk_start, 2000)
            chunk_path = os.path.join(out_dir, f"{i}.csv")
            chunk_df.write_csv(chunk_path)