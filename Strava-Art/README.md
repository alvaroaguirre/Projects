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
then the full collage holds for 2.5 s. Outputs in `out/anim/`: `.gif` (hard-edged 1-bit transparency),
`.webm` (VP9 alpha) and `.mov` (ProRes 4444 alpha – best for Premiere / Final Cut / DaVinci / CapCut desktop).
