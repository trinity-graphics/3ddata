cd ..

for chunk in {56..59}
do
    python3 download.py --split_dỉr /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype gltf --source github --chunk $chunk
done
