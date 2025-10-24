NUM_PARALLEL=${1:-16}

INPUT_DIR="/mnt/shape/abo/3dmodels/obj"
OUTPUT_DIR="/mnt/clean/abo/3dmodels/obj"

echo "Running shape_clean.py with ${NUM_PARALLEL} parallel jobs..."

CHUNKS=({0..9} {A..Z})

printf "%s\n" "${CHUNKS[@]}" | xargs -n 1 -P "${NUM_PARALLEL}" -I {} \
python3 shape_clean.py \
    --input_dir "${INPUT_DIR}/{}" \
    --output_dir "${OUTPUT_DIR}/{}"

echo "All chunks processed."