import urllib.request
from PIL import Image, ImageEnhance

print("Downloading avatar...")
urllib.request.urlretrieve("https://github.com/Davinchii53.png", "avatar.png")

print("Processing image...")
img_color = Image.open("avatar.png").convert("RGB")
img_gray = img_color.convert("L")

enhancer = ImageEnhance.Contrast(img_gray)
img_gray = enhancer.enhance(1.8)

cols = 65
w, h = img_color.size
aspect_ratio = h / w
rows = int(aspect_ratio * cols * 0.45)

img_color = img_color.resize((cols, rows))
img_gray = img_gray.resize((cols, rows))

pixels_color = img_color.load()
pixels_gray = img_gray.load()

chars = " .`-_':,;^=+/\"|)\\<>)iv%xclrs{*}I?!][1taeo7zjLunT#JCwfy325Fp6mqSghVd4EgXPGZbYkOA&8U$@KHDBWNMR0Q"

ascii_lines = []
for j in range(rows):
    line_spans = []
    for i in range(cols):
        brightness = pixels_gray[i, j]
        r, g, b = pixels_color[i, j]
        
        if brightness < 30:
            char = " "
        else:
            char_idx = int((brightness / 255.0) * (len(chars) - 1))
            char = chars[char_idx]
        
        if char == "&": char = "&amp;"
        elif char == "<": char = "&lt;"
        elif char == ">": char = "&gt;"
        elif char == " ": char = "&#160;"
        
        r = min(255, int(r * 1.3))
        g = min(255, int(g * 1.3))
        b = min(255, int(b * 1.3))
        
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        line_spans.append(f'<tspan fill="{hex_color}">{char}</tspan>')
        
    ascii_lines.append("".join(line_spans))

font_size = 9
line_height = 11

def generate_svg(is_mobile=False):
    if is_mobile:
        svg_width = 450
        ascii_height = rows * line_height
        right_panel_x = 20
        right_panel_y = 50 + ascii_height + 40
        right_panel_max_y = right_panel_y + 495 + 40
        svg_height = right_panel_max_y
        border_width = svg_width - 20
        border_height = svg_height - 20
    else:
        svg_width = 950
        right_panel_max_y = 50 + 495 + 40
        left_panel_max_y = 50 + (rows * line_height) + 40
        svg_height = max(right_panel_max_y, left_panel_max_y)
        right_panel_x = 420
        right_panel_y = 50
        border_width = svg_width - 20
        border_height = svg_height - 20

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
  <style>
    .bg {{ fill: #0d1117; }}
    .text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size: {font_size}px; font-weight: bold; }}
    .glow {{ filter: drop-shadow(0 0 1px rgba(0, 240, 255, 0.3)); }}
    .terminal-border {{ fill: none; stroke: #00F0FF; stroke-width: 2; opacity: 0.3; }}
    .info-title {{ fill: #FF0055; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; font-weight: bold; font-size: 18px; letter-spacing: 1px; }}
    .info-text {{ fill: #FFFFFF; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; font-size: 16px; }}
    .info-label {{ fill: #00F0FF; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; font-size: 16px; font-weight: bold; }}
    @keyframes scan {{
      0% {{ transform: translateY(0); }}
      100% {{ transform: translateY({border_height}px); }}
    }}
    .scanner {{ animation: scan 4s linear infinite; opacity: 0.15; }}
    @keyframes flicker {{
      0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {{ opacity: 1; }}
      20%, 24%, 55% {{ opacity: 0.6; }}
    }}
    .hologram {{ animation: flicker 6s infinite; }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.6; }}
    }}
    .pulse {{ animation: pulse 2s infinite; }}
  </style>
  <rect class="bg" width="{svg_width}" height="{svg_height}" />
  <rect class="terminal-border glow" x="10" y="10" width="{border_width}" height="{border_height}" rx="5" />
  <rect class="scanner" x="10" y="10" width="{border_width}" height="15" fill="#00F0FF" />
  <g class="hologram" transform="translate(20, 50)">
"""
    for idx, line in enumerate(ascii_lines):
        svg_content += f'    <text class="text" xml:space="preserve" x="0" y="{idx * line_height}">{line}</text>\\n'

    svg_content += f"""
  </g>
  <g transform="translate({right_panel_x}, {right_panel_y})">
    <text class="info-title pulse" x="0" y="0">SYSTEM.INFO // RESEARCH.SCHOLAR</text>
    <path d="M0 15 L350 15" stroke="#FF0055" stroke-width="1" stroke-dasharray="4" opacity="0.5" />
    <text class="info-label" x="0" y="45">Role:</text>
    <text class="info-text" x="120" y="45">Digital Architect &amp; Dev</text>
    <text class="info-label" x="0" y="70">Affiliation:</text>
    <text class="info-text" x="120" y="70">Earth</text>
    <text class="info-label" x="0" y="95">Status:</text>
    <text class="info-text" x="120" y="95">Researching / Building</text>
    <text class="info-title pulse" x="0" y="150">RESEARCH.NODE</text>
    <path d="M0 165 L350 165" stroke="#FF0055" stroke-width="1" stroke-dasharray="4" opacity="0.5" />
    <text class="info-label" x="0" y="195">Primary:</text>
    <text class="info-text" x="120" y="195">Autonomous Systems</text>
    <text class="info-label" x="0" y="220">Direction:</text>
    <text class="info-text" x="120" y="220">Multi-agent systems</text>
    <text class="info-title pulse" x="0" y="275">BUILD.LOG</text>
    <path d="M0 290 L350 290" stroke="#FF0055" stroke-width="1" stroke-dasharray="4" opacity="0.5" />
    <text class="info-label" x="0" y="320">NodeAI:</text>
    <text class="info-text" x="120" y="320">Intelligent wallet</text>
    <text class="info-label" x="0" y="345">ProofID:</text>
    <text class="info-text" x="120" y="345">Web3 trust layer</text>
    <text class="info-label" x="0" y="370">Quorum:</text>
    <text class="info-text" x="120" y="370">Agent coordination</text>
    <text class="info-title pulse" x="0" y="425">GRID.LINKS</text>
    <path d="M0 440 L350 440" stroke="#FF0055" stroke-width="1" stroke-dasharray="4" opacity="0.5" />
    <text class="info-label" x="0" y="470">GitHub:</text>
    <text class="info-text" x="120" y="470">github.com/Davinchii53</text>
    <text class="info-label" x="0" y="495">Status:</text>
    <text class="info-text" x="120" y="495">g.pal.locked &gt; AGENTS</text>
  </g>
  <rect x="{border_width - 10}" y="20" width="10" height="10" fill="#00F0FF" class="glow pulse" />
  <rect x="{border_width - 30}" y="20" width="10" height="10" fill="#FF0055" class="glow pulse" />
  <rect x="{border_width - 50}" y="20" width="10" height="10" fill="#FFFFFF" class="glow pulse" />
</svg>
"""
    return svg_content

with open("terminal-desktop.svg", "w", encoding="utf-8") as f:
    f.write(generate_svg(is_mobile=False))

with open("terminal-mobile.svg", "w", encoding="utf-8") as f:
    f.write(generate_svg(is_mobile=True))

print("Both SVGs Generated.")
