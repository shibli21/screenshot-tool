#!/usr/bin/env python3
"""Resize gpt-image-2 edit outputs to exact App Store frame dimensions.

The edit endpoint generates at a multiple-of-16 size near the device aspect; this resizes
each to the precise App Store W x H (a uniform scale, no distortion) and renames them in
order to 01.png ... 0N.png.

Usage:
  python finalize.py --indir <device>/generated/edits --device iphone \
    --outdir <device>/generated/frames
"""
import argparse, glob, os, sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required. Run: pip install pillow")

DEVICES = {
    "iphone": (1320, 2868),
    "ipad": (2064, 2752),
    "iphone65": (1242, 2688),
}


def natural_key(p):
    base = os.path.basename(p)
    digits = "".join(c for c in base if c.isdigit())
    return (int(digits) if digits else 0, base)


def main():
    ap = argparse.ArgumentParser(description="Resize edit outputs to exact App Store frames.")
    ap.add_argument("--indir", required=True, help="Folder of raw edit outputs (one per frame).")
    ap.add_argument("--device", required=True, choices=sorted(DEVICES))
    ap.add_argument("--outdir", required=True, help="Output folder for 01.png ... 0N.png.")
    ap.add_argument("--resample", default="lanczos", choices=["lanczos", "bicubic"])
    args = ap.parse_args()

    fw, fh = DEVICES[args.device]
    filt = {"lanczos": Image.LANCZOS, "bicubic": Image.BICUBIC}[args.resample]
    files = sorted(
        [f for f in glob.glob(os.path.join(args.indir, "*"))
         if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))],
        key=natural_key,
    )
    if not files:
        sys.exit(f"No images found in {args.indir}")
    if len(files) > 10:
        sys.exit("More than 10 frames (App Store limit).")

    os.makedirs(args.outdir, exist_ok=True)
    for i, f in enumerate(files, 1):
        im = Image.open(f).convert("RGB")
        if (im.width, im.height) != (fw, fh):
            im = im.resize((fw, fh), filt)
        out = os.path.join(args.outdir, f"{i:02d}.png")
        im.save(out)
        print(f"{os.path.basename(f)} -> {out}  ({fw}x{fh})")
    print(f"Done: {len(files)} frame(s) at {fw}x{fh} -> {args.outdir}")


if __name__ == "__main__":
    main()
