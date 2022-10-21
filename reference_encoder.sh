#!/bin/bash
#Source: https://gist.github.com/mattst/9ffee93f5053ba59275af800f0dbd654

infile="sample_1280x720_surfing_with_audio.mkv"
datafile="TestClipTwoMinData.csv"

crfs=("18" "19" "20" "21" "22" "23" "24" "25" "26" "27")
presets=("ultrafast" "superfast" "veryfast" "faster" "fast" "medium" "slow" "slower" "veryslow")

echo 'CRF,Preset,Time (Secs),Size (MB)' >> "$datafile"

for crf in "${crfs[@]}"; do
    for preset in "${presets[@]}"; do
        outfile=Out_CRF_"$crf"_Preset_"$preset".mp4
        time_start=$(date +%s.%N)
        ffmpeg -i "$infile" -c:a copy -c:v libx264 -crf "$crf" -preset "$preset" "$outfile"
        time_end=$(date +%s.%N)
        # Dividing by 1 forces the scale to be used.
        time=$(echo "scale = 2; ($time_end - $time_start)/1" | bc)
        size_bytes=$(ls -l "$outfile" | awk '{ print $5 }')
        size_mb=$(echo "scale = 2; $size_bytes / 1000000" | bc)
        echo $crf,$preset,$time,$size_mb >> "$datafile"
    done
done
