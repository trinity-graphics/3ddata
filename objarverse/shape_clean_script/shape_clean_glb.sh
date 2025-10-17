INPUT_DIR="/mnt/shape/objarverse_shape"
OUTPUT_DIR="/mnt/clean/objarverse_clean"

cd ..

for chunk_index in {0..492}
do 
    python3 shape_clean.py \
        --input_dir "${INPUT_DIR}/glb/github/chunk_${chunk_index}" \
        --output_dir "${OUTPUT_DIR}/glb/github/chunk_${chunk_index}"
done