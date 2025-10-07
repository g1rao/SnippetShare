from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = 'screenshots'
os.makedirs(OUT_DIR, exist_ok=True)

WIDTH, HEIGHT = 1200, 800
files = [
    ('home.png', 'Home — SnippetShare'),
    ('editor.png', 'Editor — SnippetShare'),
    ('share.png', 'Share — SnippetShare'),
]

for fname, title in files:
    img = Image.new('RGB', (WIDTH, HEIGHT), '#0f172a')
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype('DejaVuSans-Bold.ttf', 56)
        sub_font = ImageFont.truetype('DejaVuSans.ttf', 20)
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    # Use textbbox for size (fallback to font.getsize)
    try:
        bbox = draw.textbbox((0, 0), title, font=title_font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        w, h = title_font.getsize(title)

    draw.text(((WIDTH - w) / 2, (HEIGHT / 2) - 40), title, font=title_font, fill=(255, 255, 255))
    subtitle = 'Placeholder screenshot — replace with real capture'
    try:
        sbbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        sw, sh = sbbox[2] - sbbox[0], sbbox[3] - sbbox[1]
    except AttributeError:
        sw, sh = sub_font.getsize(subtitle)
    draw.text(((WIDTH - sw) / 2, (HEIGHT / 2) + 20), subtitle, font=sub_font, fill=(180, 180, 180))

    path = os.path.join(OUT_DIR, fname)
    img.save(path, format='PNG')

print(f'Placeholders created in ./{OUT_DIR}/')