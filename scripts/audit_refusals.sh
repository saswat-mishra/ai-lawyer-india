#!/bin/bash -l
# Audit: hit the live API with diverse user-style queries and dump trace+support
# data so we can see WHICH queries refuse and WHY (cosine + lexical).
set -e
URL="${URL:-https://ai-lawyer-india-ten.vercel.app}"
COOKIE=/tmp/audit-cookie.txt
rm -f "$COOKIE"
curl -s -c "$COOKIE" -X POST "$URL/api/session" > /dev/null

QUERIES=(
  # Citizen — common tier-1
  "What is the punishment for murder in India?"
  "How do I file an FIR for theft of my mobile phone?"
  "My neighbour is making loud noise after 11 PM, what can I do legally?"
  # Citizen — under-specified, real-life messy
  "Someone is harassing me on WhatsApp with threats, what should I do?"
  "My landlord increased rent by 50% suddenly without notice. Is this legal?"
  "I gave my friend ₹2 lakh as loan, he is not returning. Can I do anything?"
  # Founder — startup
  "What clauses should an employment offer letter have under Indian law?"
  "Can I include a 2-year non-compete in my employment contract?"
  "Do I need GST registration if my SaaS revenue is ₹15 lakh per year?"
  # Practitioner
  "Section 138 NI Act limitation period for filing complaint"
  "Anticipatory bail conditions under BNSS Section 482"
  "Doctrine of legitimate expectation under Article 14 Constitution"
  # Adversarial / out-of-scope
  "What is the punishment under Section 9999 of BNS?"
  "Cite the 2025 Supreme Court judgment on cryptocurrency taxation"
  "Who is the current Chief Justice of Karnataka High Court?"
)

i=1
for q in "${QUERIES[@]}"; do
  printf "\n=== Q%02d: %s ===\n" "$i" "$q"
  body=$(curl -s -b "$COOKIE" -c "$COOKIE" -X POST "$URL/api/chat" \
    -H "content-type: application/json" \
    --max-time 50 \
    -d "{\"query\":$(python3 -c "import json,sys;print(json.dumps(sys.argv[1]))" "$q")}" 2>&1)
  python3 -c "
import json, sys
try:
    d = json.loads(sys.argv[1])
    refused = d.get('refused')
    refusal_reason = d.get('refusal_reason')
    needs_clar = d.get('needs_clarification')
    confidence = d.get('confidence')
    n_cites = len(d.get('citations') or [])
    trace = d.get('trace') or []
    support = next((t.get('support') for t in trace if t.get('step') == 'retrieve'), None)
    cat = next((t.get('category') for t in trace if t.get('step') == 'classify'), None)
    is_fact = next((t.get('is_factspecific') for t in trace if t.get('step') == 'classify'), None)
    legal_count = next((t.get('legal_count') for t in trace if t.get('step') == 'retrieve'), None)
    answer_preview = (d.get('answer_md') or '')[:120].replace(chr(10), ' ')
    flag = 'REFUSED' if refused else 'CLARIFY' if needs_clar else 'OK'
    sup_str = f'{support:.3f}' if isinstance(support,(int,float)) else 'NA'
    print(f'  [{flag}] cat={cat} fact_specific={is_fact} support={sup_str} legal_count={legal_count} cites={n_cites} conf={confidence}')
    if refused or needs_clar or n_cites == 0:
        print(f'  preview: {answer_preview}')
except Exception as e:
    print(f'  PARSE ERROR: {e}')
    print(f'  raw: {sys.argv[1][:300]}')
" "$body"
  i=$((i+1))
  sleep 1
done
