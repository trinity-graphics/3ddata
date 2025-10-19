NUM_PARALLEL=${1:-4}

INPUT_DIR="/mnt/shape/objarverse_shape"
OUTPUT_DIR="/mnt/clean/objarverse_clean"

cd ..

echo "Running shape_clean.py with ${NUM_PARALLEL} parallel jobs..."

seq 0 754 | xargs -n 1 -P "${NUM_PARALLEL}" -I {} \
python3 shape_clean.py \
    --input_dir "${INPUT_DIR}/fbx/github/chunk_{}" \
    --output_dir "${OUTPUT_DIR}/fbx/github/chunk_{}"

echo "All chunks processed."
