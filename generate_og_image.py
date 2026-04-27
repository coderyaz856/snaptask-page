"""Generate 1200x630 og-image.png for snaptask.org social previews."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).parent / "og-image.png"
SCREEN = Path(__file__).parent.parent / "snaptask_visuals" / "screen2_notification.png"

W, H = 1200, 630

# Gradient background (matches site hero: #0066ff -> #0044cc)
img = Image.new("RGB", (W, H), "#0066ff")
draw = ImageDraw.Draw(img)
top = (0, 102, 255)
bot = (0, 68, 204)
for y in range(H):
    t = y / H
    r = int(top[0] * (1 - t) + bot[0] * t)
    g = int(top[1] * (1 - t) + bot[1] * t)
    b = int(top[2] * (1 - t) + bot[2] * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Phone screenshot on right side, scaled to fit
phone = Image.open(SCREEN).convert("RGBA")
phone_h = H - 80  # leave 40px margin top/bottom
ratio = phone_h / phone.height
phone_w = int(phone.width * ratio)
phone = phone.resize((phone_w, phone_h), Image.LANCZOS)

# Add subtle drop shadow under phone
shadow = Image.new("RGBA", (phone_w + 40, phone_h + 40), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(shadow)
sdraw.rounded_rectangle((20, 20, phone_w + 20, phone_h + 20), radius=40, fill=(0, 0, 0, 80))
shadow = shadow.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(15))

phone_x = W - phone_w - 60
phone_y = 40
img.paste(shadow, (phone_x - 20, phone_y - 10), shadow)
img.paste(phone, (phone_x, phone_y), phone)

# Text on left side
def load_font(size, bold=False):
    candidates = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    return ImageFont.load_default()

font_brand = load_font(38, bold=True)
font_title = load_font(64, bold=True)
font_sub = load_font(28)
font_cta = load_font(26, bold=True)

text_x = 60
draw.text((text_x, 70), "SnapTask", font=font_brand, fill=(255, 214, 10))

title_lines = ["Capture tasks", "without opening", "any app."]
y = 140
for line in title_lines:
    draw.text((text_x, y), line, font=font_title, fill="white")
    y += 78

draw.text((text_x, y + 30),
          "Type in your notification bar.",
          font=font_sub, fill=(220, 230, 255))
draw.text((text_x, y + 65),
          "17 languages. 100% offline.",
          font=font_sub, fill=(220, 230, 255))

# CTA pill
cta_x, cta_y, cta_w, cta_h = text_x, H - 90, 280, 56
draw.rounded_rectangle((cta_x, cta_y, cta_x + cta_w, cta_y + cta_h),
                       radius=12, fill=(255, 214, 10))
draw.text((cta_x + 32, cta_y + 14), "snaptask.org", font=font_cta, fill=(26, 26, 26))

img.save(OUT, "PNG", optimize=True)
print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
