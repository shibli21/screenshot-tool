# Screenshot Copy Playbook

The copy craft behind Step 2. Sources: @designerants' best practices (1,000+ App Store screenshots
optimized; one rewrite drove +80% conversion), via Paul Solt's "The Screenshot Mistake That's Costing
You Downloads" — plus patterns distilled from ~167 real sets in `examples/screenshotfirst/`.

## Text is the product

The UI is evidence; the text is the argument. Write the headline **before** the screen exists — if you
can't name the change in 8 words, you don't understand it yet, and the UI behind it is just visual proof.

A user scanning your page asks **"is this for me?"**, not "what does it do?". Feature labels ("Dark
mode", "iCloud sync", "Customizable widgets") are true and useless — they answer the wrong question and
read like patch notes to someone who hasn't bought in.

## Show what changes — feature → outcome

Specificity makes the promise real. "Productivity app" is invisible; "Never lose a meeting note again"
is a reason to download. Rewrite every feature label as the user's life *after* the app:

| Feature label (don't) | Outcome (do) |
|---|---|
| customizable dashboard | see everything that matters, at a glance |
| workout tracking | you'll never forget what you lifted again |
| Notes → Slides. Instantly. | Stop designing slides — write notes, start presenting |
| Auto-numbering that works | Never fix slides manually again |
| Full screen, readable | Stay focused while you present |

## Examples for each stage

(The four stages — Pain, Shift, Proof, Delivery — are defined in [SKILL.md](SKILL.md). Headlines below
are models for each.)

- **Pain** — "Buried in notes you'll never find again?" · "Family chaos." · "Stop drowning in school
  emails." · "Bye bye boredom."
- **Shift** — "Everything you capture, organized automatically." · "Turn chaos into progress." · "Take
  control of your time." · "Process your inbox in 6 min a week."
- **Proof** — see proof devices below.
- **Delivery** — keep it benefit-led, not a label: "Block distractions. Stay on task." · "Track your
  bus in real time." · utility apps teach the gesture as the benefit ("Pull down to add", "Swipe right
  to check off").

## Proof devices (recurring in the corpus)

- **Hard numbers**: "Trusted by 1.8 billion seated diners each year" (OpenTable) · "190+ million people
  helping each other" (GoFundMe) · "Trusted by +40M individuals, families and teams".
- **Rank badge**: "#1 Prayer App for Lent" · "The No.1 Self-Discovery Companion" · "App of the Day".
- **Rating + count**: "4.8 ★ · 700+ reviews".
- **Press logos**: Forbes, TIME, The Washington Post, ELLE, Reader's Digest.
- **A real testimonial as the headline**: "This is where my soul is finding peace."
- **Concrete numbers inside the UI** beat empty states — show real $ amounts, step counts, calories,
  refunds, not zeroed placeholders.

## Visual patterns (render guidance for Step 4)

Distilled across ~68 closely-read sets — fold these into the gpt-image-2 prompt:

- **One brand palette across ALL frames** — usually a single saturated background color, high-contrast
  headline. Color carries continuity even in "independent" layouts.
- **Headline in the top ~25–30%**, the device/UI beneath it as proof (the dominant pattern).
- **Emphasize one word** in an accent color or italic: "Meet *new* people offline" · "Bye bye
  *boredom*" · "your best *great* meal".
- **Mockup style by category**: flat UI on a color field for productivity/finance; hands-holding-phone
  or a lifestyle photo behind the device for social/dating/consumer/lifestyle.
- **Human touches**: handwritten annotations and arrows ("planned!", "start now!", "Done!") make a set
  feel personal rather than corporate.
- **Big bold sans-serif headlines**; subheads small and secondary, one line.

## Study the corpus before writing

Pull 5–10 real sets in your app's category before drafting copy:

- `examples/screenshotfirst/` — ~167 sets; **each `<tweetid>_N.jpg` file is one app's complete set**.
- `examples/before.click/{app}/` — 225 apps, categorized `aso/` and `onboarding/` frames.

## The afternoon rewrite (for an existing listing)

You don't need a designer, just an afternoon: pull the current screenshots, cover the UI, read only the
headlines aloud, rewrite anything that sounds like a feature list, then run the new set for 30 days and
compare conversion in App Analytics. One rewrite session teaches more than months of keyword tweaks.
