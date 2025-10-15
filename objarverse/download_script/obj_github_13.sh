cd ..

for chunk in {663..713}
do
    python3 download.py --split_dir /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype obj --source github --chunk $chunk
done
