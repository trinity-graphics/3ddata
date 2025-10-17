INPUT_DIR="/mnt/shape/objarverse_shape"
OUTPUT_DIR="/mnt/clean/objarverse_clean"

cd ..

for chunk_index in {0..810}
do 
    python3 shape_clean.py \
        --input_dir "${INPUT_DIR}/obj/github/chunk_${chunk_index}" \
        --output_dir "${OUTPUT_DIR}/obj/github/chunk_${chunk_index}"
done