"""Longterm storage for scraped & pre-tokenized web pages.

Each scraped page is stored as a single JSON file under ``<project-root>/data/``.
A page file has the following shape::

    {
        "url": "https://...",
        "source": "wikipedia" | "pdf",
        "scraped_at": "2026-10-07T15:47:07+00:00",
        "tokens": ["token1", "token2", ...]
    }

Additionally an ``index.json`` is kept inside the data directory that maps every
already-scraped URL to its page file. This is used to avoid scraping (and
storing) the same URL twice and makes the whole dataset easy to load again for a
later "build a tokenset from the dataset" step.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


# ``__file__`` lives at ``<project-root>/src/llm/data/dataset.py`` so the project
# root is four parents up.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
INDEX_FILE = DATA_DIR / "index.json"
MERGES_FILE = DATA_DIR / "merges.json"
TOKENS_FILE = DATA_DIR / "tokens.json"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_index() -> dict[str, str]:
    "Return the mapping of ``url`` -> page filename. Empty dict if none yet."
    if not INDEX_FILE.exists():
        return {}
    with open(INDEX_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save_index(index: dict[str, str]) -> None:
    _ensure_data_dir()
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def is_scraped(url: str) -> bool:
    "Check whether the given url has already been scraped and stored."
    return url in load_index()


def _filename_for(url: str, source: str) -> str:
    "Build a stable, filesystem-safe filename for a url."
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    return f"{source}_{digest}.json"


def save_page(url: str, source: str, tokens: list[str]) -> Path:
    """Store a scraped page as a token list and register it in the index.

    Returns the path of the written page file.
    """
    _ensure_data_dir()

    filename = _filename_for(url, source)
    page_path = DATA_DIR / filename

    payload = {
        "url": url,
        "source": source,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "tokens": tokens,
    }

    with open(page_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    index = load_index()
    index[url] = filename
    _save_index(index)

    return page_path


def load_pages() -> list[dict]:
    "Load every stored page file. Useful for building a tokenset later."
    index = load_index()
    pages: list[dict] = []
    for filename in index.values():
        page_path = DATA_DIR / filename
        if not page_path.exists():
            continue
        with open(page_path, encoding="utf-8") as f:
            pages.append(json.load(f))
    return pages


def load_tokens() -> list[str]:
    "Concatenate the token lists of every stored page into one corpus."
    tokens: list[str] = []
    for page in load_pages():
        tokens += page.get("tokens", [])
    return tokens


def save_merges(merges: dict[tuple, str]) -> Path:
    "Persist BPE merges to ``<project-root>/data/merges.json``."
    _ensure_data_dir()
    with open(MERGES_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [[k[0], k[1], v] for k, v in merges.items()],
            f,
            ensure_ascii=False,
            indent=2,
        )
    return MERGES_FILE


def load_merges() -> dict[tuple, str]:
    "Load BPE merges from ``<project-root>/data/merges.json``."
    with open(MERGES_FILE, encoding="utf-8") as f:
        return {(a, b): v for a, b, v in json.load(f)}


def save_tokens(tokens: list[str]) -> Path:
    """Persist the token set as a ``{token: index}`` dict.

    The tokens are sorted before indexing so the mapping is stable.
    Written to ``<project-root>/data/tokens.json``.
    """
    _ensure_data_dir()
    sorted_tokens = sorted(tokens)
    token_index = {token: idx for idx, token in enumerate(sorted_tokens)}
    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(token_index, f, ensure_ascii=False, indent=2)
    return TOKENS_FILE


def load_tokens_index() -> dict[str, int]:
    "Load the ``{token: index}`` mapping from ``<project-root>/data/tokens.json``."
    with open(TOKENS_FILE, encoding="utf-8") as f:
        return json.load(f)
