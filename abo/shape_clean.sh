NUM_PARALLEL=${1:-16}

INPUT_DIR="/mnt/shape/shapenet_shape"
OUTPUT_DIR="/mnt/clean/shapenet_clean"

cd ../objarverse

echo "Running shape_extract.py with ${NUM_PARALLEL} parallel jobs..."

python3 shape_clean.py \
    --input_dir "${INPUT_DIR}" \
    --output_dir "${OUTPUT_DIR}"