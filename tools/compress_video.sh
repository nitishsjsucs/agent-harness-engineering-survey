#!/usr/bin/env bash
# Shrink a screen recording of the talk so it fits in the GitHub repo.
#
# GitHub rejects files over 100 MB and warns above 50 MB. A slide talk is mostly
# static frames, so 1280x720 H.264 at CRF 30 keeps text crisp and lands well
# under that limit for a 15-20 minute recording.
#
# Usage:  bash tools/compress_video.sh path/to/recording.mp4
# Output: video/short_story_presentation.mp4
set -euo pipefail

in="${1:?usage: compress_video.sh <recording.mp4|mov>}"
out="$(cd "$(dirname "$0")/.." && pwd)/video/short_story_presentation.mp4"

ffmpeg -y -i "$in" \
  -vf "scale=1280:-2:flags=lanczos,fps=15" \
  -c:v libx264 -preset slow -crf 30 -tune stillimage -pix_fmt yuv420p \
  -c:a aac -b:a 96k -ac 1 \
  -movflags +faststart \
  "$out"

size_mb=$(du -m "$out" | cut -f1)
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out" | cut -d. -f1)
echo "wrote $out  (${size_mb} MB, $((dur / 60))m $((dur % 60))s)"
if [ "$size_mb" -ge 95 ]; then
  echo "Still over 95 MB: re-run with a higher CRF (edit -crf 30 -> 33) or use Git LFS:"
  echo "  git lfs install && git lfs track 'video/*.mp4' && git add .gitattributes"
fi
if [ "$dur" -lt 900 ]; then
  echo "WARNING: the rubric asks for a video of at least 15 minutes; this one is shorter."
fi
