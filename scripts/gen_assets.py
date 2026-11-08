"""Gera os SVGs de assets/ (variantes -dark e -light) usados no README.

Uso: python scripts/gen_assets.py
Icones de tecnologia em scripts/icons/, vindos do simple-icons 13.21.0 (CC0).
"""
import re
import sys
from pathlib import Path

ICONS = Path(__file__).parent / "icons"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

HEAVY = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SHADOW = 12

# Paleta Primer do GitHub; LEVELS = tons do grafico de contribuicoes
THEMES = {
    "dark": dict(CANVAS="#0D1117", PAPER="#161B22", INK="#E6EDF3", MUTED="#7D8590", DIM="#30363D",
                 ACCENT="#3FB950", ON_ACCENT="#0D1117",
                 LEVELS=["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"]),
    "light": dict(CANVAS="#F6F8FA", PAPER="#FFFFFF", INK="#1F2328", MUTED="#656D76", DIM="#D0D7DE",
                  ACCENT="#2DA44E", ON_ACCENT="#FFFFFF",
                  LEVELS=["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"]),
}


def use(theme):
    globals().update(THEMES[theme])


def icon_path(name):
    svg = (ICONS / f"{name}.svg").read_text(encoding="utf-8")
    return re.search(r'<path d="([^"]+)"', svg).group(1)


def write(name, content):
    (OUT / name).write_text(content.strip() + "\n", encoding="utf-8")


def slab(x, y, w, h, fill, stroke=4, shadow=SHADOW):
    """Bloco brutalista: sombra dura deslocada + retangulo com contorno grosso."""
    return (
        f'<rect x="{x + shadow}" y="{y + shadow}" width="{w}" height="{h}" fill="{INK}"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="{stroke}"/>'
    )


# ---------- banner ----------
def banner():
    W, H = 1200, 400
    src = [(800, 120), (800, 180), (800, 240), (800, 300)]
    mid = [(950, 150), (950, 270)]
    out = (1100, 210)
    edges = [(*src[0], *mid[0]), (*src[1], *mid[0]), (*src[1], *mid[1]),
             (*src[2], *mid[1]), (*src[3], *mid[1]), (*mid[0], *out), (*mid[1], *out)]

    paths = []
    for k, (x1, y1, x2, y2) in enumerate(edges):
        mx = (x1 + x2) / 2
        d = f"M{x1},{y1} H{mx} V{y2} H{x2}"
        paths.append(f'<path d="{d}" class="edge"/>')
        paths.append(f'<path d="{d}" class="flow" style="animation-delay:-{k * 0.4:.1f}s"/>')

    nodes = [f'<rect x="{x - 11}" y="{y - 11}" width="22" height="22" fill="{INK}"/>' for x, y in src]
    nodes += [f'<rect x="{x - 16}" y="{y - 16}" width="32" height="32" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
              for x, y in mid]
    ox, oy = out
    nodes.append(f'<rect x="{ox - 22}" y="{oy - 22}" width="52" height="52" fill="{INK}"/>')
    nodes.append(f'<rect x="{ox - 30}" y="{oy - 30}" width="52" height="52" fill="{ACCENT}" stroke="{INK}" stroke-width="5" class="out"/>')

    words = ["pipelines", "data lakes", "data warehouses", "data platforms"]
    rotating = "\n    ".join(
        f'<text x="40" y="352" class="word" style="animation-delay:{i * 3}s">'
        f'<tspan fill-opacity="0">&gt; building </tspan>{w}</text>'
        for i, w in enumerate(words)
    )

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W + SHADOW + 4}" height="{H + SHADOW + 4}" viewBox="-2 -2 {W + SHADOW + 4} {H + SHADOW + 4}" role="img" aria-labelledby="t d">
  <title id="t">Lucas Abreu, Data Engineer</title>
  <desc id="d">Brutalist banner with the name, the role and an animated graph of a data pipeline.</desc>
  <style>
    .bar {{ font: 700 17px {MONO}; fill: {PAPER}; letter-spacing: 1px; }}
    .name {{ font: 800 104px {HEAVY}; fill: {INK}; }}
    .role {{ font: 800 30px {HEAVY}; fill: {ON_ACCENT}; }}
    .prompt {{ font: 700 22px {MONO}; fill: {MUTED}; }}
    .word {{ font: 700 22px {MONO}; fill: {INK}; opacity: 0;
             animation: cycle 12s linear infinite; }}
    .cap {{ font: 700 14px {MONO}; fill: {INK}; letter-spacing: 2px; }}
    .edge {{ fill: none; stroke: {DIM}; stroke-width: 5; }}
    .flow {{ fill: none; stroke: {INK}; stroke-width: 5; stroke-dasharray: 14 26; animation: flow 2.4s linear infinite; }}
    .out {{ animation: jolt 2.4s steps(1) infinite; }}
    @keyframes flow {{ to {{ stroke-dashoffset: -80; }} }}
    @keyframes jolt {{ 50% {{ transform: translate(4px, 4px); }} }}
    @keyframes cycle {{ 0% {{ opacity: 0; }} 2% {{ opacity: 1; }} 24% {{ opacity: 1; }} 25% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .flow, .out {{ animation: none; }}
      .word {{ animation: none; }} .word:first-of-type {{ opacity: 1; }}
    }}
  </style>
  {slab(0, 0, W, H, PAPER, stroke=6)}
  <rect x="0" y="0" width="{W}" height="52" fill="{INK}"/>
  <text x="28" y="33" class="bar">LUCXSZS / README.MD</text>
  <rect x="{W - 142}" y="16" width="20" height="20" fill="{LEVELS[1]}"/>
  <rect x="{W - 112}" y="16" width="20" height="20" fill="{LEVELS[2]}"/>
  <rect x="{W - 82}" y="16" width="20" height="20" fill="{LEVELS[3]}"/>
  <rect x="{W - 52}" y="16" width="20" height="20" fill="{LEVELS[4]}"/>

  <text x="36" y="180" class="name" textLength="640" lengthAdjust="spacingAndGlyphs">LUCAS ABREU</text>
  <g transform="rotate(-2 200 248)">
    {slab(40, 216, 320, 60, ACCENT, stroke=4, shadow=7)}
    <text x="58" y="258" class="role" textLength="284" lengthAdjust="spacingAndGlyphs">DATA ENGINEER</text>
  </g>
  <text x="40" y="352" class="prompt">&gt; building</text>
  <g>
    {rotating}
  </g>

  <rect x="724" y="52" width="6" height="{H - 52}" fill="{INK}"/>
  {"".join(paths)}
  {"".join(nodes)}
  <text x="800" y="368" class="cap" text-anchor="middle">INGEST</text>
  <text x="950" y="368" class="cap" text-anchor="middle">MODEL</text>
  <text x="1096" y="368" class="cap" text-anchor="middle">DECIDE</text>
</svg>
"""


# ---------- stack grid ----------
def sql_glyph():
    return (
        f'<g fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="square">'
        '<ellipse cx="12" cy="5" rx="8" ry="3"/>'
        '<path d="M4 5v14c0 1.66 3.58 3 8 3s8-1.34 8-3V5"/>'
        '<path d="M4 12c0 1.66 3.58 3 8 3s8-1.34 8-3"/></g>'
    )

STACK = [
    ("Python", "python"),
    ("SQL", None),
    ("Spark", "apachespark"),
    ("Airflow", "apacheairflow"),
    ("dbt", "dbt"),
    ("DuckDB", "duckdb"),
    ("AWS", "amazonwebservices"),
    ("Docker", "docker"),
    ("Kubernetes", "kubernetes"),
]


def stack():
    cols, tw, th, gap, pad, strip = 3, 188, 140, 22, 26, 40
    rows = (len(STACK) + cols - 1) // cols
    iw = pad * 2 + cols * tw + (cols - 1) * gap + 6
    ih = pad * 2 + rows * th + (rows - 1) * gap + 6
    tiles = []
    for i, (label, slug) in enumerate(STACK):
        r, c = divmod(i, cols)
        x = pad + c * (tw + gap)
        y = pad + r * (th + gap)
        glyph = sql_glyph() if slug is None else f'<path d="{icon_path(slug)}" fill="{INK}"/>'
        s = 46 / 24
        tiles.append(
            "<g>"
            + slab(x, y, tw, th, PAPER, stroke=4, shadow=6)
            + f'<g transform="translate({x + (tw - 46) / 2} {y + 22}) scale({s:.4f})">{glyph}</g>'
            + f'<rect x="{x}" y="{y + th - strip}" width="{tw}" height="{strip}" fill="{INK}"/>'
            + f'<text x="{x + tw / 2}" y="{y + th - 13}" text-anchor="middle" class="label">{label.upper()}</text>'
            + "</g>"
        )
    W, H = iw + SHADOW + 4, ih + SHADOW + 4
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="-2 -2 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">Tech stack: {", ".join(l for l, _ in STACK)}</title>
  <style>
    .label {{ font: 700 17px {MONO}; fill: {PAPER}; letter-spacing: 1.5px; }}
  </style>
  {slab(0, 0, iw, ih, CANVAS, stroke=6)}
  {"".join(tiles)}
</svg>
"""


# ---------- contact button ----------
def button():
    w, h = 300, 72
    W, H = w + 8 + 4, h + 8 + 4
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="-2 -2 {W} {H}" role="img" aria-label="LinkedIn">
  {slab(0, 0, w, h, PAPER, stroke=4, shadow=8)}
  <rect x="0" y="0" width="72" height="{h}" fill="{ACCENT}" stroke="{INK}" stroke-width="4"/>
  <text x="36" y="49" text-anchor="middle" font-family="{HEAVY}" font-weight="800" font-size="30" fill="{ON_ACCENT}">in</text>
  <text x="90" y="33" font-family="{HEAVY}" font-weight="800" font-size="20" fill="{INK}">LINKEDIN</text>
  <text x="90" y="54" font-family="{MONO}" font-weight="700" font-size="13" fill="{INK}">/in/lucasdantasabreu</text>
  <path d="M262 26 L278 26 L278 42 M278 26 L260 44" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="square"/>
</svg>
"""


# ---------- divider ----------
def divider():
    W, H, cell, gap = 1000, 14, 14, 4
    n = (W + gap) // (cell + gap)
    off = (W - (n * cell + (n - 1) * gap)) / 2
    # padrao fixo e pseudo-aleatorio, mais intenso no centro
    cells = []
    for i in range(n):
        center = 1 - abs(i - n / 2) / (n / 2)
        lvl = min(4, int(center * 4 + ((i * 7919) % 13) / 13 * 1.6))
        cells.append(f'<rect x="{off + i * (cell + gap):.1f}" y="0" width="{cell}" height="{cell}" rx="2" fill="{LEVELS[lvl]}"/>')
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">
  {"".join(cells)}
</svg>
"""


for theme in THEMES:
    use(theme)
    write(f"banner-{theme}.svg", banner())
    write(f"stack-{theme}.svg", stack())
    write(f"btn-linkedin-{theme}.svg", button())
    write(f"divider-{theme}.svg", divider())
print("ok", sorted(p.name for p in OUT.iterdir()))
