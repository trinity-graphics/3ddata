INPUT_DIR="/mnt/clean/shapenet_clean"
OUTPUT_DIR="/mnt/clean/shapenet_analysis"

cd ../objarverse/analysis

python3 base.py \
    --folder_path "${INPUT_DIR}" \
    --output_path "${OUTPUT_DIR}/shapenet.csv"
