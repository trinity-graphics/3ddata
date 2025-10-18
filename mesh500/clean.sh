INPUT_DIR="/mnt/raw/mesh_500/mesh_500/obj"
OUTPUT_DIR="/mnt/clean/mesh_500_clean"

cd ../objarverse

python3 shape_clean.py \
    --input_dir "${INPUT_DIR}/train" \
    --output_dir "${OUTPUT_DIR}/train"

python3 shape_clean.py \
    --input_dir "${INPUT_DIR}/val" \
    --output_dir "${OUTPUT_DIR}/val"