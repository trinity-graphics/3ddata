cd ..

for chunk in {0..0}
do
    python3 download.py --split_dỉr /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype abc --source github --chunk $chunk
done
