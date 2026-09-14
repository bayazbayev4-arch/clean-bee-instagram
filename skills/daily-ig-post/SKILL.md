---
name: daily-ig-post
description: Make and schedule tomorrow's 3 static Instagram posts for Clean Bumble Bee (Astana dry cleaning) — pick ideas, generate backgrounds with Higgsfield, render Russian text + logo with compose.py, save to posts/, schedule in Metricool at its best times (draft or live per config.json), log everything. Use for the daily routine or when Bee says "make tomorrow's posts" / "make a Clean Bee post".
---

# Daily Instagram posts — Clean Bumble Bee

Paths are relative to the `Clean Bee Instagram/` folder. Read `CLAUDE.md`, `MEMORY.md`, `config.json`, `brand/brand.md`, `plan/pillars.md` first.

## 0. Date and mode
- Target date = **tomorrow** in `config.timezone` (unless Bee names a date).
- If `posts/` already has 3 folders for the target date, or `log.csv` has 3 non-failed rows for it → stop, report "already done".
- `publish_mode`:
  - `auto_from` is null → set it to today + 14 days (DD-MM-YYYY), write `config.json`.
  - today ≥ `auto_from` and `publish_mode` is `"draft"` → switch to `"auto"`, write `config.json`, note the switch in `MEMORY.md`.
  - Bee setting `publish_mode` back to `"draft"` by hand wins — only auto-switch once (record `"auto_switched": true` in config).

## 1. Check what's allowed to be promoted
- Fetch https://cleanbumblebee.com/uslugi-i-tseny. Services with «Скоро» are off-limits. Note live prices only if you'll use them.
- Fetch fails → no service-offer posts today; use tips / relatable / process posts only.

## 2. Pick 3 ideas
- If `plan/calendar.csv` has rows for the target date, use them.
- Otherwise one idea per group from `plan/pillars.md` (A morning, B midday, C evening).
- Reject anything whose idea is in `log.csv` in the last 30 days. Vary the layout: at least one `photo` and one `card` per day.
- For each: pillar, idea, headline (≤ 7 words, Russian), subline (≤ 12 words), caption, layout.

## 3. Times — Metricool best times
- `getBestTimeToPostByNetwork`: `brandId` = `config.metricool_brand_id`, `socialNetwork` `instagram`, `timezone` `Asia/Almaty`, from/to = target date 00:00–23:59 `+05:00`. (If the id is null: `getBrandSettings`, find `cleanbumblebee`, save its `id`.)
- All values 0 = no data yet (new account) → use `fallback_times`.
- Choose the 3 highest-scoring hours inside `posting_window`, at least `min_gap_hours` apart; earliest → group A, middle → B, latest → C.
- No data (new account) → `fallback_times`. Record which source was used in `meta.json`.

## 4. Make each image
1. **Background (photo layout)** — Higgsfield `generate_image`, portrait 4:5 (or 3:4 then crop), prompt in English: bright clean real-life scene tied to the idea (Astana apartment, coat on a hanger, folded linen, courier at a door), soft daylight, brand pastels (blue #0690F1 / light blue #BAEBFF / yellow #FFD16F accents), lots of empty space in the lower third, **"no text, no letters, no logos"**. Download the result to the post folder as `bg.png`.
2. **Card layout** — no generation. Pick `--bgcolor` from the pastels in `brand/brand.md`, `--icon` = the live service's icon from `brand/services/` or `brand/cbb-mascot.png`.
3. Render:
   ```
   python3 skills/daily-ig-post/scripts/compose.py --layout photo --bg posts/<folder>/bg.png \
     --headline "…" --sub "…" --out posts/<folder>/image.png
   ```
4. **Look at `image.png`** (Read it). Reject and redo (max 2 retries) if: text overflows or is hard to read, the model drew fake letters/logos, faces/hands look wrong, it looks dark or gloomy.

Folder name: `posts/DD-MM-YYYY-<a|b|c>-<short-latin-slug>/`.

## 5. Caption — `caption.md`
- Russian, 40–120 words, rules from `brand/brand.md` → Voice.
- Hook line first, value in the middle, one CTA last, then 5–8 hashtags.
- Facts only from "How it works" and the live prices page.

## 6. Host the image
- Metricool needs a public image URL. Use the method in `config.image_host` (set once Bee decides). If null → stop before scheduling, report that hosting isn't configured.

## 7. Schedule in Metricool
- Before creating, `getScheduledPosts` for the target date — skip any slot that already has a post (no duplicates on re-runs).
- `createScheduledPost` with `blogId` = `config.metricool_brand_id`, `date` = ISO with `+05:00`, and `info` JSON:
  ```json
  {"autoPublish": true, "draft": <true if publish_mode is "draft">, "descendants": [], "firstCommentText": "",
   "hasNotReadNotes": false, "media": ["<public image URL>"], "mediaAltText": ["<short Russian description>"],
   "providers": [{"network": "instagram"}], "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Asia/Almaty"},
   "shortener": false, "smartLinkData": {"ids": []}, "text": "<caption>",
   "instagramData": {"type": "POST", "isAiGenerated": <true if the background came from Higgsfield>}}
  ```
- Do NOT use `createScheduledPostForReview` — it needs a team plan and emails reviewers.

## 8. Save + log
- `meta.json`: date, slot, time, time_source, pillar, idea, layout, higgsfield_prompt, higgsfield_url, image_url, metricool_post_id, mode.
- Append a row to `log.csv` (status `scheduled`, `draft` or `failed` + reason).
- If running in the cloud repo: `git add posts log.csv config.json MEMORY.md && git commit -m "posts: <target date>" && git push`.

## 9. Report (short)
Target date, the 3 times, headline of each, mode, anything that failed. In draft mode end with: "3 drafts waiting in Metricool for approval."
