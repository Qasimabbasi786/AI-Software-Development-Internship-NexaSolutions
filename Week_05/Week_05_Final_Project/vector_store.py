"""
Week 5 Project — Step 2: Chunk, Embed, and Store
Loads the corpus, splits into overlapping chunks, generates embeddings, and indexes in ChromaDB with persistent storage.
"""
import os
import json
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

COLLECTION_NAME = "library_rag_final"
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db_data")

# Persistent Chroma Client
_client = None


def chunk_text(text: str, chunk_size: int = 350, overlap: int = 40) -> list[str]:
    """
    Fixed-size chunking with overlap to preserve sentence boundaries.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def get_chroma_client():
    global _client
    if _client is None:
        os.makedirs(DB_DIR, exist_ok=True)
        _client = chromadb.PersistentClient(path=DB_DIR)
    return _client


def get_embedding_function():
    # ChromaDB native embedding function for local reliability
    return embedding_functions.DefaultEmbeddingFunction()


def build_vector_store(corpus_file: str = None):
    """
    Ingests all documents from corpus.json into ChromaDB persistent collection.
    """
    if corpus_file is None:
        corpus_file = os.path.join(os.path.dirname(__file__), "corpus.json")

    if not os.path.exists(corpus_file):
        from fetch_corpus import build_and_save_corpus
        documents = build_and_save_corpus(corpus_file)
    else:
        with open(corpus_file, "r", encoding="utf-8") as f:
            documents = json.load(f)

    client = get_chroma_client()
    embedding_fn = get_embedding_function()

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    all_chunks = []
    all_metadatas = []
    all_ids = []

    for doc in documents:
        doc_id = doc["id"]
        doc_text = doc["text"]
        base_meta = doc["metadata"]

        chunks = chunk_text(doc_text)
        for i, chunk in enumerate(chunks):
            meta = dict(base_meta)
            meta["chunk_index"] = i
            meta["source"] = base_meta.get("title", doc_id)

            all_chunks.append(chunk)
            all_metadatas.append(meta)
            all_ids.append(f"{doc_id}_chunk_{i}")

    if all_chunks:
        collection.add(
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )

    print(f"[VECTOR STORE] Successfully indexed {len(all_chunks)} chunks across {len(documents)} books into '{COLLECTION_NAME}'.")
    return collection


def retrieve_relevant_chunks(question: str, k: int = 3) -> tuple[list[str], list[dict]]:
    client = get_chroma_client()
    embedding_fn = get_embedding_function()
    
    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_fn
        )
    except Exception:
        collection = build_vector_store()

    results = collection.query(query_texts=[question], n_results=k)
    chunks = results["documents"][0] if results["documents"] else []
    metas = results["metadatas"][0] if results["metadatas"] else []
    return chunks, metas


if __name__ == "__main__":
    col = build_vector_store()
    test_q = "Which books discuss distributed systems and replication?"
    docs, metas = retrieve_relevant_chunks(test_q, k=2)
    print(f"\nTest Query: '{test_q}'")
    for i, (d, m) in enumerate(zip(docs, metas)):
        print(f"[{i+1}] Source: {m['source']} | Chunk: {d}")
