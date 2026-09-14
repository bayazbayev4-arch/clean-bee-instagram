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
  - Not yet proven end-to-end from the cloud: first real feed-post run is 15-09 21:00 (fills 16-09). Check its run log.

## Output
- 1080×1080 PNG (guideline Instagram feed spec). Layouts `tips` / `fact` / `photo` in compose.py; official logo on top, Astana chip, Safe Blue CTA pill at the bottom.
- Fonts: Manrope subsets copied from the Clean Bee site build (`.next/static/media`) — cyrillic, latin, latin-ext; Montserrat only as a last-resort glyph fallback.

## Tools
- Metricool MCP — brand `cleanbumblebee` id **6957992** (also Facebook + TikTok). Tools: getBrandSettings, getBestTimeToPostByNetwork (= the heat map), getScheduledPosts, createScheduledPost (`draft` flag in info), updateScheduledPost. Media = public URLs only; Metricool copies them to static.metricool.com on creation.
- Metricool brand timezone is Europe/London — always pass Asia/Almaty explicitly.
- **Approving or updating a Metricool post changes its `id`** (uuid stays). Re-read ids with getScheduledPosts before updateScheduledPost.
- 14-09-2026: heat map all zeros (new account) → fallback times 08:30 / 12:30 / 17:00 / 20:30.
- Higgsfield `gpt_image_2_5`, aspect 4:3 for photo backgrounds; always Read the result — the first curtains prompt produced a room with no visible curtains, so match the headline to what the photo actually shows.
