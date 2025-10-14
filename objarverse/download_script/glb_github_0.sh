cd ..

for chunk in {0..30}
do
    python3 download.py --split_dỉr /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype glb --source github --chunk $chunk
done
