files=(
  "zip_objarverse_abc_clean.yaml"
  "zip_objarverse_dae_clean.yaml"
  "zip_objarverse_fbx_clean.yaml"
  "zip_objarverse_glb_clean.yaml"
  "zip_objarverse_gltf_clean.yaml"
  "zip_objarverse_obj_clean.yaml"
)

# Loop through and apply each file
for file in "${files[@]}"; do
  echo "Applying $file..."
  kubectl apply -f "$file"
done