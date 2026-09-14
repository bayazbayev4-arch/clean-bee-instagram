# Clean Bumble Bee — brand sheet for Instagram

Source of truth: `App Developer/niches/dry-cleaning/clean-bee/References/Images/00-brand-guidelines/11-09-2026-clean-bumblebee-brand-identity-guidelines.pdf` (v2.0, 11-09-2026). This sheet is the Instagram-relevant summary. `compose.py` already applies every visual rule below.

## Colours
- **Vibrant Blue `#0690F1` is the majority colour.** Never under white text — use **Safe Blue `#0578CC`** for blue buttons/banners with white text.
- **Dark Navy `#1E2B94`** — headlines and small accents on white only. Never dominates a post; never dark/navy posts.
- **Warm Honey `#FFD16F`** — promos, highlight chips. Ice Sky `#BAEBFF`, Background Wash `#EAF6FE` for soft areas.
- **Text on pastel:** headline `#08528C`, body `#3D4759`. Never white or grey text on pastels.
- Body text on white: Deep Ink `#16233D`.
- The feel: airy, sparkling, bright — dominated by white and sky blue.

### One pastel per service (always pair the service with its own tint)
| Service | Tint | Icon |
|---|---|---|
| Стирка и складывание | `#BAEBFF` | `services/wash-fold.png` |
| Стирка и глажка | `#FAB4C3` | `services/wash-iron.png` |
| Химчистка | `#94EBE5` | `services/dry-cleaning.png` |
| Только глажка | `#FEE5AE` | `services/ironing.png` |
| Домашний текстиль | `#DED9FF` | `services/home-textiles.png` |
| Обувь | `#FFD6BF` | `services/shoes.png` |
| Особый уход | `#DDF4B8` | `services/special.png` |
General tips not tied to a service: `#BAEBFF` or `#EAF6FE`.

## Logos (only the official files in `logos/`)
- `primary-horizontal.png` — top of every post (on white). `inverse-on-blue.png` — on brand-blue areas. `stacked-centred.png`, `app-icon.png` — avatar/covers.
- Never stretch, recolour, add shadows/glows, place over busy or dark photos, or re-type the wordmark.
- **No 3D mascots, character poses or cartoon avatars.** The flat 2D bee mark (`cbb-mascot.png` = the mark) is fine as a small accent only.

## Typography
Manrope only (`fonts/`). Headlines ExtraBold, body Medium/SemiBold.

## Instagram feed format (guideline §08)
- **1080 × 1080.** Top ~15%: horizontal logo lockup with clear space.
- Centre: service icon on its pastel chip **or** a high-key photo.
- Headline: **max 6 words.**
- Bottom: Safe Blue pill button with the CTA (`config.json` → `cta.button_label`).

## Photography (for Higgsfield backgrounds)
- High-key natural morning light through windows; fresh Scandinavian / modern minimalist Astana interiors; crisp white bedsheets, fluffy towels, neatly pressed shirts; cheerful people enjoying free time.
- **Forbidden:** dark or industrial laundromats, fluorescent tubes, cluttered rooms, piles of dirty clothes, grain filters, gloomy light, any text/letters/logos in the image.

## Voice (Russian)
- Helpful & neighbourly, fast & direct, radically transparent. Short active sentences, «вы».
- Positive verbs: «Заберите время себе», «Оформите заказ за 60 секунд».
- Official lines you can use: «Чистота на лету», «Забудьте о стирке насовсем — курьер заберёт вещи прямо у двери», «Свежесть прямо к порогу».
- Vocabulary: Курьер · Доставка до двери · Фотофиксация при приёме · Защитный чехол для одежды · Особые пожелания к вещам.
- **Never:** logistics jargon («плечо курьера», «регламент обработки»), computer-error wording, over-promising turnaround before inspection, invented numbers.
- Emojis 0–2. Hashtags 5–8 (#астана #химчисткаастана #стиркаастана …).

## Facts you may state (how it works)
1. Choose services and a 2-hour pickup window — booking takes about a minute.
2. The courier picks up at the door; every bag gets its own code; the handover is photographed.
3. At the station items are inspected; the exact price comes as a Kaspi invoice; cleaning starts only after payment.
4. Clean items come back in the chosen window; status is visible online.
- Service area: Astana. Languages: Russian, Kazakh, English.
- **Numbers (turnaround hours, delivery fee, free-delivery threshold, prices) only if read from the live site in the same run.** The guideline PDF quotes numbers that are still changing — don't copy them.

## Services
Full catalogue above. Only promote services without the «Скоро» badge on https://cleanbumblebee.com/uslugi-i-tseny. On 14-09-2026 only **химчистка** and **домашний текстиль** were live. General care tips about any fabric are fine.
