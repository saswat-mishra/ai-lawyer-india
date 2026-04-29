# LLM Evals

Separate from `backend/tests/`. The test suite asserts code correctness.
**Evals assert LLM output quality** — they call the real OpenAI API and
score the agent's behaviour against gold expectations.

## Suites

| Suite | What it measures | Threshold |
|---|---|---|
| `citation_faithfulness` | Every citation in the final answer exists in the corpus and quoted text matches the source. | 100% (we ship this guarantee) |
| `retrieval_recall` | Expected gold chunk in top-5 retrieval, using real embeddings. | recall@5 ≥ 0.85 |
| `refusal` | Refuses on unanswerable, answers on answerable. | accuracy ≥ 0.90 |
| `bns_currency` | Cites BNS for post-1-Jul-2024 facts; cites IPC for pre-Jul-2024 facts. | accuracy ≥ 0.90 |
| `persona` | Citizen vs Practitioner outputs differ materially in length and register. | divergence ≥ threshold |
| `adversarial` | Adversarial prompts trying to elicit fabricated citations are caught by the verifier. | 100% |

## Run

```bash
cd backend
PYTHONPATH=. python -m evals.runner --suite all
PYTHONPATH=. python -m evals.runner --suite citation_faithfulness
PYTHONPATH=. python -m evals.runner --suite adversarial
```

Results are written to `evals/results/<timestamp>/<suite>.json` plus a
human-readable scorecard printed to stdout.

## Gold sets

JSONL files in `evals/gold/`. Easy to extend — add a row, re-run.
