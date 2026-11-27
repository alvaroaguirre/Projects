# Strava-Art

Route-art cards and a poster of every run in a marathon block, made from Strava data.

- `data/runs.json` – runs since 1 Jul 2026 (name, date, distance, pace, moving time, simplified route polyline)
- `render.py` – stdlib-only Python; writes `out/cards/*.svg` (1080×1080, one per run) and `out/poster.svg` / `out/poster.html`
- `to_png.js` – converts all SVGs to PNG with Playwright

```bash
python3 render.py            # add --gps-only to drop treadmill runs
node to_png.js
```

Strava's own share images aren't available through the API, so the routes are drawn here from each
activity's polyline. Runs without GPS (treadmill) get a made-up but realistic-looking route
(seeded by activity id, so it stays the same between renders). Note: routes reveal where you start runs (e.g. home) – crop or skip those before posting.

## Animation (transparent overlay)

```bash
./make_anim.sh            # 1080x1920 vertical; ./make_anim.sh 1920 1080 for landscape
```

Every run draws itself in, in random order, scattered across the frame (size scales with distance),
its stats fading in underneath; then the full collage holds for 2.5 s. Outputs in `out/anim/`: `.gif` (hard-edged 1-bit transparency)
and `.webm` (VP9 alpha, smooth edges), plus `_small.gif` (720 wide, ~5 MB) and `.mp4` (black background, ~400 KB, plays anywhere). Each route is labelled with distance, pace, duration and date.

### Instagram Story

```bash
./make_story.sh   # -> out/anim/runs_instagram_story.mp4
```

1080×1920, 30 fps, H.264 High / yuv420p, 8 Mbps target, silent AAC track, `+faststart`.
Routes stay out of the story header (top 250 px) and reply bar (bottom 340 px).
