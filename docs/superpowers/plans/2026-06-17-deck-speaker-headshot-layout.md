# Deck Speaker Headshot-Beside-Text Layout — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move each speaker's headshot to sit beside their name, panel role, and job title, arranged in a two-up grid, in both deck builders.

**Architecture:** Job titles come from the website `speakers/*.md` front matter via new helpers in `build_deck.py`. Grid geometry is computed once by a shared `speaker_grid_cells()` helper that both renderers consume, so the PNG deck (`build_deck.py`) and the native/editable deck (`build_deck_native.py`) stay aligned. Pure logic (slug, title loading, geometry) is unit-tested with stdlib `unittest`; the pixel rendering is verified by producing sample slides.

**Tech Stack:** Python 3.14 (run via `deck/.venv/bin/python`), Pillow 12, python-pptx. Tests use stdlib `unittest`.

**Spec:** `docs/superpowers/specs/2026-06-17-deck-speaker-headshot-layout-design.md`

> **Git note (2026-06-17):** The user asked *not to commit yet* and to decide on git later. Treat every **Commit** step below as a checkpoint: run it only once the user opts into committing. Otherwise complete the step's verification and move on without committing.

> **Test command (run from the project root, no `cd` needed):**
> `deck/.venv/bin/python deck/test_deck_layout.py -v`
> The test file lives next to `build_deck.py`, so `import build_deck` resolves from the script directory.

---

## File Structure

- `deck/build_deck.py` (modify) — add `re`/`math` imports, `SPEAKER_PAGES_DIR`, the title helpers (`slugify`, `_read_front_matter_value`, `load_speaker_titles`, `speaker_title_for`), the geometry helper (`speaker_grid_cells`), and rewrite `draw_speaker_row`.
- `deck/build_deck_native.py` (modify) — rewrite `place_speakers` to consume `bd.speaker_grid_cells` + `bd.speaker_title_for`.
- `deck/test_deck_layout.py` (create) — `unittest` tests for the helpers and geometry, plus render smoke tests.

---

## Task 1: Title data helpers

**Files:**
- Create: `deck/test_deck_layout.py`
- Modify: `deck/build_deck.py` (imports near top; new functions after the `font()` helper, before the Agenda section)

- [ ] **Step 1: Write the failing tests**

Create `deck/test_deck_layout.py`:

```python
#!/usr/bin/env python3
"""
Title: Deck Layout Tests

Description:
    Unit tests for the convening deck's pure logic: name->slug conversion,
    speaker job-title loading from the website speaker pages, two-up grid
    geometry, and render smoke tests for both deck builders.

Usage:
    deck/.venv/bin/python deck/test_deck_layout.py -v

Changelog:
    2026-06-17  Initial version for the headshot-beside-text layout.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_deck as bd


class TestSlugify(unittest.TestCase):
    def test_simple_two_words(self):
        self.assertEqual(bd.slugify("Kim Pezza"), "kim-pezza")

    def test_internal_capitals(self):
        self.assertEqual(bd.slugify("LaRon Russell"), "laron-russell")

    def test_three_words(self):
        self.assertEqual(bd.slugify("Cyrena Chiles Eitler"), "cyrena-chiles-eitler")


class TestSpeakerTitles(unittest.TestCase):
    def test_known_title(self):
        self.assertEqual(
            bd.speaker_title_for("Kim Pezza"),
            "Climate Resilience Director, Maryland Comptroller's Office",
        )

    def test_speaker_without_photo_still_has_title(self):
        self.assertEqual(
            bd.speaker_title_for("Eric Leshinsky"),
            "Chief of Comprehensive Planning, City of Annapolis",
        )

    def test_unknown_speaker_returns_none(self):
        self.assertIsNone(bd.speaker_title_for("Nobody McNotreal"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `deck/.venv/bin/python deck/test_deck_layout.py -v`
Expected: FAIL — `AttributeError: module 'build_deck' has no attribute 'slugify'`.

- [ ] **Step 3: Add the imports**

In `deck/build_deck.py`, the top imports currently are:

```python
import argparse
import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter
```

Change to:

```python
import argparse
import math
import os
import re

from PIL import Image, ImageDraw, ImageFont, ImageFilter
```

- [ ] **Step 4: Add the speaker-pages path constant**

In `deck/build_deck.py`, the Paths block currently ends with:

```python
SPEAKER_IMG_DIR = os.path.join(PROJECT_DIR, "assets", "images", "speakers")
LOGO_IMG_DIR = os.path.join(PROJECT_DIR, "assets", "images", "logos")
```

Add one line after `LOGO_IMG_DIR`:

```python
SPEAKER_PAGES_DIR = os.path.join(PROJECT_DIR, "speakers")
```

- [ ] **Step 5: Add the title helpers**

In `deck/build_deck.py`, immediately after the `font()` function (it ends with `return _font_cache[key]`) and before the `# Agenda data` comment block, add:

```python
# --------------------------------------------------------------------------
# Speaker job titles (sourced from the website speaker pages)
# --------------------------------------------------------------------------
_speaker_titles_cache = None


def slugify(name):
    """
    Convert a speaker's display name to their page slug.

    Lowercases the name, replaces every run of non-alphanumeric characters
    with a single hyphen, and strips leading/trailing hyphens, matching the
    speakers/<slug>.md filenames.

    Parameters:
        name (str): a speaker's display name, e.g. "LaRon Russell".

    Returns:
        str: the slug, e.g. "laron-russell".
    """
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _read_front_matter_value(path, key):
    """
    Return a single value from a Markdown file's YAML front matter.

    Reads the block between the first two `---` fences and returns the value
    for ``key`` with any surrounding single/double quotes stripped.

    Parameters:
        path (str): path to the .md file.
        key (str): front-matter key, e.g. "speaker_title".

    Returns:
        str | None: the value, or None if the key is absent.
    """
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    prefix = key + ":"
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith(prefix):
            value = line[len(prefix):].strip()
            if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
                value = value[1:-1]
            return value
    return None


def load_speaker_titles():
    """
    Read job titles from the website speaker pages.

    Scans speakers/*.md, pulls the ``speaker_title`` value from each file's
    leading front-matter block, and caches the result for the build.

    Returns:
        dict[str, str]: {page slug: job title}, e.g.
        {"kim-pezza": "Climate Resilience Director, Maryland Comptroller's Office"}.
    """
    global _speaker_titles_cache
    if _speaker_titles_cache is not None:
        return _speaker_titles_cache

    titles = {}
    if os.path.isdir(SPEAKER_PAGES_DIR):
        for filename in sorted(os.listdir(SPEAKER_PAGES_DIR)):
            if not filename.endswith(".md"):
                continue
            title = _read_front_matter_value(
                os.path.join(SPEAKER_PAGES_DIR, filename), "speaker_title"
            )
            if title:
                titles[filename[:-3]] = title
    _speaker_titles_cache = titles
    return titles


def speaker_title_for(name):
    """
    Look up a speaker's job title by display name.

    Parameters:
        name (str): speaker display name.

    Returns:
        str | None: the job title from their website page, or None if there
        is no matching speakers/<slug>.md or no title in it.
    """
    return load_speaker_titles().get(slugify(name))
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `deck/.venv/bin/python deck/test_deck_layout.py -v`
Expected: PASS — 6 tests (3 slugify + 3 titles) OK.

- [ ] **Step 7: Commit** *(checkpoint — see Git note)*

```bash
git add deck/build_deck.py deck/test_deck_layout.py
git commit -m "feat(deck): load speaker job titles from website speaker pages"
```

---

## Task 2: Two-up grid geometry

**Files:**
- Modify: `deck/build_deck.py` (new `speaker_grid_cells` in the Drawing helpers section, after `split_kicker`)
- Modify: `deck/test_deck_layout.py` (add geometry tests)

- [ ] **Step 1: Write the failing tests**

In `deck/test_deck_layout.py`, add this class before the `if __name__` block:

```python
class TestSpeakerGrid(unittest.TestCase):
    def test_single_speaker_one_centered_cell(self):
        grid = bd.speaker_grid_cells(1, 700, 1150)
        self.assertEqual(grid["columns"], 1)
        self.assertEqual(len(grid["cells"]), 1)
        cell_x, _, cell_w, _ = grid["cells"][0]
        self.assertEqual(cell_x, (bd.WIDTH - cell_w) // 2)

    def test_two_speakers_single_row(self):
        grid = bd.speaker_grid_cells(2, 700, 1150)
        self.assertEqual((grid["columns"], grid["rows"]), (2, 1))
        self.assertEqual(len(grid["cells"]), 2)
        self.assertEqual(grid["cells"][0][1], grid["cells"][1][1])  # same row y
        self.assertLess(grid["cells"][0][0], grid["cells"][1][0])   # left, right

    def test_three_speakers_two_plus_one(self):
        grid = bd.speaker_grid_cells(3, 700, 1150)
        self.assertEqual((grid["columns"], grid["rows"]), (2, 2))
        third_x, third_y, third_w, _ = grid["cells"][2]
        self.assertEqual(third_x, (bd.WIDTH - third_w) // 2)        # centered
        self.assertGreater(third_y, grid["cells"][0][1])            # second row

    def test_four_speakers_two_by_two(self):
        grid = bd.speaker_grid_cells(4, 700, 1150)
        self.assertEqual((grid["columns"], grid["rows"]), (2, 2))
        self.assertEqual(len(grid["cells"]), 4)
        self.assertEqual(grid["cells"][0][1], grid["cells"][1][1])  # row 0 shared y
        self.assertEqual(grid["cells"][0][0], grid["cells"][2][0])  # col 0 shared x
        self.assertLess(grid["cells"][0][0], grid["cells"][1][0])

    def test_grid_stays_within_zone(self):
        grid = bd.speaker_grid_cells(4, 700, 1150)
        top = min(c[1] for c in grid["cells"])
        bottom = max(c[1] + c[3] for c in grid["cells"])
        self.assertGreaterEqual(top, 700)
        self.assertLessEqual(bottom, 1150)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `deck/.venv/bin/python deck/test_deck_layout.py -v`
Expected: FAIL — `AttributeError: module 'build_deck' has no attribute 'speaker_grid_cells'`.

- [ ] **Step 3: Implement `speaker_grid_cells`**

In `deck/build_deck.py`, add this function right after `split_kicker` (which ends with `return None, title`) and before the `# Slide composition` divider:

```python
def speaker_grid_cells(count, zone_top, zone_bottom):
    """
    Compute the two-up grid geometry for a slide's speaker zone.

    Lays ``count`` speakers into a grid (1 -> one centered cell, otherwise two
    columns filled left-to-right, top-to-bottom) and vertically centers the
    grid within [zone_top, zone_bottom]. A final short row and a lone single
    cell are centered horizontally. The same geometry feeds both the image
    renderer and the native-object renderer so the two decks line up.

    Parameters:
        count (int): number of speakers (>= 1).
        zone_top (int): top of the available vertical band, in canvas px.
        zone_bottom (int): bottom of the band, in canvas px.

    Returns:
        dict: {
            "columns" (int), "rows" (int),
            "head" (int): headshot diameter in px,
            "inner_gap" (int): px between headshot and text block,
            "name_size" (int), "role_size" (int): canvas font sizes,
            "title_sizes" (list[int]): descending sizes for title auto-fit,
            "gap_after_name" (int), "gap_after_role" (int): px,
            "cells" (list[tuple]): one (cell_x, cell_y, cell_w, cell_h) per
                speaker, in speaker order.
        }
    """
    usable_w = WIDTH - MARGIN * 2
    col_gap = 90
    row_gap = 40

    if count == 1:
        columns, col_w, head, cell_h = 1, 1400, 240, 300
        name_size, role_size, title_sizes = 46, 30, [40, 35, 31, 27]
    else:
        columns = 2
        col_w = (usable_w - col_gap) // 2
        if math.ceil(count / columns) == 1:           # exactly two speakers
            head, cell_h, name_size, role_size = 220, 280, 44, 30
            title_sizes = [38, 33, 29, 25]
        else:                                          # three or four speakers
            head, cell_h, name_size, role_size = 156, 196, 40, 26
            title_sizes = [32, 29, 26, 23]

    rows = math.ceil(count / columns)
    total_h = rows * cell_h + (rows - 1) * row_gap
    grid_top = zone_top + max(0, (zone_bottom - zone_top - total_h) // 2)

    cells = []
    for index in range(count):
        row = index // columns
        col = index % columns
        cells_in_row = min(columns, count - row * columns)
        row_w = cells_in_row * col_w + (cells_in_row - 1) * col_gap
        row_x0 = (WIDTH - row_w) // 2
        cell_x = row_x0 + col * (col_w + col_gap)
        cell_y = grid_top + row * (cell_h + row_gap)
        cells.append((cell_x, cell_y, col_w, cell_h))

    return {
        "columns": columns,
        "rows": rows,
        "head": head,
        "inner_gap": 28,
        "name_size": name_size,
        "role_size": role_size,
        "title_sizes": title_sizes,
        "gap_after_name": 10,
        "gap_after_role": 8,
        "cells": cells,
    }
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `deck/.venv/bin/python deck/test_deck_layout.py -v`
Expected: PASS — 11 tests OK (6 from Task 1 + 5 geometry).

- [ ] **Step 5: Commit** *(checkpoint — see Git note)*

```bash
git add deck/build_deck.py deck/test_deck_layout.py
git commit -m "feat(deck): add two-up speaker grid geometry helper"
```

---

## Task 3: Rewrite the image renderer (`draw_speaker_row`)

**Files:**
- Modify: `deck/build_deck.py:540-593` (`draw_speaker_row`)
- Modify: `deck/test_deck_layout.py` (add a render smoke test)

- [ ] **Step 1: Write the failing smoke test**

In `deck/test_deck_layout.py`, add before the `if __name__` block:

```python
class TestRenderSmoke(unittest.TestCase):
    def test_four_speaker_slide_renders(self):
        item = bd.AGENDA[7]        # Panel: Federal and State Financing (4 speakers)
        next_item = bd.AGENDA[8]
        image = bd.render_slot_slide(item, next_item)
        self.assertEqual(image.size, (bd.WIDTH, bd.HEIGHT))
        self.assertEqual(image.mode, "RGB")

    def test_single_speaker_slide_renders(self):
        item = bd.AGENDA[1]        # Welcoming Remarks (1 speaker)
        next_item = bd.AGENDA[2]
        image = bd.render_slot_slide(item, next_item)
        self.assertEqual(image.size, (bd.WIDTH, bd.HEIGHT))
```

(These already pass against the old renderer — they are guardrails that the
rewrite must keep render working end-to-end. Run them after the rewrite.)

- [ ] **Step 2: Replace `draw_speaker_row`**

In `deck/build_deck.py`, replace the entire current `draw_speaker_row` function (from `def draw_speaker_row(canvas, draw, speakers, zone_top, zone_bottom, shape="circle"):` through the end of its body) with:

```python
def draw_speaker_row(canvas, draw, speakers, zone_top, zone_bottom, shape="circle"):
    """
    Lay out speakers as a two-up grid: each headshot at left with the speaker's
    name, panel role, and job title stacked to its right.

    Parameters:
        canvas/draw: target image and its draw context.
        speakers (list): (name, role, image filename[, mode]) tuples.
        zone_top/zone_bottom (int): vertical band the grid is centered within.
        shape (str): default headshot shape, "circle" or "square".
    """
    count = len(speakers)
    if count == 0:
        return

    grid = speaker_grid_cells(count, zone_top, zone_bottom)
    head = grid["head"]
    inner_gap = grid["inner_gap"]
    name_font = font("sans-700", grid["name_size"])
    role_font = font("sans-600", grid["role_size"])
    name_lh = int(grid["name_size"] * 1.12)
    role_lh = int(grid["role_size"] * 1.25)

    # A 4th tuple element overrides the session shape; "full" shows the photo
    # uncropped, "square" / "circle" pick the badge shape.
    normalized = [
        (sp[0], sp[1], sp[2], sp[3] if len(sp) > 3 else shape) for sp in speakers
    ]

    for (name, role, filename, mode), (cell_x, cell_y, cell_w, cell_h) in zip(
        normalized, grid["cells"]
    ):
        path = os.path.join(SPEAKER_IMG_DIR, filename) if filename else None
        text_x = cell_x + head + inner_gap
        text_w = cell_w - head - inner_gap

        # Fit the name (<= 2 lines) and the job title (<= 2 lines, auto-shrunk).
        name_lines = wrap_text(draw, name, name_font, text_w)[:2]
        title = speaker_title_for(name)
        title_lines, title_size = [], None
        if title:
            _, title_lines, title_size = fit_display_text(
                draw, title, text_w, 2, grid["title_sizes"], font_name="sans-400"
            )
        title_lh = int(title_size * 1.18) if title_size else 0

        block_h = len(name_lines) * name_lh + grid["gap_after_name"] + role_lh
        if title_lines:
            block_h += grid["gap_after_role"] + len(title_lines) * title_lh

        # Headshot, vertically centered in the cell.
        if mode == "full":
            badge = headshot_full(path, head)
        else:
            badge = headshot(path, head, shape=mode)
        head_y = cell_y + (cell_h - head) // 2
        badge_x = cell_x + (head - badge.width) // 2
        badge_y = head_y + (head - badge.height) // 2
        paste_with_shadow(canvas, badge, badge_x, badge_y,
                          shape="circle" if mode == "circle" else "square")

        # Text block, vertically centered against the headshot.
        ty = cell_y + (cell_h - block_h) // 2
        for line in name_lines:
            draw.text((text_x, ty), line, font=name_font, fill=INK, anchor="la")
            ty += name_lh
        ty += grid["gap_after_name"]
        draw_tracked(draw, (text_x, ty), role.upper(), role_font, RED_DARK, 4, anchor="la")
        ty += role_lh
        if title_lines:
            ty += grid["gap_after_role"]
            title_font = font("sans-400", title_size)
            for line in title_lines:
                draw.text((text_x, ty), line, font=title_font, fill=INK_SOFT, anchor="la")
                ty += title_lh
```

- [ ] **Step 3: Run the smoke tests**

Run: `deck/.venv/bin/python deck/test_deck_layout.py -v`
Expected: PASS — 13 tests OK (the two render smoke tests now exercise the new grid).

- [ ] **Step 4: Render sample slides and inspect them visually**

Run each and open the resulting PNG:

```bash
deck/.venv/bin/python deck/build_deck.py --only 7   # 4 speakers, long titles
deck/.venv/bin/python deck/build_deck.py --only 5   # 3 speakers (2 + 1)
deck/.venv/bin/python deck/build_deck.py --only 1   # 1 speaker (centered)
```

Each writes `deck/build/sample-<key>.png`. Confirm: headshot sits left of name;
role (red, small caps) and job title read clearly beneath the name; long titles
wrap to two lines without overrunning the column or the Up Next band; the
3-speaker slide shows two on top and one centered below.

- [ ] **Step 5: Commit** *(checkpoint — see Git note)*

```bash
git add deck/build_deck.py deck/test_deck_layout.py
git commit -m "feat(deck): render speakers as headshot-beside-text two-up grid (PNG deck)"
```

---

## Task 4: Rewrite the native renderer (`place_speakers`)

**Files:**
- Modify: `deck/build_deck_native.py:203-239` (`place_speakers`)
- Modify: `deck/test_deck_layout.py` (add a native build smoke test)

- [ ] **Step 1: Write the failing smoke test**

In `deck/test_deck_layout.py`, add the native import next to the existing
`import build_deck as bd` line:

```python
import build_deck_native as bdn
```

Then add this class before the `if __name__` block:

```python
class TestNativeBuildSmoke(unittest.TestCase):
    def test_native_build_has_all_slides(self):
        output_path, presentation = bdn.build()
        self.assertTrue(os.path.exists(output_path))
        expected_slides = 1 + sum(1 for item in bd.AGENDA if item["slide"])
        self.assertEqual(len(presentation.slides), expected_slides)
```

(`bdn.build()` regenerates `deck/convening-registration-deck-editable.pptx` as a
side effect; that file is rebuilt again in Task 5, so this is fine.)

- [ ] **Step 2: Run it to confirm the rewrite is needed**

Run: `deck/.venv/bin/python deck/test_deck_layout.py -v`
Expected: PASS already (the old `place_speakers` still builds). This test is a
guardrail — keep it green through the rewrite.

- [ ] **Step 3: Replace `place_speakers`**

In `deck/build_deck_native.py`, replace the entire current `place_speakers`
function with:

```python
def place_speakers(slide, speakers, zone_top, zone_bottom, default_shape):
    """
    Lay out native headshots as a two-up grid with name + role + title beside
    each photo, matching the image renderer's geometry.

    Parameters:
        slide: the python-pptx slide to populate.
        speakers (list): (name, role, image filename[, mode]) tuples.
        zone_top/zone_bottom (int): vertical band the grid is centered within.
        default_shape (str): session default headshot shape ("circle"/"square").
    """
    count = len(speakers)
    if count == 0:
        return

    grid = bd.speaker_grid_cells(count, zone_top, zone_bottom)
    head = grid["head"]
    inner_gap = grid["inner_gap"]
    name_font = bd.font("sans-700", grid["name_size"])
    name_lh = int(grid["name_size"] * 1.12)
    role_lh = int(grid["role_size"] * 1.25)

    normalized = [
        (sp[0], sp[1], sp[2], sp[3] if len(sp) > 3 else default_shape)
        for sp in speakers
    ]

    for (name, role, filename, mode), (cell_x, cell_y, cell_w, cell_h) in zip(
        normalized, grid["cells"]
    ):
        path = os.path.join(bd.SPEAKER_IMG_DIR, filename) if filename else None
        text_x = cell_x + head + inner_gap
        text_w = cell_w - head - inner_gap

        name_lines = bd.wrap_text(_SCRATCH, name, name_font, text_w)[:2]
        title = bd.speaker_title_for(name)
        title_lines, title_size = [], None
        if title:
            _, title_lines, title_size = bd.fit_display_text(
                _SCRATCH, title, text_w, 2, grid["title_sizes"], font_name="sans-400"
            )
        title_lh = int(title_size * 1.18) if title_size else 0

        block_h = len(name_lines) * name_lh + grid["gap_after_name"] + role_lh
        if title_lines:
            block_h += grid["gap_after_role"] + len(title_lines) * title_lh

        # Headshot, vertically centered in the cell.
        head_y = cell_y + (cell_h - head) // 2
        add_headshot(slide, path, cell_x, head_y, head,
                     "square" if mode == "square" else "circle")

        # Text block (name, role, title), vertically centered against the photo.
        text_top = cell_y + (cell_h - block_h) // 2
        add_text(slide, text_x, text_top, text_w, name_lh * len(name_lines) + 8,
                 lines=name_lines, font_name=PUBLIC_SANS, size_px=grid["name_size"],
                 fill=bd.INK, bold=True, align=PP_ALIGN.LEFT)

        role_y = text_top + len(name_lines) * name_lh + grid["gap_after_name"]
        add_text(slide, text_x, role_y, text_w, role_lh + 6, role.upper(),
                 font_name=PUBLIC_SANS, size_px=grid["role_size"], fill=bd.RED_DARK,
                 bold=True, align=PP_ALIGN.LEFT, tracking_px=4)

        if title_lines:
            title_y = role_y + role_lh + grid["gap_after_role"]
            add_text(slide, text_x, title_y, text_w, title_lh * len(title_lines) + 8,
                     lines=title_lines, font_name=PUBLIC_SANS, size_px=title_size,
                     fill=bd.INK_SOFT, bold=False, align=PP_ALIGN.LEFT)
```

- [ ] **Step 4: Run the tests**

Run: `deck/.venv/bin/python deck/test_deck_layout.py -v`
Expected: PASS — 14 tests OK.

- [ ] **Step 5: Build the native deck and inspect it**

Run:

```bash
deck/.venv/bin/python deck/build_deck_native.py --verify
```

Expected: prints `Wrote .../convening-registration-deck-editable.pptx` and a
per-slide summary; each speaker slide reports one picture per speaker. Open the
`.pptx` and confirm a speaker slide (e.g. Federal & State Financing) shows each
headshot beside its name/role/title, matching the PNG deck's layout. Native text
renders in installed fonts (Oswald / Public Sans) — install them or use
PowerPoint's "Embed fonts" if the look drifts.

- [ ] **Step 6: Commit** *(checkpoint — see Git note)*

```bash
git add deck/build_deck_native.py deck/test_deck_layout.py
git commit -m "feat(deck): render headshot-beside-text two-up grid (editable deck)"
```

---

## Task 5: Full build of both decks + final verification

**Files:** none (build + inspect only)

- [ ] **Step 1: Run the full test suite**

Run: `deck/.venv/bin/python deck/test_deck_layout.py -v`
Expected: PASS — all 14 tests OK.

- [ ] **Step 2: Build the PNG deck**

Run: `deck/.venv/bin/python deck/build_deck.py`
Expected: writes `slide-00-cover.png` … `slide-12-wrap-up.png` and
`deck/convening-registration-deck.pptx`.

- [ ] **Step 3: Build the editable deck**

Run: `deck/.venv/bin/python deck/build_deck_native.py --verify`
Expected: writes `deck/convening-registration-deck-editable.pptx` + summary.

- [ ] **Step 4: Cross-check the two decks**

Open both `.pptx` files. On every speaker slide confirm the headshot-beside-text
layout matches between them, all five headshot slides look right (1, 3, and
4-speaker panels), and the two photo-less speakers (Eric Leshinsky, Harry
Kleiser) still show the placeholder image with their name/role/title beside it.

- [ ] **Step 5: Commit** *(checkpoint — see Git note)*

```bash
git add deck/convening-registration-deck.pptx deck/convening-registration-deck-editable.pptx
git commit -m "build(deck): rebuild decks with headshot-beside-text layout"
```

---

## Self-Review

**Spec coverage:**
- Headshot beside name/role/title → Tasks 3 & 4 (`draw_speaker_row`, `place_speakers`).
- Two-up grid (1/2/3/4 behavior) → Task 2 (`speaker_grid_cells`) + tests.
- Titles from `speakers/*.md` → Task 1 (`load_speaker_titles`, `speaker_title_for`).
- Keep panel role → role line retained in both renderers (Tasks 3 & 4).
- Both builders updated → Task 3 (PNG) + Task 4 (native).
- Fallback when no title → `if title:` guards in both renderers; `test_unknown_speaker_returns_none`.
- Circle/square/full overrides preserved → `mode` handling kept in both renderers.
- No new dependency → stdlib `re`/`math`, front matter parsed directly.

**Placeholder scan:** No TBD/TODO; every code step contains complete code and exact commands.

**Type consistency:** `speaker_grid_cells` returns the same dict keys consumed in both renderers (`head`, `inner_gap`, `name_size`, `role_size`, `title_sizes`, `gap_after_name`, `gap_after_role`, `cells`); `speaker_title_for` / `slugify` / `load_speaker_titles` names match across tasks; `fit_display_text(draw, text, max_width, max_lines, sizes, font_name=...)` call matches its definition in `build_deck.py`.
