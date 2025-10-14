cd ..

for chunk in {112..119}
do
    python3 download.py --split_dỉr /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype blend --source github --chunk $chunk
done
