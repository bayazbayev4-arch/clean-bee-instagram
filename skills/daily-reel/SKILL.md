---
name: daily-reel
description: Make and schedule one AI "trend" Reel for Clean Bumble Bee — scan this week's AI videos (Apify), pick a format that fits a clothes moment Clean Bee solves, write an original timed prompt with Bee as the main character, make reference stills (branded props where natural) and a 10 s vertical video on Higgsfield, add the real-logo end card, host it on the media branch and schedule it as an Instagram Reel + TikTok in Metricool. Use for the nightly reel routine, "make a Clean Bee reel", or "run the A/B/C test".
---

# Daily AI Reel — Clean Bumble Bee

Paths are relative to the `Clean Bee Instagram/` folder. Read `CLAUDE.md`, `MEMORY.md`, `config.json` (`reels`, `trends`, `cta`), `brand/brand.md`, `reels/prompts/example-street-collision.md` and `reels/formats.md` first.

## 0. Gate — does this run make a Reel?
- `config.reels.enabled` is false → reply "reels paused", stop.
- Target date = **tomorrow** in `config.timezone` (unless Bee names a date).
- Due: take the last row in `reels/log.csv` with status `scheduled` or `draft`; next due date = its `date` + `reels.every_n_days`. Target date earlier → "next reel DD-MM", stop. No rows → due.
- `getScheduledPosts` for the target date already has an Instagram REEL → "already done", stop.
- Credits: Higgsfield `balance`. Needed = `reels.models[model].credits` × 2 (room for one redo) + 8 (stills) + `reels.credit_reserve`. Less → stop, report "not enough credits: have X, need Y". Never buy or top up anything.
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
- **Branded props (Bee, 15-09-2026):** when the story has a natural everyday object — a drink can, a coffee cup, a water bottle, a tote bag, an umbrella, a phone case, Bee's T-shirt or cap — it carries the official Clean Bumble Bee logo, printed straight onto the prop like real merch — no white box, panel or sticker behind it (Bee, 15-09-2026). The logo only ever comes from a reference still (step 3), never from words in the video prompt. **Service items don't exist yet** (branded bags, garment covers, wrap, courier uniforms — Bee, 14-09-2026): never show branded versions of them. No other text, letters, signs, brands or screens with writing in the video.
- Fetch https://cleanbumblebee.com/uslugi-i-tseny: tie the concept only to services without «Скоро». No prices, discounts, speed or "free" claims unless read on that page in this run. Fetch fails → keep the tie-in general (stains, clothes care), no service names.
- Skip ideas already in `reels/log.csv` in the last 30 days.
- Folder `reels/DD-MM-YYYY-<short-latin-slug>/` → `concept.md`: trend link(s), the format in one line, the story in 3 beats, which prop carries the logo, the end-card line (Russian, ≤ 6 words, voice rules from brand.md).

## 3. Reference stills (Higgsfield)
- **@PERSON:** `generate_image`, model `nano_banana_pro`, `aspect_ratio` 9:16, `resolution` 2k. Prompt starts with `<<<reels.person_element_id>>>`, then: full body, the concept's outfit, plain light background, photoreal, sharp face, "no text, no logos". This AI still — not Bee's raw photo — goes into the video.
- **@PROP** stills (0–2) only for objects the story needs: `nano_banana_pro`, `aspect_ratio` 1:1, `resolution` 2k, plain light-grey background, photoreal.
  - **Branded** (everyday objects, see step 2): pick the logo by the colour of the surface it's printed on — light or mid-tone → `reels.logo_element_id` (navy lettering); dark (black, navy, deep green, burgundy, charcoal) → `reels.logo_dark_element_id` (white lettering). Both are transparent cut-outs. Prompt: the object first, then `the exact logo from <<<id>>> printed directly onto its surface — transparent background: only the bee and the lettering, no white box, panel, sticker, badge or outline around it; the object's own colour and pattern run right up to the logo; same artwork, colours and spelling, not redrawn; large and facing the camera`, then "no other text, letters or logos". On a busy pattern, put the logo on a calmer part of it — never add a box to make it read.
  - **Plain** (service items, or an object where a logo would look wrong): "no text, no letters, no logo".
- `jobs_wait` until done, download, **Read every still**. Person: not Bee's face / broken hands / any letters → redo once. Branded prop: compare the logo with `reels.logo_file` (dark surfaces: `reels.logo_dark_file`) — misspelled "Clean Bumble Bee", wrong bee, extra letters, a warped mark, or a box, panel or sticker behind it → redo once; still wrong → make the plain version of that prop instead. Save as `refs/person.png`, `refs/<prop>.png`.
- How the stills reach the video depends on `reels.models[model].refs`:
  - `"image_references"` → pass the image job ids in `medias` with role `image_references`, and call them "the person from image 1", "the cup from image 2" in the prompt.
  - `"elements"` → save each still as an Element (`show_reference_elements`, action `create`, medias `[{"id": <image job id>, "url": <result url>, "type": "image_job"}]`, name `cb-<ref>-DDMM`) and write `<<<element_id>>>` in the prompt where the reference goes.

## 4. Prompt — `prompt.md`
Same shape as `reels/prompts/example-street-collision.md`:
- One continuous shot (or clearly marked cuts), framed for vertical 9:16.
- `SUBJECT: the person from <ref> — identical face and outfit.` plus one line per prop with "identical" locks — for a branded prop: "identical object, label artwork and Clean Bumble Bee logo".
- Second-by-second beats covering 0.0–10.0 s. The clothes moment lands by ~7 s; give a branded prop at least one calm, close beat (slow motion or a macro hold) so the logo reads; the last 1–2 s are calm and readable because the end card follows.
- A `STYLE:` line (lens, grade, light) and a sound line (ambience, foley, music described in words). No dialogue, no voice-over.
- Last sentence: with a branded prop → "No other text, letters or logos besides the Clean Bumble Bee logo on the <prop>."; without → "No text, no letters, no logos, no watermarks."

## 5. Generate the video
- `generate_video` with `model` = `reels.model`, `aspect_ratio` = `reels.aspect_ratio`, that model's `params` from config, references as in step 3. Call once with `get_cost: true` first — above `credits` × 1.2 → stop and report.
- The server sometimes answers with a preset recommendation instead of a job ("Preset … was recommended instead of submitting a job") — nothing started and nothing was charged. Resubmit the same request with `declined_preset_id` = that preset's id (seen 15-09-2026 on all three test models).
- `jobs_wait` until done (5–10 min), download the result to `raw.mp4`.
- Refused (real face / moderation) → retry once. Refused again → log `failed`, report, stop. Never switch models on your own.
- Check: frames at 1, 4, 7 and 9.5 s (`ffmpeg -ss <t> -i raw.mp4 -frames:v 1 frames/<t>.png`) and **Read them**. Redo once with the same prompt if the face isn't Bee, hands or limbs break, objects melt, text or logos appear other than the prop's Clean Bee logo, the logo is clearly warped in a close-up, or the clothes moment is missing. Second take also bad → log `failed`, report, stop.
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
- `meta.json`: date, time, time_source, mode, model, credits_spent, trend_urls, element_ids, image_job_ids, branded_props, video_job_id, video_url, metricool_post_id, tiktok_post_id, qa.
- Append one row to `reels/log.csv` (status `scheduled` / `draft` / `failed` + reason in `notes`).
- `git add reels/<folder> reels/log.csv reels/trends` (explicit paths only) → commit → push `main`. Stills, frames and videos stay out of git (`reels/.gitignore`).
- Facts learned → `MEMORY.md`. Rule changes → `MEMORY.md` → "Proposed instruction changes" (CLAUDE.md → Self-improvement). Never edit this SKILL.md, `reels/formats.md` or `config.json` yourself.

## A/B/C model test (only when Bee asks)
- Prompt: `reels/prompts/example-street-collision.md`, unchanged.
- Stills, made once and shared by all models: **@PERSON** — Bee (from `reels.person_element_id`) in a white T-shirt under an open light-blue linen shirt, navy chinos, white sneakers; **@GLASSES** — gold metal aviator sunglasses with amber-tinted lenses; **@DRINK** — a slim aluminium can of pink lemonade with pastel abstract label art.
- Run the prompt on each model with its config `params` and `refs` style. One retry per model for technical failures only — the comparison is on first takes.
- Each gets an end card (line «Пятно? Курьер заберёт у двери»), its own folder `reels/DD-MM-YYYY-abc-<model>/` and a Metricool **draft** (Instagram only) on the same evening, 30 min apart, caption starting «A/B/C тест: <model>».
- Log all as `draft` — they count toward `drafts_before_auto`.
- Report: credits per model and what each got right or wrong (face, props, slow motion, stray letters), then one recommendation. First run 15-09-2026: Seedance 2.5 won (see MEMORY.md).

## 11. Report
Russian, 3–6 short lines: date and time, draft or live, model and credits, the concept in one line, links, failures. Name any proposal added to MEMORY.md.
