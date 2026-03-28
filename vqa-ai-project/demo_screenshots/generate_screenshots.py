"""
demo_screenshots/generate_screenshots.py
-----------------------------------------
Generates upload.png and result.png — pixel-perfect mockups of the
VQA app UI — using Pillow only.
Run once:  python demo_screenshots/generate_screenshots.py
"""
from PIL import Image, ImageDraw
import os

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 800

# ── Palette ───────────────────────────────────────────────────────────────
BG       = (10, 13, 20)
SURFACE  = (17, 21, 32)
SURFACE2 = (24, 29, 46)
ACCENT   = (255, 200, 60)
ACC_DIM  = (40, 35, 10)
TEXT     = (238, 240, 247)
MUTED    = (122, 130, 160)
FAINT    = (61, 68, 90)
BORDER   = (40, 46, 65)
SUCCESS  = (68, 224, 154)


def rr(draw, xy, r, fill, outline=None, ow=1):
    """Shorthand rounded_rectangle."""
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=ow)


def base_canvas():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # grid lines
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=(18, 22, 33), width=1)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=(18, 22, 33), width=1)
    # blobs (soft circles)
    blob = Image.new("RGB", (W, H), BG)
    bd = ImageDraw.Draw(blob)
    bd.ellipse([800, -150, 1350, 400], fill=(30, 26, 8))
    bd.ellipse([-150, 500, 450, 1050], fill=(10, 14, 35))
    img = Image.blend(img, blob, 0.35)
    d = ImageDraw.Draw(img)

    # logo chip
    rr(d, [W//2 - 60, 22, W//2 + 60, 46], 12, ACC_DIM, ACCENT, 1)
    d.text((W//2, 34), "⬡  VQA · AI", fill=ACCENT, anchor="mm")

    # title
    d.text((W//2, 78), "Visual Question Answering", fill=TEXT, anchor="mm")
    d.text((W//2, 108),
           "Upload any image  ·  Ask a question  ·  Get an answer in your language",
           fill=MUTED, anchor="mm")

    # card shadow hint
    rr(d, [148, 140, W - 148, H - 52], 18, (14, 17, 26))

    # card
    rr(d, [152, 144, W - 152, H - 56], 16, SURFACE, BORDER, 1)

    # ── steps ────────────────────────────────────────────────────────────
    steps = [
        ("1", "Upload Image",  True),
        ("2", "Ask Question",  False),
        ("3", "Get Answer",    False),
    ]
    base_x = W // 2 - 195
    for i, (num, label, active) in enumerate(steps):
        cx = base_x + i * 195
        fc = ACCENT if active else SURFACE2
        tc = (0, 0, 0) if active else MUTED
        d.ellipse([cx - 11, 178, cx + 11, 200], fill=fc, outline=ACCENT if active else BORDER, width=1)
        d.text((cx, 189), num, fill=tc, anchor="mm")
        d.text((cx + 18, 189), label, fill=ACCENT if active else MUTED, anchor="lm")
        if i < 2:
            d.line([(cx + 80, 189), (cx + 115, 189)], fill=BORDER, width=1)

    return img, d


# ─────────────────────────────────────────────────────────────────────────────
# upload.png
# ─────────────────────────────────────────────────────────────────────────────
img1, d1 = base_canvas()

# upload zone
rr(d1, [210, 222, W - 210, 422], 12, SURFACE2, (55, 65, 88), 2)
# camera emoji area
rr(d1, [W//2 - 28, 262, W//2 + 28, 318], 8, SURFACE)
d1.text((W//2, 290), "🖼", fill=TEXT, anchor="mm")

d1.text((W//2, 348), "Drop an image here, or", fill=MUTED, anchor="mm")
# "browse" underlined accent
d1.text((W//2 + 75, 348), "browse", fill=ACCENT, anchor="mm")
d1.line([(W//2 + 45, 354), (W//2 + 106, 354)], fill=ACCENT, width=1)

d1.text((W//2, 378), "PNG  ·  JPG  ·  WEBP  ·  GIF  ·  BMP     |     max 16 MB",
        fill=FAINT, anchor="mm")

# question input
d1.text((212, 442), "YOUR QUESTION", fill=FAINT, anchor="lm")
rr(d1, [210, 458, W - 210, 504], 8, SURFACE2, BORDER, 1)
d1.text((248, 481), "💬", fill=MUTED, anchor="lm")
d1.text((280, 481), "e.g. What colour is the shirt? How many people are there?",
        fill=FAINT, anchor="lm")

# language select
d1.text((212, 524), "OUTPUT LANGUAGE", fill=FAINT, anchor="lm")
rr(d1, [210, 540, W - 210, 586], 8, SURFACE2, BORDER, 1)
d1.text((248, 563), "English", fill=MUTED, anchor="lm")
d1.text((W - 235, 563), "▾", fill=MUTED, anchor="lm")

# submit button
rr(d1, [210, 608, W - 210, 658], 8, ACCENT)
d1.text((W//2, 633), "Get Answer  →", fill=(10, 13, 20), anchor="mm")

# footer
d1.text((W//2, H - 28),
        "Built with Flask · Gemini Vision · PIL · deep-translator  |  Dhanekula Institute of Engineering & Technology",
        fill=FAINT, anchor="mm")

img1.save(os.path.join(OUT, "upload.png"))
print("✓  upload.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# result.png — show an answered question
# ─────────────────────────────────────────────────────────────────────────────
img2, d2 = base_canvas()

# mark step 3 active (re-draw steps)
steps2 = [("1","Upload Image",False,"done"),
          ("2","Ask Question",False,"done"),
          ("3","Get Answer",True,"active")]
bx = W//2 - 195
for i, (num, label, active, state) in enumerate(steps2):
    cx = bx + i * 195
    if state == "done":
        fc, tc, oc = SUCCESS, (0,0,0), SUCCESS
    elif state == "active":
        fc, tc, oc = ACCENT, (0,0,0), ACCENT
    else:
        fc, tc, oc = SURFACE2, MUTED, BORDER
    d2.ellipse([cx-11,178,cx+11,200], fill=fc, outline=oc, width=1)
    d2.text((cx,189), num, fill=tc, anchor="mm")
    d2.text((cx+18,189), label,
            fill=ACCENT if state=="active" else (SUCCESS if state=="done" else MUTED),
            anchor="lm")
    if i < 2:
        lc = SUCCESS if state == "done" else BORDER
        d2.line([(cx+80,189),(cx+115,189)], fill=SUCCESS, width=1)

# thumbnail
rr(d2, [210, 222, 460, 410], 10, SURFACE2, BORDER, 1)
d2.text((335, 316), "📷", fill=MUTED, anchor="mm")
d2.text((335, 355), "download.jpg", fill=FAINT, anchor="mm")
# X remove button
d2.ellipse([440, 226, 460, 246], fill=(30,30,40), outline=BORDER, width=1)
d2.text((450, 236), "✕", fill=MUTED, anchor="mm")

# question display
rr(d2, [480, 222, W-210, 262], 8, SURFACE2, BORDER, 1)
d2.text((510, 242), "💬  What colour is the shirt?", fill=TEXT, anchor="lm")

# language badge
rr(d2, [480, 278, 564, 304], 14, ACC_DIM, ACCENT, 1)
d2.text((522, 291), "Telugu", fill=ACCENT, anchor="mm")

# character count area
rr(d2, [480, 316, W-210, 356], 8, SURFACE2, BORDER, 1)
d2.text((510, 336), "OUTPUT LANGUAGE  ▸  Telugu", fill=MUTED, anchor="lm")

# ANSWER BOX ──────────────────────────────────────────────────────────────────
rr(d2, [210, 420, W-210, 660], 12, (16, 14, 4), (100, 80, 20), 1)

# answer header row
rr(d2, [228, 438, 298, 462], 10, ACCENT)
d2.text((263, 450), "Telugu", fill=(0,0,0), anchor="mm")
d2.text((314, 450), "ANSWER", fill=MUTED, anchor="lm")
rr(d2, [W-310, 438, W-228, 462], 12, SURFACE2, BORDER, 1)
d2.text((W-269, 450), "⎘  Copy", fill=MUTED, anchor="mm")

# Telugu answer lines
d2.text((228, 488),
        "చొక్కా యొక్క రంగు ఎరుపు, మరియు ముదురు నీలి రంగు డెనిమ్ ప్యాంటుతో బాగా",
        fill=TEXT, anchor="lm")
d2.text((228, 518),
        "కలిసి ఉంటుంది. అతను పచ్చని పార్కులో నిలబడి ఉన్నాడు.",
        fill=TEXT, anchor="lm")

# english note divider
d2.line([(228, 554), (W-228, 554)], fill=(60, 50, 15), width=1)
d2.text((228, 574),
        "English:  The shirt is red, paired well with dark blue denim. He is standing in a green park.",
        fill=MUTED, anchor="lm")

# reset button
rr(d2, [W//2-115, 672, W//2+115, 706], 20, SURFACE, BORDER, 1)
d2.text((W//2, 689), "Ask Another Question", fill=MUTED, anchor="mm")

# footer
d2.text((W//2, H-28),
        "Built with Flask · Gemini Vision · PIL · deep-translator  |  Dhanekula Institute of Engineering & Technology",
        fill=FAINT, anchor="mm")

img2.save(os.path.join(OUT, "result.png"))
print("✓  result.png saved")
print("\nAll screenshots generated successfully!")
