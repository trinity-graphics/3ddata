cd ..

for chunk in {0..2}
do
    python3 download.py --split_dỉr /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype usdz --source github --chunk $chunk
done
