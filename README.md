sc# Convening Website

Static event website built for GitHub Pages with markdown-first content editing.

## What Is Included

- Professional multi-page site layout
- Core pages: Home, Agenda, Location, Speaker Bios, Registration
- External registration link support (no in-site registration system)
- Simple CSS styling and mobile-friendly design

## Quick Content Edits

### 1) Update Registration URL

Edit `registration_url` in `_config.yml`.

### 2) Update Core Content

- Home overview: `index.md`
- Agenda: `agenda.md`
- Location/logistics: `location.md`
- Speaker bios: `speakers.md`
- Registration page copy: `register.md`

### 3) Add Speaker Photos

Put images in `assets/images/speakers/` and update filenames in `speakers.md`.

## Deploy to GitHub Pages

1. Push this folder to a GitHub repository.
2. In repository settings, open **Pages**.
3. Set **Build and deployment** to **Deploy from a branch**.
4. Select branch: `main` and folder: `/ (root)`.
5. Save.

GitHub Pages will build and publish the site automatically.

## Optional Local Preview (Jekyll)

If you have Ruby installed, you can add a Gemfile and run Jekyll locally. For many workflows, editing and pushing directly to GitHub Pages is enough.

## Railway Option

You can deploy this site to Railway, but for this static use case GitHub Pages is simpler and free.
