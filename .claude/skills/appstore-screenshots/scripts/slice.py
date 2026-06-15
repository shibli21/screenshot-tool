#!/usr/bin/env python3
"""Slice one wide AI-generated image into N exact App Store frames.

Resizes the wide image to exactly (N x frame_W) x frame_H so the AI composition is
preserved, then cuts N equal vertical slices at the precise App Store dimension.
"""
import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required. Run: pip install pillow")

# Exact App Store Connect portrait dimensions (W, H).
DEVICES = {
    "iphone": (1320, 2868),   # iPhone 6.9" (16 Pro Max)
    "ipad": (2064, 2752),     # iPad 13" (Pro M4)
    # legacy / optional:
    "iphone65": (1242, 2688), # iPhone 6.5"
}


def main():
    p = argparse.ArgumentParser(description="Slice a wide image into N App Store frames.")
    p.add_argument("--input", required=True, help="Path to the wide AI image.")
    p.add_argument("--device", required=True, choices=sorted(DEVICES),
                   help="Target device dimension key.")
    p.add_argument("--frames", type=int, required=True, help="Number of frames (1-10).")
    p.add_argument("--outdir", required=True, help="Output directory for frames.")
    p.add_argument("--resample", default="lanczos",
                   choices=["lanczos", "bicubic", "nearest"],
                   help="Resampling filter for resize (default lanczos).")
    args = p.parse_args()

    if not 1 <= args.frames <= 10:
        sys.exit("--frames must be between 1 and 10 (App Store limit).")
    if not os.path.isfile(args.input):
        sys.exit(f"Input not found: {args.input}")

    fw, fh = DEVICES[args.device]
    target_w = fw * args.frames
    filt = {"lanczos": Image.LANCZOS, "bicubic": Image.BICUBIC,
            "nearest": Image.NEAREST}[args.resample]

    os.makedirs(args.outdir, exist_ok=True)
    img = Image.open(args.input).convert("RGB")
    if (img.width, img.height) != (target_w, fh):
        img = img.resize((target_w, fh), filt)

    for i in range(args.frames):
        left = i * fw
        frame = img.crop((left, 0, left + fw, fh))
        out = os.path.join(args.outdir, f"{i + 1:02d}.png")
        frame.save(out)
        print(f"wrote {out}  ({fw}x{fh})")

    print(f"Done: {args.frames} frame(s) at {fw}x{fh} -> {args.outdir}")


if __name__ == "__main__":
    main()
