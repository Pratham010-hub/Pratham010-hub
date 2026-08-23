"""
make_section_headers.py

Generates small terminal-style SVGs for section labels that "type" the
text out character by character with a blinking cursor, then freeze.
Used in place of plain <h3> text so the headers animate on the profile
page (GitHub strips inline <style>/CSS on raw markdown text, but SVGs
embedded via <img> still play their SMIL/CSS animations).

Usage:
    python make_section_headers.py
    -> writes header-contributions.svg, header-whoami.svg
"""

FONT_SIZE = 18
CHAR_W = 10.8
HEIGHT = 30
PROMPT_COLOR = "#39d353"
TEXT_COLOR = "#c9d1d9"
CURSOR_COLOR = "#39d353"
TYPE_SPEED = 0.045  # seconds per character


def build_header_svg(text: str) -> str:
    full_width = int(len(text) * CHAR_W) + 20
    n_chars = len(text)
    total_type_time = n_chars * TYPE_SPEED

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{full_width}" height="{HEIGHT}" '
        f'viewBox="0 0 {full_width} {HEIGHT}" font-family="monospace" font-size="{FONT_SIZE}">'
    ]

    # reveal-wipe clip, mirrors the ascii-portrait technique
    parts.append('<clipPath id="typeClip">')
    parts.append(f'  <rect x="0" y="0" width="0" height="{HEIGHT}">')
    parts.append(
        f'    <animate attributeName="width" from="0" to="{full_width}" '
        f'begin="0s" dur="{total_type_time:.2f}s" fill="freeze" />'
    )
    parts.append("  </rect>")
    parts.append("</clipPath>")

    text_escaped = (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    parts.append('<g clip-path="url(#typeClip)">')
    parts.append(
        f'  <text x="4" y="{HEIGHT - 9}" fill="{TEXT_COLOR}" xml:space="preserve">{text_escaped}</text>'
    )
    parts.append("</g>")

    # blinking cursor that rides the end of the typed text, then keeps blinking
    cursor_x = 4 + n_chars * CHAR_W
    parts.append(
        f'<rect x="{cursor_x:.1f}" y="4" width="9" height="{FONT_SIZE}" fill="{CURSOR_COLOR}" opacity="0">'
    )
    parts.append(
        f'  <animate attributeName="opacity" values="0;0;1;0" keyTimes="0;{min(0.999, total_type_time/ (total_type_time+1.2)):.3f};1;1" '
        f'dur="{total_type_time + 1.2:.2f}s" begin="0s" fill="freeze" />'
    )
    parts.append(
        f'  <animate attributeName="opacity" values="1;0;1" dur="1s" begin="{total_type_time:.2f}s" repeatCount="indefinite" />'
    )
    parts.append("</rect>")

    parts.append("</svg>")
    return "\n".join(parts)


SECTIONS = {
    "header-contributions.svg": "pratham@github ~ $ ./contributions.sh",
    "header-whoami.svg": "pratham@github ~ $ whoami",
}

if __name__ == "__main__":
    for filename, text in SECTIONS.items():
        with open(filename, "w") as f:
            f.write(build_header_svg(text))
        print(f"wrote {filename}")
