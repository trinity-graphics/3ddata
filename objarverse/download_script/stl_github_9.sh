cd ..

for chunk in {1215..1349}
do
    python3 download.py --split_dỉr /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype stl --source github --chunk $chunk
done
