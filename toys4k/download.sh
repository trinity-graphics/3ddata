#!/bin/bash
# =====================================================
# Download and extract Toys4K dataset ZIP files
# =====================================================

# Create a base directory for downloads
cd /mnt/data
BASE_DIR="toys4k"
mkdir -p "$BASE_DIR"
cd "$BASE_DIR" || exit

# List of files to download
declare -A FILES=(
  ["toys4k_blend_files.zip"]="https://www.dropbox.com/scl/fi/vc3u2ixkqhazsofy8bqq6/toys4k_blend_files.zip?rlkey=fxxvvjkvim3ba5lx53i70msl2&e=1"
  ["toys4k_obj_files.zip"]="https://www.dropbox.com/scl/fi/3ush4uwwt11gxp8gmkgqs/toys4k_obj_files.zip?rlkey=af73mx37c7ysf95ctc6rdc0fe&e=1"
  ["toys4k_point_clouds.zip"]="https://www.dropbox.com/scl/fi/n2weud7tda5061ln4kvh2/toys4k_point_clouds.zip?rlkey=s3ove8qawzhqravfzd1fy52h3&e=1"
  ["toys_blend_sample_renders.zip"]="https://www.dropbox.com/scl/fi/2yeds4oipozdghdiwyfqv/toys_blend_sample_renders.zip?rlkey=u1g6t9p4gppusbdrp1b7o2401&e=1"
  ["toys_obj_sample_renders.zip"]="https://www.dropbox.com/scl/fi/g3f3oz6ny8wfb4w37mokh/toys_obj_sample_renders.zip?rlkey=9a38iyhlifcnxatxnz1usez7u&e=1"
)

# Function to download and extract
download_and_extract() {
  local filename="$1"
  local url="$2"

  echo "--------------------------------------------------"
  echo "Downloading: $filename"
  echo "--------------------------------------------------"

  # Use curl or wget depending on what's available
  if command -v curl &> /dev/null; then
    curl -L -o "$filename" "$url"
  elif command -v wget &> /dev/null; then
    wget -O "$filename" "$url"
  else
    echo "Error: neither curl nor wget found."
    exit 1
  fi

  # Extract zip file
  echo "Extracting: $filename"
  unzip -o "$filename" -d "${filename%.zip}"
  echo "Cleaning up..."
  rm "$filename"
  echo "Done with $filename"
  echo
}

# Loop through all files
for file in "${!FILES[@]}"; do
  download_and_extract "$file" "${FILES[$file]}"
done

echo "✅ All downloads and extractions completed!"
