INPUT_DIR="/mnt/raw/objarverse_shape"
OUTPUT_DIR="/mnt/shape/objarverse_clean"

cd ..

for chunk_index in {0..810}
do 
    python3 shape_clean.py \
        --input_dir "${INPUT_DIR}/obj/github/chunk_${chunk_index}" \
        --output_dir "${OUTPUT_DIR}/obj/github/chunk_${chunk_index}" \
        --file_ext obj
done