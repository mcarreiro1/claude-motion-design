#!/usr/bin/env bash
# Chop gameplay videos into Instagram Reels clips (1080x1920, 9:16, H.264/AAC).
# Usage: scripts/make_reels.sh [input_dir] [output_dir] [clip_seconds]
# Defaults: ASSETS/source -> ASSETS, 60-second clips.
# Horizontal sources are center-cropped to 9:16; vertical sources are scaled.
# The trailing partial clip is dropped if shorter than half the clip length.
set -euo pipefail
IN="${1:-ASSETS/source}"; OUT="${2:-ASSETS}"; LEN="${3:-60}"
mkdir -p "$OUT"
VF="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
shopt -s nullglob nocaseglob
for src in "$IN"/*.{mp4,mkv,webm,mov}; do
  base="$(basename "${src%.*}" | tr -c 'A-Za-z0-9_-' '_' | sed 's/_*$//')"
  dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src")"
  n="$(awk -v d="$dur" -v l="$LEN" 'BEGIN{print int(d/l) + ((d - int(d/l)*l) >= l/2)}')"
  for ((i=0; i<n; i++)); do
    out="$OUT/${base}_reel$(printf '%03d' $((i+1))).mp4"
    [ -s "$out" ] && continue
    ffmpeg -nostdin -v error -y -ss $((i*LEN)) -t "$LEN" -i "$src" \
      -vf "$VF" -c:v libx264 -preset medium -crf 27 -pix_fmt yuv420p \
      -c:a aac -b:a 128k -movflags +faststart "$out"
    echo "wrote $out"
  done
done
