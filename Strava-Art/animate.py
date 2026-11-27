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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import DATA, OUT, ACCENT, decode_polyline, fake_route, route_path  # noqa: E402

W, H = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (1080, 1920)
FPS = 20
STAGGER = 0.09   # seconds between one route starting and the next
DRAW = 0.6       # seconds each route takes to draw itself
HOLD = 2.5       # seconds the full collage stays at the end


def layout(runs, rng):
    """Place circles (one per run) without overlap; shrink until everything fits."""
    weights = [math.sqrt(max(r["distance_km"], 2)) for r in runs]
    margin = 0.04 * min(W, H)
    scale = math.sqrt(0.62 * W * H / sum(math.pi * w * w for w in weights))
    while True:
        placed, ok = [], True
        for i in sorted(range(len(runs)), key=lambda i: -weights[i]):  # big ones first
            rad = weights[i] * scale
            for _ in range(4000):
                x = rng.uniform(margin + rad, W - margin - rad)
                y = rng.uniform(margin + rad, H - margin - rad)
                if all((x - px) ** 2 + (y - py) ** 2 > (rad + pr + 4) ** 2 for _, px, py, pr in placed):
                    placed.append((i, x, y, rad))
                    break
            else:
                ok = False
                break
        if ok:
            return {i: (x, y, rad) for i, x, y, rad in placed}
        scale *= 0.96


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
        x, y, rad = pos[i]
        box = rad * 2
        d = route_path(coords, x - rad, y - rad, box, box, pad=0.02)
        items.append({"d": d, "start": k * STAGGER, "width": max(2.5, box / 45)})
    total = len(items) * STAGGER + DRAW + HOLD
    spec = {"width": W, "height": H, "fps": FPS, "draw": DRAW, "duration": total,
            "color": ACCENT, "items": items}
    os.makedirs(os.path.join(OUT, "anim"), exist_ok=True)
    path = os.path.join(OUT, "anim", f"spec_{W}x{H}.json")
    json.dump(spec, open(path, "w"))
    print(f"{len(items)} routes, {total:.1f}s @ {FPS}fps -> {path}")


if __name__ == "__main__":
    main()
