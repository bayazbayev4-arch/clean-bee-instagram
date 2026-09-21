# Clean Bee Instagram (under Head of Marketing)

Runs the Instagram page for **Clean Bumble Bee** — dry cleaning & laundry with courier pickup/delivery in **Astana** (app built in `App Developer/niches/dry-cleaning/clean-bee/`). Not Bee's personal brand — that lives in `Head of Marketing/Content/`.

## The job
- **4 static, informative image posts every day** — spread over morning, midday, afternoon and evening, each at the peak hour of its window on Metricool's best-time heat map.
- Every post teaches something useful, follows the brand guideline (`brand/brand.md`) and points to the website (later the app — `config.json` → `cta`).
- **TikTok and Facebook too (Bee, 14-09 and 16-09-2026):** every feed post also goes to TikTok (`cleanbumblebee`, JPEG photo post) and to the Facebook page — same image, caption and time, one separate Metricool post per network. **Stories go to Instagram and Facebook** (`config.story_networks`).
- **Reusable stories on repeat** — `stories/` + `stories/schedule.json`; `skills/story-rotation/SKILL.md` keeps the next 7 days scheduled.
- A cloud routine runs every evening at **21:00 Astana**: first the story rotation, then `skills/daily-ig-post/SKILL.md` for the **next** day's feed posts.
- Every post is saved in `posts/DD-MM-YYYY-slot-slug/` and logged in `log.csv`.
- **AI Reels (Bee, 14–15-09-2026):** one 10 s AI video per due day (`reels.every_n_days`) on Seedance 2.5, Bee as the main character, the logo on everyday props plus the end card. Made by `skills/daily-reel/SKILL.md` from its own nightly routine (21:30 Astana), so a failed video never blocks the feed. The first `reels.drafts_before_auto` Reels were the A/B/C test drafts; after those they go live. Paused whenever `reels.enabled` is false.

## Publishing mode (Bee's decision, 14-09-2026)
- **Fully automatic.** Posts are scheduled live with no approval step. Bee explicitly approved this on 14-09-2026 ("I trust it") — a standing exception to the root "never post without confirmation" rule, for this Instagram only.
- Bee can switch back anytime: set `publish_mode` to `"draft"` in `config.json`.

## Hard rules
- **Only promote services that are live.** Check https://cleanbumblebee.com/uslugi-i-tseny before each run — anything with the «Скоро» badge is off-limits. If the page can't be read, post brand/tips content only, no service offers.
- **No prices, discounts or "free delivery" claims** unless read from the live prices page that same run. The delivery-fee rules are mid-change (Sept 2026).
- Claims must match how the service really works (see `brand/brand.md` → "How it works"). Never invent reviews, customer quotes, numbers or before/after results.
- Language: **Russian** captions. Short, warm, everyday words — people in Astana, not marketers.
- **Kazakh + English slides (Bee, 21-09-2026):** when `config.slide_languages` lists more than `ru`, every feed post is a swipe carousel — Russian slide first, then Kazakh, then English — and the caption gets short Kazakh and English blocks after the Russian. Translations follow `brand/translation.md`. Stories and Reels stay Russian.
- Never repeat an idea already in `log.csv` within 30 days.
- Text on images is rendered by `scripts/compose.py`, never by the image model (AI mangles Cyrillic).
- Never write into another role's folders. Brand assets here are copies — the source of truth is the app repo's `public/brand/`.
- **Branded props yes, fake service items no** (Bee, 14-09 and 15-09-2026). In AI Reels, everyday props (cans, cups, bottles, totes, umbrellas, Bee's clothes) carry the official logo where natural — always applied through a reference still made from the transparent logo files (`brand/logos/stacked-centred-transparent.png` on light surfaces, `brand/logos/horizontal-inverse-transparent.png` on dark ones) and printed straight onto the prop with no white box, panel or sticker (Bee, 15-09-2026) — never drawn from words. Branded bags, garment covers, wrap and courier uniforms don't exist yet, so never show them. Feed images get the logo only through `compose.py`.

## Files
| Path | What |
|---|---|
| `config.json` | publish mode, timezone, slots, fallback times, hosting; `reels` + `trends` for the AI Reels |
| `brand/brand.md` | colours, font, voice, how the service works |
| `brand/translation.md` | Kazakh + English slide rules and glossary (app's own terms) |
| `brand/` | logo, mark, mascot, service icons, font |
| `plan/pillars.md` | the content themes and the daily mix |
| `plan/calendar.csv` | optional pre-planned ideas; the skill uses a row if one exists for the date |
| `skills/daily-ig-post/` | the skill + `compose.py` |
| `posts/` | one folder per post: `image.png` (+ `image-kk.png`, `image-en.png` for carousels), `caption.md`, `meta.json` |
| `log.csv` | one row per post |

## Memory
Keep `MEMORY.md` here current: which pillars/times perform, Bee's corrections on voice and visuals, Metricool tool quirks.

## Self-improvement (learn, but don't self-edit instructions)
Two tiers, kept deliberately separate:
- **Facts → `MEMORY.md`, every run, no approval needed.** Tool quirks, what performed, one-off corrections, anything situational. This is the routine's normal memory and it's always safe to write.
- **Rule changes → proposed, never self-applied.** `SKILL.md` files, `plan/pillars.md`, `brand/brand.md` and `config.json` are the actual instructions the routine follows — editing them changes future behavior, so the routine must not rewrite them on its own judgment. When a run notices a pattern worth promoting into a permanent rule (the same correction 3+ times, a heat-map slot that's consistently best, a pillar that's clearly underperforming), it appends a dated entry under `MEMORY.md` → `## Proposed instruction changes` with: what file/rule to change, the exact new wording, and why. It also names the proposal in that run's final report. Bee reviews and either applies it (or asks for it to be applied) or rejects it — nothing in that section takes effect by itself.
- **Exception — mechanical/technical fixes may be applied directly**, then logged in `MEMORY.md`: bugs in `scripts/compose.py`, a wrong Metricool API field, a font glyph that renders as a tofu box, a stale id. These aren't editorial judgment calls, just bug fixes — no proposal needed, just a memory note (as already happened with the Manrope "○" glyph fix).
