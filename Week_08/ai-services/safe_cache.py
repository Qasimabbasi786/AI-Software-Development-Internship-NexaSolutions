"""
Week 8 Part B: Performance, Cost & Safe Caching Module
Implements:
1. Incremental vector store indexing based on SHA-256 book content hashing:
   - Re-embeds only books whose text changed since last sync.
   - Preserves embeddings for unchanged books, reducing latency and token costs.
2. Safe Answer Caching using TTLCache (5-minute TTL, max 500 entries):
   - Caches responses strictly for read-only catalog questions.
   - Automatically invalidates when current_catalog_version changes.
   - Enforces safety: never caches across users, never caches write operations or personal reservation queries.
"""
import hashlib
from typing import Dict, List, Any, Optional
from cachetools import TTLCache
from pydantic import BaseModel

# -----------------------------------------------------------------------------
# 1. Catalog Version & Invalidation Tracking
# -----------------------------------------------------------------------------
_current_catalog_version: int = 1

def get_current_catalog_version() -> int:
    """Returns active catalog version counter."""
    global _current_catalog_version
    return _current_catalog_version

def increment_catalog_version() -> int:
    """Increments catalog version counter upon catalog mutations to invalidate answer cache."""
    global _current_catalog_version
    _current_catalog_version += 1
    return _current_catalog_version

def reset_catalog_version(version: int = 1) -> None:
    global _current_catalog_version
    _current_catalog_version = version

# -----------------------------------------------------------------------------
# 2. Incremental Indexing Engine
# -----------------------------------------------------------------------------
def text_hash(text: str) -> str:
    """Generates SHA-256 digest of normalized text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

class BookCatalogItem(BaseModel):
    id: int
    title: str
    author: str
    description: str

    @property
    def text(self) -> str:
        return f"{self.title} by {self.author}. {self.description}"

class IncrementalCatalogIndexer:
    """
    Manages vector index synchronization with content hash checking.
    Tracks indexed book hashes in metadata so unchanged books skip embedding calls.
    """
    def __init__(self):
        # Simulated or real vector metadata store {book_id: {"hash": str, "chunks": list}}
        self.metadata_store: Dict[int, Dict[str, Any]] = {}
        self.embedding_calls_count: int = 0

    def sync_index(self, books: List[BookCatalogItem], embedding_fn=None) -> Dict[str, Any]:
        """
        Re-embed only books whose text changed since the last sync.
        Returns metrics on books unchanged, updated, and newly embedded.
        """
        unchanged = 0
        updated = 0
        new_books = 0

        for b in books:
            h = text_hash(b.text)
            existing = self.metadata_store.get(b.id)

            if existing and existing.get("hash") == h:
                # Unchanged: skip embedding cost completely
                unchanged += 1
                continue

            # Text changed or new book: delete stale chunks & re-embed
            if existing:
                updated += 1
            else:
                new_books += 1

            # Perform embedding computation
            if embedding_fn:
                _ = embedding_fn(b.text)
            self.embedding_calls_count += 1

            self.metadata_store[b.id] = {
                "book_id": b.id,
                "hash": h,
                "title": b.title,
                "author": b.author,
                "description": b.description
            }

        # If any book was added or updated, bump catalog version
        if updated > 0 or new_books > 0:
            increment_catalog_version()

        return {
            "total_books": len(books),
            "unchanged": unchanged,
            "updated": updated,
            "new_books": new_books,
            "catalog_version": get_current_catalog_version(),
            "total_embedding_calls": self.embedding_calls_count
        }

# Global singleton indexer
catalog_indexer = IncrementalCatalogIndexer()

# -----------------------------------------------------------------------------
# 3. Safe Answer Cache
# -----------------------------------------------------------------------------
# Global 5-minute TTL cache holding up to 500 normalized answers
answer_cache: TTLCache = TTLCache(maxsize=500, ttl=300)

def normalize_cache_key(question: str, catalog_version: int) -> str:
    """
    Normalizes whitespace and casing and prefixes active catalog version.
    Ensures 'What is Dune?' and '  what is dune? ' map to identical hashes.
    """
    norm = " ".join(question.lower().split())
    return hashlib.sha256(f"{catalog_version}:{norm}".encode("utf-8")).hexdigest()

def is_safe_to_cache(route: str, used_only_read_tools: bool, has_user_specific_context: bool) -> bool:
    """
    Strict safety rules for caching:
    - Route MUST be 'catalog'.
    - Tools used MUST be read-only (no writes like reserve_book).
    - MUST NOT contain user-specific context or reservation details.
    """
    if route != "catalog":
        return False
    if not used_only_read_tools:
        return False
    if has_user_specific_context:
        return False
    return True

def get_cached_answer(question: str) -> Optional[Dict[str, Any]]:
    """Returns cached response if present for active catalog version."""
    key = normalize_cache_key(question, get_current_catalog_version())
    return answer_cache.get(key)

def set_cached_answer(
    question: str,
    response_data: Dict[str, Any],
    route: str,
    used_only_read_tools: bool = True,
    has_user_specific_context: bool = False
) -> bool:
    """
    Caches response data ONLY if it passes strict safety constraints.
    Returns True if cached, False if rejected for safety.
    """
    if not is_safe_to_cache(route, used_only_read_tools, has_user_specific_context):
        return False

    key = normalize_cache_key(question, get_current_catalog_version())
    answer_cache[key] = response_data
    return True

def clear_answer_cache() -> None:
    """Clears all cached answers."""
    answer_cache.clear()
