NUM_PARALLEL=${1:-16}

INPUT_DIR="/mnt/raw/shapenet/shapenet"
OUTPUT_DIR="/mnt/shape/shapenet_shape"

cd ../objarverse

echo "Running shape_extract.py with ${NUM_PARALLEL} parallel jobs..."

python3 shape_extract.py \
    --input_dir "${INPUT_DIR}" \
    --output_dir "${OUTPUT_DIR}" \
    --file_ext obj \
    --jobs ${NUM_PARALLEL}