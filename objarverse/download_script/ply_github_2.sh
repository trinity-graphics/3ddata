cd ..

for chunk in {54..80}
do
    python3 download.py --split_dir /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype ply --source github --chunk $chunk
done
