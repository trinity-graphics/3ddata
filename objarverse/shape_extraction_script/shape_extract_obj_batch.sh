NUM_PARALLEL=${1:-4}

INPUT_DIR="/mnt/raw/objarverse_raw"
OUTPUT_DIR="/mnt/shape/objarverse_shape"

cd ..

echo "Running shape_extract.py with ${NUM_PARALLEL} parallel jobs..."

seq 0 810 | xargs -n 1 -P "${NUM_PARALLEL}" -I {} \
python3 shape_extract.py \
    --input_dir "${INPUT_DIR}/obj/github/chunk_{}" \
    --output_dir "${OUTPUT_DIR}/obj/github/chunk_{}" \
    --file_ext obj
echo "All chunks processed."