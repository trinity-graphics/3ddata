cd ..

for chunk in {40..43}
do
    python3 download.py --split_dir /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype dae --source github --chunk $chunk
done
