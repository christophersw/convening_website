# Deck Speaker Layout: Headshot Beside Name + Role + Title

**Date:** 2026-06-17
**Status:** Approved (design)

## Overview

The convening registration deck (`deck/build_deck.py` and
`deck/build_deck_native.py`) renders one "Happening Now / Up Next" slide per
agenda slot. Speaker slots currently show each headshot stacked **above** the
person's name and panel role, laid out in a single centered horizontal row.

This change moves each headshot to sit **beside** a stacked text block — name,
panel role, and job title — and arranges speakers in a **two-up grid** so the
slide uses its width and can carry the longer job titles. Job titles are pulled
from the website's speaker pages so the deck stays in sync with the site.

## Goals

- Headshot at left of each speaker; name + role + job title stacked at right.
- Two-column grid layout (1→centered cell, 2→one row, 3→2+1, 4→2×2).
- Job titles sourced from `speakers/*.md` front matter (single source of truth).
- Keep the existing panel role label ("Moderator" / "Panelist" / "Speaker").
- Apply the change to **both** builders so the image deck and the editable
  (native-object) deck match.

## Non-Goals

- No separate "organization" line (the job title string already contains the
  org as written on the site, e.g. *"…, Maryland Comptroller's Office"*).
- No change to non-speaker slots (notes, breaks, cover, Up Next band).
- No change to headshot cropping, the circle/square/full shape overrides, the
  placeholder behavior, or the agenda data itself.
- No new third-party dependency (front matter is parsed directly, not via PyYAML).

## Data Layer

### Title source

A new helper in `build_deck.py`:

- `slugify(name)` — lowercase, collapse any run of non-alphanumeric characters
  to a single hyphen, strip leading/trailing hyphens. Produces the same stems
  as the existing files: `"LaRon Russell"` → `laron-russell`,
  `"Cyrena Chiles Eitler"` → `cyrena-chiles-eitler`.
- `load_speaker_titles()` — scan `speakers/*.md`, read the `speaker_title:`
  value from each file's leading front-matter block (the text between the first
  two `---` lines), strip surrounding quotes, and return a `{stem: title}` dict.
  Result is cached at module level so the scan happens once per build.
- `speaker_title_for(name)` — `load_speaker_titles().get(slugify(name))`,
  returning `None` when no matching file/title exists.

All 15 current speakers map cleanly (verified against `speakers/`). The match is
by speaker **name**, not photo filename, so the two speakers without photos
(`Eric Leshinsky`, `Harry Kleiser`) still resolve their titles.

### Fallback

If `speaker_title_for(name)` is `None`, the cell renders name + role only (no
title line). Missing photos continue to use the shared placeholder image.

## Layout

### Shared geometry

To keep the two renderers identical, the grid math is extracted into one helper
in `build_deck.py` — `speaker_grid_cells(count, zone_top, zone_bottom)` — that
returns the column/row counts, headshot diameter, font sizes, and a per-speaker
list of cell rectangles. Both `draw_speaker_row` (PNG) and `place_speakers`
(native) consume this and only differ in how they draw. Text wrapping/fitting
uses the existing shared `wrap_text` / `fit_display_text`, so both renderers
compute identical line counts and therefore identical positions.

### Grid rules

- `columns = 1 if count == 1 else 2`; `rows = ceil(count / columns)`.
- Cells fill left-to-right, top-to-bottom. A final short row (the 3-speaker
  case) is centered horizontally; a single cell (1 speaker) is centered.
- Usable width = `WIDTH - 2*MARGIN` (2220 px); column gap ≈ 90 px.
- Headshot diameter scales with row count (starting values, tunable in
  implementation): `rows == 1 → 220 px`, `rows == 2 → 156 px`.
- Each cell: headshot at left (vertically centered in the cell), inner gap
  ≈ 28 px, then a text block occupying the remaining column width
  (≈ 870 px per column at 2 columns).

### Per-speaker text block (top to bottom)

1. **Name** — Public Sans 700, ink. ≈ 44 px (rows 1) / 40 px (rows 2); wraps to
   at most 2 lines within the text width.
2. **Role** — Public Sans 600, deep red, uppercase, letter-tracked (the current
   role styling). ≈ 26–28 px.
3. **Job title** — Public Sans 400, soft ink, auto-fit to ≤ 2 lines within the
   text width by picking the largest size from a descending list
   (e.g. `[34, 30, 27, 24]`). Omitted entirely when no title is found.

The text block is vertically centered against the headshot within the cell.
The whole grid is vertically centered in the existing speaker zone
(`zone_top = max(title_bottom + 40, 700)` to `zone_bottom = 1150`), unchanged.

### Headshot shape

Circle remains the default. The existing per-session `headshot_shape` override
and the per-speaker 4th-tuple `mode` (`circle` / `square` / `full`) continue to
work; only the position relative to the text changes.

## Files Changed

- `deck/build_deck.py`
  - Add `slugify`, `load_speaker_titles`, `speaker_title_for`,
    `speaker_grid_cells`.
  - Rewrite `draw_speaker_row` to render the two-up grid from the shared
    geometry, with name/role/title beside each headshot.
- `deck/build_deck_native.py`
  - Rewrite `place_speakers` to render the same grid using native picture +
    text-box objects, consuming `bd.speaker_grid_cells` and `bd.speaker_title_for`.

## Edge Cases

- **No title found** → name + role only.
- **No photo** → placeholder image (unchanged), still in the headshot slot.
- **3 speakers** → 2 on top, 1 centered below.
- **1 speaker** → single centered cell with a larger headshot.
- **Long titles** (e.g. Brian Lazarchick, Lisa Swoboda) → wrap to 2 lines and/or
  shrink via the auto-fit list; the wide column accommodates them.
- **Name with 3 words** (Cyrena Chiles Eitler) → fits one line at the chosen
  size; the 2-line allowance covers any overflow.

## Verification

Run with the deck virtualenv (`deck/.venv`, which has Pillow + python-pptx):

1. `python deck/build_deck.py --only 7` → sample PNG of the 4-person Federal &
   State Financing panel; eyeball headshot/title alignment and wrapping.
2. Spot-check a 1-speaker slot (index 1, Welcoming Remarks) and a 3-speaker slot
   (index 5, Energy panel) the same way.
3. `python deck/build_deck.py` → full PNG deck + `convening-registration-deck.pptx`.
4. `python deck/build_deck_native.py --verify` → editable deck +
   structural summary; confirm picture/text counts per slide look right and the
   two decks visually match.
