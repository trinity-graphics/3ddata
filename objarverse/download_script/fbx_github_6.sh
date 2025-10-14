cd ..

for chunk in {288..335}
do
    python3 download.py --split_dỉr /mnt/data/objarverse_df_splits --savedir /mnt/data --filetype fbx --source github --chunk $chunk
done
