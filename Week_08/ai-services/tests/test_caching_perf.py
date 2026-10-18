"""
Tests verifying Week 8 Part B:
1. Incremental Indexing using text hashing (only changed books re-embedded).
2. Cache Invalidation upon catalog version increment.
3. Cache Safety (ensuring user-specific / write answers are never cached across users).
"""
import pytest
import time
from safe_cache import (
    BookCatalogItem,
    IncrementalCatalogIndexer,
    get_current_catalog_version,
    increment_catalog_version,
    normalize_cache_key,
    get_cached_answer,
    set_cached_answer,
    clear_answer_cache,
    reset_catalog_version
)

def test_incremental_indexing_skips_unchanged():
    """Verify that books with identical text hashes skip re-embedding."""
    indexer = IncrementalCatalogIndexer()
    books = [
        BookCatalogItem(id=1, title="Clean Code", author="Robert C. Martin", description="Craftsmanship rules."),
        BookCatalogItem(id=2, title="Dune", author="Frank Herbert", description="Desert planet Arrakis.")
    ]

    # First sync: both books embedded
    res1 = indexer.sync_index(books)
    assert res1["unchanged"] == 0
    assert res1["new_books"] == 2
    assert indexer.embedding_calls_count == 2

    # Second sync without changes: 0 embedding calls
    res2 = indexer.sync_index(books)
    assert res2["unchanged"] == 2
    assert res2["updated"] == 0
    assert res2["new_books"] == 0
    assert indexer.embedding_calls_count == 2  # No new embedding calls!

    # Update one book description: only 1 embedding call
    books[1].description = "Desert planet Arrakis and spice melange."
    res3 = indexer.sync_index(books)
    assert res3["unchanged"] == 1
    assert res3["updated"] == 1
    assert indexer.embedding_calls_count == 3  # Exactly 1 new call!

def test_cache_invalidation_on_catalog_version_change():
    """
    Challenge: Edit a book description, then ask the same question.
    Show the answer updates because the catalog version changed.
    """
    clear_answer_cache()
    reset_catalog_version(1)

    question = "What is Dune about?"
    initial_answer = {"answer": "Dune is about the desert planet Arrakis.", "sources": ["Dune"]}

    # Cache answer for version 1
    cached = set_cached_answer(question, initial_answer, route="catalog", used_only_read_tools=True)
    assert cached is True
    assert get_cached_answer(question) == initial_answer

    # Catalog version increments (simulating book update)
    increment_catalog_version()
    assert get_current_catalog_version() == 2

    # Querying the same question now misses the cache because version changed!
    assert get_cached_answer(question) is None

    # New answer set for version 2
    updated_answer = {"answer": "Dune is about Arrakis, spice melange, and Paul Atreides.", "sources": ["Dune"]}
    set_cached_answer(question, updated_answer, route="catalog", used_only_read_tools=True)
    assert get_cached_answer(question) == updated_answer

def test_cache_safety_user_specific_and_write_tools_never_cached():
    """
    Challenge: Write a test proving a user-specific answer ("what have I reserved?")
    is never served from the shared cache to another user.
    """
    clear_answer_cache()

    # 1. User-specific reservation query must be rejected from cache
    user_query = "What have I reserved?"
    res_user = {"answer": "You currently have reserved Book #1 (Clean Code)."}
    saved = set_cached_answer(
        question=user_query,
        response_data=res_user,
        route="action",
        used_only_read_tools=True,
        has_user_specific_context=True
    )
    assert saved is False, "User-specific answer must NEVER be admitted into the shared cache!"
    assert get_cached_answer(user_query) is None

    # 2. Write tool execution must be rejected from cache
    write_query = "Reserve Dune for me"
    res_write = {"answer": "Successfully reserved Dune."}
    saved_write = set_cached_answer(
        question=write_query,
        response_data=res_write,
        route="action",
        used_only_read_tools=False,
        has_user_specific_context=False
    )
    assert saved_write is False, "Write actions must NEVER be admitted into answer cache!"
    assert get_cached_answer(write_query) is None

if __name__ == "__main__":
    pytest.main(["-v", __file__])
