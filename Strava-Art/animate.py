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
FPS = 20
STAGGER = 0.09   # seconds between one route starting and the next
DRAW = 0.6       # seconds each route takes to draw itself
HOLD = 2.5       # seconds the full collage stays at the end
ASPECT_W, ASPECT_H = 1.4, 2.0  # item box relative to its route square
GAP = 4


def layout(runs, rng):
    """Place a rectangle per run (route square + stats below) without overlap.

    Sizes vary a little with distance; everything shrinks until it all fits.
    """
    weights = [max(3.0, min(r["distance_km"], 30.0)) ** 0.12 for r in runs]
    margin = 0.03 * min(W, H)
    unit = math.sqrt(0.80 * W * H / sum(ASPECT_W * w * ASPECT_H * w for w in weights))
    while True:
        placed, ok = [], True
        for i in sorted(range(len(runs)), key=lambda i: -weights[i]):  # big ones first
            s = weights[i] * unit
            # widest stats line ~ 0.52 em per char at 0.84 of the distance font (0.25 * s)
            text_w = len(stat_line(runs[i])) * 0.52 * 0.84 * 0.25 * s
            bw, bh = max(s * ASPECT_W, text_w + 6), s * ASPECT_H
            for _ in range(6000):
                x = rng.uniform(margin, W - margin - bw)
                y = rng.uniform(margin, H - margin - bh)
                if all(x + bw + GAP <= px or px + pw + GAP <= x or y + bh + GAP <= py or py + ph + GAP <= y
                       for _, px, py, pw, ph in placed):
                    placed.append((i, x, y, bw, bh))
                    break
            else:
                ok = False
                break
        if ok:
            return {i: (x, y, bw, bh, weights[i] * unit) for i, x, y, bw, bh in placed}
        unit *= 0.97


def stat_line(r):
    pace = (r["avg_pace"] or "").replace(" /km", "/km")
    return f'{pace} · {fmt_dur(r["moving_time_s"])}'


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
        fs = sq * 0.25  # distance line; others scale from it
        date = datetime.fromisoformat(r["start_local"])
        items.append({
            "d": d, "start": k * STAGGER, "width": max(2.5, sq / 40),
            "cx": x + bw / 2, "ty": y + sq + fs * 1.05, "fs": fs,
            "lines": [f'{r["distance_km"]:.1f} km', stat_line(r),
                      f'{date:%a %d %b}'],
        })
    total = len(items) * STAGGER + DRAW + HOLD
    spec = {"width": W, "height": H, "fps": FPS, "draw": DRAW, "duration": total,
            "color": ACCENT, "items": items}
    os.makedirs(os.path.join(OUT, "anim"), exist_ok=True)
    path = os.path.join(OUT, "anim", f"spec_{W}x{H}.json")
    json.dump(spec, open(path, "w"))
    print(f"{len(items)} routes, {total:.1f}s @ {FPS}fps -> {path}")


if __name__ == "__main__":
    main()
