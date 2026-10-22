# System Architecture Specification

**Product:** Nexa Solutions AI Library System (Capstone Release v1.0.0)  
**Author:** Senior Systems Architect & Documentation Architect  
**Status:** Approved & Implemented  
**Date:** 2026-10-23  

---

## 1. System Overview

The Nexa Solutions Library System is an enterprise-grade, multi-tier, multi-agent AI web application. It integrates modern reactive frontend architecture, high-performance ASP.NET Core backend services, autonomous Python AI microservices powered by LangGraph, relational PostgreSQL persistence, and semantic vector retrieval with ChromaDB.

---

## 2. Component Topology & Container Mesh

The system is deployed as four decoupled microservices communicating across an isolated Docker bridge network (`library-net`):

```mermaid
graph TB
    subgraph Client Tier ["Client Tier (Browser)"]
        Browser["User Browser / SPA Client"]
    end

    subgraph Docker Mesh ["Docker Compose Network (library-net)"]
        subgraph Web ["web: Nginx Alpine (Port 4200:80)"]
            SPA["Angular 18 SPA Bundles<br/>(Signals, Tailwind, RxJS SSE)"]
        end

        subgraph API ["api: ASP.NET Core 8 Web API (Port 5000:8080)"]
            Kestrel["Kestrel HTTP Engine ($APP_UID non-root)"]
            SecHeaders["Security Headers & HSTS Middleware"]
            AuthMiddle["JWT Auth & Role-Based Authorization"]
            RateLimit["FixedWindow RateLimiter (15 req/min, 5 login/min)"]
            PollyResilience["Polly Exponential Retry & Circuit Breaker"]
            EFCore["EF Core Repository Tier"]
            Seeder["Database Seeder (Admin, Demo, 16 Books)"]
        end

        subgraph AIService ["ai-service: FastAPI Microservice (Port 8000:8000)"]
            FastAPIApp["FastAPI Uvicorn (app non-root UID 1000)"]
            SafeCache["Safe TTLCache (Read-Only Catalog Cache)"]
            RouterNode["Model Router (gemini-1.5-flash)"]
            LangGraphEngine["LangGraph StateGraph Engine"]
            Checkpointer["SqliteSaver (Thread Checkpoint Persistence)"]
            ChromaStore["Chroma Vector Store (/data/chroma)"]
        end

        subgraph RelationalDB ["db: PostgreSQL 16 Alpine (Port 5432:5432)"]
            PostgresEngine["PostgreSQL Database (librarydb_week3)"]
        end
    end

    Browser -->|"HTTP/REST & SSE"| SPA
    SPA -->|"REST API & SSE /agent/run"| Kestrel
    Kestrel --> SecHeaders --> AuthMiddle --> RateLimit
    RateLimit --> EFCore -->|"Npgsql"| PostgresEngine
    RateLimit --> PollyResilience -->|"HTTP /agent/run (X-Service-Key)"| FastAPIApp
    FastAPIApp --> SafeCache
    FastAPIApp --> RouterNode --> LangGraphEngine
    LangGraphEngine --> Checkpointer
    LangGraphEngine --> ChromaStore
    LangGraphEngine -.->|"Tool: check_availability"| Kestrel
```

---

## 3. Trust Boundaries & Security Enclaves

The architecture enforces four distinct trust boundaries to defend against lateral traversal and privilege escalation:

```mermaid
graph LR
    subgraph TB0 ["Trust Boundary 0: Untrusted Public Network"]
        PublicUser["Public Web Browser / User Agent"]
    end

    subgraph TB1 ["Trust Boundary 1: Edge Web Server"]
        NginxGateway["Nginx Alpine Static Host (Port 4200)"]
    end

    subgraph TB2 ["Trust Boundary 2: Authenticated Application Gateway"]
        DotNetAPI[".NET Web API (Port 5000 / 8080)"]
    end

    subgraph TB3 ["Trust Boundary 3: Internal Service Mesh & Storage"]
        FastAPIService["Python AI Microservice (Port 8000)"]
        DatabaseEngine["PostgreSQL Database (Port 5432)"]
        ChromaStorage["Chroma Vector Volume (/data)"]
        SQLiteCheckpoints["SQLite Thread Store (/data)"]
    end

    PublicUser -->|1. HTTPS / WSS| NginxGateway
    PublicUser -->|2. JWT Bearer + Correlation-ID| DotNetAPI
    DotNetAPI -->|3. Database Connection String| DatabaseEngine
    DotNetAPI -->|4. Mutual Secret Header X-Service-Key| FastAPIService
    FastAPIService -->|5. Local Volume Access| ChromaStorage
    FastAPIService -->|6. Local Volume Access| SQLiteCheckpoints
```

### Trust Boundary Rules
1. **Public vs. Edge (TB0 ➔ TB1):** Nginx serves compiled static Angular assets with strict Content Security Policy (`CSP`), anti-clickjacking (`X-Frame-Options: DENY`), and MIME sniffing prevention (`X-Content-Type-Options: nosniff`).
2. **Edge vs. Application Gateway (TB1 ➔ TB2):** Client invokes ASP.NET Core API using short-lived JWT Bearer tokens. Rate limiters defend against brute-force logins and agent flooding.
3. **Gateway vs. AI Service (TB2 ➔ TB3):** Direct external browser access to the Python AI service is prohibited in production. Inter-service HTTP calls require the internal pre-shared `X-Service-Key` header and forward user identity via `X-Forwarded-User-Token`.
4. **Non-Root Execution:** All application containers run as low-privileged users (`$APP_UID` in .NET, `app` UID 1000 in Python, `postgres` UID 70 in DB).

---

## 4. End-to-End Sequence: Human-in-the-Loop (HITL) Approval Run

The following sequence details an agent invocation executing a state-changing write (book reservation), illustrating the human approval card workflow and interrupted turn resumption:

```mermaid
sequenceDiagram
    autonumber
    actor User as User (Angular Client)
    participant UI as Angular Web SPA
    participant API as ASP.NET Core API
    participant AI as FastAPI (LangGraph Engine)
    participant DB as PostgreSQL DB

    User->>UI: Types "Please reserve Dune (Book 4) for me"
    UI->>API: POST /api/agent/run (JWT Token, Correlation-ID)
    API->>API: Validate Rate Limits & Deduct Token Budget
    API->>AI: POST /agent/run (X-Service-Key, X-Forwarded-User-Token)
    AI->>AI: Router Node classifies intent: Action Trajectory
    AI->>AI: Tool Node proposes `reserve_book(book_id=4)`
    AI->>AI: Interrupted! LangGraph halts at `approval_node`
    AI->>API: SSE Event: `approval_required` {threadId, book_id: 4, action: "reserve"}
    API->>UI: SSE Forward: `approval_required`
    UI-->>User: Displays Interactive HITL Approval Card (Book 4, Confirm / Cancel)

    alt User Approves Reservation
        User->>UI: Clicks "Approve Reservation"
        UI->>API: POST /api/agent/resume {threadId, approved: true}
        API->>AI: POST /agent/runs/{thread_id}/resume {approved: true}
        AI->>AI: Resume Command unlocks graph execution
        AI->>API: HTTP POST /api/books/4/reserve (Forwarded User JWT)
        API->>DB: INSERT INTO Reservations (BookId, UserId, IdempotencyKey)
        DB-->>API: 201 Created (Reservation #892)
        API-->>AI: 200 OK {status: "confirmed", reservationId: 892}
        AI->>API: SSE Event: `final` "Dune has been successfully reserved! Reference #892."
        API->>UI: SSE Forward: `final`
        UI-->>User: Displays Success Banner & Reservation Details
    else User Rejects Reservation
        User->>UI: Clicks "Cancel / Reject"
        UI->>API: POST /api/agent/resume {threadId, approved: false}
        API->>AI: POST /agent/runs/{thread_id}/resume {approved: false}
        AI->>AI: Graph handles rejection branch gracefully
        AI->>API: SSE Event: `final` "Reservation cancelled. No changes were made."
        API->>UI: SSE Forward: `final`
        UI-->>User: Displays Cancellation Notice
    end
```

---

## 5. Architectural Decision Records (ADRs)

Key architectural trade-offs are documented in formal ADRs:
- **[ADR-001: Separate FastAPI Microservice vs. In-Process Python](adr/ADR-001-separate-fastapi-service.md)** — Isolation of AI dependencies, independent scaling, and fault tolerance.
- **[ADR-002: SQLite Checkpointer vs. Shared PostgreSQL](adr/ADR-002-sqlite-checkpointer-vs-postgres.md)** — Thread state isolation and rapid schema-less turn resumption.
- **[ADR-003: Chroma Vector Store & Read-Only Catalog Caching](adr/ADR-003-chroma-vector-store-and-hitl-writes.md)** — Content-hash incremental indexing and zero-token safe caching.
- **[ADR-004: Breaking Circular Startup Dependencies in Compose](adr/ADR-004-breaking-circular-dependency.md)** — Decoupling container liveness from runtime tool dependencies.
