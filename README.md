# Convening Website

Static Jekyll site for the **Resilience Planning for Maryland Defense Communities** event.

- Production URL: https://mdresilienceconvening.org
- Platform: Jekyll (Markdown + Liquid templates)

## Site Structure

Core content pages:

- `index.md` — Home
- `agenda.md` — Agenda
- `location.md` — Location and logistics
- `speakers.md` — Speaker bios
- `register.md` — Registration page

Session detail pages:

- `sessions/*.md` — Individual agenda session pages

Layouts and styling:

- `_layouts/default.html` — Global page shell/nav/footer
- `_layouts/session.html` — Session page template
- `_layouts/speaker.html` — Speaker page template
- `assets/css/site.css` — Site styles

Images and media:

- `assets/images/logos/` — Partner/agency logos
- `assets/images/speakers/` — Speaker headshots/placeholders

## Configuration

Main config lives in `_config.yml`:

- `url` should be `https://mdresilienceconvening.org`
- `registration_url` controls the Register button/link target
- `title`, `description`, and `email` are used across templates

## Local Development

### Prerequisites

- Ruby installed (Ruby 3.x recommended)
- Bundler (`gem install bundler` if needed)

### Install dependencies

From the repo root:

```convening_website/README.md#L1-1
bundle install
```

### Run local server

```convening_website/README.md#L1-1
bundle exec jekyll serve
```

Then open:

- http://127.0.0.1:4000

Jekyll will rebuild automatically as files change.

## Local Testing Checklist

### 1) Build test (required)

Run a production-style build and confirm no errors:

```convening_website/README.md#L1-1
bundle exec jekyll build
```

### 2) Spot-check key pages

Verify these render and navigate correctly:

- `/`
- `/agenda/`
- `/location/`
- `/speakers/`
- `/register/`

### 3) Validate agenda/session links

From `/agenda/`, click each session title and confirm each resolves to `/agenda/sessions/.../`.

### 4) Check external links

Confirm external destinations open and are current (registration, partner logos, maps, agency links).

### 5) Mobile/responsive check

Use browser dev tools to test common widths (mobile/tablet/desktop), especially:

- Agenda list readability
- Navigation wrapping
- Logo grid layout

## Deploying

This repository is intended to be published as the live site at:

- https://mdresilienceconvening.org

Use your existing deployment flow for this repo (for example, GitHub Pages or your configured host) after running the local build test above.
