---
name: daily-reel
description: Make and schedule one AI "trend" Reel for Clean Bumble Bee — scan this week's AI videos (Apify), pick a format that fits a clothes moment Clean Bee solves, write an original timed prompt with Bee as the main character, make reference stills and a 10 s vertical video on Higgsfield, add the real-logo end card, host it on the media branch and schedule it as an Instagram Reel + TikTok in Metricool. Use for the nightly reel routine, "make a Clean Bee reel", or "run the A/B/C test".
---

# Daily AI Reel — Clean Bumble Bee

Paths are relative to the `Clean Bee Instagram/` folder. Read `CLAUDE.md`, `MEMORY.md`, `config.json` (`reels`, `trends`, `cta`), `brand/brand.md`, `reels/prompts/example-street-collision.md` and `reels/formats.md` first.

## 0. Gate — does this run make a Reel?
- `config.reels.enabled` is false → reply "reels paused", stop.
- Target date = **tomorrow** in `config.timezone` (unless Bee names a date).
- Due: take the last row in `reels/log.csv` with status `scheduled` or `draft`; next due date = its `date` + `reels.every_n_days`. Target date earlier → "next reel DD-MM", stop. No rows → due.
- `getScheduledPosts` for the target date already has an Instagram REEL → "already done", stop.
- Credits: Higgsfield `balance`. Needed = `reels.models[model].credits` × 2 (room for one redo) + 6 (stills) + `reels.credit_reserve`. Less → stop, report "not enough credits: have X, need Y". Never buy or top up anything.
- Mode: rows in `reels/log.csv` with status `draft` < `reels.drafts_before_auto` → this Reel is a Metricool **draft** (Bee approves it on his phone). Otherwise it goes live.

## 1. Find this week's AI video formats (Apify connector)
- **TikTok:** one run of `trends.tiktok.actor` per keyword in `trends.tiktok.keywords`, input `{"keywords": [kw], "maxItems": per_keyword, ...trends.tiktok.input}` (one keyword per run — with several keywords the actor fills `maxItems` from the first one only). Fields: `title`, `views`, `likes`, `shares`, `uploadedAt` (unix), `postPage`, `hashtags`, `video.duration`, `video.cover`.
- **Instagram:** one run of `trends.instagram.actor` per query in `trends.instagram.queries`, input `{"query": q, "maxPages": 1}`. Fields: `code` (link = `https://www.instagram.com/reel/<code>/`), `caption.text`, `play_count`, `like_count`, `taken_at_date`, `video_duration`, `thumbnail_url`.
- Keep posts from the last 30 days, 5–20 s long, clearly AI-made (caption/hashtags name a model or AI, or the cover shows an impossible shot). Rank by views. The search results are noisy — plenty of low-view or unrelated posts; judge the *format*, not the numbers alone.
- Look at the top ~8 covers if they download (the cloud network may block TikTok/Instagram image hosts — then judge from caption, hashtags and stats).
- Save the shortlist to `reels/trends/DD-MM-YYYY.json`: url, views, date, the format in one line, fit 0–3.
- Apify unavailable or nothing scores ≥ 2 → take a format from `reels/formats.md` and note "no trend used".

## 2. Pick one, write an original concept
- Borrow the **format** (camera move, effect, story beat) — never the clip: don't recreate its shots, reuse its audio, people, characters or brands, and never download or re-upload anyone's video.
- Every concept needs a clothes moment Clean Bee solves: a stain or spill, mud or slush, wrinkles, a suit or dress for an event, a winter coat, bedding. Bee is the main character.
- **No Clean Bee items exist** (Bee, 14-09-2026: no branded bags, garment covers, wrap, uniforms or merch) → never show branded items or the logo inside the video. The brand appears only on the end card. No text, letters, signs or screens with writing in the video either.
- Fetch https://cleanbumblebee.com/uslugi-i-tseny: tie the concept only to services without «Скоро». No prices, discounts, speed or "free" claims unless read on that page in this run. Fetch fails → keep the tie-in general (stains, clothes care), no service names.
- Skip ideas already in `reels/log.csv` in the last 30 days.
- Folder `reels/DD-MM-YYYY-<short-latin-slug>/` → `concept.md`: trend link(s), the format in one line, the story in 3 beats, the end-card line (Russian, ≤ 6 words, voice rules from brand.md).

## 3. Reference stills (Higgsfield)
- **@PERSON:** `generate_image`, model `nano_banana_pro`, `aspect_ratio` 9:16, `resolution` 2k. Prompt starts with `<<<reels.person_element_id>>>`, then: full body, the concept's outfit, plain light background, photoreal, sharp face, "no text, no logos". This AI still — not Bee's raw photo — goes into the video: Seedance models reject real-person photos.
- **@PROP** stills (0–2) only for objects the story needs (a cup, an umbrella…): generic, unbranded, "no text, no letters, no logo".
- `jobs_wait` until done, download, **Read every still**. Not Bee's face / broken hands / any letters → redo once. Save as `refs/person.png`, `refs/<prop>.png`.
- How the stills reach the video depends on `reels.models[model].refs`:
  - `"elements"` → save each still as an Element (`show_reference_elements`, action `create`, medias `[{"id": <image job id>, "url": <result url>, "type": "image_job"}]`, name `cb-<ref>-DDMM`) and write `<<<element_id>>>` in the prompt where the reference goes.
  - `"image_references"` → pass the image job ids in `medias` with role `image_references`, and call them "the person from image 1", "the cup from image 2" in the prompt.

## 4. Prompt — `prompt.md`
Same shape as `reels/prompts/example-street-collision.md`:
- One continuous shot (or clearly marked cuts), framed for vertical 9:16.
- `SUBJECT: the person from <ref> — identical face and outfit.` plus one line per prop with "identical" locks.
- Second-by-second beats covering 0.0–10.0 s. The clothes moment lands by ~7 s; the last 1–2 s are calm and readable because the end card follows.
- A `STYLE:` line (lens, grade, light) and a sound line (ambience, foley, music described in words). No dialogue, no voice-over.
- Last sentence: "No text, no letters, no logos, no watermarks."

## 5. Generate the video
- `generate_video` with `model` = `reels.model`, `aspect_ratio` = `reels.aspect_ratio`, that model's `params` from config, references as in step 3. Call once with `get_cost: true` first — above `credits` × 1.2 → stop and report.
- The server sometimes answers with a preset recommendation instead of a job ("Preset … was recommended instead of submitting a job") — nothing started and nothing was charged. Resubmit the same request with `declined_preset_id` = that preset's id (seen 15-09-2026 on all three test models).
- `jobs_wait` until done (5–10 min), download the result to `raw.mp4`.
- Refused (real face / moderation) → retry once with the person still as an `image_references` media instead of an Element. Refused again → log `failed`, report, stop. Never switch models on your own.
- Check: frames at 1, 4, 7 and 9.5 s (`ffmpeg -ss <t> -i raw.mp4 -frames:v 1 frames/<t>.png`) and **Read them**. Redo once with the same prompt if the face isn't Bee, hands or limbs break, objects melt, letters or logos appear, or the clothes moment is missing. Second take also bad → log `failed`, report, stop.
- No ffmpeg in the cloud → `pip install imageio-ffmpeg` and use `python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`.

## 6. End card
```
python3 skills/daily-reel/scripts/endcard.py --in reels/<folder>/raw.mp4 --out reels/<folder>/final.mp4 \
  --line "<end-card line>" --site "<config.cta.url>"
```
Adds 2 s of white card (official stacked logo, the line, Safe Blue pill with the site, «Ссылка в профиле») with a short fade; the video's sound fades out under it. Read one frame from the last second to confirm it looks right.

## 7. Host the video — `media` branch
```
bash skills/daily-reel/scripts/publish_media.sh reels/<folder>/final.mp4 <folder>.mp4
```
Prints the public commit-pinned URL. Videos never go on `main` (`reels/.gitignore`). `curl -sI <url>` must return 200 before scheduling — retry for up to ~2 min.

## 8. Caption — `caption.md`
- Russian, 20–60 words: a hook about the moment → one line tying it to Clean Bee (a fact from brand.md → "Facts you may state") → `config.cta.caption_line` → 4–6 hashtags (#астана #химчисткаастана …).
- Voice rules from brand.md. No invented numbers, reviews or promises.

## 9. Schedule in Metricool
- Time: `getBestTimeToPostByNetwork` (instagram, `Asia/Almaty`, target date). Take the best hour inside `reels.time_window` that is at least `reels.min_gap_from_feed_minutes` away from every feed post that day (`getScheduledPosts`). All zeros → `reels.fallback_time`.
- Instagram — `createScheduledPost`, `blogId` = `config.metricool_brand_id`, `date` with `+05:00`, `info`:
```json
{"autoPublish": true, "draft": <mode from step 0>, "descendants": [], "firstCommentText": "", "hasNotReadNotes": false,
 "media": ["<video URL>"], "mediaAltText": [], "providers": [{"network": "instagram"}],
 "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Asia/Almaty"},
 "shortener": false, "smartLinkData": {"ids": []}, "text": "<caption>",
 "instagramData": {"type": "REEL", "showReelOnFeed": true, "isAiGenerated": true}}
```
- TikTok — a **second, separate** post (same date, video and caption), `"providers": [{"network": "tiktok"}]`, no `instagramData`, and:
```json
"tiktokData": {"title": "<hook, max 90 chars>", "privacyOption": "PUBLIC_TO_EVERYONE", "disableComment": false, "disableDuet": false, "disableStitch": false, "autoAddMusic": false, "commercialContentThirdParty": false, "commercialContentOwnBrand": true, "isAigc": true}
```
- `isAiGenerated` / `isAigc` stay true: both platforms require the AI label on realistic AI video.

## 10. Save, log, commit
- `meta.json`: date, time, time_source, mode, model, credits_spent, trend_urls, element_ids, image_job_ids, video_job_id, video_url, metricool_post_id, tiktok_post_id.
- Append one row to `reels/log.csv` (status `scheduled` / `draft` / `failed` + reason in `notes`).
- `git add reels/<folder> reels/log.csv reels/trends` (explicit paths only) → commit → push `main`.
- Facts learned → `MEMORY.md`. Rule changes → `MEMORY.md` → "Proposed instruction changes" (CLAUDE.md → Self-improvement). Never edit this SKILL.md, `reels/formats.md` or `config.json` yourself.

## A/B/C model test (only when Bee asks)
- Prompt: `reels/prompts/example-street-collision.md`, unchanged.
- Stills, made once and shared by all three models: **@PERSON** — Bee (from `reels.person_element_id`) in a white T-shirt under an open light-blue linen shirt, navy chinos, white sneakers; **@GLASSES** — gold metal aviator sunglasses with amber-tinted lenses; **@DRINK** — a slim aluminium can of pink lemonade with pastel abstract label art, no letters or logos, cold condensation.
- Run the prompt on `kling3_0`, `seedance_2_5` and `cinematic_studio_3_0` with each model's config `params` and `refs` style. One redo per model at most.
- Each gets an end card (line «Пятно? Курьер заберёт у двери»), its own folder `reels/DD-MM-YYYY-abc-<model>/` and a Metricool **draft** (Instagram only) on the same evening, 30 min apart, caption starting «A/B/C тест: <model>».
- Log all three as `draft` — they are the first `drafts_before_auto` drafts.
- Report: credits per model and what each got right or wrong (face, glasses, can, slow motion, no stray letters), then one recommendation.

## 11. Report
Russian, 3–6 short lines: date and time, draft or live, model and credits, the concept in one line, links, failures. Name any proposal added to MEMORY.md.
