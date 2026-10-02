"""
Week 5 Final Project - Part 1: Ingestion & Vector Storage Pipeline
==================================================================
Reads records from corpus.json, chunks each document, generates embeddings
via Google Gemini API / ChromaDB embedding function, and indexes them into 
the persistent Chroma collection 'library_rag_final' with rich metadata.
"""
import os
import json
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

# Load local environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

COLLECTION_NAME = "library_rag_final"
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db_data")
CORPUS_FILE = os.path.join(os.path.dirname(__file__), "corpus.json")


def chunk_text(text: str, chunk_size: int = 350, overlap: int = 40) -> list[str]:
    """
    Fixed-size sliding window chunking with overlap to preserve conceptual context.
    """
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def get_chroma_client() -> chromadb.PersistentClient:
    """
    Initializes and returns a persistent ChromaDB client pointing to chroma_db_data directory.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    return chromadb.PersistentClient(path=DB_DIR)


def get_embedding_function():
    """
    Configures embedding generation. Uses Google Gemini API if key is present and configured,
    or falls back cleanly to ChromaDB default embeddings for offline reliability.
    """
    if GEMINI_API_KEY and not GEMINI_API_KEY.startswith("your_"):
        try:
            import google.genai as genai
            # Test key initialization
            _client = genai.Client(api_key=GEMINI_API_KEY)
            
            class GeminiChromaEmbeddingFunction:
                def __init__(self, client):
                    self.client = client

                def __call__(self, input: list[str]) -> list[list[float]]:
                    results = []
                    for text in input:
                        res = self.client.models.embed_content(
                            model="models/gemini-embedding-001",
                            contents=text
                        )
                        results.append(res.embedding.values)
                    return results

            print("[EMBEDDINGS] Initialized Gemini Embedding Function (models/gemini-embedding-001).")
            return GeminiChromaEmbeddingFunction(_client)
        except Exception as ex:
            print(f"[WARN] Gemini embedding initialization note ({ex}). Using Chroma local embedding function.")
            return embedding_functions.DefaultEmbeddingFunction()

    return embedding_functions.DefaultEmbeddingFunction()


def ingest_corpus(corpus_path: str = CORPUS_FILE) -> int:
    """
    Loads books from corpus.json, chunks them, and stores them in ChromaDB collection 'library_rag_final'.
    """
    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"Corpus file not found at: {corpus_path}")

    with open(corpus_path, "r", encoding="utf-8") as f:
        books = json.load(f)

    print(f"\n==================================================")
    print(f"  Ingesting Library Corpus: {len(books)} Books")
    print(f"  Chroma Collection: {COLLECTION_NAME}")
    print(f"==================================================")

    client = get_chroma_client()
    embedding_fn = get_embedding_function()

    # Recreate collection to ensure clean state
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"[CLEANUP] Deleted existing collection '{COLLECTION_NAME}'.")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    all_chunks = []
    all_metadatas = []
    all_ids = []

    for book in books:
        doc_id = str(book.get("id", "book_unknown"))
        text_content = book.get("text", "")
        meta = book.get("metadata", {})

        chunks = chunk_text(text_content, chunk_size=350, overlap=40)
        for idx, chunk in enumerate(chunks):
            chunk_meta = {
                "title": str(meta.get("title", "Untitled")),
                "author": str(meta.get("author", "Unknown Author")),
                "category": str(meta.get("category", "General")),
                "source": str(meta.get("source", meta.get("title", doc_id))),
                "chunk_index": idx
            }
            all_chunks.append(chunk)
            all_metadatas.append(chunk_meta)
            all_ids.append(f"{doc_id}_chunk_{idx}")

    if all_chunks:
        collection.add(
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )

    print(f"\n[SUCCESS] Successfully chunked and indexed {len(all_chunks)} chunks across {len(books)} books into ChromaDB!")
    print(f"[VERIFY] Collection count: {collection.count()} vectors stored in '{COLLECTION_NAME}'.")
    return collection.count()


if __name__ == "__main__":
    count = ingest_corpus()
    print(f"\nPart 1 Ingestion Pipeline completed with {count} chunks stored.")
