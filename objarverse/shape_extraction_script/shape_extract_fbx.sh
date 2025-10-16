INPUT_DIR="/mnt/raw/objarverse_raw"
OUTPUT_DIR="/mnt/shape/objarverse_shape"

cd ..

for chunk_index in {0..754}
do 
    python3 shape_extract.py \
        --input_dir "${INPUT_DIR}/fbx/github/chunk_${chunk_index}" \
        --output_dir "${OUTPUT_DIR}/fbx/github/chunk_${chunk_index}" \
        --file_ext fbx
done