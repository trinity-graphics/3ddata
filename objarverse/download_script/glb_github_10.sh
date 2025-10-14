cd ..

for chunk in {310..340}
do
    python3 download.py --split_dỉr /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype glb --source github --chunk $chunk
done
