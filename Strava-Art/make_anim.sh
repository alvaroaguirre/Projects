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
# ProRes 4444 with alpha: best for Premiere / Final Cut / DaVinci.
ffmpeg -y -loglevel error -framerate "$FPS" -i "$FR" -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le "$OUTB.mov"
ls -lh "$OUTB".*
