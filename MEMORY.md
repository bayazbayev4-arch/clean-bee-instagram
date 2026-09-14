# Clean Bee Instagram — Memory

## Voice
- Russian, simple everyday words, informative first (see brand/brand.md, taken from the 11-09-2026 brand guideline PDF).

## Process
- 14-09-2026 (Bee): **4 posts/day, fully automatic (no approval)**, each at the peak hour of its window on Metricool's heat map; every post informative, on-brand, CTA to cleanbumblebee.com (switch config `cta` to the app once it's in the App Store).
- Next day filled at 21:00 Astana by the cloud routine.

## Projects
- **Stories (14-09-2026):** 5 reusable stories in `stories/` (see its README). 69 scheduled live for 15-09 → 28-09 by hand. **On autopilot:** the nightly routine runs `skills/story-rotation/SKILL.md` first and keeps 7 days ahead filled from `stories/schedule.json` (−25% story drops out 01-01-2027 via the schedule).
- **Clean Bumble Bee opens 28-09-2026** (Bee). Bio in `brand/instagram-bio.md` — swap to the "after opening" version that day. Live offers 14-09: −25% on everything until 31.12, first order free pickup/delivery, then free from 10 000 ₸ (500 ₸/trip otherwise).
- Public repo bayazbayev4-arch/clean-bee-instagram (images served from raw.githubusercontent.com). Cloud routine **trig_01BPXHcuLGJnHNtob7Jbykmv**, cron `0 16 * * *` UTC = 21:00 Astana.
- 15-09-2026: 4 live posts made by hand from the local session (Metricool ids 375498575, 375499113, 375498777, 375498902).
- **Routine blocked (first run 14-09-2026):** (1) `git push` 403 — the Claude GitHub App was never installed on Bee's GitHub account; (2) the cloud environment's network blocked the Higgsfield CDN and cleanbumblebee.com.
  - (2) FIXED 14-09-2026: Default cloud environment → Network access **Custom**, allowed `d8j0ntlcm91z4.cloudfront.net` + `cleanbumblebee.com`, "include default list" kept on (keeps the Trusted list; GitHub and MCP traffic bypass the allowlist anyway).
  - (1) FIXED 14-09-2026: Claude GitHub App installed (installation 161596437), repository access = only `clean-bee-instagram`. Bee did GitHub's email verification.
- **14-09-2026 one-off test run (Bee's request):** target date forced to 16-09-2026 instead of tomorrow, everything else normal. First end-to-end proof from the cloud session: git push, Higgsfield fetch, cleanbumblebee.com fetch, raw GitHub 200 checks and Metricool scheduling all worked with no blockers — the (1)/(2) fixes above hold. Story rotation: all 7 days (15-09 → 21-09) already had their 5 slots each from the earlier by-hand scheduling — 0 added. Feed: 4 posts scheduled live for 16-09-2026 (Metricool ids 375585971, 375586019, 375586070, 375586096) — new ideas (coffee stain, care-label circle symbol, bag-code/photo/online-status transparency, coats+puffer before heating season), since the pillar ideas already used were 15-09's (30-day repeat rule). Heat map was still all zero → fallback times again. One redo: `layout fact` with a literal "○" character in `--sub` renders as a tofu box — the Manrope subsets have no glyph for it and there's no fallback face; describe it in words ("значок-кружок") instead of using the Unicode circle character.
  - Runs on 14-09 and 15-09 at 21:00 will find 15-09 / 16-09 already full and add no feed posts. First normal run that makes feed posts: **16-09-2026 21:00 → fills 17-09** — check that log.
  - Fixed after the test: post b (16-09) said the circle symbol means "dry clean only, never wash at home" — wrong. Circle = professional cleaning allowed; home washing is the washtub symbol. Image + caption corrected and the Metricool post updated (new id 375589063). When replacing an image at the same path, give Metricool the commit-pinned raw URL (`.../<commit-sha>/posts/...`) — the `main` URL can serve the cached old file for a few minutes.

- **TikTok (Bee, 14-09-2026): feed posts only, stories stay Instagram-only.** Each feed post gets a separate TikTok-only Metricool post (same image, caption, time; `tiktokData` in SKILL.md). Added by hand for 15-09 (ids 375608953, 375609402, 375609441, 375609488) and 16-09 (375610040, 375610088, 375610126, 375610202); the nightly routine does it from 17-09. Metricool accepted them as PENDING — **first real TikTok publish is 15-09 08:30**; if it doesn't appear, the TikTok is probably a personal account (Metricool then sends a phone notification instead of posting) → Bee switches to a Business account.

## Output
- 1080×1080 PNG (guideline Instagram feed spec). Layouts `tips` / `fact` / `photo` in compose.py; official logo on top, Astana chip, Safe Blue CTA pill at the bottom.
- Fonts: Manrope subsets copied from the Clean Bee site build (`.next/static/media`) — cyrillic, latin, latin-ext; Montserrat only as a last-resort glyph fallback.

## Tools
- Metricool MCP — brand `cleanbumblebee` id **6957992** (also Facebook + TikTok). Tools: getBrandSettings, getBestTimeToPostByNetwork (= the heat map), getScheduledPosts, createScheduledPost (`draft` flag in info), updateScheduledPost. Media = public URLs only; Metricool copies them to static.metricool.com on creation.
- Metricool brand timezone is Europe/London — always pass Asia/Almaty explicitly.
- **Approving or updating a Metricool post changes its `id`** (uuid stays). Re-read ids with getScheduledPosts before updateScheduledPost.
- 14-09-2026: heat map all zeros (new account) → fallback times 08:30 / 12:30 / 17:00 / 20:30.
- Higgsfield `gpt_image_2_5`, aspect 4:3 for photo backgrounds; always Read the result — the first curtains prompt produced a room with no visible curtains, so match the headline to what the photo actually shows.
