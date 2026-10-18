# Architecture Decision Record

## ADR-001: Separate FastAPI Service vs. Calling LLMs Directly from .NET

- **Status:** Accepted
- **Deciders:** Muhammad Qasim (Lead Architect), Engineering Team
- **Date:** 2026-10-18
- **Scope:** System Tiering & AI Orchestration Boundary

---

### Context & Problem Statement
Our application stack consists of an enterprise ASP.NET Core 8 Web API managing business entities, authentication, and SQL Server persistence, paired with an Angular 18 frontend. We required an autonomous conversational agent capable of tool execution, directed-graph routing, human-in-the-loop interruption, and vector-backed RAG.

We had to decide whether to:
1. Orchestrate the AI agent directly within the .NET process using Microsoft Semantic Kernel or LangChain.NET.
2. Maintain a dedicated, isolated Python FastAPI microservice running LangGraph and LangChain, communicating with .NET via HTTP REST and a shared internal service key.

### Decision Drivers
- **Ecosystem Velocity:** AI research, state graph frameworks (LangGraph), chunking strategies, and retrieval libraries evolve dramatically faster in the Python ecosystem.
- **Fault Domain Isolation:** Python AI libraries (ChromaDB, Pydantic, LLM SDKs) consume unpredictable memory and can cause thread starvation. An out-of-memory crash or unhandled model exception in the AI pipeline must not bring down the transactional .NET core API.
- **Compute & Scaling Heterogeneity:** The .NET API is I/O-bound with high throughput and low CPU overhead. The AI orchestrator is latency-bound, token-heavy, and potentially GPU-accelerated.
- **Developer Specialization:** Enables Python AI engineers to iterate on agent logic, prompt evaluation, and guardrails without touching .NET enterprise database contexts or migrations.

---

### Considered Options
1. **Option 1: In-process .NET LLM Integration (Semantic Kernel / LangChain.NET)**
   - *Pros:* Single deployable backend; no inter-service network overhead or service-to-service authentication; shared memory objects.
   - *Cons:* Semantic Kernel and LangChain.NET significantly lag behind Python LangGraph in state graph persistence, interrupt primitives, multi-agent patterns, and vector store connectors; high risk of AI dependencies crashing primary business APIs.
2. **Option 2: Dedicated Python FastAPI Service running LangGraph (Chosen)**
   - *Pros:* Native access to first-class LangGraph features (`StateGraph`, `SqliteSaver`, `interrupt()`, `Command(resume=...)`); clean separation of concerns; independent scaling and containerization.
   - *Cons:* Adds network serialization overhead (~5–15ms per turn); requires service-to-service authentication (`X-Service-Key`); introduces a distributed system with two backends to deploy and monitor.

---

### Decision Outcome
**Chosen Option:** **Option 2 (Dedicated FastAPI Service running LangGraph)**.

We deploy FastAPI as an autonomous AI orchestrator. The .NET API acts as the secure API Gateway and Resource Server. When an authenticated user submits a chat message, .NET validates the JWT, checks daily token quotas, logs the request, and forwards it to FastAPI over an internal container network passing `X-Correlation-Id` and `X-Service-Key`. When the agent requires tool execution (e.g., reserving a book or checking inventory), it calls back into .NET via authenticated endpoints.

#### Consequences
- **Positive:**
  - Full access to Python's rich AI ecosystem, native LangGraph state graphs, dynamic checkpointers, and LangSmith tracing.
  - Zero risk of Python garbage collection pauses or C-extension crashes affecting .NET database transactions.
  - Granular horizontal scaling: we can scale FastAPI agent workers independently of .NET API instances.
- **Negative / Trade-offs:**
  - Additional operational complexity: two distinct Docker containers, separate dependency scanning (`dotnet list package` + `pip-audit`), and inter-service health checking.
  - Network hop adds ~8ms latency per interaction.

---

### Strongest Counter-Argument & Conditions for Reversal
> **Strongest Counter-Argument:**
> Maintaining two distinct backend runtimes (.NET 8 and Python 3.12) imposes double cognitive overhead on engineers, doubles container memory footprints, and introduces inter-service serialization latency and distributed failure modes (e.g., circular startup dependencies). If Semantic Kernel achieves feature parity with LangGraph's cyclical state machines and durable interrupt checkpoints, an all-.NET architecture would drastically simplify DevOps, debugging, and deployment.

> **Evidence That Would Reverse This Decision:**
> 1. Microsoft Semantic Kernel or native .NET agent frameworks provide first-class cyclic graph orchestration with production-grade durable human-in-the-loop interruption identical to LangGraph.
> 2. Operational telemetry reveals inter-service HTTP latency accounts for >25% of total request latency under high concurrency.
> 3. Enterprise hosting constraints mandate a single unified runtime binary.
