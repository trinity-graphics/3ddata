INPUT_DIR="/mnt/clean/mesh_500_clean"
OUTPUT_DIR="/mnt/clean/mesh_500_analysis"

cd ../objarverse/analysis

python3 base.py \
    --folder_path "${INPUT_DIR}/train" \
    --output_path "${OUTPUT_DIR}/train.csv"

python3 base.py \
    --folder_path "${INPUT_DIR}/val" \
    --output_path "${OUTPUT_DIR}/val.csv"
