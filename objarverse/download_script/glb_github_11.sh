cd ..

for chunk in {341..371}
do
    python3 download.py --split_dir /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype glb --source github --chunk $chunk
done
