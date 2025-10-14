cd ..

for chunk in {32..35}
do
    python3 download.py --split_dỉr /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype dae --source github --chunk $chunk
done
