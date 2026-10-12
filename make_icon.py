"""Genera icona per Estrai P7M: PDF con freccia di estrazione."""
from PIL import Image, ImageDraw, ImageFont
import os, subprocess, shutil

SIZE = 512

def make_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size

    # Sfondo documento (rettangolo arrotondato bianco/grigio chiaro)
    fold = int(s * 0.18)
    doc_left   = int(s * 0.12)
    doc_right  = int(s * 0.78)
    doc_top    = int(s * 0.06)
    doc_bottom = int(s * 0.88)

    # Ombra
    d.rounded_rectangle(
        [doc_left+4, doc_top+6, doc_right+4, doc_bottom+6],
        radius=int(s*0.06), fill=(0,0,0,60)
    )
    # Corpo documento
    d.rounded_rectangle(
        [doc_left, doc_top, doc_right, doc_bottom],
        radius=int(s*0.06), fill=(245, 245, 250, 255), outline=(200,200,210,255), width=2
    )
    # Orecchio (angolo in alto a destra)
    ear_x = doc_right - fold
    ear_y = doc_top + fold
    d.polygon([
        (ear_x, doc_top),
        (doc_right, doc_top),
        (doc_right, ear_y),
    ], fill=(200, 200, 210, 255))
    d.polygon([
        (ear_x, doc_top),
        (doc_right, ear_y),
        (ear_x, ear_y),
    ], fill=(220, 220, 230, 255))

    # Testo "PDF" in rosso
    cx = (doc_left + doc_right) // 2
    cy = int(s * 0.42)
    font_size = int(s * 0.22)
    font = None
    for path in [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, font_size)
                break
            except Exception:
                continue
    if font is None:
        font = ImageFont.load_default()
    bbox = d.textbbox((0, 0), "PDF", font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((cx - tw//2, cy - th//2), "PDF", font=font, fill=(210, 40, 40, 255))

    # Linee documento (simulano righe di testo)
    line_color = (180, 180, 195, 200)
    lx1, lx2 = int(s*0.22), int(s*0.68)
    for ly in [int(s*0.64), int(s*0.72), int(s*0.80)]:
        d.rounded_rectangle([lx1, ly, lx2, ly+int(s*0.04)], radius=2, fill=line_color)

    # Freccia verde "estrazione" in basso a destra (sovrapposta)
    ax = int(s * 0.62)
    ay = int(s * 0.58)
    ar = int(s * 0.30)  # raggio cerchio sfondo

    # Cerchio verde
    d.ellipse([ax - ar, ay - ar, ax + ar, ay + ar], fill=(34, 160, 80, 240))

    # Freccia bianca verso il basso (download/estrazione)
    fw = int(ar * 0.45)
    fh = int(ar * 0.55)
    fx, fy = ax, ay
    # gambo
    stem_w = int(fw * 0.45)
    d.rectangle([fx - stem_w, fy - fh, fx + stem_w, fy], fill=(255,255,255,255))
    # punta freccia
    pts = [
        (fx - fw, fy),
        (fx + fw, fy),
        (fx, fy + fh),
    ]
    d.polygon(pts, fill=(255,255,255,255))

    return img


# Genera tutte le dimensioni necessarie per un .icns
sizes = [16, 32, 64, 128, 256, 512, 1024]
iconset_dir = "/tmp/EstraiP7M.iconset"
os.makedirs(iconset_dir, exist_ok=True)

for sz in sizes:
    img = make_icon(sz)
    img.save(f"{iconset_dir}/icon_{sz}x{sz}.png")
    if sz <= 512:
        img2x = make_icon(sz * 2)
        img2x.save(f"{iconset_dir}/icon_{sz}x{sz}@2x.png")

# Crea .icns
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EstraiP7M.icns")
subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", out], check=True)
print(f"Icona creata: {out}")
shutil.rmtree(iconset_dir)
