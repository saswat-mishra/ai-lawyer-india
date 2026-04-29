#!/bin/bash -l
set -e
TEAM=team_moy99GmwInjVeqIVffSdbb6X
PROJ=prj_rMAOhbSSGybCs6zSZuTgYfK8PKlR
TOKEN=vcp_86QrA9oZtRx6xLpHF6NX17ctX2npWjV5b1s8cO0nAHSsODPtVR1n8zNo

add_env () {
  local key="$1" val="$2"
  curl -sX POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.vercel.com/v10/projects/$PROJ/env?teamId=$TEAM" \
    -d "{\"type\":\"plain\",\"key\":\"$key\",\"value\":\"$val\",\"target\":[\"production\",\"preview\",\"development\"]}" \
    | python3 -c "import json,sys;d=json.load(sys.stdin);print('$key:', 'created' if 'created' in d else d.get('error',d))"
}

OAI_KEY="$(grep '^OPENAI_API_KEY=' '/Users/saswat/Library/Application Support/Claude/local-agent-mode-sessions/656e5ddc-cfbe-46c5-9602-db1b8eb2d434/17734287-26b1-4093-845c-b14f6e891800/local_6b051a79-32ff-43de-8b7b-3746e72bc2c1/outputs/ai-lawyer-india/.env' | cut -d= -f2-)"

add_env OPENAI_API_KEY "$OAI_KEY"
add_env OPENAI_MODEL_DEFAULT gpt-4o-mini
add_env OPENAI_MODEL_HEAVY gpt-4o
add_env OPENAI_MODEL_NANO gpt-4o-mini
add_env OPENAI_EMBEDDING_MODEL text-embedding-3-small
add_env OPENAI_EMBEDDING_DIM 1536
add_env SUPABASE_URL https://dcqvznagpsouslkaqlct.supabase.co
add_env SUPABASE_ANON_KEY sb_publishable_Laj_nVbNbhuIxJTyP8yCxA_EE9TuaEM
add_env DEVICE_COOKIE_SECRET "$(openssl rand -hex 32)"
add_env APP_ENV production
add_env AIL_FORCE_MEMORY 1
