# Layoff & Youth Jobs Tracker

Static dashboard (GitHub Pages): major layoff announcements Oct 2024 – Oct 2026 and youth / recent-graduate unemployment in the US and China.

- `site/` — the website (no build step; Chart.js via CDN). Data in `site/data/*.json`, each with source URL and as-of date.
- `scripts/update.py` — manually refresh BLS, NY Fed, Layoffs.fyi and China NBS series: `python3 scripts/update.py`
- `scripts/build_static.py` — hand-verified layoff rows, fact-checks, Challenger monthly totals.

Unofficial; every figure links to its source. Announcements are not completed layoffs.
