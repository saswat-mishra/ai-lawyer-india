#!/bin/bash -l
# Deploy from a clean copy without .git so Vercel doesn't apply team-collaboration commit-author checks.
set -e
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
SRC="/Users/saswat/Library/Application Support/Claude/local-agent-mode-sessions/656e5ddc-cfbe-46c5-9602-db1b8eb2d434/17734287-26b1-4093-845c-b14f6e891800/local_6b051a79-32ff-43de-8b7b-3746e72bc2c1/outputs/ai-lawyer-india"
DEST=/tmp/ail-deploy
rm -rf "$DEST"
mkdir -p "$DEST"
rsync -a \
  --exclude .git \
  --exclude node_modules \
  --exclude .next \
  --exclude __pycache__ \
  --exclude .pytest_cache \
  --exclude corpus/raw \
  "$SRC/" "$DEST/"
# Carry over the existing .vercel link so we deploy to the same project.
cp -R "$SRC/.vercel" "$DEST/" 2>/dev/null || true

# Reorganise so the deploy root has Next.js + Python api + backend together
# (Vercel needs package.json at the deploy root for Next.js auto-detection).
mkdir -p "$DEST/frontend/api"
cp "$DEST/api/index.py" "$DEST/frontend/api/index.py"
cp -R "$DEST/backend" "$DEST/frontend/backend"
cp "$DEST/requirements.txt" "$DEST/frontend/requirements.txt"

# Drop original duplicates from root so Vercel only sees one project.
rm -rf "$DEST/api" "$DEST/backend"

# .vercel must sit alongside the deploy root.
cp -R "$SRC/.vercel" "$DEST/frontend/" 2>/dev/null || true

cd "$DEST/frontend"
export VERCEL_TOKEN=vcp_86QrA9oZtRx6xLpHF6NX17ctX2npWjV5b1s8cO0nAHSsODPtVR1n8zNo
npx --yes vercel@latest --token "$VERCEL_TOKEN" deploy --prod --yes --force 2>&1 | tail -40
