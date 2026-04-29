"""Shared scraper primitives: caching, rate limiting, robots.txt."""
from __future__ import annotations

import asyncio
import hashlib
import os
import time
import urllib.robotparser
from pathlib import Path

import httpx

USER_AGENT = "AILawyerIndia/0.1 (research; contact: maintainer@example.com)"
DEFAULT_RATE_HZ = 0.5  # 1 request every 2 seconds
CACHE_ROOT = Path(os.environ.get("AIL_CORPUS_DIR", "./corpus/raw"))
_robots_cache: dict[str, urllib.robotparser.RobotFileParser] = {}
_last_request: dict[str, float] = {}


def _cache_path(url: str, ext: str) -> Path:
    h = hashlib.sha1(url.encode()).hexdigest()
    host = httpx.URL(url).host or "unknown"
    p = CACHE_ROOT / host / f"{h}.{ext}"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


async def fetch(url: str, *, ext: str = "html", rate_hz: float = DEFAULT_RATE_HZ,
                  use_cache: bool = True) -> bytes:
    cache = _cache_path(url, ext)
    if use_cache and cache.exists():
        return cache.read_bytes()

    if not _allowed_by_robots(url):
        raise PermissionError(f"robots.txt disallows {url}")

    host = httpx.URL(url).host or ""
    delay = 1.0 / rate_hz
    last = _last_request.get(host, 0.0)
    wait = (last + delay) - time.monotonic()
    if wait > 0:
        await asyncio.sleep(wait)

    async with httpx.AsyncClient(headers={"User-Agent": USER_AGENT},
                                    timeout=30, follow_redirects=True) as client:
        resp = await client.get(url)
    _last_request[host] = time.monotonic()
    resp.raise_for_status()
    cache.write_bytes(resp.content)
    return resp.content


def _allowed_by_robots(url: str) -> bool:
    parsed = httpx.URL(url)
    base = f"{parsed.scheme}://{parsed.host}"
    rp = _robots_cache.get(base)
    if rp is None:
        rp = urllib.robotparser.RobotFileParser()
        try:
            rp.set_url(f"{base}/robots.txt")
            rp.read()
        except Exception:
            # Permissive on robots.txt fetch failure.
            class _Allow:
                def can_fetch(self, ua, target):  # type: ignore[no-redef]
                    return True
            rp = _Allow()
        _robots_cache[base] = rp
    return rp.can_fetch(USER_AGENT, str(parsed))
