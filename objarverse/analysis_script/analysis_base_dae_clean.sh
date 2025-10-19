INPUT_DIR="/mnt/clean/objarverse_clean"
OUTPUT_DIR="/mnt/clean/objarverse_analysis"

cd ../analysis

for chunk_index in {0..61}
do 
    python3 base.py \
        --folder_path "${INPUT_DIR}/dae/github/chunk_${chunk_index}" \
        --output_path "${OUTPUT_DIR}/dae/github/chunk_${chunk_index}.csv"
done