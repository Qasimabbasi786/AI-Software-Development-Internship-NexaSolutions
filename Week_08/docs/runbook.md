# Production Operations Runbook

**System:** Nexa Solutions AI Library Management System  
**Audience:** SRE, DevOps, Platform Engineers, On-Call Support  
**Version:** 1.0.0 (Production)  
**Last Updated:** 2026-10-23  

---

## 1. Quick Operations Reference

### 1.1 Starting and Stopping the Cluster
```bash
# Navigate to Week 8 deployment directory
cd Week_08

# Start all containers in the background with build validation
docker compose up --build -d

# Check live container health status
docker compose ps

# Graceful shutdown (preserves persistent volumes)
docker compose down

# Full cluster teardown including volumes (DESTRUCTIVE: resets database & checkpoints)
docker compose down -v
```

### 1.2 Health Check & Diagnostic Endpoints
| Component | Endpoint URL | Expected Status | Purpose |
| :--- | :--- | :--- | :--- |
| **.NET API (Live)** | `http://localhost:5000/health/live` | HTTP 200 OK | Confirms Kestrel process is listening (Liveness probe) |
| **.NET API (Ready)** | `http://localhost:5000/health/ready` | HTTP 200 OK | Validates PostgreSQL and AI service reachability (Readiness probe) |
| **AI Service (Health)**| `http://localhost:8000/health` | HTTP 200 OK | Reports Chroma vector collection status and indexed document count |
| **Angular Web App** | `http://localhost:4200/` | HTTP 200 OK | Verifies Nginx Alpine is serving static SPA bundles |

---

## 2. Container Log Locations & Triage

All containers stream structured JSON or human-readable logs to `stdout`/`stderr`.

### Viewing Live Aggregated Logs
```bash
# Stream logs across all services with timestamps
docker compose logs -f --tail=100

# Inspect specific service logs
docker compose logs -f api
docker compose logs -f ai-service
docker compose logs -f db
docker compose logs -f web
```

### Filtering Logs by Correlation ID
All logs in the .NET API and FastAPI microservice include the `correlation_id` property:
```bash
# Linux / macOS / WSL
docker compose logs api | grep "cid_4a8b79e1"

# Windows PowerShell
docker compose logs api | Select-String "cid_4a8b79e1"
```

---

## 3. Common Failures, Diagnostics & Triage Playbook

### Incident 1: API Container Fails to Start (`CrashLoopBackOff`)
- **Symptoms:** `docker compose ps` shows `library-api` in an unhealthy or restarting state.
- **Root Cause:** PostgreSQL database container is still initializing or port conflict exists on host port `5000`.
- **Triage Steps:**
  1. Inspect API logs: `docker compose logs api --tail=50`.
  2. Verify PostgreSQL is healthy: `docker compose ps db` (must report `healthy`).
  3. If database credentials changed, verify `POSTGRES_PASSWORD` in `.env` matches `db` configuration.
  4. Test database socket directly:
     ```bash
     docker exec -it library-db pg_isready -U postgres -d librarydb_week3
     ```

### Incident 2: AI Service Reports HTTP 503 or Degraded Health
- **Symptoms:** `/health/ready` on API returns `Unhealthy`; agent runs fail with timeout.
- **Root Cause:** Invalid or exhausted LLM API key, or corrupted Chroma vector store volume.
- **Triage Steps:**
  1. Query AI service diagnostics directly: `curl http://localhost:8000/health`.
  2. If `vector_store_reachable` is false, check filesystem permissions on `/data`:
     ```bash
     docker exec -it library-ai-service ls -ld /data/chroma
     ```
  3. Validate LLM API keys in `.env` (`GEMINI_API_KEY`, `OPENAI_API_KEY`). Ensure no trailing whitespaces or expired quotas.

### Incident 3: 404 Not Found on Angular Route Refresh
- **Symptoms:** Navigating to `/catalog` works when clicking links, but hitting browser refresh triggers Nginx 404.
- **Root Cause:** Nginx configuration missing SPA fallback directive `try_files $uri $uri/ /index.html;`.
- **Fix:** Check `frontend/nginx.conf` in the web container:
  ```bash
  docker exec -it library-web cat /etc/nginx/conf.d/default.conf
  ```

---

## 4. Key & Secret Rotation Procedure

When credentials (JWT signing key, service-to-service key, or database password) are compromised:

### 4.1 Rotating JWT Signing Key
1. Generate a new high-entropy 256-bit secret string (at least 32 characters).
2. Update `JWT_KEY` in `Week_08/.env`.
3. Restart the API container:
   ```bash
   docker compose up -d --no-deps api
   ```
4. Note: Existing user sessions will be invalidated, requiring users to log in again.

### 4.2 Rotating Inter-Service Key (`SERVICE_KEY`)
1. Generate a new secret key string.
2. Update `SERVICE_KEY` in `Week_08/.env`.
3. Simultaneously restart both the API and AI service containers:
   ```bash
   docker compose up -d --no-deps api ai-service
   ```

---

## 5. Maintenance Procedures: Vector Index Rebuilding

When catalog data is heavily updated or the Chroma collection becomes desynchronized:

### Rebuilding Chroma Vector Index
1. Exec into the AI service container:
   ```bash
   docker exec -it library-ai-service /bin/bash
   ```
2. Trigger the incremental vector sync script:
   ```bash
   python -c "from index_sync import sync_catalog_embeddings; print('Synced:', sync_catalog_embeddings())"
   ```
3. To perform a clean rebuild (purge and recreate):
   ```bash
   rm -rf /data/chroma/*
   python main.py &
   ```
   The application automatically re-chunks and re-embeds the catalog documents on startup.
