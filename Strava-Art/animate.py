#!/usr/bin/env python3
"""Lay every run out as a scattered collage (no grid) and write an animation spec.

Each route gets a random spot, size scaled by distance, and a random appearance
time; animate.js turns the spec into transparent PNG frames, ffmpeg into GIF/WebM/MOV.

Usage: python3 animate.py [WIDTH HEIGHT]   (default 1080 1920, vertical video)
"""
import json
import math
import os
import random
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import DATA, OUT, ACCENT, decode_polyline, fake_route, route_path  # noqa: E402

W, H = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (1080, 1920)
FPS = int(os.environ.get("FPS", 20))
# Keep clear of UI overlays, e.g. Instagram story header/reply bar (px).
SAFE_TOP = int(os.environ.get("SAFE_TOP", 0))
SAFE_BOTTOM = int(os.environ.get("SAFE_BOTTOM", 0))
TAG = os.environ.get("TAG", f"{W}x{H}")
STAGGER = 0.09   # seconds between one route starting and the next
DRAW = 0.6       # seconds each route takes to draw itself
HOLD = 2.5       # seconds the full collage stays at the end
FS = 0.28                      # distance font size relative to route square
LINE_SIZES = [1.0, 0.86, 0.86, 0.8]   # distance, pace, duration, date (x FS)
LINE_GAP = 1.02                        # baseline spacing in ems of each line
ASPECT_W = 1.15                        # min box width relative to route square
ASPECT_H = 1 + FS * (0.3 + sum(LINE_SIZES) * LINE_GAP)  # route + text block
GAP = 4


def layout(runs, rng):
    """Place a rectangle per run (route square + stats below) without overlap.

    Sizes vary a little with distance; everything shrinks until it all fits.
    """
    weights = [max(3.0, min(r["distance_km"], 30.0)) ** 0.12 for r in runs]
    margin = 0.03 * min(W, H)
    unit = math.sqrt(0.80 * W * (H - SAFE_TOP - SAFE_BOTTOM) / sum(ASPECT_W * w * ASPECT_H * w for w in weights))
    while True:
        placed, ok = [], True
        for i in sorted(range(len(runs)), key=lambda i: -weights[i]):  # big ones first
            s = weights[i] * unit
            # widest stats line, ~0.55 em per character
            text_w = max(len(t) * 0.55 * k for t, k in zip(stat_lines(runs[i]), LINE_SIZES)) * FS * s
            bw, bh = max(s * ASPECT_W, text_w + 6), s * ASPECT_H
            # Sample many valid spots, keep the one hugging its neighbours most
            # (denser packing -> bigger text) while still looking scattered.
            best, best_score, valid = None, None, 0
            for _ in range(3000):
                x = rng.uniform(margin, W - margin - bw)
                y = rng.uniform(margin + SAFE_TOP, H - margin - SAFE_BOTTOM - bh)
                if all(x + bw + GAP <= px or px + pw + GAP <= x or y + bh + GAP <= py or py + ph + GAP <= y
                       for _, px, py, pw, ph in placed):
                    gaps = [max(px - (x + bw), x - (px + pw), py - (y + bh), y - (py + ph), 0)
                            for _, px, py, pw, ph in placed]
                    edge = min(x - margin, W - margin - bw - x)
                    score = min(gaps + [edge]) + rng.uniform(0, 6)
                    if best_score is None or score < best_score:
                        best, best_score = (x, y), score
                    valid += 1
                    if valid >= 40:
                        break
            if best is None:
                ok = False
                break
            placed.append((i, best[0], best[1], bw, bh))
        if ok:
            return {i: (x, y, bw, bh, weights[i] * unit) for i, x, y, bw, bh in placed}
        unit *= 0.985


def stat_lines(r):
    pace = (r["avg_pace"] or "").replace(" /km", "/km")
    date = datetime.fromisoformat(r["start_local"])
    return [f'{r["distance_km"]:.1f} km', pace, fmt_dur(r["moving_time_s"]), f'{date:%a %d %b}']


def fmt_dur(sec):
    h, rem = divmod(int(sec), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main():
    rng = random.Random(42)
    runs = json.load(open(DATA, encoding="utf-8"))
    pos = layout(runs, rng)
    order = list(range(len(runs)))
    rng.shuffle(order)
    items = []
    for k, i in enumerate(order):
        r = runs[i]
        coords = decode_polyline(r["polyline"]) if r["polyline"] else fake_route(int(r["id"]), r["distance_km"])
        x, y, bw, bh, sq = pos[i]  # sq: route square, centred horizontally
        d = route_path(coords, x + (bw - sq) / 2, y, sq, sq, pad=0.04)
        fs = sq * FS
        items.append({
            "d": d, "start": k * STAGGER, "width": max(2.5, sq / 40),
            "cx": x + bw / 2, "ty": y + sq + fs * 1.0, "fs": fs,
            "lines": stat_lines(r), "sizes": LINE_SIZES, "gap": LINE_GAP,
        })
    total = len(items) * STAGGER + DRAW + HOLD
    spec = {"tag": TAG, "width": W, "height": H, "fps": FPS, "draw": DRAW, "duration": total,
            "color": ACCENT, "items": items}
    os.makedirs(os.path.join(OUT, "anim"), exist_ok=True)
    path = os.path.join(OUT, "anim", f"spec_{TAG}.json")
    json.dump(spec, open(path, "w"))
    print(f"{len(items)} routes, {total:.1f}s @ {FPS}fps -> {path}")


if __name__ == "__main__":
    main()
