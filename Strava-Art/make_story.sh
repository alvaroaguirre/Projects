#!/usr/bin/env bash
# Instagram Story MP4: 1080x1920, 30 fps, H.264 High, yuv420p, silent AAC track,
# routes kept out of the story header (top 250 px) and reply bar (bottom 340 px).
set -euo pipefail
cd "$(dirname "$0")"
export FPS=30 SAFE_TOP=250 SAFE_BOTTOM=340 TAG=story
python3 animate.py 1080 1920
node animate.js out/anim/spec_story.json
ffmpeg -y -loglevel error -framerate 30 -i out/anim/frames_story/f%04d.png \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -filter_complex "color=c=black:s=1080x1920:r=30[bg];[bg][0]overlay=shortest=1,format=yuv420p[v]" \
  -map "[v]" -map 1:a -shortest \
  -c:v libx264 -profile:v high -level 4.1 -preset slow -b:v 8M -maxrate 10M -bufsize 16M -r 30 -g 60 \
  -c:a aac -b:a 128k -movflags +faststart out/anim/runs_instagram_story.mp4
ls -lh out/anim/runs_instagram_story.mp4
