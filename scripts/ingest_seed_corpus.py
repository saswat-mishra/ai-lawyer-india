"""One-shot ingester. Loads the in-memory seed corpus + IPC->BNS mapping.

Run this once after starting the backend if you want a working corpus without
running the full scrapers.
"""
import asyncio

from app.ingest.legal_seed import seed_legal_corpus


async def _main() -> None:
    n = await seed_legal_corpus()
    print(f"seeded: {n}")


if __name__ == "__main__":
    asyncio.run(_main())
