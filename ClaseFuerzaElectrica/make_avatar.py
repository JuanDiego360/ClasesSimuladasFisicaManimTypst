"""Recorta avatar.png en un círculo real y lo guarda como avatar_circle.png."""
from PIL import Image
import numpy as np
from pathlib import Path

src = Path("avatar.png")
dst = Path("avatar_circle.png")
img = Image.open(src).convert("RGBA")
size = min(img.size)
img = img.crop(((img.size[0] - size) // 2, (img.size[1] - size) // 2,
                (img.size[0] + size) // 2, (img.size[1] + size) // 2))
img = img.resize((512, 512), Image.LANCZOS if hasattr(Image, "LANCZOS") else Image.ANTIALIAS)
arr = np.array(img)
h, w = arr.shape[:2]
yy, xx = np.ogrid[:h, :w]
cx, cy = w / 2, h / 2
r = min(cx, cy)
mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= r ** 2
arr[..., 3] = (arr[..., 3] * mask).astype(np.uint8)
Image.fromarray(arr, "RGBA").save(dst)
print(f"OK -> {dst}  ({dst.stat().st_size} bytes)")
