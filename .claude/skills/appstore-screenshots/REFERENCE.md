# Reference

## Device dimensions (portrait, App Store Connect)

| Key | Device | W × H |
|-----|--------|-------|
| `iphone` | iPhone 6.9" (16 Pro Max) | 1320 × 2868 |
| `ipad` | iPad 13" (Pro M4) | 2064 × 2752 |
| `iphone65` | iPhone 6.5" (legacy) | 1242 × 2688 |

Uploading the two largest (`iphone`, `ipad`) satisfies current App Store Connect requirements;
Apple downscales for smaller devices.

## gpt-image-2 prompt template

Fill `{N}`, `{app}`, `{layout}`, paste your `copy.md` headlines into `{headlines}`, and reference the
original screenshot's style. The headlines are written in Step 2 — they are the product; the UI is proof.

```
Create ONE wide image that is exactly {N} App Store screenshots placed side by side,
portrait orientation, for the app "{app}". Match the visual style, color palette, and UI
of the attached original screenshot.

Each of the {N} panels renders this exact headline (verbatim, the dominant element, large
bold sans-serif in the top ~25-30% of the panel) with the app UI beneath it as visual proof:
{headlines}
  1) <frame 1 headline> / <optional subhead>
  2) <frame 2 headline> / <optional subhead>
  ... through N

Keep ONE brand palette across all panels. Emphasize one key word per headline in an accent
color where natural.

Layout mode: {layout}
- panorama: the background gradient/scene and the headline band flow continuously across
  all {N} panels so the full strip reads as a single connected image when scrolled.
- independent: each panel is self-contained with its own background, but shares the palette.

Constraints: headline text exactly as given and fully legible, no watermarks, no Apple logos,
high resolution, consistent margins so the strip can be cut into {N} equal vertical slices.
```

## Choosing layout (step 3)

- **Panorama** when the app is visual/lifestyle/storytelling, few features, brand-forward.
- **Independent** when each screenshot sells a distinct feature, or order may change.

Default to panorama for ≤5 frames unless `app.md` says otherwise.

## Slicing notes

- The slicer resizes the wide image to `(N × frame_W) × frame_H` before cutting, so the AI
  output size need not match exactly — composition is preserved, edges align.
- For non-uniform AI aspect ratios, generation should still target ~`N:1 × frame ratio`
  to avoid heavy distortion on resize.
- Output frames are named `01.png … 0N.png` in upload order.

## app.md template

Captures what the copy needs (the **pain** and **proof** especially) — not a feature list. See
[PLAYBOOK.md](PLAYBOOK.md).

```
# <App Name>
One-line pitch.
Audience: who uses it.
Tone: e.g. playful / premium / minimal.
Pain: the frustration the user lives with before this app.
Shift: what changes for them once they have it.
Proof: hard numbers / rank / press / a real user quote.
Hero features (the 1–2 that deliver the Shift): …
Brand colors: #...
```
