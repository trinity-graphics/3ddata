from glob import glob
from tqdm import tqdm

import os
import argparse
import polars as pl

import filter_book


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter 3D mesh dataset based on predefined criteria.")
    parser.add_argument("--input_dir", type=str, help="Path to the input directory containing mesh data.")
    parser.add_argument("--output_dir", type=str, help="Path to the output directory to save filtered data.")
    parser.add_argument("--filter_name", type=str, default="miv512_mia0d001_mac8_mic2_com10",
                        help="Name of the filter book to use for filtering.")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    log_path = os.path.join(args.output_dir, f'{args.filter_name}_log.txt')

    # Query analysis folder
    mesh_500_analysis_dir = f'{args.input_dir}/mesh_500_analysis'
    objarverse_analysis_dir = f'{args.input_dir}/objarverse_analysis'
    shapenet_analysis_dir = f'{args.input_dir}/shapenet_analysis'

    mesh_500_csvs = glob(os.path.join(mesh_500_analysis_dir, '*.csv'))
    objarverse_csvs = glob(os.path.join(objarverse_analysis_dir, '*/*/*.csv'))
    shapenet_csvs = glob(os.path.join(shapenet_analysis_dir, '*.csv'))

    csvs = mesh_500_csvs + objarverse_csvs + shapenet_csvs

    if len(csvs) == 0:
        raise ValueError("No CSV files found in the specified input directory.")
    
    if len(mesh_500_csvs) == 0:
        raise Warning("No Mesh 500 CSV files found in the specified input directory.")
    
    if len(objarverse_csvs) == 0:
        raise Warning("No Objaverse CSV files found in the specified input directory.")

    if len(shapenet_csvs) == 0:
        raise Warning("No Shapenet CSV files found in the specified input directory.")

    # Apply filters from the filter book
    filters_to_apply = filter_book.__dict__.get(args.filter_name, None)
    if filters_to_apply is None:
        raise ValueError(f"Filter book '{args.filter_name}' not found.")

    dataframes = []
    for csv_file in tqdm(csvs):
        df = pl.read_csv(csv_file)
        dataframes.append(df)
    merged_df: pl.DataFrame = pl.concat(dataframes)

    with open(log_path, 'w') as log_file:
        log_file.write(f"Filter log for: {args.filter_name}\n")
        log_file.write(f"Initial DataFrame shape: {merged_df.shape}\n\n")
        for i, filter_entry in enumerate(filters_to_apply):
            filter_func = filter_entry['filter']
            filter_params = filter_entry['params']
            before_shape = merged_df.shape
            log_file.write(f"Filter {i+1}: {filter_func.__name__}\n")
            log_file.write(f"  Params: {filter_params}\n")
            log_file.write(f"  Shape before: {before_shape}\n")
            filtered_df = filter_func(merged_df, **filter_params)
            if filtered_df is not None:
                merged_df = filtered_df
                after_shape = merged_df.shape
                log_file.write(f"  Shape after: {after_shape}\n\n")
            else:
                log_file.write(f"  No filtering applied (None returned)\n\n")
        log_file.write(f"Final DataFrame shape: {merged_df.shape}\n")
    # Save the filtered DataFrame to CSV
    output_path = os.path.join(args.output_dir, f'filtered_{args.filter_name}.csv')
    merged_df.write_csv(output_path)