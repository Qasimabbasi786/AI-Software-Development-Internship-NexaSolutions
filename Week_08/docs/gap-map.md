# Curriculum Gap Map & Self-Assessment Matrix

**Milestone:** Week 8 — Capstone Deliverable 12  
**Candidate:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Evaluation Date:** 2026-10-23  

---

## 1. Curriculum Coverage & Status Breakdown

Eight weeks cannot cover every single specialty in modern full-stack AI engineering. The following gap map honestly documents what was mastered in depth, what was partially implemented, what was touched at an awareness level, and what was deliberately deferred.

| Technical Domain | Curriculum Coverage | Implementation Scope & Notes | Suggested Next Step |
| :--- | :--- | :--- | :--- |
| **C#, OOP, Collections, LINQ, Async, ASP.NET Core, EF Core, JWT Auth** | **Covered** | Weeks 1–4, applied through Week 8 across all CRUD, authentication, and gateway layers. | Production performance profiling with BenchmarkDotNet. |
| **SOLID, Clean Architecture, Middleware Design** | **Partial** | N-tier architecture, DI, custom correlation and security middleware implemented. | Refactor backend into a strict Hexagonal / Onion architecture with MediatR CQRS. |
| **Angular: Components, Services, Forms, Routing, HttpClient, Guards** | **Covered** | Weeks 1–4, 6–7. Interactive standalone components, reactive signals, and SSE client streams. | Advanced reactive form custom validators and sub-modules. |
| **RxJS Depth & Enterprise State Management** | **Awareness** | Basic RxJS subjects and observables used; no centralized NgRx / Redux store implemented. | Build a dedicated feature using `@ngrx/signals` or NgRx ComponentStore. |
| **Lazy Loading, Angular Material, Charts & Dashboards** | **Not Covered** | Hand-crafted Tailwind and CSS used rather than component libraries. | Build an administrative analytics dashboard for token costs and latency metrics. |
| **File Uploads (Angular ➔ .NET ➔ AI Document Q&A)** | **Not Covered** | System consumed pre-seeded catalog strings and JSON rather than multipart file uploads. | Implement multipart upload for user PDF ingestion into ChromaDB. |
| **Python Fundamentals, FastAPI, Pydantic** | **Covered** | Weeks 3–4, 6–8. Production microservice with custom async middlewares and data schemas. | Asynchronous task queues with Celery / Redis. |
| **LLM APIs (Anthropic, OpenAI, Gemini), Streaming, Structured Outputs** | **Covered** | Weeks 6–8. Google Gemini primary driver, OpenAI fallback, SSE streaming (`astream`). | Multi-provider fallback load balancing with LiteLLM. |
| **Prompt Engineering & Prompt Injection Defense** | **Covered** | Weeks 4, 7, 8. Untrusted document wrappers, Pydantic guardrails, and adversarial red-teaming. | Automated red-teaming pipelines with PyRIT or Garak. |
| **Embeddings, ChromaDB, Recursive Chunking, LangChain RAG** | **Covered** | Weeks 5–6, 8. Content-hash incremental indexing, Chroma vector store persistence. | Dynamic metadata filtering and chunk size experimentation. |
| **PDF / Unstructured Document Loaders & Ingestion Pipelines** | **Not Covered** | Relational catalog texts indexed; no PDF/DOCX binary parsing pipeline built. | Integrate `unstructured` or `PyPDFLoader` for arbitrary document parsing. |
| **Alternative Vector Stores (Qdrant, Pinecone, Weaviate, FAISS)** | **Awareness** | ChromaDB was exclusively used as the local embedded vector store. | Swap ChromaDB with self-hosted Qdrant or Milvus behind a repository interface. |
| **Advanced RAG (Hybrid Search, Re-Ranking, Contextual Retrieval)** | **Partial** | MultiQueryRetriever implemented; no cross-encoder re-ranking or dense-sparse hybrid search. | Implement BM25 + dense embedding hybrid search with Cohere / FlashRank re-ranking. |
| **LangGraph: State Machines, Memory, HITL, Persistence** | **Covered** | Weeks 7–8. StateGraph nodes, Human-in-the-Loop interrupts, SQLite checkpointer. | Long-term memory extraction and semantic user profile synthesis. |
| **Multi-Agent Orchestration (Supervisor / Hierarchical Swarms)** | **Stretch Only** | Single-agent multi-tool graph with intent router; multi-agent supervisor not productionized. | Build a 2-agent supervisor pattern (Researcher Agent + Critic/Auditor Agent). |
| **Evaluation, Tracing, Guardrails, Caching, Token Budgeting** | **Covered** | Weeks 6–8. 20-scenario eval harness, safe `TTLCache`, distributed correlation tracing. | Integrate LangSmith / Phoenix Arize for online production telemetry. |
| **AI Application Security (OWASP Top 10 for LLMs)** | **Covered** | Week 7 red-team audit, Week 8 security hardening, rate limiting, and GDPR erasure. | Implement cryptographically signed tool execution payloads. |
| **Local Models (Ollama, HuggingFace Transformers)** | **Not Covered** | Cloud API models utilized exclusively throughout the internship. | Deploy local Llama-3.1-8B via Ollama for zero-cost offline development. |
| **Model Context Protocol (MCP) & Semantic Kernel** | **Awareness** | Explored in Week 7 research write-ups; no direct runtime MCP servers deployed. | Expose library tools via an MCP server compliant with Anthropic Desktop. |

---

## 2. Objective Competency Self-Assessment (1–4 Scale)

**Rating Scale Definition:**
- **1 = Heard of it:** Understand the general term and purpose, but have not configured or coded it.
- **2 = Can explain it:** Understand the architectural concepts, trade-offs, and failure modes; can discuss it in an interview.
- **3 = Can build it:** Capable of implementing and debugging it independently using official documentation.
- **4 = Could teach it:** Deep conceptual and operational mastery; capable of mentoring others and designing enterprise implementations.

| Technical Competency Area | Self-Rating | Mentor Rating (Expected) | Gap Analysis & Justification |
| :--- | :---: | :---: | :--- |
| **C# & ASP.NET Core Web API Development** | **4 / 4** | 4 / 4 | Demonstrated mastery of middleware pipelines, JWT auth, Polly resilience, EF Core, and health probes. |
| **Relational Data Modeling & EF Core (PostgreSQL)** | **3 / 4** | 3 / 4 | Strong schema design and migrations; can deepen knowledge on query execution plans and index optimization. |
| **Angular 18 Reactive Architecture (Signals, Standalone)** | **3 / 4** | 3 / 4 | Built production UI with live SSE streams; would benefit from deeper NgRx state management patterns. |
| **Python Microservice Architecture (FastAPI, Pydantic)** | **4 / 4** | 4 / 4 | Authored production-ready async services with structured logging, CORS, security dependencies, and SSE. |
| **Vector Search & Embeddings (ChromaDB)** | **3 / 4** | 3 / 4 | Implemented content-hash incremental indexing; want hands-on experience with clustered enterprise vector databases. |
| **LangChain LCEL & MultiQuery Retrieval** | **3 / 4** | 3 / 4 | Mastered chain composition and fallback models; want to expand into hybrid re-ranking. |
| **LangGraph StateGraph & Human-in-the-Loop (HITL)** | **4 / 4** | 4 / 4 | Deep mastery of interrupt state, SQLite checkpointer persistence, and typed turn resumption. |
| **AI Application Security & Prompt Red-Teaming** | **3 / 4** | 3 / 4 | Strong defense against prompt injection and unauthorized writes; want to study multi-turn jailbreaks. |
| **Docker & Multi-Container Deployment Orchestration** | **4 / 4** | 4 / 4 | Packaged 4-tier stack with multi-stage builds, non-root users, volume persistence, and acyclic healthchecks. |
| **Observability, Tracing & Distributed Correlation** | **3 / 4** | 3 / 4 | Implemented end-to-end `X-Correlation-Id`; next step is OpenTelemetry distributed collectors. |

---

## 3. Top Three Knowledge Gaps for the Next 90 Days & Concrete Follow-Up Projects

Based on the self-assessment and curriculum gap map, three strategic technical gaps have been identified for post-internship acceleration. Each gap is paired with an actionable, production-grade project.

---

### 🚀 Strategic Gap 1: Enterprise Document Ingestion & Hybrid RAG (Dense + Sparse Search)
- **The Gap:** Our current catalog RAG indexes static text chunks from relational databases. In real-world enterprise environments, documents are unstructured PDFs, scanned files, or markdown hierarchies where pure dense semantic search struggles with exact part numbers, acronyms, or specific citations.
- **90-Day Concrete Project:** **`DocuPulse: Enterprise Hybrid Multimodal Document Q&A Engine`**
  - **Stack:** Python 3.12, FastAPI, Qdrant / Weaviate, Cohere Re-ranker, Unstructured.io, Docker.
  - **Architecture:** Multipart PDF file upload endpoint ➔ PyMuPDF / Unstructured text and table extraction ➔ Hierarchical semantic chunking ➔ Dual indexing: Dense embeddings (Chroma/Qdrant) + Sparse BM25 (Rank-BM25) ➔ Reciprocal Rank Fusion (RRF) with Cohere cross-encoder re-ranking top 5 chunks into Gemini-1.5-Pro.
  - **Target Milestone:** Deliver a containerized microservice achieving >95% retrieval accuracy on technical financial filings (10-K forms) within 30 days.

---

### 🚀 Strategic Gap 2: Advanced Angular Reactive State Management (NgRx Signals Store) & Observability Dashboard
- **The Gap:** The current Angular frontend handles state reactively using component-level Signals, but lacks an enterprise-wide immutable state store and administrative telemetry visualization.
- **90-Day Concrete Project:** **`NexaPulse: Real-Time AI Fleet Observability Dashboard`**
  - **Stack:** Angular 18, `@ngrx/signals`, Apache ECharts / Chart.js, TailwindCSS, WebSocket/SSE.
  - **Architecture:** Standalone admin dashboard with role-guarded routes (`/admin/telemetry`) ➔ Centralized NgRx Signal Store managing global state (active SSE streams, per-user daily token consumption, error rates) ➔ Real-time live visual graphs rendering latency percentiles (p50, p95), circuit breaker states, and cache hit ratios.
  - **Target Milestone:** Deploy an accessible, WCAG-compliant analytics dashboard with lazy-loaded route chunks and dark mode within 60 days.

---

### 🚀 Strategic Gap 3: Multi-Agent Hierarchical Orchestration (Supervisor Pattern) with Model Context Protocol (MCP)
- **The Gap:** While our LangGraph system executes dynamic tools with human approvals, it operates as a single agent. Complex tasks require specialized swarms (e.g. a catalog specialist collaborating with a user account auditor and a policy compliance reviewer) adhering to modern interoperability standards like MCP.
- **90-Day Concrete Project:** **`SwarmOps: Hierarchical Multi-Agent Audit Mesh with MCP`**
  - **Stack:** LangGraph 0.2+, FastMCP, Anthropic Claude 3.5 Sonnet, Local Llama-3.1-8B via Ollama.
  - **Architecture:** Supervisor agent coordinating two specialized worker agents:
    1. *Catalog Researcher Agent:* Connects via MCP to external library repositories and publishers.
    2. *Compliance & Budget Auditor Agent:* Evaluates user borrowing policies, quotas, and safety guidelines.
    Supervisor synthesizes outputs and coordinates user HITL approval when policies require human judgment.
  - **Target Milestone:** Implement and benchmark the multi-agent supervisor pattern, demonstrating zero hallucination on complex cross-domain research inquiries within 90 days.
