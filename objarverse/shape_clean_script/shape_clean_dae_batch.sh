#!/bin/bash

# Usage: bash myfile.sh <num_parallel_jobs>
# Example: bash myfile.sh 8

# Default parallel jobs to 4 if not provided
NUM_PARALLEL=${1:-4}

INPUT_DIR="/mnt/shape/objarverse_shape"
OUTPUT_DIR="/mnt/clean/objarverse_clean"

cd ..

echo "Running shape_clean.py with ${NUM_PARALLEL} parallel jobs..."

seq 0 61 | xargs -n 1 -P "${NUM_PARALLEL}" -I {} \
python3 shape_clean.py \
    --input_dir "${INPUT_DIR}/dae/github/chunk_{}" \
    --output_dir "${OUTPUT_DIR}/dae/github/chunk_{}"

echo "All chunks processed."
