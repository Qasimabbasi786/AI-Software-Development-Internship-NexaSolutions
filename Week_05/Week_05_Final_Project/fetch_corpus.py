"""
Week 5 Project — Step 1: Build the Corpus from Real Data
Fetches the book catalog from the .NET API (GET /api/books) and formats each book into a text document.
"""
import os
import json
import requests

DOTNET_API_URL = os.getenv("DOTNET_API_URL", "http://localhost:5000/api/books")
OUTPUT_CORPUS_FILE = "corpus.json"

# Fallback seed data matching the SQL Server Library database schema
FALLBACK_BOOKS = [
    {
        "id": 1,
        "title": "Clean Architecture: A Craftsman's Guide to Software Structure and Design",
        "author": "Robert C. Martin",
        "category": "Software Engineering",
        "description": "Comprehensive patterns on decoupling business rules from frameworks, databases, and UI layers using SOLID principles, dependency inversion, component cohesion, and hexagonal architecture patterns."
    },
    {
        "id": 2,
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "category": "Database & Distributed Systems",
        "description": "Data is at the center of many challenges in system design today. Difficult issues need to be figured out, such as scalability, consistency, reliability, efficiency, and maintainability. Covers storage engines, replication, partitioning, transactions, and Apache Kafka stream processing."
    },
    {
        "id": 3,
        "title": "Building Microservices: Designing Fine-Grained Systems",
        "author": "Sam Newman",
        "category": "Software Engineering",
        "description": "Practical guide to distributed microservice architectures, domain-driven service decomposition, asynchronous messaging, API gateways, database decomposition patterns, resilience engineering, and observable telemetry."
    },
    {
        "id": 4,
        "title": "Raja Gidh (The Vulture King)",
        "author": "Bano Qudsia",
        "category": "Urdu Novels",
        "description": "A monumental psychological and philosophical Urdu novel exploring socio-moral values, spiritual disintegration, illegal means of sustenance (rizq-e-haram), and the profound emotional consequences of unrestrained human desires through allegorical storytelling."
    },
    {
        "id": 5,
        "title": "Peer-e-Kamil (The Perfect Mentor)",
        "author": "Umera Ahmed",
        "category": "Urdu Novels",
        "description": "A widely acclaimed modern Urdu literary masterpiece chronicling the transformative spiritual journeys of Imama Hashim and Salar Sikandar, depicting personal redemption, unshakeable faith, and the quest for existential guidance."
    },
    {
        "id": 6,
        "title": "Jannat Kay Pattay (Leaves of Heaven)",
        "author": "Nemrah Ahmed",
        "category": "Urdu Novels",
        "description": "A suspenseful and spiritually awakening Urdu novel centering on Haya Suleman, a law student studying in Turkey who navigates intrigue, espionage, personal growth, modesty, and divine trials with unwavering resilience."
    },
    {
        "id": 7,
        "title": "The Reluctant Fundamentalist",
        "author": "Mohsin Hamid",
        "category": "Pakistani Literature",
        "description": "An international bestselling novella presented as an elegant dramatic monologue in Lahore, reflecting on cultural identity, corporate ambition on Wall Street, post-9/11 geopolitical tensions, and the dualities of immigrant life."
    },
    {
        "id": 8,
        "title": "Moth Smoke",
        "author": "Mohsin Hamid",
        "category": "Pakistani Literature",
        "description": "A poignant contemporary novel exploring Lahore during the nuclear tests of 1998, delving into friendship, social disparities, moral conflicts, and economic decay through the shifting voice of its protagonist Darashikoh Shezad."
    },
    {
        "id": 9,
        "title": "A Case of Exploding Mangoes",
        "author": "Mohammed Hanif",
        "category": "Pakistani Literature",
        "description": "A razor-sharp political satire and dark comedy investigating the mysterious plane crash of General Zia-ul-Haq, interweaving military conspiracies, mango crates, and bureaucratic absurdities in 1980s Pakistan."
    },
    {
        "id": 10,
        "title": "Aab-e-Hayat (Elixir of Life)",
        "author": "Umera Ahmed",
        "category": "Urdu Novels",
        "description": "The profound sequel to Peer-e-Kamil following the mature lives of Salar and Imama, exploring financial ethics, interest-free economic ideals, marital harmony, philanthropic commitments, and social justice in contemporary society."
    }
]


def fetch_books_from_api() -> list[dict]:
    """
    Calls GET /api/books on .NET API.
    If the .NET API is not currently running locally, falls back to the database-matched corpus.
    """
    try:
        print(f"[FETCH] Requesting book catalog from .NET API: {DOTNET_API_URL} ...")
        resp = requests.get(DOTNET_API_URL, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            print(f"[SUCCESS] Retrieved {len(data)} books directly from .NET API.")
            return data
        else:
            print(f"[WARN] API returned status {resp.status_code}. Using local corpus data.")
            return FALLBACK_BOOKS
    except Exception as ex:
        print(f"[INFO] .NET API not reachable ({ex}). Using local seed catalog.")
        return FALLBACK_BOOKS


def format_book_document(book: dict) -> dict:
    """
    Transforms a single book database record into a standardized document structure.
    """
    title = book.get("title", "Untitled")
    author = book.get("author", "Unknown Author")
    category = book.get("category", book.get("genre", "General"))
    description = book.get("description", "")

    document_text = (
        f"Title: {title}\n"
        f"Author: {author}\n"
        f"Category: {category}\n"
        f"Description: {description}"
    )

    return {
        "id": f"book_{book.get('id', title.lower().replace(' ', '_'))}",
        "text": document_text,
        "metadata": {
            "title": title,
            "author": author,
            "category": category,
            "source": title
        }
    }


def build_and_save_corpus(output_path: str = OUTPUT_CORPUS_FILE) -> list[dict]:
    books = fetch_books_from_api()
    documents = [format_book_document(b) for b in books]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2)

    print(f"[CORPUS] Saved {len(documents)} formatted documents to {output_path}")
    return documents


if __name__ == "__main__":
    docs = build_and_save_corpus()
    for d in docs:
        print(f"\n--- Document ID: {d['id']} ---")
        print(d["text"])
