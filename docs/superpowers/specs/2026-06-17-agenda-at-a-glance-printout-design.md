# Agenda at a Glance — Printable One-Pager

**Date:** 2026-06-17
**Status:** Approved (design)

## Goal

A print-ready "Agenda at a Glance" sheet for the day of the convening: the full
agenda, panel descriptions, and speaker headshots with titles, on **one** US-Letter
portrait side, in color, following the site's existing look and feel.

## Approach

A print-optimized Jekyll page at `/agenda/print/`. It pulls descriptions, speakers,
titles, and headshots **live** from the existing `sessions/` and `speakers/`
front-matter, so the printout never drifts from the website. The user opens the page
and prints via the browser (Cmd-P → Save as PDF / print).

Chosen layout — **Direction B (Schedule Rail + Session Cards)** — selected over an
integrated single-column timeline (too tight for descriptions) and a schedule-band +
unified speaker-gallery (squeezes descriptions). B keeps the schedule compact in a rail
so descriptions and faces get room.

## Layout

- **Header band** — full-width diagonal black/gold/red/cream stripe matching
  `.site-header`; event title in Oswald; date · time · venue line. No site nav/footer.
- **Left rail (~28%)** — "At a Glance": all 14 schedule rows in order
  (Registration → Adjourn). Times in Oswald red; breaks / lunch / transition muted italic.
- **Main area (~72%)** — "Sessions & Speakers" description cards in **two balanced
  columns** (the room that allows the *extended*, full-length descriptions). Each card:
  session time + title, full description, then the session's speakers as
  headshot + name + title. Moderators/facilitators marked. Welcoming Remarks
  (Lisa Swoboda) and Regional Workshops render as compact cards so all 15 faces appear.
- **Footer** — slim partner-logo strip: MD Commerce, OLDCC, CHHS, MDEM, MD Planning.

## Files

| File | Purpose |
|------|---------|
| `_layouts/print.html` | Minimal shell — doctype, fonts, print stylesheet. No nav/footer. |
| `print-agenda.md` | `permalink: /agenda/print/`. Defines the ordered rail; loops the session cards. |
| `_includes/print-session-card.html` | One session card (description + speaker headshots/titles), reused per session. |
| `assets/css/print-agenda.css` | Scoped styles; `@page { size: letter }`; `print-color-adjust: exact`. |

## Data & ordering

- The rail's 14 rows (including non-session rows: Registration, Breaks, Lunch,
  Transition, Adjourn) are listed inline in `print-agenda.md`, consistent with how
  `agenda.md` already authors the schedule skeleton. Session times/titles are typed there.
- Session **descriptions, speakers, titles, and photos** are looked up by permalink/url
  from the session and speaker pages (same mechanism as `_includes/agenda-panel-detail.html`).
- Cards rendered for: Project Findings, Fireside Chat, Innovative Energy, Federal & State
  Financing, Creative Financing (full description + speakers), plus compact Welcoming
  Remarks (Lisa) and Regional Workshops (description only).

## Defensive rules

- Suppress placeholder body text equal to "Coming Soon."
- Skip speakers with no `url` (e.g., the Wrap-Up placeholder "Closing Speaker Name").
- Missing photo → `placeholder.svg`.
- Long titles wrap to two lines.

## Color & print

- `@page { size: letter; }` with a safe margin so nothing clips on consumer printers.
- `-webkit-print-color-adjust: exact; print-color-adjust: exact;` so the gradient header
  and brand colors print.
- Fonts: Oswald (display) + Public Sans (body), already used site-wide.

## Verification

Build with Jekyll, render the page at US-Letter, and confirm it is exactly **one**
printed page. Single-side fit is the hard constraint. If the extended descriptions spill
to a second page, first tighten type/spacing; only trim a description as a last resort,
and flag it to the user.

## Out of scope

- Refactoring the live `agenda.md` or introducing a shared `_data/agenda.yml`.
- Any change to existing site pages.
