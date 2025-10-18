#!/usr/bin/env bash

# === Amazon Berkeley Objects Dataset Downloader ===
# This script checks for file existence, downloads, and extracts if compressed.
# Usage: ./abo_downloader.sh

set -e  # exit on any error

# List of URLs to download
urls=(
  "https://amazon-berkeley-objects.s3.amazonaws.com/LICENSE-CC-BY-4.0.txt"
  "https://amazon-berkeley-objects.s3.amazonaws.com/README.md"
  "https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-listings.tar"
  "https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-images-original.tar"
  "https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-images-small.tar"
  "https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-spins.tar"
  "https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-3dmodels.tar"
  "https://amazon-berkeley-objects.s3.amazonaws.com/benchmarks/abo-mvr.csv.xz"
  "https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-benchmark-material.tar"
  "https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-part-labels.tar"
)

# Directory to store downloads
cd /mnt/data
download_dir="abo"
mkdir -p "$download_dir"

# Function: check if URL exists (HTTP 200)
check_exists() {
    local url="$1"
    if curl --head --silent --fail "$url" > /dev/null; then
        echo "[✔] Exists: $url"
        return 0
    else
        echo "[✖] Not found: $url"
        return 1
    fi
}

# Function: download a file
download_file() {
    local url="$1"
    local output="$download_dir/$(basename "$url")"
    if [[ -f "$output" ]]; then
        echo "[→] Skipping (already downloaded): $output"
        return
    fi
    echo "[↓] Downloading: $url"
    curl -L -o "$output" "$url"
}

# Function: extract if compressed
extract_file() {
    local file="$1"
    case "$file" in
        *.tar) 
            echo "[📦] Extracting tar: $file"
            tar -xf "$file" -C "$download_dir"
            ;;
        *.tar.gz|*.tgz) 
            echo "[📦] Extracting tar.gz: $file"
            tar -xzf "$file" -C "$download_dir"
            ;;
        *.xz) 
            echo "[📦] Extracting xz: $file"
            unxz -k "$file"
            ;;
        *)
            echo "[ℹ] Not compressed: $file"
            ;;
    esac
}

# Main loop
for url in "${urls[@]}"; do
    if check_exists "$url"; then
        download_file "$url"
        file_path="$download_dir/$(basename "$url")"
        extract_file "$file_path"
    fi
done

echo "✅ All available files processed and extracted."
