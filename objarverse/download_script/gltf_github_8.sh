cd ..

for chunk in {32..35}
do
    python3 download.py --split_dir /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype gltf --source github --chunk $chunk
done
