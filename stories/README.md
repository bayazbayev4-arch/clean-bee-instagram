# Reusable stories

Rendered with `skills/daily-ig-post/scripts/story.py` (1080×1920, top 250 px and bottom 350 px kept clear). Metricool media URL: `https://raw.githubusercontent.com/bayazbayev4-arch/clean-bee-instagram/main/stories/<file>`.

| File | Story | Valid until |
|---|---|---|
| `00-opening-28-09.png` | Скоро открытие · 28.09 | 27-09-2026 |
| `01-how-it-works.png` | Как это работает — 3 шага | evergreen |
| `02-promo-25.png` | Акция −25% до 31 декабря | 31-12-2026 |
| `03-first-order-free.png` | Первый заказ — забор и доставка бесплатно | while the offer is live |
| `04-pay-after-inspection.png` | Честная цена — платите после осмотра | evergreen |

## Autopilot
- The rotation lives in `schedule.json`: 15-09 → 27-09 5 a day (with the opening story), 28-09 → 31-12 4 a day, from 01-01-2027 3 a day (the −25% story drops out).
- The nightly routine runs `skills/story-rotation/SKILL.md` first: it keeps the next 7 days filled and only adds missing slots. It needs only the Metricool connector, so it works even while the feed-post part is blocked.
- 14-09-2026: 15-09 → 28-09 already scheduled by hand (69 stories).

Metricool `createScheduledPost` info for a story: no `text`, `"instagramData": {"type": "STORY"}`, `media` = the raw URL.
