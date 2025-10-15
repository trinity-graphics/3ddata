cd ..

for chunk in {8..11}
do
    python3 download.py --split_dir /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype gltf --source github --chunk $chunk
done
