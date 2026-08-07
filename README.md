# SULUH ECOSYSTEM

> **Sovereign, PDPA-compliant AI infrastructure for Southeast Asia's research communities.**
> *Private — not for public distribution. Research artefacts and consortium use only.*

---

## The one-line summary

SULUH is **one ecosystem, three packages, one academic programme** — a sovereign, provenance-tracked, multi-LLM-deliberated, IRB-aware AI platform for Malaysian (and SEA) higher education research.

---

## The three packages

| Package | Codename | Role | Status |
|---|---|---|---|
| **`israg`** | IsRAG — *Isnad-chain RAG* | Provenance + trust + cultural context for every retrieved knowledge unit | v0.1 alpha, working |
| **`council`** | Dewan Council | Multi-LLM deliberation with 3-stage review and isnad-anchored consensus | v0.1 alpha, working |
| **`suluh`** | SULUH AI / SULUH Swarm | Multi-agent swarm orchestration platform: gateway, router, LangGraph workflows, Vue 3 Workbench | v0.1 planned, target Phase 0 end |

```
┌────────────────────────────────────────────────────────────────────────┐
│                       SULUH ECOSYSTEM v0.1                            │
│                                                                        │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  packages/suluh/   — Multi-agent platform & gateway            │  │
│  │  (Tier 1-3: User, Application, Orchestration)                   │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  │  │
│  │  │  Vue 3 Bench   │  │  FastAPI GW    │  │  LangGraph      │  │  │
│  │  │  Jupyter ext   │→ │  JWT · RBAC    │→ │  Swarm Coord.   │  │  │
│  │  │  Admin Console │  │  Audit · SSE   │  │  Query Router   │  │  │
│  │  └────────────────┘  └────────────────┘  └────────┬────────┘  │  │
│  └──────────────────────────────────────────────────│────────────┘  │
│                                                      │               │
│                          composes                    ▼               │
│  ┌────────────────────────────┐    ┌────────────────────────────┐    │
│  │  packages/israg/           │    │  packages/council/         │    │
│  │  Provenance + Trust        │◄──►│  Multi-LLM Deliberation    │    │
│  │  + Cultural Context        │    │  (7 members, 3 stages)     │    │
│  │                            │    │                            │    │
│  │  KnowledgeEntry            │    │  Stage 1: First opinions   │    │
│  │  ProvenanceChain           │    │  Stage 2: Cross-review     │    │
│  │  VerificationRecord        │    │  Stage 3: Chairman synth.  │    │
│  │  TrustEngine (5 factors)   │    │  + full Isnad output       │    │
│  │  CulturalContext (13 fw)   │    │                            │    │
│  │  IsnadChain                │    │  OpenRouter single API     │    │
│  └────────────────────────────┘    └────────────────────────────┘    │
│                                                                        │
│  Tier 4 (data): pgvector · MinIO · LangFuse · Redis · Debezium CDC     │
│  Hardware: EXO 5-node 1,280 GB cluster (DGX Spark + Mac Studio)        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Why this is one ecosystem, not three products

The three packages exist as separate Python packages with their own pyproject.toml, but they are **conceptually inseparable**:

- **IsRAG** defines *what every retrieved fact looks like* — it has the data model (KnowledgeEntry, ProvenanceChain, TrustEngine, CulturalContext, IsnadChain)
- **Council** defines *how multiple LLMs combine their views* — it consumes IsRAG entries to ground deliberation in verifiable knowledge
- **SULUH** defines *how agents coordinate and execute* — it uses IsRAG for retrieval-with-provenance and Council for complex multi-perspective answers

**Each one without the others is incomplete:**
- IsRAG alone = great provenance, no multi-LLM synthesis
- Council alone = great deliberation, no trust-weighted knowledge grounding
- SULUH alone = orchestration without provenance or consensus primitives

**Together they form a single research contribution**: a sovereign, auditable, deliberation-grounded multi-agent platform with cultural and epistemological awareness built in by default.

---

## The academic contribution (1 proposal + 3 papers)

This ecosystem is designed to produce **one consolidated research programme** with three paper-level contributions. The submission package in `research/` contains:

### `research/proposal/`
- **`SULUH-ECOSYSTEM-PROPOSAL.md`** — the unified programme proposal suitable for MOHE/FRGS, UPSI DVC R&I, and consortium partners. Covers the whole ecosystem as one funded programme.

### `research/papers/`
- **`paper-1-israg.md`** — *IsRAG: Provenance-Chain Retrieval Augmented Generation for Trustworthy AI Systems.* Target venues: ACL, EMNLP, FAccT, JCDL (digital libraries). Contributions: the IsRAG data model, TrustEngine, cultural-framework integration, empirical comparison to standard RAG.
- **`paper-2-council.md`** — *Multi-LLM Deliberation with Provenance Chains for Research Synthesis.* Target venues: AAMAS, NeurIPS (workshop), ACL (workshop), HCI journals. Contributions: 3-stage deliberation protocol, consensus metrics, evaluation against single-LLM and human baselines.
- **`paper-3-suluh.md`** — *Sovereign Multi-Agent AI Platforms: A Reference Architecture for PDPA/IRB-Compliant Research in Higher Education.* Target venues: FAccT, AIES, IEEE Security & Privacy. Contributions: the 4-tier architecture, PDPA/IRB enforcement by design, consortium federation design, lessons from the 12-month UPSI pilot.

The three papers share an author list, share the same evaluation infrastructure (golden sets, benchmarks, instrumentation), and reference each other.

---

## Repository layout

```
suluh-ecosystem/                          ← private monorepo
├── README.md                             ← you are here
├── LICENSE                               ← Apache 2.0 (or institutional; TBD)
├── pyproject.toml                        ← workspace root
│
├── packages/
│   ├── israg/                            ← Package 1: provenance-aware RAG
│   │   ├── pyproject.toml
│   │   ├── README.md
│   │   ├── src/israg/
│   │   │   ├── __init__.py
│   │   │   └── israg_engine.py
│   │   ├── tests/
│   │   └── examples/
│   │
│   ├── council/                          ← Package 2: multi-LLM deliberation
│   │   ├── pyproject.toml
│   │   ├── README.md
│   │   ├── src/council/
│   │   │   ├── __init__.py
│   │   │   └── council_engine.py
│   │   └── examples/
│   │
│   └── suluh/                            ← Package 3: orchestration platform
│       ├── pyproject.toml
│       ├── README.md
│       ├── src/suluh/
│       │   ├── gateway/                  ← FastAPI: JWT, RBAC, audit, SSE
│       │   ├── router/                   ← Query classifier + complexity scorer
│       │   ├── swarm/                    ← LangGraph Swarm Coordinator
│       │   ├── rag/                      ← Hybrid RAG (vector + SQL)
│       │   ├── docling/                  ← Document intelligence
│       │   ├── pdpa/                     ← PDPA masking layer
│       │   ├── irb/                      ← IRB ethics gate
│       │   └── registry/                 ← Agent registry
│       ├── frontend/                     ← Vue 3 AI Workbench
│       └── ops/                          ← Docker compose, deployment
│
├── docs/
│   ├── ARCHITECTURE.md                   ← ecosystem-level architecture
│   ├── PRINCIPLES.md                     ← the 7 immutable design principles
│   ├── COMPLIANCE.md                     ← PDPA + IRB enforcement model
│   ├── SULUH-PRD-ANALYSIS.md             ← analysis of the source UPSI PRD
│   └── SULUH-README-ORIGINAL.md          ← original SULUH standalone README
│
├── research/
│   ├── proposal/
│   │   └── SULUH-ECOSYSTEM-PROPOSAL.md   ← unified programme proposal
│   ├── papers/
│   │   ├── paper-1-israg.md
│   │   ├── paper-2-council.md
│   │   └── paper-3-suluh.md
│   └── golden-sets/
│       └── README.md                     ← golden set authoring pipeline
│
├── benchmarks/
│   └── README.md                         ← Phase 0 model + latency benchmarks
│
└── ops/
    └── README.md                         ← deployment, infra, CI
```

---

## Quick start (developer)

```bash
# All three packages install in editable mode from the workspace root
cd suluh-ecosystem
pip install -e "packages/israg[dev]"
pip install -e "packages/council[dev]"
pip install -e "packages/suluh[dev]"

# Run IsRAG engine
python -c "from israg import IsRAGEngine, SourceType; e = IsRAGEngine(); \
  e.ingest(content='ASEAN has 670M people', author='UN', source_type=SourceType.GOVERNMENT); \
  print(e.retrieve('ASEAN population'))"

# Run Dewan Council
python -c "from council import DewanCouncil; c = DewanCouncil(api_key='sk-or-...'); \
  print(c.deliberate('What is the best AI strategy for ASEAN?'))"

# Run SULUH gateway (Phase 0 target)
cd packages/suluh && uvicorn suluh.gateway.main:app --reload
```

---

## Project governance

- **Lead Architect / Principal Investigator:** Putra Nasution
- **Academic oversight:** Dr. Suzani binti Mohamad Samuri (UPSI, Faculty of Meta)
- **License:** TBD with consortium partners (likely Apache 2.0 with institutional-use carve-outs)
- **Distribution:** Private. This repository is not for public release. It exists to support the academic programme, the UPSI pilot, and the SEA consortium expansion.

---

## Relationship to other projects

```
~/Documents/PROJECTS/
├── suluh-ecosystem/      ← THIS REPOSITORY (consolidated, private)
├── krag/                 ← legacy: superseded by packages/israg/
├── dewan-council/        ← legacy: superseded by packages/council/
├── suluh-ai/             ← legacy: superseded by packages/suluh/
└── INTELIGENSIA-English/ ← book; the SULUH ecosystem is referenced as Chapter 12
```

The legacy directories are kept for archaeology. Active development happens in `suluh-ecosystem/`.

---

*SULUH = suluh (سولوه) = torch, beacon, light that guides. A swarm of such lights, working in concert.*
