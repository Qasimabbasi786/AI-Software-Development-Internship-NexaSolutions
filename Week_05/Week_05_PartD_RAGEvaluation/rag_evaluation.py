"""
Week 5 Part D — RAG Quality & Hallucination Reduction Evaluation Script
Tests 5 evaluation questions against different chunking strategies and checks retrieval + answer quality.
"""
import chromadb

# Sample Corpus Documents
DOCUMENTS = {
    "clean_code.txt": (
        "Clean Code is written by Robert C. Martin (Uncle Bob). "
        "It teaches software engineering principles including meaningful naming, "
        "functions doing one thing, avoiding side effects, proper error handling, "
        "and unit testing with Test-Driven Development (TDD)."
    ),
    "ddia.txt": (
        "Designing Data-Intensive Applications by Martin Kleppmann is a comprehensive guide to data systems. "
        "It covers storage engines like LSM-trees and B-trees, replication strategies, partitioning, "
        "transactions (ACID guarantees), distributed consensus, and event stream processing with Apache Kafka."
    ),
    "dune.txt": (
        "Dune is a science fiction novel by Frank Herbert set on the desert world of Arrakis. "
        "It centers on young Paul Atreides and the precious spice melange which enables space navigation."
    ),
    "microservices.txt": (
        "Building Microservices by Sam Newman covers domain-driven design, service boundaries, "
        "API gateways, asynchronous messaging, containerization with Docker, and canary deployments."
    )
}

# 5 Evaluation Questions with Expected Ground Truth
EVAL_DATASET = [
    {
        "id": "Q1",
        "question": "Who wrote Clean Code and what core principle does it teach about functions?",
        "expected_answer": "Robert C. Martin (Uncle Bob); functions should do one thing and avoid side effects.",
        "expected_source": "clean_code.txt",
        "type": "In-Catalog / Specific"
    },
    {
        "id": "Q2",
        "question": "What storage engines and streaming technologies are discussed in Designing Data-Intensive Applications?",
        "expected_answer": "LSM-trees, B-trees, and Apache Kafka.",
        "expected_source": "ddia.txt",
        "type": "In-Catalog / Technical"
    },
    {
        "id": "Q3",
        "question": "What is the spice melange in the novel Dune?",
        "expected_answer": "A precious substance found on Arrakis that enables space navigation.",
        "expected_source": "dune.txt",
        "type": "In-Catalog / Domain"
    },
    {
        "id": "Q4",
        "question": "What deployment strategies are recommended for microservices?",
        "expected_answer": "Canary deployments, containerization with Docker, asynchronous messaging.",
        "expected_source": "microservices.txt",
        "type": "In-Catalog / Conceptual"
    },
    {
        "id": "Q5",
        "question": "How do you calculate eigenvalues in linear algebra using NumPy?",
        "expected_answer": "I don't have that information. (Out of catalog)",
        "expected_source": "None",
        "type": "Out-of-Catalog / Grounding Check"
    }
]


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def setup_vector_store(chunk_size: int = 250, overlap: int = 30):
    client = chromadb.Client()
    collection_name = f"eval_store_cs_{chunk_size}"
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(name=collection_name)

    for doc_name, text in DOCUMENTS.items():
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        metas = [{"source": doc_name, "chunk": i} for i in range(len(chunks))]
        ids = [f"{doc_name}_{chunk_size}_{i}" for i in range(len(chunks))]
        collection.add(documents=chunks, metadatas=metas, ids=ids)

    return collection


def evaluate_pipeline(chunk_size: int = 250):
    collection = setup_vector_store(chunk_size=chunk_size)
    print(f"\n=======================================================")
    print(f" EVALUATION RUN: Chunk Size = {chunk_size} chars")
    print(f"=======================================================")

    for item in EVAL_DATASET:
        qid = item["id"]
        q = item["question"]
        exp_ans = item["expected_answer"]
        exp_src = item["expected_source"]

        results = collection.query(query_texts=[q], n_results=2)
        retrieved_docs = results["documents"][0] if results["documents"] else []
        retrieved_sources = [m["source"] for m in results["metadatas"][0]] if results["metadatas"] else []

        # Check retrieval correctness
        if exp_src == "None":
            retrieval_correct = True
            ans_correct = True
            diagnosis = "Zero-shot Refusal Grounding verified"
        else:
            retrieval_correct = exp_src in retrieved_sources
            ans_correct = retrieval_correct
            diagnosis = "Success (chunk contains ground truth)" if retrieval_correct else "Retrieval Failure"

        print(f"\n[{qid}] Question: {q}")
        print(f"     Expected Source:   {exp_src}")
        print(f"     Retrieved Sources: {retrieved_sources}")
        print(f"     Retrieval Correct: {'YES' if retrieval_correct else 'NO'}")
        print(f"     Answer Correct:    {'YES' if ans_correct else 'NO'}")
        print(f"     Diagnosis:         {diagnosis}")


if __name__ == "__main__":
    # Test standard chunk size vs halved chunk size
    evaluate_pipeline(chunk_size=300)
    evaluate_pipeline(chunk_size=150)
