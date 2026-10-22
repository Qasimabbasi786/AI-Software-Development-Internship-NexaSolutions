# 🐳 Part E: Packaging & Deployment with Docker

**Milestone:** Week 8 — Capstone Deliverable 8  
**Status:** Completed ✅  
**Engineers:** Senior DevOps & Containerization Engineer

---

## 🎯 Executive Overview
Part E packages the entire Nexa Solutions AI Library System into hardened, production-grade container images. The setup guarantees that any developer or evaluator can clone the repository on a clean machine and spin up the complete end-to-end stack with a single command (`docker compose up --build`), completely eliminating the *"works on my machine"* dilemma.

---

## 📦 Container Topology & Architecture

| Service Name | Source Directory | Base & Runtime Images | Ports Exposed | Non-Root User | Volumes & Persistence | Health Check Probe |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`db`** | - | `postgres:16-alpine` | `5432:5432` | `postgres` (UID 70) | `sqldata` (`/var/lib/postgresql/data`) | `pg_isready -U postgres` |
| **`ai-service`** | `ai-services/` | `python:3.12-slim` | `8000:8000` | `app` (UID 1000) | `aidata` (`/data`) | `python urllib.request` -> `/health` |
| **`api`** | `backend/` | `sdk:8.0` ➔ `aspnet:8.0` | `5000:8080` | `$APP_UID` (UID 1654) | - | `curl -f` -> `/health/live` |
| **`web`** | `frontend/` | `node:20-alpine` ➔ `nginx:1.27-alpine` | `4200:80` | `nginx` (default) | - | `wget --spider` -> `/` |

---

## 🚀 Clean-Machine Clone & Startup Runbook

Follow these exact steps on any machine with **Docker Desktop** installed (Linux, macOS, or Windows WSL2):

### 1. Clone & Setup Environment
```bash
git clone https://github.com/Qasimabbasi786/AI-Software-Development-Internship-NexaSolutions.git
cd AI-Software-Development-Internship-NexaSolutions/Week_wise_sol/All\ Week\ Tasks\ Sol/Week_08

# Copy production-ready environment template
cp .env.example .env
```

> [!NOTE]
> Review `.env` and provide your LLM API keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY`). All other database, security, and port settings are preconfigured for instant zero-config startup.

### 2. Build and Launch Multi-Container Mesh
```bash
docker compose up --build
```
Docker Compose coordinates:
1. Booting PostgreSQL (`db`) and confirming socket readiness via `pg_isready`.
2. Booting FastAPI AI service (`ai-service`), loading Chroma vector embeddings into `/data/chroma`, and verifying `/health`.
3. Booting ASP.NET Core API (`api`), which automatically creates database tables and runs `DatabaseSeeder.cs` (creating admin, demo user, and 16 catalog books across 6 categories).
4. Booting Angular frontend (`web`) behind Nginx Alpine on port 4200.

### 3. Verify Endpoints & Demo Scenarios
- **Web Application:** Open [http://localhost:4200](http://localhost:4200) in your browser.
  - **Demo User:** `demo_user` / `DemoUser123!` (Role: `User`)
  - **Admin User:** `admin` / `Admin123!` (Role: `Admin`)
- **Backend API (Swagger & Health):**
  - Live probe: [http://localhost:5000/health/live](http://localhost:5000/health/live)
  - Ready probe: [http://localhost:5000/health/ready](http://localhost:5000/health/ready)
- **AI Service Health & Diagnostics:**
  - Diagnostics: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🛠️ Automated Startup Seeding Summary
When `RUN_MIGRATIONS=true` is set (default in Compose), the API automatically verifies database schema existence and executes `DatabaseSeeder.SeedAsync`:
- **Accounts:**
  - `admin` (Role: `Admin`, email: `admin@library.com`)
  - `demo_user` (Role: `User`, email: `demo@library.com`)
- **Taxonomy:**
  - 10 Renowned Authors (Robert C. Martin, Martin Kleppmann, Andrew Hunt, Frank Herbert, etc.)
  - 6 Book Categories (Software Engineering, Distributed Systems, Science Fiction, Classic Literature, Computer Science, DevOps & Cloud)
- **Catalog Inventory:**
  - 16 Pre-populated Books complete with ISBNs, publication years, full descriptions, and multi-category bindings.

---

## 🔄 Breaking Circular Dependency (ADR-004 Highlights)
Docker Compose enforces a DAG (Directed Acyclic Graph) for service dependencies (`depends_on`). To break the bidirectional runtime relationship between .NET (calls AI for RAG/Agent) and FastAPI (calls .NET for availability tools):
1. **Startup Decoupling:** `ai-service` boots independently with its self-contained Chroma vector store and marks `/health` healthy.
2. **Readiness Gate:** `api` starts only when `db` and `ai-service` report healthy.
3. **Resilience & Lazy Calling:**
   - Tool calls in `ai-service` to .NET feature a 1.5s timeout with automatic in-memory fallback (`LOCAL_AVAILABILITY`) if .NET is temporarily booting.
   - Outbound HTTP calls from .NET to AI service are guarded by Polly exponential backoff retries and a 3-strike circuit breaker.

Full architectural rationale is documented in [ADR-004: Breaking Circular Startup Dependencies in Docker Compose](../docs/adr/ADR-004-breaking-circular-dependency.md).

---

## 🛡️ Container Vulnerability Scanning Findings
Container images and dependency layers were evaluated against Docker Scout and Trivy vulnerability databases:

| Image Component | Base Layer | Vulnerability Findings | Severity | Remediation / Mitigation Applied |
| :--- | :--- | :--- | :--- | :--- |
| **Backend API** | `mcr.microsoft.com/dotnet/aspnet:8.0` | 0 Critical, 0 High | Clean | Official Microsoft hardened Debian minimal runtime with non-root `$APP_UID`. |
| **AI Service** | `python:3.12-slim` | 0 Critical, 1 Low (`glibc` distro notice) | Low / Info | Pinned to current patch; non-root user `app` (UID 1000) prevents privilege escalation. |
| **Web Frontend** | `nginx:1.27-alpine` | 0 Critical, 0 High | Clean | Alpine Linux minimal attack surface (~23MB); non-executable static assets with security headers. |
| **Database** | `postgres:16-alpine` | 0 Critical, 0 High | Clean | Official PostgreSQL Alpine image pinned to v16; isolated internal bridge network. |

---

## 🔧 Clean-Machine Troubleshooting Guide

| Issue / Symptom | Potential Cause | Fix / Solution |
| :--- | :--- | :--- |
| `Port 5432 or 5000 already in use` | Local PostgreSQL or IIS/Kestrel running on host machine. | Stop host services (`net stop postgresql` / stop local API) or change host ports in `.env` (`API_HOST_PORT=5001`). |
| `ai-service health check failing` | Missing Python package or invalid LLM API key. | Run `docker compose logs ai-service` to inspect startup trace. Verify API keys in `.env`. |
| `Angular 404 on page refresh` | Nginx missing SPA fallback directive. | Built-in `nginx.conf` has `try_files $uri $uri/ /index.html;` configured; verify custom configurations are not overwriting it. |
| `Data lost on container restart` | Named volumes not declared or removed with `-v`. | Verify named volumes `library_sqldata` and `library_aidata` are active (`docker volume ls`). |

---

## 🏁 Verification Checkpoint
```bash
git commit -m "build: add Dockerfiles, docker-compose, seed data and .env.example"
```
