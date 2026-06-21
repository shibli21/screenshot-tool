---
name: appstore-screenshots
description: Generate conversion-focused, App-Store-COMPLIANT screenshots for iPhone and iPad. Write the headline copy FIRST (each frame is an ad: pain → shift → proof → delivery), then generate the WHOLE SET as one connected strip in a single gpt-image-2 edit pass (image-to-image via the fal MCP tool) — feeding the user's REAL screenshots so the actual app UI is preserved while AI builds the headlines, device frames, and a continuous background on one locked grid, then slice into exact frames. Use when the user wants to create or rewrite iOS/iPad App Store marketing screenshots, write screenshot caption/headline copy, turn raw app screenshots into polished store frames, or prepare images for App Store Connect.
---

# App Store Screenshots

Three rules decide whether a set converts and whether Apple accepts it:

1. **The headline is ~70% of conversion** — not the UI. A copy-only rewrite has driven +80%
   conversion on unchanged screens. So **each frame is an ad**, not a screen tour: write the words
   first, render the real screen beneath them as proof.
2. **Edit, don't fake.** Feed gpt-image-2 the user's **real screenshots as input images**
   (image-to-image); it builds the headline, device frame, and background *around the untouched UI*.
   **Never** text-to-image a frame — AI-invented UI is garbled and misrepresentative, which App Store
   Connect rejects (guideline 2.3.10). The real UI must survive unchanged.
3. **One strip, one grid.** Generate the **whole set as a single wide strip in one edit pass** (all N
   screenshots in, one image out), then slice it. One generation = one coordinate system = devices,
   headlines, and background **locked to an identical grid** across every frame. This is what makes a
   set look designed instead of assembled. (Per-frame generation is a fallback — see Method B.)

## Prerequisites

- **fal MCP server connected** with the **edit** endpoint `openai/gpt-image-2/edit` (image-to-image).
  Find it: `ToolSearch("fal image generation")`. If no fal edit tool exists, STOP and tell the user.
- **Python 3 + Pillow** for upload + slice/resize (`pip install pillow`).
- A **FAL key** to upload local screenshots (`scripts/fal_upload.py` reads `$FAL_KEY`), OR
  `mcp__fal-ai__upload_file` (base64) for files <1 MB.

## Folder layout (one device at a time)

```
<app-name>/
├── app.md                 # app pitch, audience, the user's PAIN, proof points (feeds copy)
├── copy.md                # headlines per frame (Step 2 output — written before any image)
├── ios/
│   ├── original/          # input: the user's REAL iPhone screenshots (one per frame)
│   └── generated/
│       ├── strip.png      # the single wide edit output (Method A, pre-slice)
│       └── frames/        # output: 01.png … 0N.png at exact App Store dims
└── ipad/{original/, generated/{strip.png, frames/}}
```
iPad is optional — skip it if `ipad/original/` is empty.

## Exact dimensions (portrait)

| Device | Key | Frame W × H | Strip gen size (Method A) |
|--------|-----|-------------|---------------------------|
| iPhone 6.9" (16 Pro Max) | `iphone` | 1320 × 2868 | width 3840, height = round₁₆(3840 / (N × 0.46)) — e.g. N=5 → 3840×1664 |
| iPad 13" (Pro M4) | `ipad` | 2064 × 2752 | width 3840, height = round₁₆(3840 / (N × 0.75)) — e.g. N=5 → 3840×1024 |

gpt-image-2 limits: multiples of 16, ≤3:1, ≤3840 px/edge. `slice.py` resizes the strip to
`(N × frame_W) × frame_H` then cuts — composition preserved, edges exact. Up to 10 frames/device;
default **N = 5**.

## The converting sequence

A set tells ONE story, in order. Each frame does one job, carries one message — if it needs two
sentences, split it into two frames. The default spine for N = 5:

1. **Pain** — name the frustration the user lives with before the app.
2. **Shift** — the after: what changes once they have it.
3. **Proof** — a hard number, rank, press logo, or real user quote (emotional proof if none exist).
4. **Delivery** — the one or two features that deliver the Shift's promise (×2 for N=5).

This is the *single source of truth* for the sequence. [PLAYBOOK.md](PLAYBOOK.md) holds the copy craft;
[REFERENCE.md](REFERENCE.md) holds the design spec, both prompt templates, and endpoint details.

## Workflow (process each device fully, then the next)

1. **Gather inputs.** Read every screenshot in `original/` and read `app.md`. If `app.md` lacks the
   user's **pain** and **proof points**, ask for them. Ask for N if unspecified (default 5).
   *Done when:* you can name the pain in one sentence and have N.

2. **Write the copy first — before any image.** Read [PLAYBOOK.md](PLAYBOOK.md). For each frame write a
   headline of **≤8 words** (mark one emphasis word); subheads are optional and usually cut (they vanish
   at thumbnail scale). Follow the converting sequence. **Show what changes; never name a feature.**
   Save to `copy.md`. *Done when all three pass:* every headline ≤8 words; **cover-the-UI test**
   (headlines alone tell pain→shift→proof→delivery, not a feature list); **shuffle test** (reordering
   any two frames breaks the story).

3. **Map + art-direct.** Pick the ONE real screenshot that proves each frame's headline. Choose a
   **locked design system** held identical across ALL frames: one palette (1 background + 1 accent +
   neutrals), one device treatment (realistic bezel with 9:41 / bezelless card / tilt), one headline
   position. See the design spec in [REFERENCE.md](REFERENCE.md); state your choices, let the user
   override. *Done when:* every frame has a screenshot + one shared design direction.

4. **Upload the source screenshots** to fal:
   `python scripts/fal_upload.py "<path>"` (prints a CDN URL), once per screenshot, in order.
   *Done when:* every frame has an `image_urls` URL.

5. **Generate.** Default to **Method A**; use **Method B** only when N>6 or a busy screen needs max
   fidelity/sharpness (see [REFERENCE.md](REFERENCE.md) for both prompt templates).
   - **Method A — single strip (default).** ONE call to `openai/gpt-image-2/edit` with
     `image_urls = [all N screenshot URLs, in frame order]`, the **strip prompt** (grid declaration +
     per-panel headlines verbatim + the locked design system + the fidelity clause), `image_size` =
     the strip gen size, `quality:"high"`. Save to `generated/strip.png`, then
     `python scripts/slice.py --input generated/strip.png --device iphone --frames N --outdir
     generated/frames`.
   - **Method B — per-frame (fallback).** One edit call per frame (`image_urls=[that frame]`, the
     per-frame prompt), then `python scripts/finalize.py --indir generated/edits --device iphone
     --outdir generated/frames`.
   *Done when:* N frames exist at the exact device W×H.

6. **Verify — the UI must survive unchanged.** Open each finalized frame beside its `original/`
   screenshot and check, per frame: (a) **fidelity** — no app text/icon/layout altered, garbled, or
   invented; (b) headline matches `copy.md`, spelled exactly; (c) status bar reads 9:41 (or your
   choice); (d) one message; (e) **grid** — device size, floor line, and headline baseline match the
   other frames. **Re-roll on failure:** for Method A, re-run Step 5 strengthening the weak panel's
   line; if one panel keeps failing fidelity, regenerate just that frame with Method B and swap it in.
   Then re-run the cover-the-UI test on the outputs. *Done when:* all N frames pass (a)–(e). Process
   the next device.
