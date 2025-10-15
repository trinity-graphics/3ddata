SAVEDIR=${1:-}

if [ -z "$SAVEDIR" ]; then
    echo "Error: SAVEDIR argument not provided."
    echo "Usage: $0 SAVEDIR"
    exit 1
fi

chunks=2159
groups=16
chunks_per_group=$(( (chunks + groups - 1) / groups ))  # Ceiling division

start=0
for group in $(seq 0 $((groups-1))); do
    script="stl_github_${group}.sh"
    end=$(( start + chunks_per_group - 1 ))
    if [ $end -ge $((chunks-1)) ]; then
        end=$((chunks-1))
    fi

    echo "cd .." > $script
    echo "" >> $script
    echo "for chunk in {$start..$end}" >> $script
    echo "do" >> $script
    echo "    python3 download.py --split_dir /mnt/data/objarverse_df_splits --savedir $SAVEDIR --filetype stl --source github --chunk \$chunk" >> $script
    echo "done" >> $script

    start=$((end+1))
    if [ $start -ge $chunks ]; then
        break
    fi
done