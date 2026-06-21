# Reference

The design spec, both edit prompt templates, and the fal endpoint details. Distilled from ~82
professional App Store sets in `examples/screenshotfirst/` plus gpt-image-2 prompt practice
(grid composition, input fidelity).

## Device dimensions (portrait, App Store Connect)

| Key | Device | Frame W × H | Per-frame edit size (Method B) |
|-----|--------|-------------|--------------------------------|
| `iphone` | iPhone 6.9" (16 Pro Max) | 1320 × 2868 | 1296 × 2816 |
| `ipad` | iPad 13" (Pro M4) | 2064 × 2752 | 2048 × 2736 |
| `iphone65` | iPhone 6.5" (legacy) | 1242 × 2688 | 1216 × 2624 |

**Strip gen size (Method A):** width 3840, height = round-to-16 of `3840 / (N × frameAspect)` where
frameAspect = W/H (iphone ≈ 0.46, ipad ≈ 0.75). N=5 iphone → **3840 × 1664**. gpt-image-2 limits:
multiples of 16, ≤3:1, ≤3840 px/edge. `slice.py` then resizes to `(N × frameW) × frameH` and cuts.

## The edit endpoint

`openai/gpt-image-2/edit` (image-to-image) — builds a new image *around* input images while keeping
them. Local screenshots must be uploaded first (the endpoint takes URLs): `scripts/fal_upload.py`
(reads `$FAL_KEY`) or `mcp__fal-ai__upload_file` (base64, <1 MB). Calls usually return
`status:"processing"` → poll `check_job` → `get_job_result`.

| param | Method A (strip) | Method B (per-frame) |
|-------|------------------|----------------------|
| `image_urls` | all N screenshot URLs, **in frame order** | `[ this frame's URL ]` |
| `image_size` | strip gen size, e.g. `{width:3840,height:1664}` | `{width:1296,height:2816}` |
| `quality` | `"high"` | `"high"` |
| `output_format` | `"png"` | `"png"` |

## Method A vs B — which to use

- **Method A — single strip (DEFAULT).** All N screenshots → one generation → one wide strip → slice.
  *Wins:* one coordinate system locks device size, headline baseline, and a continuous background to an
  identical grid across all frames; maximum cohesion; one billed generation. *Cost:* each panel is
  `3840/N` px wide, upscaled to the frame on slice (N=5 → 768→1320, mild softening). Best for **N ≤ 6**.
- **Method B — per-frame (FALLBACK).** One edit per frame at near-native size. *Wins:* sharper per-frame
  UI; needed for **N ≥ 7** (Method A panels get too small to read). *Cost:* device size/position and
  bezel shape drift between frames — verify the grid and re-roll outliers.
- **Optional sharpness pass:** after Method A, upscale each sliced frame ~2× with a fal upscaler
  (`search_models("upscale")`) to recover detail while keeping the locked grid. Use when the app UI is
  text-dense.

## Edit prompt — Method A (single strip)

The **grid declaration** and the **fidelity clause** are the two load-bearing parts. Keep the design
block byte-identical for every panel; vary only the per-panel headline.

```
Create ONE wide landscape image: exactly {N} equal-width portrait panels side by side, forming a
single connected App Store screenshot strip for "{app}". The panels share ONE continuous background
and an IDENTICAL layout grid, so the set looks perfectly aligned and cohesive when scrolled.

{N} reference screenshots of the REAL app UI are provided, in order. They are the one and only UI
reference: reproduce each EXACTLY with high fidelity — do not redesign, simplify, re-typeset, or
alter any text, icon, color, or layout in any way. Panel 1 shows reference image 1, panel 2 image 2,
… panel {N} image {N}.

Shared design system, IDENTICAL in every panel:
- Background: {background — e.g. deep charcoal #15110D with a soft warm radial glow}, flowing
  continuously across the whole strip. Locked palette: {bg} + {accent} + neutrals only.
- Place each panel's screenshot inside {device treatment — e.g. a realistic black iPhone with thin
  even bezels, rounded corners, and a Dynamic Island} — SAME size and SAME vertical position in
  every panel, floating with a soft drop shadow and a subtle rim-light so it separates from the
  background; bottom bleeds slightly off the panel edge.
- Status bar in every phone: 9:41 left, full signal + wi-fi + battery right (clean iOS).
- Each panel: headline in the top ~22%, large bold white sans-serif, 1-2 lines, tight leading, SAME
  baseline in every panel, exactly one word in {accent}. Spell each exactly:
  Panel 1: {HEADLINE 1}  (accent word: {EMPH 1})
  … Panel {N}: {HEADLINE N}  (accent word: {EMPH N})

Premium editorial App Store quality, crisp legible typography, equal margins so the strip cuts into
{N} equal vertical panels. No watermark, no Apple logo, no extra UI, zero AI artifacts.
```

## Edit prompt — Method B (per-frame)

```
Turn the attached iPhone app screenshot into a premium App Store marketing screenshot, PORTRAIT.

CRITICAL: the attached image is the real app UI and the one and only reference. Reproduce it EXACTLY
and unchanged inside the phone screen — do not redesign, simplify, re-typeset, translate, or move ANY
text, icon, color, card, or layout in any way. The only NEW things you add are the device frame,
background, status-bar icons, and the headline.

Composition:
- Background: {background}. One locked palette: {bg} + {accent} + neutrals.
- Place the screenshot inside {device treatment}, floating in the LOWER ~62%, centered, soft drop
  shadow; bottom bleeds slightly off the frame edge.
- Status bar: 9:41 left, full signal + wi-fi + battery right (clean iOS).
- Top ~25%: headline in large bold white sans-serif, 1-2 lines, centered, tight leading:
  "{HEADLINE}". Render ONLY {EMPH} in {accent}; rest white. Spell exactly.

No watermark, no Apple logo, no extra UI. High resolution, crisp text, zero AI artifacts.
```

## Design spec (what the pros do — fold into the prompt's design block)

Ranked across the corpus: **DOMINANT** (>50% of sets) / COMMON / OCCASIONAL.

- **Layout** — DOMINANT: *independent-shared-palette* — each frame a self-contained ad unified by ONE
  locked palette, one type system, one accent, a repeated device recipe. (Method A renders this as a
  continuous strip but keeps each panel a self-contained ad.) DOMINANT: fixed grid rhythm — headline
  top band, device below, identical margins frame to frame.
- **Background** — DOMINANT: one locked palette is the primary continuity device; flat solid color or a
  soft single-color gradient. COMMON: per-frame hue rotation within one family; full-bleed lifestyle
  photo for the hero only.
- **Device** — DOMINANT: real UI ALWAYS, in a realistic bezel (Dynamic Island + 9:41) OR a bezelless
  rounded card, floating with a soft shadow in the lower ~65-75%. COMMON: partial bottom bleed; slight
  3D tilt (~5-15°) with a second screen peeking for depth.
- **Headline** — DOMINANT: top band ~18-30%, heavy bold sans, 1-2 lines, high contrast. DOMINANT:
  two-tier structure (small eyebrow + giant phrase) OR headline only. COMMON: ≤8 words, benefit-led;
  small ALL-CAPS letter-spaced eyebrow above.
- **Emphasis** — DOMINANT: recolor ONE word to the single accent. COMMON: size-jump a key number 2-3×.
- **Proof** — DOMINANT: concrete real numbers shown *inside* the UI (not zeroed states). COMMON: star
  rating + count pill; hard usage number; laurel/rank badge; **front-loaded on frame 1**.
- **Decorations** — DOMINANT: floating "pulled-out" UI callout chips lifted from the real app, each
  shadowed. COMMON: soft shadows under everything; stickers only for Gen-Z social, restrained for B2B.

### Composition archetypes (pick per frame; keep the system consistent)

1. **Solid-Color Feature Card** — the workhorse: flat brand color, bold headline top, one real
   screenshot floating center-low. Default for productivity/finance/health/utility and frames 2-N.
2. **Hero / Cover Frame** — device-free or device-secondary opener: big logo or giant claim + front-
   loaded proof (rating, laurel, user count, press). Use as frame 1 when you have real proof.
3. **Lifestyle-Photo Hero** — full-bleed graded photo, giant overlaid headline. Social/dating/travel.
4. **UI-Extraction Spotlight** — no full phone; one real UI component floated oversized as proof.
5. **Tilted-Device Depth** — real phone rotated ~8-15° with a second screen behind + corner callouts.
6. **Panorama Strip** — one continuous background across all N frames; Method A is the clean way to
   build it.

### Render rules (relative to a 1320 × 2868 frame; express as prompt guidance)

- Keep text/critical UI ≥96 px from sides, ≥80 px from top; ~128 px bottom safe area.
- Headline zone ~ top 22-25%. Device top ~ y≈980; bottom bleeds past the edge.
- Heavy bold sans, tight leading (1.05-1.15), 1-2 lines, contrast ≥4.5:1. Subheads usually cut.
- One bg color + one accent + neutrals, **locked across all N frames**; accent = the emphasis word.
- Identical headline baseline and device floor across frames (Method A enforces this automatically).
- **Contrast guard:** on a dark app over a dark background, add a subtle rim-light/glow behind the
  device so it separates — dark-on-dark flattens the set.

## Compliance (App Store Connect)

- **Real UI only** in every frame — never AI-generate, redraw, or fabricate interface elements (2.3.10).
  This is why we use the *edit* endpoint with real screenshots as input, never text-to-image.
- Each frame ends at the **exact** dimension; resize uniformly, never upscale a tiny image beyond the
  Method-A panel ratio.
- Show authentic legible UI: real data, status bar 9:41 with plausible indicators — no blank/garbled.
- AI adds only the device frame, background, status-bar icons, and headline text.
- No Apple logos, no App Store badges, no fabricated awards/ratings; proof claims must be true.

## Fidelity guardrails (the one failure mode that matters)

Edit models can subtly re-render UI text or warp a layout. Defenses, in order:
1. Keep the **fidelity clause** verbatim ("the one and only reference … do not alter in any way") and
   `quality:"high"`.
2. **Verify every frame** against its original (Step 6); re-roll any that altered/garbled the UI.
3. If one panel in a strip keeps mutating, regenerate just that frame with **Method B** and swap it in.
4. Persistent low fidelity → fall back to `fal-ai/gpt-image-1.5/edit` with `input_fidelity:"high"`.
5. Busy status bars: pre-clean a 9:41 status bar onto the source in PIL before upload so the model
   changes less.
