# Nairobi Wings Fest landing page

Live at https://nairobiwingsfest.com. The page ships as one self-contained `index.html` (fonts, images and scripts inlined), built from the readable files in `src/`.

## Edit and rebuild

1. Edit files in `src/`, never `index.html` directly.
2. Run `python3 build.py` (Python 3 only, no packages needed). This rewrites `index.html`.
3. Open `index.html` in a browser to check it, then commit and push. Vercel deploys on every push to `main`.

## Where things live

- `src/template.html` page markup and page-specific CSS. Placeholders like `__IMG_P1__` are filled in by the build.
- `src/css/common.css`, `src/css/ticket.css` shared styles and the ticket card.
- `src/js/` countdown, 20 spots, sign-up form, ticket card behaviour.
- `src/ticket.html` ticket card markup.
- `src/img/` all images. `hero-*` are the four corner photos, `pill-p1..p6` the What to expect pills, `spots-drip` the 20 spots image, `door-cook` and `door-partner` the two cards.
- `src/fonts/` Anton and Instrument Sans.
- `build.py` FAQ text, crown icon and the sample QR code are defined here.

To swap an image, replace the file in `src/img/` with the same name (webp, transparent where the original is) and rebuild.

## Still to finish before launch

Event date, venue, ticket price, social links, and the sign-up form endpoint (`FORM_ENDPOINT` in `src/js/shared.js`). Until the endpoint is set, the form does not send emails anywhere.
