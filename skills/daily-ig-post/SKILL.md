---
name: daily-ig-post
description: Make and schedule tomorrow's 4 static, informative Instagram posts for Clean Bumble Bee (Astana dry cleaning) — pick useful ideas, render on-brand 1080×1080 images with compose.py (Higgsfield only for photo backgrounds), save to posts/, schedule in Metricool at the peak hour of each time window from its best-time heat map, log everything. Use for the daily routine or when Bee says "make tomorrow's posts" / "make a Clean Bee post".
---

# Daily Instagram posts — Clean Bumble Bee

Paths are relative to the `Clean Bee Instagram/` folder. Read `CLAUDE.md`, `MEMORY.md`, `config.json`, `brand/brand.md`, `plan/pillars.md` first. `brand/brand.md` is the brand guideline summary — follow it.

## 0. Date and mode
- Target date = **tomorrow** in `config.timezone` (unless Bee names a date).
- `publish_mode`: `"auto"` → posts go live at their time. `"draft"` → Metricool drafts. Bee sets it; don't change it.
- `getScheduledPosts` for the target date. If it already has `posts_per_day` posts → stop, report "already done". Otherwise fill only the missing slots.

## 1. What may be promoted
- Fetch https://cleanbumblebee.com/uslugi-i-tseny. Services with «Скоро» are off-limits for offers. Read any number you plan to use (price, fee, threshold, turnaround) from this page in this run.
- Fetch fails → no service offers and no numbers; general care tips + how-it-works posts only.

## 2. Pick 4 ideas
- Rows in `plan/calendar.csv` for the target date win. Otherwise one idea per slot from `plan/pillars.md` (a morning tip, b myth/fact, c how it works, d seasonal photo).
- Reject ideas already in `log.csv` in the last 30 days.
- Every post must teach something concrete. Headline ≤ 6 words. Tips ≤ 7 words each.

## 3. Times — peak of each window (Metricool heat map)
- `getBestTimeToPostByNetwork`: `brandId` = `config.metricool_brand_id`, `socialNetwork` `instagram`, `timezone` `Asia/Almaty`, from/to = target date 00:00–23:59 `+05:00`. The response is Metricool's heat map: a value per hour, higher = better.
- For each of the 4 `time_windows`, take the hour with the highest value → slots a, b, c, d. If two picks are closer than `min_gap_hours`, move the later one to its window's next-best hour.
- A window whose values are all 0 → that slot's `fallback_times` entry. Record `time_source` (`heatmap` / `fallback`) in `meta.json`.

## 4. Make each image — `scripts/compose.py`
Never let an image model draw text. Pick the layout from the pillar:

| Layout | Use | Key args |
|---|---|---|
| `tips` | 3 quick steps/tips | `--headline`, `--tips "…|…|…"`, `--tint`, `--icon` |
| `fact` | myth vs fact, label decoder, one clear message | `--eyebrow "МИФ"`, `--headline`, `--sub`, `--tint`, `--icon` |
| `photo` | seasonal / lifestyle | `--bg`, `--headline`, `--sub` |

All layouts add the official logo on top and the Safe Blue CTA button (`--button` = `config.cta.button_label`) at the bottom.
- `--tint` + `--icon`: the service's pastel and icon from the table in `brand/brand.md`; general tips → `#BAEBFF` + the closest service icon.
- **Photo backgrounds:** Higgsfield `generate_image`, aspect 1:1 (or 4:3 — compose crops), English prompt following brand.md → Photography, ending with "no text, no letters, no logos, no watermark". Wait for the job, download `result_url` to `posts/<folder>/bg.png`. Download blocked → switch that slot to `fact` instead of failing.

```
python3 skills/daily-ig-post/scripts/compose.py --layout tips --tint "#94EBE5" \
  --icon brand/services/dry-cleaning.png --headline "Как хранить пальто летом" \
  --tips "Почистите перед хранением|Используйте дышащий чехол|Держите вдали от солнца" \
  --button "Заказать на cleanbumblebee.com" --out posts/<folder>/image.png
```

**Look at every `image.png`** (Read it). Redo (max 2 tries) if text is cut, cramped or hard to read, the photo is dark/cluttered, or the model drew letters/logos.

Folder: `posts/DD-MM-YYYY-<a|b|c|d>-<short-latin-slug>/`.

## 5. Caption — `caption.md`
- Russian, 50–130 words, voice rules in `brand/brand.md`.
- Hook line → the useful content (3–5 sentences or a short list with «—») → `config.cta.caption_line` → 5–8 hashtags.
- Facts only from brand.md → "Facts you may state" and numbers read live in step 1.

## 6. Publish the image
- `compose.py` writes `image.png` (Instagram) and `image.jpg` (TikTok — it rejects PNG with "The 'image/png' type is not allowed, use 'image/jpeg' or 'image/webp'"). A folder without `image.jpg` → `python3 -c "from PIL import Image; Image.open('posts/<folder>/image.png').convert('RGB').save('posts/<folder>/image.jpg', quality=92, subsampling=0)"`.
- `git add posts && git commit -m "posts: <date>" && git push`.
- Image URLs = `config.image_url_pattern` (PNG, Instagram) and `config.tiktok_image_url_pattern` (JPEG, TikTok) with the folder. Confirm both return HTTP 200 (`curl -sI`) before scheduling; raw GitHub can lag ~1 min, retry.

## 7. Schedule in Metricool
`createScheduledPost` with `blogId` = `config.metricool_brand_id`, `date` = ISO with `+05:00`, `info`:
```json
{"autoPublish": true, "draft": <publish_mode == "draft">, "descendants": [], "firstCommentText": "",
 "hasNotReadNotes": false, "media": ["<image URL>"], "mediaAltText": ["<short Russian description>"],
 "providers": [{"network": "instagram"}], "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Asia/Almaty"},
 "shortener": false, "smartLinkData": {"ids": []}, "text": "<caption>",
 "instagramData": {"type": "POST", "isAiGenerated": <true only if a Higgsfield photo is used>}}
```
Metricool copies the image to its own storage on creation. Don't use `createScheduledPostForReview`.

**TikTok (Bee, 14-09-2026 — feed posts only, never stories):** for every post in `config.networks` beyond Instagram, make a **second, separate** `createScheduledPost` with the same date and caption and the **JPEG** image URL (`config.tiktok_image_url_pattern` — a PNG fails with "The 'image/png' type is not allowed"), `"providers": [{"network": "tiktok"}]`, no `instagramData`, and:
```json
"tiktokData": {"title": "<headline, max 90 chars>", "privacyOption": "PUBLIC_TO_EVERYONE", "disableComment": false, "disableDuet": false, "disableStitch": false, "autoAddMusic": true, "photoCoverIndex": 0, "commercialContentThirdParty": false, "commercialContentOwnBrand": true, "isAigc": false}
```
Separate posts keep one network's error from blocking the other. When counting "already done" for a date, count Instagram posts only (`instagramData.type == "POST"` with an instagram provider); if Instagram is full but a TikTok copy is missing, add just the TikTok copy. Log both ids in `meta.json` (`metricool_post_id`, `tiktok_post_id`).

## 8. Save + log
- `meta.json`: date, slot, time, time_source, pillar, idea, layout, higgsfield_prompt, image_url, metricool_post_id, mode.
- Append one row per post to `log.csv` (status `scheduled` / `draft` / `failed` + reason). Note anything learned in `MEMORY.md`.
- Commit and push.

## 9. Learn, don't self-edit rules
Facts (what performed, corrections, tool quirks) always go straight into `MEMORY.md` — no approval needed. If you notice a pattern worth becoming a permanent rule (same correction 3+ times, a slot/pillar that's consistently over- or under-performing, a heat-map hour that's reliably best) — do NOT edit this SKILL.md, `plan/pillars.md`, `brand/brand.md` or `config.json` yourself. Instead add a dated entry to `MEMORY.md` → `## Proposed instruction changes` (file/rule, exact proposed wording, why) and mention it in the final report. Pure mechanical/technical fixes (a compose.py bug, a wrong API field, a font glyph issue) are the one exception — fix those directly and just log them, no proposal needed.

## 10. Report
Russian, short: date, 4 times + headlines, live or draft, failures. If step 9 added a proposal, name it in one line ("предложение в MEMORY.md: …").
