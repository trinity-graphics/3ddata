cd ..

for chunk in {144..191}
do
    python3 download.py --split_dỉr /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype fbx --source github --chunk $chunk
done
