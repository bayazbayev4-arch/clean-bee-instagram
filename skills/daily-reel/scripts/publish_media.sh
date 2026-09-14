#!/usr/bin/env bash
# Put one finished Reel on the repo's `media` branch and print a public URL for Metricool.
#
# Videos never go on main — the repo would grow by ~15 MB a video and the nightly
# clone would slow down. Every run makes ONE fresh commit on `media` holding only the
# newest `reels.media_keep` videos and force-pushes it, so old videos drop out of
# history. Metricool copies the file to its own storage when the post is created,
# so the GitHub copy is only needed for a few minutes.
#
# Usage (run from the Clean Bee Instagram folder):
#   bash skills/daily-reel/scripts/publish_media.sh reels/<folder>/final.mp4 <folder>.mp4
set -euo pipefail

SRC="$1"
NAME="${2:-$(basename "$SRC")}"
REPO="$(python3 -c 'import json; print(json.load(open("config.json"))["github_repo"])')"
BRANCH="$(python3 -c 'import json; print(json.load(open("config.json"))["reels"]["media_branch"])')"
KEEP="$(python3 -c 'import json; print(json.load(open("config.json"))["reels"]["media_keep"])')"

GITDIR="$(git rev-parse --absolute-git-dir)"
WORK="$(mktemp -d)"
IDX="$(mktemp -u)"
trap 'rm -rf "$WORK" "$IDX"' EXIT

# Start from the videos already on the media branch, if it exists.
if git fetch -q origin "$BRANCH" 2>/dev/null; then
  git archive FETCH_HEAD | tar -x -C "$WORK"
fi
cp "$SRC" "$WORK/$NAME"

# index.txt lists videos oldest → newest; keep the last $KEEP and drop the rest.
touch "$WORK/index.txt"
{ grep -vxF "$NAME" "$WORK/index.txt" || true; echo "$NAME"; } | tail -n "$KEEP" > "$WORK/index.new"
mv "$WORK/index.new" "$WORK/index.txt"
for f in "$WORK"/*.mp4; do
  [ -e "$f" ] || continue
  grep -qxF "$(basename "$f")" "$WORK/index.txt" || rm -f "$f"
done

(cd "$WORK" && GIT_INDEX_FILE="$IDX" git --git-dir="$GITDIR" --work-tree="$WORK" add -A .)
TREE="$(GIT_INDEX_FILE="$IDX" git --git-dir="$GITDIR" write-tree)"
COMMIT="$(git --git-dir="$GITDIR" commit-tree "$TREE" -m "media: $NAME")"
git push -q -f origin "$COMMIT:refs/heads/$BRANCH"

# Commit-pinned URL: never serves a cached older file with the same name.
echo "https://raw.githubusercontent.com/$REPO/$COMMIT/$NAME"
