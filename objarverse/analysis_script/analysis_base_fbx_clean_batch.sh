NUM_PARALLEL=${1:-4}

INPUT_DIR="/mnt/clean/objarverse_clean"
OUTPUT_DIR="/mnt/clean/objarverse_analysis"

cd ../analysis

seq 0 754 | xargs -n 1 -P "${NUM_PARALLEL}" -I {} \
python3 base.py \
    --folder_path "${INPUT_DIR}/fbx/github/chunk_{}" \
    --output_path "${OUTPUT_DIR}/fbx/github/chunk_{}.csv"

echo "All chunks processed."