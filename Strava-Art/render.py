#!/usr/bin/env python3
"""Render Strava runs as route-art cards and a poster grid (stdlib only).

Input:  data/runs.json  (exported from Strava: name, date, distance, pace, polyline)
Output: out/cards/<date>_<id>.svg   one card per run
        out/poster.svg              every run in a grid, marathon-block style
        out/poster.html             same poster, open in a browser / screenshot to PNG
"""
import json
import math
import os
import random
import sys
from datetime import datetime
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "runs.json")
OUT = os.path.join(HERE, "out")

BG = "#0f0f10"
FG = "#f4f4f2"
ACCENT = "#fc5200"  # Strava-ish orange for the route line
MUTED = "#8a8a8a"


def decode_polyline(s):
    """Google encoded polyline -> list of (lat, lng)."""
    coords, i, lat, lng = [], 0, 0, 0
    while i < len(s):
        for which in (0, 1):
            shift = result = 0
            while True:
                b = ord(s[i]) - 63
                i += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            delta = ~(result >> 1) if result & 1 else result >> 1
            if which == 0:
                lat += delta
            else:
                lng += delta
        coords.append((lat / 1e5, lng / 1e5))
    return coords


def fake_route(seed, distance_km):
    """Made-up but plausible city run for activities without GPS (treadmill).

    Runs out along a slightly rotated street grid, does a lap of an organic
    "park" loop, then returns home along streets. Every block is densely
    sampled with small jitter and gentle street curvature so it reads as GPS.
    """
    rng = random.Random(seed)
    angle = rng.uniform(0, math.pi / 2)
    ca, sa = math.cos(angle), math.sin(angle)
    block = 0.0012  # ~130 m in degrees
    pts = [(0.0, 0.0)]

    def walk_to(tx, ty, sub=5):
        x0, y0 = pts[-1]
        bend = rng.gauss(0, 0.08)
        for i in range(1, sub + 1):
            t = i / sub
            nx, ny = -(ty - y0), (tx - x0)  # perpendicular, for a slight curve
            b = bend * math.sin(math.pi * t)
            pts.append((x0 + (tx - x0) * t + nx * b + rng.gauss(0, block * 0.05),
                        y0 + (ty - y0) * t + ny * b + rng.gauss(0, block * 0.05)))

    def streets_to(tx, ty):
        """Zig-zag toward a target along the grid, a few blocks at a time."""
        x, y = pts[-1]
        while abs(tx - x) > block * 0.5 or abs(ty - y) > block * 0.5:
            horiz = abs(tx - x) > block * 0.5 and (abs(ty - y) <= block * 0.5 or rng.random() < 0.5)
            n = rng.randint(1, 4) * block
            if horiz:
                x += max(-n, min(n, tx - x))
            else:
                y += max(-n, min(n, ty - y))
            walk_to(x, y, sub=max(3, int(abs(n) / block) * 3))

    # Out: a park somewhere 1/4-1/3 of the run's distance away.
    reach = block * max(4, distance_km * 2.0)
    theta = rng.uniform(0, 2 * math.pi)
    px = round(math.cos(theta) * reach / block) * block
    py = round(math.sin(theta) * reach / block) * block
    streets_to(px, py)

    # Park loop: noisy ellipse, sometimes run twice.
    r = block * rng.uniform(2.5, 4.5)
    cx, cy = px + r * math.cos(theta), py + r * math.sin(theta)
    start = math.atan2(py - cy, px - cx)
    wob = [rng.uniform(0.85, 1.15) for _ in range(6)]
    laps = 2 if distance_km > 9 and rng.random() < 0.5 else 1
    n = 60 * laps
    for i in range(1, n + 1):
        a = start + 2 * math.pi * laps * i / n
        k = wob[int((a % (2 * math.pi)) / (2 * math.pi) * 6) % 6]
        pts.append((cx + r * k * 1.4 * math.cos(a) + rng.gauss(0, block * 0.04),
                    cy + r * k * 0.9 * math.sin(a) + rng.gauss(0, block * 0.04)))
    pts.append((px, py))

    # Back home by a different street pattern.
    streets_to(0.0, 0.0)

    lat0, lng0 = 40.42, -3.70
    return [(lat0 + x * ca - y * sa, lng0 + x * sa + y * ca) for x, y in pts]


def route_path(coords, x, y, w, h, pad=0.08):
    """Fit coords into box (x, y, w, h), keeping aspect ratio. Returns SVG path d."""
    if len(coords) < 2:
        return ""
    lat0 = sum(c[0] for c in coords) / len(coords)
    k = math.cos(math.radians(lat0))
    pts = [(lng * k, -lat) for lat, lng in coords]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    span = max(maxx - minx, maxy - miny) or 1e-9
    iw, ih = w * (1 - 2 * pad), h * (1 - 2 * pad)
    scale = min(iw, ih) / span
    ox = x + (w - (maxx - minx) * scale) / 2
    oy = y + (h - (maxy - miny) * scale) / 2
    return "M" + " L".join(
        f"{ox + (px - minx) * scale:.1f},{oy + (py - miny) * scale:.1f}" for px, py in pts
    )


def fmt_time(sec):
    h, rem = divmod(int(sec), 3600)
    m, s = divmod(rem, 60)
    return f"{h}h {m:02d}m" if h else f"{m}m {s:02d}s"


def card_body(run, x, y, size, show_text=True):
    """SVG fragment for one run inside a size x size square at (x, y)."""
    date = datetime.fromisoformat(run["start_local"])
    parts = []
    map_h = size * (0.72 if show_text else 1.0)
    coords = (decode_polyline(run["polyline"]) if run["polyline"]
              else fake_route(int(run["id"]), run["distance_km"]))
    d = route_path(coords, x, y, size, map_h)
    sw = max(1.6, size / 110)
    parts.append(
        f'<path d="{d}" fill="none" stroke="{ACCENT}" stroke-width="{sw:.1f}" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
    )
    if show_text:
        ty = y + map_h
        fs = size / 16
        parts.append(
            f'<text x="{x + size * 0.06:.1f}" y="{ty + fs * 1.3:.1f}" fill="{FG}" '
            f'font-size="{fs:.1f}" font-weight="700">{escape(run["name"][:28])}</text>'
        )
        stats = f'{run["distance_km"]:.2f} km · {run["avg_pace"] or ""} · {fmt_time(run["moving_time_s"])}'
        parts.append(
            f'<text x="{x + size * 0.06:.1f}" y="{ty + fs * 2.6:.1f}" fill="{FG}" '
            f'font-size="{fs * 0.8:.1f}">{escape(stats)}</text>'
        )
        parts.append(
            f'<text x="{x + size * 0.06:.1f}" y="{ty + fs * 3.8:.1f}" fill="{MUTED}" '
            f'font-size="{fs * 0.7:.1f}">{date:%a %d %b %Y}</text>'
        )
    return "\n".join(parts)


def svg_doc(w, h, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'font-family="Helvetica Neue, Helvetica, Arial, sans-serif">\n'
        f'<rect width="100%" height="100%" fill="{BG}"/>\n{body}\n</svg>\n'
    )


def main():
    runs = json.load(open(DATA, encoding="utf-8"))
    runs.sort(key=lambda r: r["start_local"])
    skip_no_gps = "--gps-only" in sys.argv
    if skip_no_gps:
        runs = [r for r in runs if r["polyline"]]

    os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)
    for r in runs:
        size = 1080
        fn = f'{r["start_local"][:10]}_{r["id"]}.svg'
        with open(os.path.join(OUT, "cards", fn), "w", encoding="utf-8") as f:
            f.write(svg_doc(size, size, card_body(r, 0, 0, size)))

    # Poster: grid of route tiles with stats underneath + header with totals.
    cols = 10
    tile, text_h, gap, margin, header = 220, 110, 28, 80, 260
    rows = math.ceil(len(runs) / cols)
    W = margin * 2 + cols * tile + (cols - 1) * gap
    H = header + margin + rows * (tile + text_h + gap)
    total_km = sum(r["distance_km"] for r in runs)
    total_s = sum(r["moving_time_s"] for r in runs)
    first = datetime.fromisoformat(runs[0]["start_local"])
    last = datetime.fromisoformat(runs[-1]["start_local"])
    body = [
        f'<text x="{margin}" y="{margin + 70}" fill="{FG}" font-size="80" font-weight="800">MARATHON BLOCK</text>',
        f'<text x="{margin}" y="{margin + 130}" fill="{MUTED}" font-size="32">'
        f'{first:%d %b} – {last:%d %b %Y}  ·  {len(runs)} runs  ·  {total_km:,.0f} km  ·  '
        f'{total_s / 3600:.0f} h</text>',
    ]
    for i, r in enumerate(runs):
        cx = margin + (i % cols) * (tile + gap)
        cy = header + (i // cols) * (tile + text_h + gap)
        body.append(card_body(r, cx, cy, tile, show_text=False))
        date = datetime.fromisoformat(r["start_local"])
        mid = cx + tile / 2
        ty = cy + tile
        body.append(
            f'<text x="{mid}" y="{ty + 28}" fill="{FG}" font-size="28" font-weight="800" '
            f'text-anchor="middle">{r["distance_km"]:.1f} km</text>'
            f'<text x="{mid}" y="{ty + 60}" fill="{FG}" font-size="22" text-anchor="middle">'
            f'{escape(r["avg_pace"] or "")} · {fmt_time(r["moving_time_s"])}</text>'
            f'<text x="{mid}" y="{ty + 90}" fill="{MUTED}" font-size="20" text-anchor="middle">'
            f'{date:%a %d %b}</text>'
        )
    poster = svg_doc(W, H, "\n".join(body))
    with open(os.path.join(OUT, "poster.svg"), "w", encoding="utf-8") as f:
        f.write(poster)
    with open(os.path.join(OUT, "poster.html"), "w", encoding="utf-8") as f:
        f.write(f'<!doctype html><meta charset="utf-8"><title>Marathon Block</title>'
                f'<body style="margin:0;background:{BG}">{poster}</body>')
    print(f"{len(runs)} cards -> {OUT}/cards, poster {W}x{H} -> {OUT}/poster.svg")


if __name__ == "__main__":
    main()
