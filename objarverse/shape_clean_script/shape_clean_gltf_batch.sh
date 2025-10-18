NUM_PARALLEL=${1:-4}

INPUT_DIR="/mnt/shape/objarverse_shape"
OUTPUT_DIR="/mnt/clean/objarverse_clean"

cd ..

echo "Running shape_clean.py with ${NUM_PARALLEL} parallel jobs..."

seq 0 63 | xargs -n 1 -P "${NUM_PARALLEL}" -I {} \
python3 shape_clean.py \
    --input_dir "${INPUT_DIR}/gltf/github/chunk_{}" \
    --output_dir "${OUTPUT_DIR}/gltf/github/chunk_{}"

echo "All chunks processed."
