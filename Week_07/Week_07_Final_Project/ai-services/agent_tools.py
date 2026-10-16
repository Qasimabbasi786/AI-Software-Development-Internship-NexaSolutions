"""
Week 7 Agent Tools Module: Secure Tool Design & Execution
Implements:
1. Pydantic argument schemas (ReserveArgs, AvailabilityArgs, SearchArgs).
2. Typed arguments validating boundary conditions (gt=0).
3. Read tools (search_catalog, check_availability, list_my_reservations).
4. Write tools (reserve_book) forwarding user JWT from config (NOT graph state) and idempotency keys.
5. Error formatting: return errors as data (ERROR_RETRYABLE, ERROR_FINAL) rather than unhandled exceptions.
"""

import os
import uuid
import httpx
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

DOTNET_URL = os.getenv("DOTNET_URL", "http://localhost:5000")

# ---------------------------------------------------------------------------
# Argument Schemas
# ---------------------------------------------------------------------------
class ReserveArgs(BaseModel):
    book_id: int = Field(gt=0, description="Numeric ID of the book to reserve. Must be a positive integer.")

class AvailabilityArgs(BaseModel):
    book_id: int = Field(gt=0, description="Numeric ID of the book to check availability for.")

class SearchArgs(BaseModel):
    query: str = Field(min_length=1, description="Keywords, genre, or book title to search in library catalog.")


# ---------------------------------------------------------------------------
# Secure Tools
# ---------------------------------------------------------------------------
@tool("search_catalog", args_schema=SearchArgs)
def search_catalog(query: str, config: RunnableConfig) -> str:
    """Search the library catalog for books matching a title, author, or genre.
    This is a READ-ONLY tool. Safe for unbounded calls."""
    try:
        with httpx.Client(timeout=8.0) as client:
            resp = client.get(f"{DOTNET_URL}/api/books")
            if resp.status_code == 200:
                books = resp.json()
                q = query.lower()
                matches = [b for b in books if q in b.get("title", "").lower() or q in b.get("genre", "").lower()]
                if not matches:
                    # Fallback return all or top 3
                    matches = books[:3]
                formatted = [
                    f"- ID {b.get('bookId', b.get('id'))}: '{b.get('title')}' by {b.get('author', 'Unknown')} (Genre: {b.get('genre', 'General')}, Available: {b.get('isAvailable', True)})"
                    for b in matches
                ]
                return f"Found {len(formatted)} books in catalog:\n" + "\n".join(formatted)
            return f"ERROR_RETRYABLE: catalog service returned HTTP {resp.status_code}"
    except httpx.TimeoutException:
        return "ERROR_RETRYABLE: library catalog service timed out."
    except Exception as ex:
        return f"ERROR_RETRYABLE: catalog connection error: {str(ex)}"


@tool("check_availability", args_schema=AvailabilityArgs)
def check_availability(book_id: int, config: RunnableConfig) -> str:
    """Check whether a specific book ID is currently available on the shelf.
    This is a READ-ONLY tool. Safe for unbounded calls."""
    try:
        with httpx.Client(timeout=8.0) as client:
            resp = client.get(f"{DOTNET_URL}/api/books/{book_id}/availability")
            if resp.status_code == 200:
                data = resp.json()
                avail = data.get("isAvailable", False)
                title = data.get("title", f"Book #{book_id}")
                return f"Book '{title}' (ID: {book_id}) is {'AVAILABLE to borrow' if avail else 'UNAVAILABLE (currently checked out or reserved)'}."
            elif resp.status_code == 404:
                return f"ERROR_FINAL: no book found with ID {book_id}."
            return f"ERROR_RETRYABLE: availability service returned HTTP {resp.status_code}"
    except httpx.TimeoutException:
        return "ERROR_RETRYABLE: library availability service timed out."
    except Exception as ex:
        return f"ERROR_RETRYABLE: availability service connection error: {str(ex)}"


@tool("reserve_book", args_schema=ReserveArgs)
def reserve_book(book_id: int, config: RunnableConfig) -> str:
    """Reserve a book for the CURRENT USER.
    Only call after the user has explicitly requested to reserve it.
    This is a WRITE TOOL that creates persistent data and modifies book availability.
    High risk: requires human approval before execution."""
    # Never read token from graph state (which gets persisted into SQLite checkpoints)
    # Token travels strictly through RunnableConfig
    configurable = config.get("configurable", {})
    token = configurable.get("user_token")
    key = configurable.get("idempotency_key") or str(uuid.uuid4())

    headers = {
        "Idempotency-Key": f"{key}:{book_id}"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        with httpx.Client(timeout=8.0) as client:
            resp = client.post(
                f"{DOTNET_URL}/api/books/{book_id}/reserve",
                headers=headers
            )
            if resp.status_code == 200:
                data = resp.json()
                return f"OK: reservation created successfully for '{data.get('title', f'Book #{book_id}')}' (Reservation ID: {data.get('reservationId')})."
            elif resp.status_code == 409:
                return f"ERROR_FINAL: book ID {book_id} is already reserved."
            elif resp.status_code in (401, 403):
                return "ERROR_FINAL: you are not authorized to reserve this book (authentication required)."
            elif resp.status_code == 404:
                return f"ERROR_FINAL: book ID {book_id} does not exist."
            else:
                return f"ERROR_RETRYABLE: reservation service returned HTTP {resp.status_code}"
    except httpx.TimeoutException:
        return "ERROR_RETRYABLE: the library reservation service timed out."
    except Exception as ex:
        return f"ERROR_RETRYABLE: connection error: {str(ex)}"


@tool("list_my_reservations")
def list_my_reservations(config: RunnableConfig) -> str:
    """Retrieve all active reservations belonging to the CURRENT USER.
    This is a READ-ONLY tool scoped strictly to the caller's JWT identity."""
    configurable = config.get("configurable", {})
    token = configurable.get("user_token")

    if not token:
        return "ERROR_FINAL: User authentication token is required to view personal reservations."

    headers = {"Authorization": f"Bearer {token}"}
    try:
        with httpx.Client(timeout=8.0) as client:
            resp = client.get(f"{DOTNET_URL}/api/me/reservations", headers=headers)
            if resp.status_code == 200:
                reservations = resp.json()
                if not reservations:
                    return "You currently have no active reservations."
                lines = [
                    f"- Reservation #{r.get('id')}: '{r.get('book', {}).get('title', 'Unknown')}' (Status: {r.get('status')}, Reserved: {r.get('createdAt')})"
                    for r in reservations
                ]
                return f"Your active reservations ({len(reservations)}):\n" + "\n".join(lines)
            elif resp.status_code in (401, 403):
                return "ERROR_FINAL: Unauthorized to view reservations."
            return f"ERROR_RETRYABLE: reservations service returned HTTP {resp.status_code}"
    except httpx.TimeoutException:
        return "ERROR_RETRYABLE: reservation service timed out."
    except Exception as ex:
        return f"ERROR_RETRYABLE: error fetching reservations: {str(ex)}"


ALL_TOOLS = [search_catalog, check_availability, reserve_book, list_my_reservations]
READ_TOOLS = [search_catalog, check_availability, list_my_reservations]
WRITE_TOOLS = [reserve_book]
RISKY_TOOLS = {"reserve_book"}
