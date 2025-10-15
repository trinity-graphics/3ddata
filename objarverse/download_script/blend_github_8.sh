cd ..

for chunk in {64..71}
do
    python3 download.py --split_dir /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype blend --source github --chunk $chunk
done
