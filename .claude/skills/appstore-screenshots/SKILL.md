---
name: appstore-screenshots
description: Generate conversion-focused App Store screenshots for iPhone and iPad — write the headline copy FIRST (each frame is an ad: pain → shift → proof → feature), then AI-generate ONE wide image (gpt-image-2 via the fal MCP tool) styled after the user's original screenshot and slice it into exact App Store frame dimensions with a local script. Use when the user wants to create or rewrite iOS/iPad App Store marketing screenshots, write screenshot caption/headline copy, generate N screenshots from an original, build visually-connected screenshot panoramas, or prepare images for App Store Connect.
---

# App Store Screenshots

**The text overlay is ~70% of what converts — not the UI.** Rewriting copy alone has driven an 80%
conversion lift on unchanged screens. So treat each frame as **an ad**, not a screen tour: write the
words first, then render the UI beneath them as visual proof.

Render trick: AI-generate ONE wide image (your headlines + UI styled after the original), then slice
it locally into exact App Store frames.

## Prerequisites

- **fal MCP server connected** with `gpt-image-2`. Find the tool first:
  `ToolSearch("fal image generation")` or `ToolSearch("select:<tool_name>")`. If no fal tool
  exists, STOP and tell the user to configure the fal MCP server.
- **Python 3 + Pillow** for slicing (`pip install pillow`).

## Folder layout (one device at a time)

```
<app-name>/
├── app.md                 # app description, audience, the user's PAIN, proof points (feeds copy)
├── copy.md                # the written headlines per frame (Step 2 output — written before any image)
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

## The converting sequence

A screenshot set tells ONE story, in order. Each frame does one job, carries one message — if it
needs two sentences, split it into two frames. The default spine for N = 5:

1. **Pain** — name the frustration the user lives with before your app.
2. **Shift** — the after: what changes for them once they have it.
3. **Proof** — a hard number, rank, press logo, or real user quote.
4. **Delivery** — the one or two features that actually deliver the Shift's promise.

This is the *single source of truth* for the sequence; [PLAYBOOK.md](PLAYBOOK.md) holds the copy craft
and a library of real headlines drawn from ~167 example sets.

## Workflow (process each device fully, then the next)

1. **Gather inputs.** Read `original/` screenshot(s) and `app.md`. If `app.md` is missing the user's
   **pain** and **proof points**, ask for them — copy can't be written without them. Ask for N if
   unspecified (default 5).
2. **Write the copy first — before any image.** For each of the N frames write a headline of **≤8
   words** plus an optional one-line subhead, following the converting sequence. **Show what changes;
   never name a feature** ("workout tracking" → "never forget what you lifted again"). Save to
   `copy.md`. Read [PLAYBOOK.md](PLAYBOOK.md) before writing.
   **Done when all three pass:**
   - every frame has a headline of ≤8 words (count them);
   - **cover-the-UI test** — cover the mockups, read only the headlines top to bottom: they tell the
     pain → shift → proof → delivery story, not a feature list;
   - **shuffle test** — reorder any two frames and the story breaks (if it survives, you have a
     catalog, not an ad — rewrite).
3. **Decide layout.** **Visually-connected panorama** (background/headline band flows continuously
   across frames) vs **independent frames**. State your choice; let the user override. See
   [REFERENCE.md](REFERENCE.md).
4. **Build the prompt.** Instruct gpt-image-2 to produce ONE wide image = the N frames side by side,
   styled after the original screenshot. Embed **your `copy.md` headlines verbatim**, each rendered as
   the dominant element with the app UI beneath it as proof. Prompt template in
   [REFERENCE.md](REFERENCE.md).
5. **Generate** via the fal MCP tool (`gpt-image-2`). Save to `<device>/generated/wide_strip.png`.
6. **Slice** to exact dimensions:
   ```
   python scripts/slice.py --input <device>/generated/wide_strip.png \
     --device iphone --frames 5 --outdir <device>/generated/frames
   ```
   Resizes the wide image to exactly `(N × frame_W) × frame_H` (preserving composition), then cuts N
   equal vertical slices at the precise App Store dimension.
7. **Verify & repeat.** On the rendered frames: each headline is legible, matches `copy.md`, carries
   one message; rerun the cover-the-UI test on the output. Then process the next device.
