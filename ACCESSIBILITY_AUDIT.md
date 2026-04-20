# Accessibility Audit Report

**Date:** April 20, 2026  
**Site:** Resilience Planning for Maryland Defense Communities  
**Style version audited:** #3 (Maryland flag / military-professional conference theme)  
**Standard:** WCAG 2.1 Level AA  
**Tool:** [axe-core 4.9.1](https://github.com/dequelabs/axe-core)

---

## Methodology

Pages were served locally via Python's built-in HTTP server (`python3 -m http.server 4173 --directory _site`) and loaded in a headless Chromium browser (Playwright). axe-core was injected into each page via CDN and executed against the full document with the following rule sets enabled:

- `wcag2a` — WCAG 2.1 Level A
- `wcag2aa` — WCAG 2.1 Level AA
- `best-practice` — Deque best-practice rules beyond the standard

The audit checks for, among other things:

- Color contrast ratios (text, UI components)
- Image alternative text
- Heading hierarchy and landmark structure
- ARIA roles, labels, and attributes
- Keyboard accessibility and focus management
- Skip navigation links
- Form labels and error identification
- Link names and button text

---

## Results

| Page | URL | Violations |
|---|---|---|
| Home | `/` | ✅ 0 |
| Agenda | `/agenda/` | ✅ 0 |
| Location | `/location/` | ✅ 0 |
| Speaker Bios | `/speakers/` | ✅ 0 |
| Registration | `/register/` | ✅ 0 |

**Total violations: 0**

All five pages passed with zero WCAG 2.1 AA violations across all tested rule sets.

---

## Notes

- The Google Maps `<iframe>` on the Location page did not load during testing due to network restrictions in the sandboxed browser environment. The iframe includes a `title` attribute and the page passed all accessibility checks regardless.
- Session pages under `/sessions/` and individual speaker profile pages were not audited in this pass due to pre-existing YAML front matter errors that prevent those pages from building. Those errors are unrelated to accessibility.

---

## How to Re-run the Audit

1. Build the site:
   ```
   bundle exec jekyll build
   ```

2. Start a local server from the `_site` directory:
   ```
   python3 -m http.server 4173 --directory _site
   ```

3. Inject axe-core and run in a browser console or via Playwright:
   ```js
   // In browser console (after manually adding the script tag):
   const script = document.createElement('script');
   script.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js';
   document.head.appendChild(script);
   script.onload = () => axe.run().then(r => console.log(r.violations));
   ```

   Or via Playwright:
   ```js
   await page.addScriptTag({ url: 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js' });
   const results = await page.evaluate(async () =>
     axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'best-practice'] } })
   );
   console.log(results.violations);
   ```
