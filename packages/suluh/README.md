# SULUH AI — Multi-Agent Orchestration Platform

> *Suluh = torch. A swarm of torches, working in concert, lighting the path for sovereign research.*

**Package:** `suluh` (in the SULUH Ecosystem monorepo)
**Status:** v0.1 — **planned**, target Phase 0 end of programme
**Paper:** See [`../../research/papers/paper-3-suluh.md`](../../research/papers/paper-3-suluh.md) for the full academic contribution.

---

## What this is

SULUH AI is the **orchestration platform** that brings IsRAG and Dewan Council together into a complete, sovereign, multi-agent AI platform for higher education research. It is the package that an institution actually installs to deploy the ecosystem.

The platform implements the four-tier architecture from the [ecosystem architecture doc](../../docs/ARCHITECTURE.md) and enforces the seven immutable design principles from [`../../docs/PRINCIPLES.md`](../../docs/PRINCIPLES.md).

---

## What's in this package

```
packages/suluh/
├── src/suluh/
│   ├── gateway/      ← FastAPI: JWT, RBAC, rate, audit, SSE, OpenAPI
│   ├── router/       ← Query classifier: PDPA class + IRB flag + complexity
│   ├── swarm/        ← LangGraph Swarm Coordinator (3 workflows)
│   ├── rag/          ← Hybrid RAG (vector arm + SQL arm)
│   ├── docling/      ← Document intelligence (OCR, tables, figures)
│   ├── pdpa/         ← PDPA masking layer (4-level classification)
│   ├── irb/          ← IRB ethics gate (5-question pre-screen)
│   └── registry/     ← Agent registry (capability catalogue)
├── frontend/         ← Vue 3 AI Workbench (single-page app)
└── ops/              ← Docker compose, deployment, CI
```

---

## The 4-tier architecture (one-liner)

```
User Layer (Vue 3) → Application Layer (FastAPI) → Orchestration Layer (Swarm + Router + RAG + Council) → Data Layer (pgvector + MinIO + LangFuse + Redis)
```

The full architectural specification is in [`../../docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md).

---

## The 7 immutable design principles

1. **Sovereign by default** — data, state, model weights stay inside the institution
2. **Read-only by design** — agents cannot write to production systems
3. **Hybrid retrieval** — vector + SQL + deterministic rules
4. **Document intelligence is mandatory** — Docling from day one
5. **Auditability over novelty** — every action attributable
6. **Evaluation-driven deployment** — golden set gates every change
7. **Model-agnostic architecture** — swap models, not the orchestrator

The full operationalisation of each principle is in [`../../docs/PRINCIPLES.md`](../../docs/PRINCIPLES.md).

---

## The dual-gate model

Every query passes through two gates before routing:

1. **PDPA gate** — classifies data (PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED); RESTRICTED never leaves the intranet
2. **IRB gate** — detects human-subject research; flagged workflows require matched protocol

Both fail-closed. Both are deterministic at the decision layer. Both are in code, not configuration.

The full compliance model is in [`../../docs/COMPLIANCE.md`](../../docs/COMPLIANCE.md).

---

## Quick start (target, Phase 0)

```bash
# All-in-one via Docker compose
cd packages/suluh/ops
docker compose up -d

# Or run gateway in dev mode
cd packages/suluh
uvicorn suluh.gateway.main:app --reload

# Frontend
cd packages/suluh/frontend
npm install && npm run dev
```

Open `http://localhost:5173` (workbench) and `http://localhost:8000/docs` (API).

---

## Hardware targets

| Phase | Hardware | Purpose |
|---|---|---|
| **Phase 0 (this phase)** | 1× Mac Studio M3 Ultra (256 GB) or 1× DGX Spark (128 GB) | Development, validation, golden set authoring |
| **Phase 1** | Same + PostgreSQL AI read replica | Staging, IRB committee review, pilot users |
| **Phase 2** | 2× Mac Studio + 2× DGX Spark | 768 GB pooled, full swarm load |
| **Phase 3 (target)** | 3× DGX Spark + 2× Mac Studio via EXO | 1,280 GB pooled, edge + core split, consortium-ready |

EXO config files: `ops/exo/`

---

## License

Apache 2.0.

## Part of the SULUH Ecosystem

SULUH AI is the third package in the [SULUH Ecosystem](../../README.md):

- **`israg`** — provenance-aware retrieval
- **`council`** — multi-LLM deliberation
- **`suluh`** — multi-agent orchestration platform (this package)

See the [ecosystem README](../../README.md), the [architecture doc](../../docs/ARCHITECTURE.md), the [compliance model](../../docs/COMPLIANCE.md), and the [research proposal](../../research/proposal/SULUH-ECOSYSTEM-PROPOSAL.md).
