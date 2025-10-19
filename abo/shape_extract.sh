NUM_PARALLEL=${1:-16}

INPUT_DIR="/mnt/raw/abo/3dmodels/original/"
OUTPUT_DIR="/mnt/shape/abo/3dmodels/obj"

echo "Running shape_extract.py with ${NUM_PARALLEL} parallel jobs..."

CHUNKS=({0..9} {A..Z})

printf "%s\n" "${CHUNKS[@]}" | xargs -n 1 -P "${NUM_PARALLEL}" -I {} \
python3 shape_extract.py \
    --input_dir "${INPUT_DIR}/{}" \
    --output_dir "${OUTPUT_DIR}/{}"

echo "All chunks processed."