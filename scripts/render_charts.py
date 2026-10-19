#!/usr/bin/env python3
"""Render simple, portable SVG charts from the curated public CSV."""

from __future__ import annotations

import csv
import html
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "summaries" / "chart-data.csv"
OUT = ROOT / "figures"
TITLES = {
    "old-metric-fourway": "Old callback measure: four-way comparison",
    "delivery-to-send-fourway": "Delivery-to-Send: four-way comparison",
    "position-delivery-to-send": "Position fixture: delivery-to-Send",
    "log-formatting": "Decision-log formatting: delivery-to-Send",
    "top-of-book": "Cached top of book versus full scan",
    "risk-control-large": "Risk checks on the larger synthetic feed",
    "group-commit": "WAL sync cost: group commit comparison",
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def render(chart: str, rows: list[dict[str, str]]) -> str:
    unit = rows[0]["unit"]
    values = [float(row["value"]) for row in rows]
    maximum = max(values) or 1.0
    width, left, right = 900, 220, 170
    row_h, top = 42, 78
    height = top + len(rows) * row_h + 78
    bar_w = width - left - right
    context = rows[0]["context"]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-labelledby="title desc" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:system-ui,-apple-system,sans-serif;fill:#17202a}'
        '.title{font-size:22px;font-weight:650}.label{font-size:15px}'
        '.value{font-size:14px;font-variant-numeric:tabular-nums}'
        '.note{font-size:12px;fill:#465363}.bar{fill:#3478c8}'
        '.grid{stroke:#d9e0e8;stroke-width:1}</style>',
        f'<title id="title">{esc(TITLES[chart])}</title>',
        f'<desc id="desc">Horizontal bars compare latency values in {esc(unit)}. {esc(context)}</desc>',
        f'<text class="title" x="24" y="36">{esc(TITLES[chart])}</text>',
        f'<text class="note" x="{left}" y="60">Latency ({esc(unit)})</text>',
    ]
    for tick in range(5):
        x = left + bar_w * tick / 4
        parts.append(f'<line class="grid" x1="{x:.1f}" y1="70" x2="{x:.1f}" y2="{top + len(rows) * row_h}"/>')
        parts.append(f'<text class="note" x="{x:.1f}" y="{top + len(rows) * row_h + 18}" text-anchor="middle">{maximum * tick / 4:.4g}</text>')
    for index, row in enumerate(rows):
        y = top + index * row_h
        value = float(row["value"])
        width_px = bar_w * value / maximum
        parts.append(f'<text class="label" x="{left - 12}" y="{y + 20}" text-anchor="end">{esc(row["variant"])}</text>')
        parts.append(f'<rect class="bar" x="{left}" y="{y + 3}" width="{width_px:.1f}" height="24" rx="4"/>')
        parts.append(f'<text class="value" x="{left + width_px + 8:.1f}" y="{y + 20}">{value:,.4g}</text>')
    parts.append(f'<text class="note" x="24" y="{height - 20}">{esc(context)}</text>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def render_metric_window() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 900 210">
<style>text{font-family:system-ui,-apple-system,sans-serif;fill:#17202a}.title{font-size:22px;font-weight:650}.label{font-size:16px}.note{font-size:13px;fill:#465363}.box{fill:#edf4fc;stroke:#3478c8;stroke-width:2}.line{stroke:#3478c8;stroke-width:3;marker-end:url(#arrow)}</style>
<title id="title">Delivery-to-Send measurement window</title>
<desc id="desc">Measure from delivery into the application to the application's Send call. Network travel and exchange processing are outside the window.</desc>
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#3478c8"/></marker></defs>
<text class="title" x="24" y="36">Corrected application latency measure</text>
<rect class="box" x="30" y="75" width="180" height="58" rx="8"/><text class="label" x="120" y="110" text-anchor="middle">Delivery entry</text>
<line class="line" x1="210" y1="104" x2="685" y2="104"/><text class="label" x="448" y="92" text-anchor="middle">application work</text>
<rect class="box" x="690" y="75" width="180" height="58" rx="8"/><text class="label" x="780" y="110" text-anchor="middle">Send entry</text>
<text class="note" x="30" y="174">Measured: wall time from delivery into the application to its Send call.</text>
<text class="note" x="30" y="194">Not measured: network travel after Send or exchange processing.</text>
</svg>
'''


def main() -> None:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    with DATA.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            grouped[row["chart"]].append(row)
    OUT.mkdir(parents=True, exist_ok=True)
    for chart, rows in grouped.items():
        (OUT / f"{chart}.svg").write_text(render(chart, rows), encoding="utf-8")
    (OUT / "metric-window.svg").write_text(render_metric_window(), encoding="utf-8")
    print(f"Rendered {len(grouped)} charts and one metric diagram in {OUT}")


if __name__ == "__main__":
    main()
