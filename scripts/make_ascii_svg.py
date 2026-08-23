"""Generate an animated ASCII portrait SVG from a supplied photograph.

Usage:
    python scripts/make_ascii_svg.py path/to/photo.jpeg
    -> writes pratham-ascii.svg
"""

import sys
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageEnhance, ImageOps

GLYPHS = " .`:-=+*cs#%@"
COLS, ROWS = 92, 50
CELL_W, CELL_H = 6, 11
FILL_COLOR = "#8b949e"


def image_to_ascii_rows(path: str) -> list[str]:
    """Centre-crop, boost contrast, and convert the image to ASCII rows."""
    image = Image.open(path).convert("L")
    image = ImageOps.fit(image, (COLS, ROWS), method=Image.Resampling.LANCZOS)
    image = ImageEnhance.Contrast(image).enhance(1.55)
    image = ImageEnhance.Sharpness(image).enhance(1.3)

    pixels = image.load()
    rows = []
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            brightness = pixels[x, y] / 255
            index = int((1 - brightness) * (len(GLYPHS) - 1))
            row.append(GLYPHS[index])
        rows.append("".join(row))
    return rows


def build_svg(rows: list[str]) -> str:
    width, height = COLS * CELL_W, ROWS * CELL_H
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="monospace" font-size="{CELL_H}">'
    ]

    for row_index, row in enumerate(rows):
        y = (row_index + 1) * CELL_H
        delay = row_index * 0.045
        clip_id = f"portrait-row-{row_index}"
        parts.extend(
            [
                f'<clipPath id="{clip_id}">',
                f'  <rect x="0" y="{y - CELL_H}" width="0" height="{CELL_H}">',
                f'    <animate attributeName="width" from="0" to="{width}" begin="{delay:.3f}s" dur="0.35s" fill="freeze"/>',
                "  </rect>",
                "</clipPath>",
                f'<g clip-path="url(#{clip_id})">',
                f'  <text x="0" y="{y}" fill="{FILL_COLOR}" xml:space="preserve">{escape(row)}</text>',
                "</g>",
            ]
        )

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/make_ascii_svg.py <photo-path>")
        sys.exit(1)

    output = Path("pratham-ascii.svg")
    output.write_text(build_svg(image_to_ascii_rows(sys.argv[1])), encoding="utf-8")
    print(f"ASCII portrait SVG written -> {output}")
