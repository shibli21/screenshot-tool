---
name: appstore-screenshots
description: Generate App Store screenshots for iPhone and iPad using AI (gpt-image-2 via the fal MCP tool) from an original app screenshot, then slice the wide AI image into exact App Store frame dimensions with a local script. Use when the user wants to create iOS/iPad App Store marketing screenshots, generate N screenshots from an original, build visually-connected screenshot panoramas, or prepare images for App Store Connect.
---

# App Store Screenshots

Generate N App Store frames per device by (1) AI-generating ONE wide image styled after the
user's original screenshot, then (2) slicing it locally into exact App Store dimensions.

## Prerequisites

- **fal MCP server connected** with `gpt-image-2`. Find the tool first:
  `ToolSearch("fal image generation")` or `ToolSearch("select:<tool_name>")`. If no fal tool
  exists, STOP and tell the user to configure the fal MCP server.
- **Python 3 + Pillow** for slicing (`pip install pillow`).

## Folder layout (one device at a time)

```
<app-name>/
├── app.md                 # optional: app description, audience, tone (feeds the AI prompt)
├── ios/
│   ├── original/          # input: raw iPhone screenshot(s) — style/content reference
│   └── generated/
│       ├── wide_strip.png # the single wide AI image (pre-slice)
│       └── frames/        # output: 01.png … 0N.png at exact App Store dims
└── ipad/
    ├── original/
    └── generated/{wide_strip.png, frames/}
```
iPad is optional — skip the `ipad` device if `ipad/original/` is empty.

## Exact dimensions (portrait)

| Device | Key | Frame W × H |
|--------|-----|-------------|
| iPhone 6.9" (16 Pro Max) | `iphone` | 1320 × 2868 |
| iPad 13" (Pro M4) | `ipad` | 2064 × 2752 |

Up to 10 frames/device; default **N = 5**.

## Workflow (process each device fully, then the next)

1. **Gather inputs.** Read `original/` screenshot(s) and `app.md` (if present). Ask the user for
   N if unspecified (default 5).
2. **Decide layout.** Based on `app.md`/screenshots, YOU choose **visually-connected panorama**
   (background/headline flow continuously across frames) vs **independent frames**. State your
   choice; let the user override.
3. **Build the prompt.** Instruct gpt-image-2 to produce ONE wide image = `N` App Store frames
   side by side, styled after the original screenshot, full UI + headlines. For panorama mode,
   add "background, color, and headline band flow continuously across all N frames so the strip
   reads as one image when scrolled." Request the largest output the model allows.
4. **Generate** via the fal MCP tool (`gpt-image-2`). Save to `<device>/generated/wide_strip.png`.
5. **Slice** to exact dimensions:
   ```
   python scripts/slice.py --input <device>/generated/wide_strip.png \
     --device iphone --frames 5 --outdir <device>/generated/frames
   ```
   The script resizes the wide image to exactly `(N × frame_W) × frame_H` (preserving the AI
   composition), then cuts N equal vertical slices at the precise App Store dimension.
6. **Verify & repeat** for the next device.

See [REFERENCE.md](REFERENCE.md) for prompt templates and the device dimension table.
