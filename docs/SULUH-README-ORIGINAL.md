# SULUH AI

**Sovereign, PDPA-compliant multi-agent AI orchestration for Malaysia's higher education research community.**

> "Suluh" (سولوه / suluh) = torch, beacon, light that guides. A swarm of such lights, working in concert.

---

## What this is

SULUH AI is the open-source implementation of the **SULUH SWARM PRD v1.0** (UPSI internal, July 2026) — a sovereign, on-premise multi-agent AI platform for academic research. It composes existing open-source primitives into a production-grade system that respects Malaysian PDPA and IRB constraints by architecture.

**The composition:**

| Layer | Implementation |
|---|---|
| Sovereign multi-agent orchestration | **LangGraph v1.0** + custom Swarm Coordinator |
| Document intelligence (OCR, tables, figures) | **IBM Docling** |
| Hybrid retrieval (vector + SQL) | **pgvector / HNSW** + **Text-to-SQL** over PostgreSQL AI read replica |
| Provenance + trust + cultural context | **IsRAG** (sibling project) — see [github.com/putranst/israg](https://github.com/putranst/israg) |
| Multi-LLM deliberation + consensus | **Dewan Council** (sibling project) — 7-LLM council via OpenRouter |
| Observability | **LangFuse** (self-hosted) |
| Edge + on-premise inference | **EXO** (disaggregated inference across heterogeneous hardware) |
| UI workbench | **Vue 3** single-page app |

All software is open-source. RM 0 licensing. No vendor lock-in.

---

## Why this exists

Malaysian universities cannot put research data — participant records, ethics approvals, pre-publication manuscripts — into OpenAI, Anthropic, or Gemini cloud APIs. **PDPA 2010 prohibits it, and IRB will not approve it.** Yet researchers need AI to stay competitive.

SULUH AI gives them AI on their own hardware, under their own jurisdiction, with full audit trails.

---

## The four-tier architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ TIER 1 — USER LAYER                                              │
│   Vue 3 AI Workbench · Jupyter Extension · CLI/SDK · Admin UI  │
└─────────────────────────────────┬───────────────────────────────┘
                                  │ JWT
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ TIER 2 — APPLICATION LAYER (FastAPI AI Gateway)                 │
│   JWT validation · RBAC · Rate limiting · Audit logging · SSE   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ TIER 3 — ORCHESTRATION LAYER                                     │
│   Query Router · Swarm Coordinator · Hybrid RAG · PDPA Masking  │
│                                                                  │
│   (composes IsRAG for provenance + Dewan Council for consensus)  │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ TIER 4 — DATA LAYER                                              │
│   PostgreSQL AI replica (with pgvector/HNSW) · MinIO/NAS ·      │
│   LangFuse telemetry · Redis state cache                         │
└─────────────────────────────────────────────────────────────────┘
```

Optional cloud escalation: anonymised, non-human-subject queries only, <5% of traffic, via Anthropic Claude.

---

## Repository status

**Phase 0 — Validation Sprint** (target: 8 weeks from kickoff)

| # | Task | Status |
|---|---|---|
| 1 | Schema introspection (production PostgreSQL → schema.yaml) | 📋 planned |
| 2 | FastAPI gateway skeleton (JWT, RBAC, audit, OpenAPI) | 📋 planned |
| 3 | LlamaIndex hybrid RAG scaffold (pgvector + SQL) | 📋 planned |
| 4 | Docling ingestion pipeline (OCR + tables + figures) | 📋 planned |
| 5 | Text-to-SQL engine (sqlglot sandbox, allowlist) | 📋 planned |
| 6 | LangFuse tracing across all layers | 📋 planned |
| 7 | Vue 3 AI Workbench (SSE, citations, confidence, swarm composer) | 📋 planned |
| 8 | LangGraph swarm + experiment + IRB workflows | 📋 planned |
| 9 | Golden evaluation set (200 query-answer pairs, bilingual) | 📋 planned |
| 10 | Regression harness (BERTScore, SQL correctness, swarm success) | 📋 planned |

See [`docs/PRD-ANALYSIS.md`](docs/PRD-ANALYSIS.md) for the full line-by-line review of the source PRD.

---

## Running locally (target Phase 0 setup)

```bash
# Requirements
# - macOS 14+ with M-series chip, 64 GB unified memory
#   OR Linux + NVIDIA GPU with 24+ GB VRAM
# - Python 3.11+
# - Node 20+ (for Vue 3 workbench)
# - Docker (for PostgreSQL + LangFuse + MinIO + Redis)

git clone https://github.com/putranst/suluh-ai.git
cd suluh-ai

# Start infrastructure
docker compose up -d

# Install Python deps
pip install -e ".[dev]"

# Run gateway
uvicorn suluh.gateway.main:app --reload

# Run workbench
cd src/frontend && npm install && npm run dev
```

Open `http://localhost:5173` for the workbench, `http://localhost:8000/docs` for the API.

---

## Hardware targets

| Phase | Hardware | Use case |
|---|---|---|
| **Phase 0 (this phase)** | 1× Mac Studio M3 Ultra (256 GB) or 1× DGX Spark (128 GB) | Development, validation, golden set authoring |
| **Phase 1** | Same + replica of production PostgreSQL | Staging, IRB committee review, pilot users |
| **Phase 2** | 2× Mac Studio + 2× DGX Spark | 768 GB pooled, full swarm load |
| **Phase 3 (target)** | 3× DGX Spark + 2× Mac Studio via EXO | 1,280 GB pooled, edge prefill / core decode split, consortium-ready |

EXO config is in [`tools/exo-single-node.yaml`](tools/exo-single-node.yaml) for Phase 0; multi-node config is added in Phase 1.

---

## Project hierarchy

```
~/Documents/PROJECTS/
├── suluh-ai/              ← THIS PROJECT (multi-agent platform, standalone)
├── krag/                  ← Provenance + trust + cultural context
├── dewan-council/         ← Multi-LLM deliberation
├── INTELIGENSIA-English/  ← Book project; Suluh AI is referenced as Chapter 12
└── NASKA OS/              ← PRD lineage; SULUH-SWARM originated there
```

---

## License

Apache 2.0 (permissive, patent grant, attribution). Open-source-first.

## Contact

- **Lead Architect:** Putra Nasution (`poetra@gmail.com`)
- **Academic oversight:** Dr. Suzani binti Mohamad Samuri, Faculty of Meta, UPSI
- **Sister projects:** [IsRAG](https://github.com/putranst/krag) · Dewan Council · INTELIGENSIA

---

*Built for the Malaysian research community. Sovereign by design. Audit-able by default.*
