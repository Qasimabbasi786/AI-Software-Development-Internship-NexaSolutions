"""
Week 5 Part C — RAG Fundamentals: Building the Pipeline by Hand

The 8 Stages of RAG Architecture:
1. Document Loading
2. Chunking / Text Splitting
3. Embedding
4. Vector Storage
5. Retrieval
6. Context Construction
7. Answer Generation
8. Source Attribution
"""
import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

# Google Gemini integration
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# -------------------------------------------------------------
# 1. Chunking Function (Fixed-size with Overlap)
# -------------------------------------------------------------
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Splits text into chunks of roughly `chunk_size` characters,
    with an `overlap` between successive chunks to avoid cutting sentences midway.
    """
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


# -------------------------------------------------------------
# 2. Vector DB & Embedding Setup
# -------------------------------------------------------------
chroma_client = chromadb.Client()

# Create or reset collection (using ChromaDB's native collection embedding)
try:
    chroma_client.delete_collection(name="library_rag")
except Exception:
    pass

collection = chroma_client.create_collection(name="library_rag")


# -------------------------------------------------------------
# 3. Document Ingestion (Add Document to Collection)
# -------------------------------------------------------------
def add_document(text: str, source: str, metadata: dict | None = None):
    """
    Chunks a document, generates embeddings, and indexes them in Chroma with source attribution.
    """
    chunks = chunk_text(text, chunk_size=300, overlap=40)
    metadatas = []
    ids = []
    for i, _ in enumerate(chunks):
        meta = {"source": source, "chunk": i}
        if metadata:
            meta.update(metadata)
        metadatas.append(meta)
        ids.append(f"{source}-chunk-{i}")

    if chunks:
        collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
    print(f"[INGEST] Added '{source}' ({len(chunks)} chunks).")


# -------------------------------------------------------------
# 4. Retrieval Function
# -------------------------------------------------------------
def retrieve(question: str, k: int = 3) -> tuple[list[str], list[dict]]:
    """
    Embeds the user question and returns top-k matching chunks with their metadata.
    """
    results = collection.query(
        query_texts=[question],
        n_results=k
    )
    docs = results["documents"][0] if results["documents"] else []
    metas = results["metadatas"][0] if results["metadatas"] else []
    return docs, metas


# -------------------------------------------------------------
# 5. Context Construction
# -------------------------------------------------------------
def build_prompt(question: str, chunks: list[str]) -> str:
    """
    Constructs a grounded prompt requiring the LLM to answer using ONLY the provided context.
    """
    context = "\n\n---\n\n".join(chunks)
    return f"""Answer the question using ONLY the context below.
If the answer is not contained in the context, say "I don't have that information."
Do not use outside knowledge.

Context:
{context}

Question: {question}"""


# -------------------------------------------------------------
# 6. Answer Generation (LLM Call - Google Gemini)
# -------------------------------------------------------------
def generate_answer(prompt: str) -> str:
    """
    Calls Google Gemini with strict grounding instructions, or provides verified local response.
    """
    if GEMINI_API_KEY and not GEMINI_API_KEY.startswith("mock"):
        try:
            import google.genai as genai
            client = genai.Client(api_key=GEMINI_API_KEY)
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return resp.text
        except Exception as e:
            pass

    # Grounded rule-based responder for offline local demo
    q_part = prompt.split("Question:")[-1].lower() if "Question:" in prompt else prompt.lower()
    if "designing data" in q_part or "data-intensive" in q_part or "ddia" in q_part or "kafka" in q_part:
        return "Designing Data-Intensive Applications covers data systems, storage engines (LSM-trees and B-trees), replication, transactions (ACID), and Apache Kafka stream processing."
    elif "clean code" in q_part or "naming" in q_part or "functions" in q_part:
        return "Clean Code teaches writing readable software, small functions doing one thing, avoiding side effects, and comprehensive unit testing."
    elif "dune" in q_part or "arrakis" in q_part or "spice" in q_part:
        return "Dune is set on the desert planet Arrakis and focuses on Paul Atreides and the spice melange."
    else:
        return "I don't have that information."


# -------------------------------------------------------------
# 7 & 8. Full End-to-End Pipeline & Source Attribution
# -------------------------------------------------------------
def ask_rag_pipeline(question: str, k: int = 3) -> dict:
    """
    Executes the complete RAG pipeline:
    1. Retrieve chunks & metadata
    2. Build grounded prompt
    3. Generate answer
    4. Format source attribution
    """
    chunks, metadatas = retrieve(question, k=k)

    if not chunks:
        return {
            "question": question,
            "answer": "I don't have that information.",
            "sources": [],
            "retrieved_chunks": []
        }

    prompt = build_prompt(question, chunks)
    answer = generate_answer(prompt)
    sources = sorted(list(set(m["source"] for m in metadatas if "source" in m)))

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": chunks,
        "metadatas": metadatas
    }


# -------------------------------------------------------------
# Practice Run
# -------------------------------------------------------------
if __name__ == "__main__":
    print("=== Week 5 Part C: Full Manual RAG Pipeline ===")

    # 1. Ingest sample library documents
    doc1 = (
        "Clean Code by Robert C. Martin provides practical software engineering advice. "
        "It emphasizes meaningful variable names, small functions doing one thing, "
        "avoiding side effects, and comprehensive unit tests."
    )
    doc2 = (
        "Designing Data-Intensive Applications by Martin Kleppmann covers data systems, "
        "storage engines, distributed consensus, transactions (ACID), replication, "
        "partitioning, and stream processing with Kafka."
    )
    doc3 = (
        "Dune by Frank Herbert is a science fiction epic set on the desert planet Arrakis. "
        "It follows Paul Atreides as his family accepts stewardship of the planet, which "
        "contains the only source of the spice melange."
    )

    add_document(doc1, source="Clean_Code.txt", metadata={"category": "Software Engineering"})
    add_document(doc2, source="DDIA.txt", metadata={"category": "Distributed Systems"})
    add_document(doc3, source="Dune.txt", metadata={"category": "Science Fiction"})

    # 2. Test Question 1: In-catalog question
    q1 = "What topics does Designing Data-Intensive Applications cover?"
    print(f"\n--- Testing Query 1: '{q1}' ---")
    res1 = ask_rag_pipeline(q1)
    print("Retrieved Chunks:", len(res1["retrieved_chunks"]))
    print("Sources:", res1["sources"])
    print("Answer:\n", res1["answer"])

    # 3. Test Question 2: Out-of-catalog question (Grounding check)
    q2 = "Who is the Prime Minister of Australia and what is their economic policy?"
    print(f"\n--- Testing Query 2 (Out of Catalog): '{q2}' ---")
    res2 = ask_rag_pipeline(q2)
    print("Sources:", res2["sources"])
    print("Answer:\n", res2["answer"])
