.PHONY: install backend frontend test test-no-key test-with-key clean

install-backend:
	cd backend && pip install -e ".[dev]" --break-system-packages

install-frontend:
	cd frontend && pnpm install

backend:
	cd backend && uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && pnpm dev

# Tests that do NOT need OpenAI or the network.
test-no-key:
	cd backend && AIL_FORCE_MEMORY=1 pytest -q -m "not openai and not live"

# Add OpenAI-gated tests too.
test-with-key:
	cd backend && AIL_FORCE_MEMORY=1 pytest -q

# Frontend lint + type + unit
fe-test:
	cd frontend && pnpm typecheck && pnpm lint && pnpm test

clean:
	rm -rf backend/.pytest_cache backend/**/__pycache__ frontend/.next
