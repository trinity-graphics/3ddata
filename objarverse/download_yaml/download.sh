files=(
  "download_abc.yaml"
  "download_blend.yaml"
  "download_dae.yaml"
  "download_fbx.yaml"
  "download_glb.yaml"
  "download_gltf.yaml"
  "download_obj.yaml"
  "download_ply.yaml"
  "download_stl.yaml"
  "download_usdz.yaml"
)

# Loop through and apply each file
for file in "${files[@]}"; do
  echo "Applying $file..."
  kubectl apply -f "$file"
done