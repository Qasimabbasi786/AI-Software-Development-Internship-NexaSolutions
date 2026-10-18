# 🐳 Part E: Packaging & Deployment with Docker

**Milestone:** Week 8 — Capstone Deliverable 8  
**Status:** Initialized 📌  

---

## 🎯 Objectives
- Package the entire multi-tier system into optimized, production-grade container images (`sqlserver`, `ai-service`, `api`, `web`).
- Implement multi-stage builds for .NET and Angular to minimize container footprints and attack surfaces.
- Enforce least-privilege security by running container processes as non-root users (`USER app`, `USER $APP_UID`).
- Configure declarative healthchecks and start ordering (`depends_on: condition: service_healthy`) to eliminate startup race conditions.
- Preserve persistent datastores (SQL Server data, Chroma vector database, and LangGraph SQLite checkpoints) via named Docker volumes.
- Provide comprehensive automated startup seeding generating demo users, admin accounts, and 15+ rich catalog books.

---

## 📦 Key Deliverables
1. **Multi-Stage Dockerfiles:**
   - `server/Dockerfile`: Multi-stage .NET 8 SDK build outputting to lightweight ASP.NET runtime image.
   - `ai-service/Dockerfile`: Python 3.12 slim with non-root app user.
   - `client/Dockerfile`: Node.js build stage with Nginx Alpine runtime and SPA fallback routing.
2. **Docker Compose Configuration:** `docker-compose.yml` declaring complete multi-service topology with healthchecks and volume bindings.
3. **Automated Seed Data Script:** Automated database seeder creating demo accounts and catalog inventory.
4. **Clean Machine Runbook:** Step-by-step verification instructions tested from a fresh clone.

---

## 🧪 Verification & Acceptance Criteria
- [ ] Clean clone executes with `docker compose up --build` without manual interventions.
- [ ] Circular dependency between .NET and AI service is broken via healthcheck polling and graceful retries.
- [ ] Angular SPA successfully serves routes on page refresh via Nginx fallback.
- [ ] Data survives container recreation (`docker compose down` followed by `docker compose up`).
