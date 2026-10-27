# Book of Astrologies

A static website for the *Book of Astrologies*: 28 astrological schools read for one birth chart (13 Oct 1998, 21:25 UT, Johnstown PA).

- `docs/` is the built site (open `docs/index.html` or serve it). It is ready for GitHub Pages (branch `main`, folder `/docs`), but Pages is not enabled.
- `src/` holds the generator: `imgs.py` (WebP conversion), `build.py` (pages and data), templates, CSS and JS, and `check.py`/`shots.py` (Playwright checks).

Rebuild: `python3 src/imgs.py && python3 src/build.py` (expects the source book at `/workspace/book_of_astrologies`).
