"""
Week 5 Final Project — Complete RAG Pipeline Module (rag_pipeline.py)
====================================================================
Integrates chunking, Google Gemini embedding generation, ChromaDB vector
storage (collection 'library_rag_final'), top-k retrieval, prompt grounding,
and LLM response generation with citation attribution.
"""
import os
import json
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

# Load environment configuration
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

COLLECTION_NAME = "library_rag_final"
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db_data")
CORPUS_FILE = os.path.join(os.path.dirname(__file__), "corpus.json")


def chunk_text(text: str, chunk_size: int = 350, overlap: int = 40) -> list[str]:
    """
    Fixed-size sliding window chunking with character overlap.
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
    os.makedirs(DB_DIR, exist_ok=True)
    return chromadb.PersistentClient(path=DB_DIR)


def get_embedding_function():
    if GEMINI_API_KEY and not GEMINI_API_KEY.startswith("your_"):
        try:
            import google.genai as genai
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

            return GeminiChromaEmbeddingFunction(_client)
        except Exception:
            return embedding_functions.DefaultEmbeddingFunction()

    return embedding_functions.DefaultEmbeddingFunction()


def ensure_collection():
    client = get_chroma_client()
    embedding_fn = get_embedding_function()
    try:
        col = client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)
        if col.count() > 0:
            return col
    except Exception:
        pass

    # Build collection from corpus
    from ingest_corpus import ingest_corpus
    ingest_corpus(CORPUS_FILE)
    return client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)


def retrieve_chunks(query: str, k: int = 3) -> tuple[list[str], list[dict]]:
    col = ensure_collection()
    results = col.query(query_texts=[query], n_results=k)
    chunks = results["documents"][0] if results["documents"] else []
    metas = results["metadatas"][0] if results["metadatas"] else []
    return chunks, metas


def build_rag_prompt(question: str, context_chunks: list[str]) -> str:
    context_str = "\n\n---\n\n".join(context_chunks)
    return f"""Answer the question using ONLY the context below.
If the answer is not contained in the context, say "I don't have that information."
Do not use outside knowledge.

Context:
{context_str}

Question: {question}"""


def query_rag_pipeline(question: str, k: int = 3) -> dict:
    chunks, metas = retrieve_chunks(question, k=k)

    if not chunks:
        return {
            "answer": "I don't have that information.",
            "sources": []
        }

    prompt = build_rag_prompt(question, chunks)
    
    # LLM Inference
    answer = None
    if GEMINI_API_KEY and not GEMINI_API_KEY.startswith("your_"):
        try:
            import google.genai as genai
            client = genai.Client(api_key=GEMINI_API_KEY)
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            answer = resp.text
        except Exception:
            pass

    if not answer:
        from main import generate_llm_response
        answer = generate_llm_response(prompt)

    sources = sorted(list(set(m.get("source", m.get("title", "Unknown")) for m in metas if m)))
    return {
        "answer": answer,
        "sources": sources
    }
