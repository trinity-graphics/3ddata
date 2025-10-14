cd ..

for chunk in {40..47}
do
    python3 download.py --split_dỉr /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype blend --source github --chunk $chunk
done
