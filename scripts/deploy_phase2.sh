#!/usr/bin/env bash
# Phase 2 deploy — run from your Mac after Claude finishes.
#
# What this does:
#   1. Releases any stale .git/index.lock the sandbox left behind.
#   2. Commits the citator citation-string fix (no-op if already committed).
#   3. Pushes to GitHub. Vercel auto-deploys from main.
#
# Usage:
#   cd /Users/saswat/Library/Application\ Support/Claude/local-agent-mode-sessions/.../outputs/ai-lawyer-india
#   bash scripts/deploy_phase2.sh

set -euo pipefail

cd "$(dirname "$0")/.."

# 1. Clear any leftover index lock (sandbox FS quirk).
if [ -f .git/index.lock ]; then
  echo "Removing stale .git/index.lock"
  rm -f .git/index.lock
fi

# 2. Commit only if there are pending changes.
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "Citator: fix KNOWN_TREATMENTS to match seed citations (31/31 resolve)

Aligns the source/cited short_citation strings in KNOWN_TREATMENTS with
the values written by legal_seed_cases.py. Result: 31/31 case-on-case
treatments resolve at boot, vs 5/30 before. Re-built corpus.jsonl now
ships 31 citator edges (was 30)."
else
  echo "Working tree clean — nothing to commit."
fi

# 3. Push (will trigger Vercel auto-deploy).
echo "Pushing to origin/main..."
git push origin main

echo
echo "=== Phase 2 deploy initiated ==="
echo "Watch the build at: https://vercel.com/saswatmishras-projects/ai-lawyer-india"
echo "Once green, audit at:  https://ai-lawyer-india-ten.vercel.app"
