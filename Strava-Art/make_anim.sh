#!/usr/bin/env bash
# Build the transparent "runs appearing" animation in three formats.
# Usage: ./make_anim.sh [WIDTH HEIGHT]   (default 1080 1920)
set -euo pipefail
cd "$(dirname "$0")"
W=${1:-1080}; H=${2:-1920}
python3 animate.py "$W" "$H"
node animate.js "out/anim/spec_${W}x${H}.json"
FR="out/anim/frames_${W}x${H}/f%04d.png"
FPS=$(python3 -c "import json;print(json.load(open('out/anim/spec_${W}x${H}.json'))['fps'])")
OUTB="out/anim/runs_${W}x${H}"

# GIF: 1-bit transparency, so edges are slightly hard.
ffmpeg -y -loglevel error -framerate "$FPS" -i "$FR" -filter_complex \
  "split[a][b];[a]palettegen=reserve_transparent=1:max_colors=32[p];[b][p]paletteuse=alpha_threshold=100" \
  "$OUTB.gif"
# WebM VP9 with alpha: smooth edges, small file.
ffmpeg -y -loglevel error -framerate "$FPS" -i "$FR" -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 2M -auto-alt-ref 0 "$OUTB.webm"
# Small GIF (720 wide, 12 fps, 16 colours) - easy to download/share.
ffmpeg -y -loglevel error -framerate "$FPS" -i "$FR" -filter_complex \
  "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=reserve_transparent=1:max_colors=16:stats_mode=diff[p];[b][p]paletteuse=alpha_threshold=100:dither=none:diff_mode=rectangle" \
  "${OUTB}_small.gif"
# MP4 (H.264, black background, no transparency) - plays everywhere incl. WhatsApp.
ffmpeg -y -loglevel error -f lavfi -i "color=c=black:s=${W}x${H}:r=${FPS}" -framerate "$FPS" -i "$FR" \
  -filter_complex "[0][1]overlay=shortest=1,format=yuv420p" -c:v libx264 -crf 22 -preset slow -movflags +faststart "$OUTB.mp4"
ls -lh "$OUTB".* "${OUTB}_small.gif"
