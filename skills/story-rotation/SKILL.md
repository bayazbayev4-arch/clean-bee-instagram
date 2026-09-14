---
name: story-rotation
description: Keep Clean Bumble Bee's reusable Instagram stories scheduled in Metricool for the next 7 days, following stories/schedule.json. Runs first in the nightly routine; needs only the Metricool connector (no git push, no downloads). Use when stories need topping up or Bee asks about the story schedule.
---

# Story rotation — Clean Bumble Bee

Paths are relative to the `Clean Bee Instagram/` folder.

1. Read `stories/schedule.json`. Brand id = `config.json` → `metricool_brand_id`.
2. For each date from **tomorrow** to **tomorrow + `horizon_days` − 1** (Asia/Almaty):
   - Find the period whose `from`/`to` covers the date (`to: null` = open-ended). No period → skip the date.
   - `getScheduledPosts` for **that single date** (00:00–23:59 `+05:00`, one day at a time — a week in one call is too large to read). Keep only posts with `instagramData.type == "STORY"`.
   - A slot counts as done if a story exists at that exact `time` (`publicationDate.dateTime` HH:MM). Never touch or delete existing stories, even ones outside the rotation.
   - For every missing slot, `createScheduledPost`:
     - `blogId`: brand id; `date`: `YYYY-MM-DDTHH:MM:00+05:00`
     - `info`: `{"autoPublish": true, "draft": false, "descendants": [], "firstCommentText": "", "hasNotReadNotes": false, "media": ["<base_url><file>"], "mediaAltText": [], "providers": [{"network": "instagram"}], "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Asia/Almaty"}, "shortener": false, "smartLinkData": {"ids": []}, "instagramData": {"type": "STORY", "isAiGenerated": false}}`
     - No `text` field for stories.
3. If a create call errors (plan limit, auth), stop the story step, report the exact error, and carry on with the rest of the routine.
4. Learn, don't self-edit rules: log any tool quirk or pattern (a slot that reliably needs re-adding, a story that's underperforming) in `MEMORY.md`. If it looks like a permanent rule change — a rotation timing/order change, dropping or adding a story — don't edit `stories/schedule.json` yourself; add a dated proposal to `MEMORY.md` → `## Proposed instruction changes` and name it in the report instead. (Fixing an outright mechanical bug, e.g. a broken `base_url`, is fine to do directly — just log it.)
5. Report one line: "Stories: N added (dates), all 7 days covered" or the error — plus, if step 4 added a proposal, a second line naming it.

Changing the rotation (new story, different times, dropping an expired offer) = edit `stories/schedule.json` only. Stories already in Metricool stay as they are; fix those by hand.
