"""
make_info_card.py

Hand-built SVG that mimics a `neofetch` panel: a title bar, then rows of
key/value info. Each row fades + slides in on a stagger via CSS keyframes
(plays once on load, then holds - no infinite loop).

Edit the FIELDS list below with your own details.

Usage:
    python make_info_card.py
    -> writes info-card.svg
"""

from xml.sax.saxutils import escape

FIELDS = [
        ("Focus", "AI, deep learning & computer vision"),
        ("Project", "NoteShield AI — currency detection"),
        ("Stack", "Python, PyTorch, Jupyter, CUDA"),
        ("Exploring", "Data science & software development"),
]

WIDTH, HEIGHT = 490, 300
ROW_HEIGHT = 34
TOP_PAD = 70
BG = "#0d1117"
BORDER = "#30363d"
LABEL_COLOR = "#39d353"
VALUE_COLOR = "#c9d1d9"


def build_svg() -> str:
    rows_svg = []
    style_rules = []

    for i, (label, value) in enumerate(FIELDS):
        y = TOP_PAD + i * ROW_HEIGHT
        anim_name = f"rowIn{i}"
        delay = 0.5 + i * 0.18

        style_rules.append(
            f"""
            @keyframes {anim_name} {{
              from {{ opacity: 0; transform: translateX(-8px); }}
              to   {{ opacity: 1; transform: translateX(0); }}
            }}
            .row{i} {{
              opacity: 0;
              animation: {anim_name} 0.4s ease-out {delay:.2f}s forwards;
            }}
            """
        )

        label_escaped = escape(label)
        value_escaped = escape(value)
        rows_svg.append(
            f'<g class="row{i}">'
            f'<text x="24" y="{y}" font-family="monospace" font-size="14" '
            f'fill="{LABEL_COLOR}" font-weight="bold">{label_escaped}:</text>'
            f'<text x="140" y="{y}" font-family="monospace" font-size="13" '
            f'fill="{VALUE_COLOR}">{value_escaped}</text>'
            f"</g>"
        )

    style_block = "<style>" + "\n".join(style_rules) + "</style>"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">
  {style_block}
  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="8" fill="{BG}" stroke="{BORDER}"/>
  <circle cx="20" cy="20" r="6" fill="#ff5f56"/>
  <circle cx="40" cy="20" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="20" r="6" fill="#27c93f"/>
  <text x="{WIDTH/2}" y="25" text-anchor="middle" font-family="monospace"
        font-size="12" fill="#8b949e">Pratham010-hub@github</text>
  <line x1="20" y1="42" x2="{WIDTH-20}" y2="42" stroke="{BORDER}"/>
  {''.join(rows_svg)}
</svg>"""


if __name__ == "__main__":
    with open("info-card.svg", "w") as f:
        f.write(build_svg())
    print("Info card SVG written -> info-card.svg")
