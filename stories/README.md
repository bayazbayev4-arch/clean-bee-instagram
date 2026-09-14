# Reusable stories

Rendered with `skills/daily-ig-post/scripts/story.py` (1080×1920, top 250 px and bottom 350 px kept clear). Metricool media URL: `https://raw.githubusercontent.com/bayazbayev4-arch/clean-bee-instagram/main/stories/<file>`.

| File | Story | Valid until |
|---|---|---|
| `00-opening-28-09.png` | Скоро открытие · 28.09 | 27-09-2026 |
| `01-how-it-works.png` | Как это работает — 3 шага | evergreen |
| `02-promo-25.png` | Акция −25% до 31 декабря | 31-12-2026 |
| `03-first-order-free.png` | Первый заказ — забор и доставка бесплатно | while the offer is live |
| `04-pay-after-inspection.png` | Честная цена — платите после осмотра | evergreen |

## Scheduled in Metricool (14-09-2026, live, type STORY)
- 15-09 → 27-09: 5 a day — 09:00 `00`, 12:00 `01`, 15:00 `02`, 18:00 `03`, 21:00 `04`.
- 28-09: 4 — 09:00 `01`, 13:00 `02`, 17:00 `03`, 21:00 `04`.
- **Next batch due before 28-09:** from 29-09, 4 a day (01–04) at 09:00 / 13:00 / 17:00 / 21:00. Drop `02` after 31-12.

Metricool `createScheduledPost` info for a story: no `text`, `"instagramData": {"type": "STORY"}`, `media` = the raw URL.
