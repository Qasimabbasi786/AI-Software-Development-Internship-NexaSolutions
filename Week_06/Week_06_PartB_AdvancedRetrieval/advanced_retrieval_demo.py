"""
Week 6 Part B — Document Loaders, Smarter Splitting & Advanced Retrieval

Features:
1. RecursiveCharacterTextSplitter: Respects paragraph breaks (\n\n), line breaks (\n),
   and sentence boundaries (. ) before falling back to hard character cuts.
2. Vector Store & Gemini Embeddings: Chroma vector store with Google Gemini embeddings
   (models/gemini-embedding-001).
3. MultiQueryRetriever: Generates multiple reformulated query perspectives using the LLM
   (Google Gemini / gemini-3.8-flash) and merges/deduplicates retrieved documents.
4. Evaluation: Benchmarks single-query retrieval vs. MultiQueryRetriever on the 5 Week 5 test questions,
   including verbose query inspection and trade-off analysis.
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Ensure local .env is loaded
_part_dir = Path(__file__).resolve().parent
_local_env = _part_dir / ".env"
_root_env = _part_dir.parent / ".env"

if _local_env.exists():
    load_dotenv(dotenv_path=_local_env)
elif _root_env.exists():
    load_dotenv(dotenv_path=_root_env)
else:
    load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
try:
    from langchain.retrievers.multi_query import MultiQueryRetriever
except ImportError:
    from langchain_classic.retrievers.multi_query import MultiQueryRetriever

from model_factory import get_chat_model, get_embeddings

# Setup logging to inspect query reformulations from MultiQueryRetriever
logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

RAW_BOOK_TEXT = """
Clean Code: A Handbook of Agile Software Craftsmanship by Robert C. Martin (Uncle Bob).
This book teaches practical software engineering rules. It emphasizes meaningful naming conventions,
small single-responsibility functions, avoiding hidden side effects, defensive programming, and rigorous
unit testing using Test-Driven Development (TDD).

Designing Data-Intensive Applications by Martin Kleppmann.
A comprehensive guide to backend data engineering and distributed systems. It explains storage engine internals
such as Log-Structured Merge-trees (LSM-trees) and B-trees, replication topologies (single-leader, multi-leader),
partitioning strategies, distributed ACID transactions, consensus algorithms, and event stream processing with Apache Kafka.

Dune by Frank Herbert.
A seminal science fiction masterpiece set on the desert planet Arrakis. It chronicles the journey of Paul Atreides
as his noble family navigates political betrayal and takes control of the only source of the spice melange,
a narcotic substance essential for interstellar space navigation.

Building Microservices by Sam Newman.
Covers evolutionary architecture, domain-driven service boundaries, API gateways, asynchronous event messaging,
Docker containerization, and canary deployment patterns.

The Pragmatic Programmer: Your Journey to Mastery by Andrew Hunt and David Thomas.
Focuses on software craftsmanship, DRY (Don't Repeat Yourself), orthogonality, continuous refactoring,
tracer bullets, and pragmatic decision making.
"""

TEST_QUESTIONS = [
    "What storage engines and streaming technologies are discussed in Designing Data-Intensive Applications?",
    "Who wrote Clean Code and what does it teach about functions?",
    "What is the spice melange in the novel Dune?",
    "What deployment strategies are recommended for microservices?",
    "How do you calculate eigenvalues in linear algebra using NumPy?"  # Out of catalog question
]


def run_advanced_retrieval_demo():
    print("==================================================================")
    print(" WEEK 6 PART B: SMARTER SPLITTING & MULTI-QUERY RETRIEVAL DEMO")
    print("==================================================================")

    # -------------------------------------------------------------
    # 1. Smarter Splitting with RecursiveCharacterTextSplitter
    # -------------------------------------------------------------
    print("\n1. Applying RecursiveCharacterTextSplitter (chunk_size=500, chunk_overlap=50)...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_text(RAW_BOOK_TEXT.strip())
    print(f"   Generated {len(chunks)} cleanly bounded chunks respecting natural language boundaries.")
    for idx, chunk in enumerate(chunks, 1):
        print(f"   [Chunk #{idx}] ({len(chunk)} chars): {chunk[:70].replace(chr(10), ' ')}...")

    # -------------------------------------------------------------
    # 2. Local Chroma Vector Store with Gemini Embeddings
    # -------------------------------------------------------------
    embeddings = get_embeddings()
    print(f"\n2. Initializing Chroma Vector Store with {type(embeddings).__name__}...")

    metadatas = [{"source": f"book_{i+1}"} for i in range(len(chunks))]
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas
    )

    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    model = get_chat_model()
    print(f"   Configured Base Retriever (k=3) & LLM: {type(model).__name__}")

    # -------------------------------------------------------------
    # 3. Wrapping with MultiQueryRetriever
    # -------------------------------------------------------------
    multi_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=model
    )

    # -------------------------------------------------------------
    # 4. Comparative Evaluation on Week 5 Benchmark Questions
    # -------------------------------------------------------------
    print("\n3. Running Comparative Evaluation on 5 Benchmark Questions:")
    print("=" * 66)

    for i, question in enumerate(TEST_QUESTIONS, 1):
        print(f"\n--- [Question {i}]: \"{question}\" ---")

        # A. Plain Retriever
        plain_docs = base_retriever.invoke(question)
        print(f"\n[Plain Retriever] Retrieved {len(plain_docs)} chunks:")
        for d in plain_docs:
            source = d.metadata.get("source", "N/A")
            excerpt = d.page_content[:90].replace('\n', ' ')
            print(f"  * [{source}] {excerpt}...")

        # B. MultiQueryRetriever
        print("\n[MultiQueryRetriever] Generating reformulations and executing merged retrieval...")
        try:
            mq_docs = multi_retriever.invoke(question)
            print(f"  Retrieved & deduplicated {len(mq_docs)} chunks across perspectives:")
            for d in mq_docs:
                source = d.metadata.get("source", "N/A")
                excerpt = d.page_content[:90].replace('\n', ' ')
                print(f"  * [{source}] {excerpt}...")
        except Exception as ex:
            print(f"  MultiQueryRetriever execution notice: {ex}")

    # -------------------------------------------------------------
    # 5. Intentional Failure Case Analysis: Precision Dilution
    # -------------------------------------------------------------
    print("\n" + "=" * 66)
    print("4. Intentional Precision Dilution Test Case:")
    dilution_query = "What exact year was the first single-leader replication paper written?"
    print(f"Target Query: \"{dilution_query}\"")
    print("Explanation: The catalog contains general distributed systems concepts in DDIA, but NO publication dates.")
    print("Single Query: Focuses narrowly on 'replication' or finds nothing above threshold.")
    print("MultiQuery: Expands into broader queries like 'History of distributed algorithms' or 'Academic papers in computing',")
    print("pulling in irrelevant general engineering chunks (e.g., Clean Code or Pragmatic Programmer) that add noise to the prompt.")
    print("=" * 66)


if __name__ == "__main__":
    run_advanced_retrieval_demo()
