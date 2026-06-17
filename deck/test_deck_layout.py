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
import build_deck_native as bdn


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

    def test_rejects_unsupported_count(self):
        with self.assertRaises(ValueError):
            bd.speaker_grid_cells(0, 700, 1150)
        with self.assertRaises(ValueError):
            bd.speaker_grid_cells(5, 700, 1150)


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

    def test_three_speaker_slide_renders(self):
        item = bd.AGENDA[5]        # Panel: Innovative Energy Partnerships (3 speakers)
        next_item = bd.AGENDA[6]
        image = bd.render_slot_slide(item, next_item)
        self.assertEqual(image.size, (bd.WIDTH, bd.HEIGHT))


class TestNativeBuildSmoke(unittest.TestCase):
    def test_native_build_has_all_slides(self):
        output_path, presentation = bdn.build()
        self.assertTrue(os.path.exists(output_path))
        expected_slides = 1 + sum(1 for item in bd.AGENDA if item["slide"])
        self.assertEqual(len(presentation.slides), expected_slides)


if __name__ == "__main__":
    unittest.main()
