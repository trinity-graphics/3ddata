cd ..

for chunk in {1620..1754}
do
    python3 download.py --split_dir /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype stl --source github --chunk $chunk
done
