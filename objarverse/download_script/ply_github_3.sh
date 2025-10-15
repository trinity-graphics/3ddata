cd ..

for chunk in {81..107}
do
    python3 download.py --split_dir /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype ply --source github --chunk $chunk
done
