SAVEDIR=${1:-}

if [ -z "$SAVEDIR" ]; then
    echo "Error: SAVEDIR argument not provided."
    echo "Usage: $0 SAVEDIR"
    exit 1
fi

bash generate_scripts_abc_github.sh $SAVEDIR
bash generate_scripts_obj_github.sh $SAVEDIR
bash generate_scripts_blend_github.sh $SAVEDIR
bash generate_scripts_dae_github.sh $SAVEDIR
bash generate_scripts_fbx_github.sh $SAVEDIR
bash generate_scripts_glb_github.sh $SAVEDIR
bash generate_scripts_gltf_github.sh $SAVEDIR
bash generate_scripts_ply_github.sh $SAVEDIR
bash generate_scripts_stl_github.sh $SAVEDIR
bash generate_scripts_usdz_github.sh $SAVEDIR