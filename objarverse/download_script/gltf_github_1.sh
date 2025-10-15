cd ..

for chunk in {4..7}
do
    python3 download.py --split_dir /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype gltf --source github --chunk $chunk
done
