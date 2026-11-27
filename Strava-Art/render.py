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
    d = route_path(decode_polyline(run["polyline"]), x, y, size, map_h)
    sw = max(1.2, size / 110)
    if d:
        parts.append(
            f'<path d="{d}" fill="none" stroke="{ACCENT}" stroke-width="{sw:.1f}" '
            f'stroke-linejoin="round" stroke-linecap="round"/>'
        )
    else:  # treadmill / no GPS
        parts.append(
            f'<text x="{x + size / 2:.1f}" y="{y + map_h / 2:.1f}" fill="{MUTED}" '
            f'font-size="{size / 14:.1f}" text-anchor="middle">treadmill</text>'
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

    # Poster: grid of route-only tiles + header with totals.
    cols = 10
    tile, gap, margin, header = 200, 16, 80, 260
    rows = math.ceil(len(runs) / cols)
    W = margin * 2 + cols * tile + (cols - 1) * gap
    H = header + margin + rows * (tile + gap) + 60
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
        cy = header + (i // cols) * (tile + gap)
        body.append(card_body(r, cx, cy, tile, show_text=False))
        body.append(
            f'<text x="{cx + tile / 2}" y="{cy + tile - 4}" fill="{MUTED}" font-size="13" '
            f'text-anchor="middle">{r["distance_km"]:.1f} km</text>'
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
