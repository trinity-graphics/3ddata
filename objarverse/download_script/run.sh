#!/bin/bash

# Usage: ./run.sh <prefix>
prefix="$1"

if [ -z "$prefix" ]; then
    echo "Usage: $0 <prefix>"
    exit 1
fi

# Gather all matching files
files=("${prefix}"_*.sh)

# Check if any files found
if [ ${#files[@]} -eq 0 ]; then
    echo "No files matching ${prefix}_*.sh found."
    exit 1
fi

# Run each file in a separate background process
for f in "${files[@]}"; do
    echo "Running $f ..."
    bash "$f" &
done

# Wait for all background jobs to finish
wait

echo "All scripts finished."