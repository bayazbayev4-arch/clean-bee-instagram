# Clean Bee Instagram — Memory

## Voice
- Russian, simple everyday words (see brand/brand.md).

## Process
- 3 static posts/day, next day filled at 21:00 Astana by a cloud routine. Drafts for the first 14 days, then automatic (Bee, 14-09-2026).

## Projects
- 14-09-2026: folder, skill and compose script built. Waiting on: Metricool MCP connector + Instagram linked in Metricool, image hosting decision. Routine not created yet.

## Output
- 1080×1350 PNG (4:5), text + logo rendered by compose.py.

## Tools
- Higgsfield MCP (connected) — background photos/illustrations, no text in the prompt.
- Metricool MCP — connected 14-09-2026. Brand `cleanbumblebee` id **6957992** (also has Facebook + TikTok). Tools: getBrandSettings, getBestTimeToPostByNetwork, getScheduledPosts, createScheduledPost (`draft` flag in info), updateScheduledPost. Media = public URLs only (or Google Drive/Dropbox links if linked in Metricool).
- Metricool brand timezone is Europe/London — always pass Asia/Almaty explicitly.
- 14-09-2026: best-time data all zeros (new account) → fallback times until data builds up.
