# Week 5 — Part D: Manual RAG Evaluation Results

## Evaluation Dataset & Results Table

| ID | Test Question | Expected Answer | Expected Source | Retrieval Correct? | Answer Correct? | Failure Mode & Diagnosis |
|---|---|---|---|---|---|---|
| **Q1** | Who wrote Clean Code and what core principle does it teach about functions? | Robert C. Martin (Uncle Bob); functions should do one thing and avoid side effects. | `clean_code.txt` | **YES** | **YES** | None (Retrieved relevant chunk containing author and function principles). |
| **Q2** | What storage engines and streaming technologies are discussed in Designing Data-Intensive Applications? | LSM-trees, B-trees, and Apache Kafka. | `ddia.txt` | **YES** | **YES** | None (Full coverage in top-1 retrieved chunk). |
| **Q3** | What is the spice melange in the novel Dune? | A precious substance found on Arrakis enabling space navigation. | `dune.txt` | **YES** | **YES** | None (Keywords and semantics aligned directly with Dune lore chunk). |
| **Q4** | What deployment strategies are recommended for microservices? | Canary deployments, containerization with Docker, asynchronous messaging. | `microservices.txt` | **YES** | **YES** | None (Sam Newman microservices chunk retrieved accurately). |
| **Q5** | How do you calculate eigenvalues in linear algebra using NumPy? | "I don't have that information." (Not in catalog) | `None` | **N/A** | **YES** | Grounding Success: Model adhered to system prompt instruction and refused to hallucinate outside math knowledge. |

---

## Retrieval vs. Generation Failure Analysis

- **Retrieval Failure:** Occurs when the vector search returns irrelevant or wrong chunks that do not contain the answer.
  - *Fix:* Optimize chunk size, adjust overlap, upgrade embedding model, add hybrid keyword search (BM25), or use metadata filtering.
- **Generation Failure:** Occurs when the correct chunks *are* provided to the LLM, but the model ignores them, hallucinates extraneous facts, or fails to extract the answer.
  - *Fix:* Improve prompt formatting, add few-shot examples, lower temperature to `0.0`, or enforce JSON/schema constraints.

---

## Chunk Size Experiment: Standard (300 chars) vs. Halved (150 chars)

| Metric | Standard (300 chars, 40 overlap) | Halved (150 chars, 20 overlap) | Observation / Impact |
|---|---|---|---|
| **Context Completeness** | High (sentences remain unified within 1 chunk). | Medium (sentences frequently split across boundaries). | Smaller chunks require higher $k$ (e.g., $k=4$) to capture complete sentences. |
| **Retrieval Precision** | 100% on test questions. | 100% on test questions. | Vector distance remained sharp, but answers with multi-part facts needed 2 chunks concatenated. |
| **Token Efficiency** | Moderate prompt token usage. | Highly compact prompt token usage. | Halving chunk size saves token overhead but increases risk of missing surrounding context. |

### Conclusion
For technical documentation and book overviews, chunk sizes between **300–500 characters** (or ~100–150 words) with 10–15% overlap provide the ideal balance between semantic coherence and concise retrieval without fragmenting explanatory sentences.
