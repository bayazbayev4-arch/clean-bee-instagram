# Clean Bee Instagram — Memory

## Voice
- Russian, simple everyday words (see brand/brand.md).

## Process
- 3 static posts/day, next day filled at 21:00 Astana by a cloud routine. Drafts for the first 14 days, then automatic (Bee, 14-09-2026).

## Projects
- 14-09-2026: set up complete. Public repo bayazbayev4-arch/clean-bee-instagram (images served from raw.githubusercontent.com). Cloud routine **trig_01BPXHcuLGJnHNtob7Jbykmv**, cron `0 16 * * *` UTC = 21:00 Astana; Metricool + Higgsfield attached. Test draft for 15-09 13:00 (slot b, Metricool id 375487661) made by hand — the first routine run fills slots a and c.

## Output
- 1080×1350 PNG (4:5), text + logo rendered by compose.py.

## Tools
- Higgsfield MCP (connected) — background photos/illustrations, no text in the prompt.
- Metricool MCP — connected 14-09-2026. Brand `cleanbumblebee` id **6957992** (also has Facebook + TikTok). Tools: getBrandSettings, getBestTimeToPostByNetwork, getScheduledPosts, createScheduledPost (`draft` flag in info), updateScheduledPost. Media = public URLs only (or Google Drive/Dropbox links if linked in Metricool).
- Metricool brand timezone is Europe/London — always pass Asia/Almaty explicitly (13:00 Almaty came back as 09:00 London = correct).
- Metricool copies the image to static.metricool.com when the post is created, so the GitHub URL only has to work at that moment.
- 14-09-2026: best-time data all zeros (new account) → fallback times until data builds up.
