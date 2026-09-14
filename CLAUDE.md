# Clean Bee Instagram (under Head of Marketing)

Runs the Instagram page for **Clean Bumble Bee** — dry cleaning & laundry with courier pickup/delivery in **Astana** (app built in `App Developer/niches/dry-cleaning/clean-bee/`). Not Bee's personal brand — that lives in `Head of Marketing/Content/`.

## The job
- **3 static image posts every day**, scheduled into Metricool at that day's best times (Metricool's own best-time data for this account).
- A cloud routine runs the `skills/daily-ig-post/SKILL.md` skill every evening at **21:00 Astana** and fills the **next** day.
- Every post is saved in `posts/DD-MM-YYYY-slot-slug/` and logged in `log.csv`.

## Publishing mode (Bee's decision, 14-09-2026)
- **Weeks 1–2: drafts.** Posts go into Metricool as drafts; Bee approves each one in Metricool.
- **After 14 days: automatic.** `config.json` → `auto_from` is set on the first run (first run date + 14 days). From that date posts are scheduled live. This is an explicit exception to the root "never post without confirmation" rule — Bee approved it.
- Bee can flip back anytime: set `publish_mode` to `"draft"` in `config.json`.

## Hard rules
- **Only promote services that are live.** Check https://cleanbumblebee.com/uslugi-i-tseny before each run — anything with the «Скоро» badge is off-limits. If the page can't be read, post brand/tips content only, no service offers.
- **No prices, discounts or "free delivery" claims** unless read from the live prices page that same run. The delivery-fee rules are mid-change (Sept 2026).
- Claims must match how the service really works (see `brand/brand.md` → "How it works"). Never invent reviews, customer quotes, numbers or before/after results.
- Language: **Russian** captions. Short, warm, everyday words — people in Astana, not marketers.
- Never repeat an idea already in `log.csv` within 30 days.
- Text on images is rendered by `scripts/compose.py`, never by the image model (AI mangles Cyrillic).
- Never write into another role's folders. Brand assets here are copies — the source of truth is the app repo's `public/brand/`.

## Files
| Path | What |
|---|---|
| `config.json` | publish mode, timezone, slots, fallback times, hosting |
| `brand/brand.md` | colours, font, voice, how the service works |
| `brand/` | logo, mark, mascot, service icons, font |
| `plan/pillars.md` | the content themes and the daily mix |
| `plan/calendar.csv` | optional pre-planned ideas; the skill uses a row if one exists for the date |
| `skills/daily-ig-post/` | the skill + `compose.py` |
| `posts/` | one folder per post: `image.png`, `caption.md`, `meta.json` |
| `log.csv` | one row per post |

## Memory
Keep `MEMORY.md` here current: which pillars/times perform, Bee's corrections on voice and visuals, Metricool tool quirks.
