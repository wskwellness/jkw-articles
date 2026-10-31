#!/usr/bin/env bash
# Publish (or update) one article's HTML galley.
#   scripts/publish.sh <year> <id> ["commit message"]
# Copies the article's published HTML from jkw-manuscripts into vNiN/<id>/index.html,
# rebuilds the landing page, commits and pushes. Live on the site about a minute later.
set -euo pipefail
YEAR=${1:?usage: publish.sh <year> <id> [message]}; ID=${2:?usage: publish.sh <year> <id> [message]}
MSG=${3:-"Update article $ID"}
MS=${JKW_MANUSCRIPTS:-/Users/ovandef/_hub/jkw-manuscripts}
REPO=$(cd "$(dirname "$0")/.." && pwd)

SRC=""
# Only articles that are actually published: frozen in reviews/published/, or moved to <year>/published/.
for c in "$MS/$YEAR/$ID/reviews/published/index.html" "$MS/$YEAR/published/$ID/reviews/published/index.html" \
         "$MS/$YEAR/published/$ID/_manuscript/index.html"; do
  [ -f "$c" ] && { SRC=$c; break; }
done
[ -n "$SRC" ] || { echo "No published index.html found for $YEAR/$ID (not published yet?)" >&2; exit 1; }

ISSUE=$(grep -o 'jkw\.v[0-9]*i[0-9]*\.'"$ID" "$SRC" | head -1 | sed -E 's/^jkw\.(v[0-9]+i[0-9]+)\..*/\1/')
[ -n "$ISSUE" ] || { echo "Could not read the volume/issue from the DOI in $SRC" >&2; exit 1; }

mkdir -p "$REPO/$ISSUE/$ID"
cp "$SRC" "$REPO/$ISSUE/$ID/index.html"
python3 "$REPO/scripts/build_index.py"
cd "$REPO"
git add "$ISSUE/$ID/index.html" index.html
if git diff --cached --quiet; then echo "No changes for $ID."; exit 0; fi
git commit -m "$MSG"
git push
echo "Published: https://$(cat CNAME)/$ISSUE/$ID/  (from $SRC)"
