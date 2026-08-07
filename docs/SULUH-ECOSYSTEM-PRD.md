# SULUH Ecosystem — Holistic Product Requirements Document

**Document version:** v1.0  
**Date:** July 2026  
**Author:** Putra Nasution (Lead Architect & Principal Investigator)  
**Status:** Private — for consortium, institutional, and AI-agent reference use  
**Repository:** `~/Documents/PROJECTS/suluh-ecosystem/` (private monorepo)

---

## Executive Summary

The SULUH Ecosystem is a **sovereign, PDPA-compliant multi-agent AI platform for higher education research in Southeast Asia**. It consists of three composable open-source packages:

| Package | Role | Status |
|---|---|---|
| **IsRAG** | Provenance-aware retrieval with trust scoring and cultural context | v0.1 alpha — 18/18 tests passing, working engine |
| **Dewan Council** | Multi-LLM deliberation with 3-stage protocol and auditable dissent | v0.1 alpha — working engine, mock mode available |
| **SULUH AI** | Orchestration platform: gateway, router, LangGraph workflows, PDPA+IRB gates, Vue 3 Workbench | Planned — package skeleton exists, zero implementation |

The three packages form **one academic research programme**: IsRAG defines *what every retrieved fact looks like* (the data model), Council defines *how multiple LLMs deliberate*, and SULUH defines *how agents coordinate and execute*. Each is independently usable; together they form a sovereign, auditable, deliberation-grounded multi-agent platform with cultural and epistemological awareness built in by default.

**Primary deployment target:** 12-month pilot at Universiti Pendidikan Sultan Idris (UPSI), Malaysia — serving ~275 research staff and 2,400+ graduate students.

---

## 1. Project Vision & Context

### 1.1 The Sovereignty Gap

Higher education institutions in Malaysia and Southeast Asia face a regulatory paradox:

- Research data (participant records, ethics approvals, pre-publication manuscripts, indigenous knowledge) **cannot legally be processed by foreign cloud AI services** under PDPA 2010, GDPR, and sectoral rules like HIPAA and IRB.
- Universities **must adopt AI** to remain competitive in research productivity, reproducibility, and funding.
- The current landscape is fragmented: ad-hoc local GPU workstations, foreign cloud tools IRBs cannot approve, and a widening capability gap between well-resourced and under-resourced institutions.

SULUH resolves this paradox by providing a **sovereign, on-premise platform** where all data, model weights, and agent state remain within institutional jurisdiction.

### 1.2 Strategic Positioning

- **First-mover advantage:** First Malaysian university to deploy a sovereign, PDPA-compliant multi-agent AI research platform on a 1,280 GB distributed cluster.
- **National alignment:** Reference implementation for Malaysia National AI Agenda 2026–2030.
- **Regional template:** Consortium expansion model for partner institutions (UTM, UM, NTU, and other ASEAN universities).
- **Academic contribution:** Grounded in a 1,000-year-old epistemology (Islamic Isnad) applied to modern AI — contributes to the global decolonial AI movement.

### 1.3 Key Metrics (12-Month Target)

| Metric | Target |
|---|---|
| Research-domain answer accuracy | 93% |
| Swarm task success rate | 90% |
| PDPA compliance score | 100% |
| IRB gate accuracy | 98% |
| Staff adoption rate | 75% |
| Average response latency | < 2.5s |
| Anthropic cloud escalation share | < 5% |
| Productive hours returned/year | 15,000–35,000 (8–18 FTE equivalent) |

---

## 2. Current State Assessment

### 2.1 What Is Built & Working

#### IsRAG (`packages/israg/`) — v0.1 alpha

**18/18 tests passing** (pytest, 0.03 seconds). Full implementation:

- **Core engine:** `IsRAGEngine` class with `ingest()`, `retrieve()`, `add_verification()`, `get_entry()`, `list_entries()`, `get_stats()`.
- **Data model:** `KnowledgeEntry`, `ProvenanceStep`, `VerificationRecord`, `TrustEngine`, `IsnadChain`, `CulturalContext`, `RetrievalResult`.
- **5-factor trust engine:** Verification level (30%), source credibility (25%), verification quality (20%), cross-references (15%), freshness (10%).
- **13 cultural frameworks:** Global, Western, East Asian, Southeast Asian, South Asian, Indonesian, Malaysian, Thai, Vietnamese, Filipino, Singaporean, Islamic, Buddhist, Indigenous.
- **Isn't yet:** Vector search (currently keyword-based), persistent storage (in-memory dict), embedding pipeline.

#### Dewan Council (`packages/council/`) — v0.1 alpha

Working engine with full protocol:

- **3-stage deliberation:** (1) Independent first opinions → (2) Cross-review matrix → (3) Chairman synthesis with dissent.
- **7-member reference council:** Ketua Claude (Opus 4.7), Anggota GPT (5.5), Gemini (3 Flash), Kimi (K2.6), Deepseek (V4 Flash), Qwen (3.6 Plus), Nemotron (3 Super).
- **Mock mode:** Works without API key for testing the protocol.
- **OpenRouter integration:** Single API for all models.
- **Integration with IsRAG:** Council opinions can be grounded in IsRAG KnowledgeEntry objects.
- **Isn't yet:** Streaming, async deliberation, learned chairman selection.

#### Documentation

- `README.md` — ecosystem-level overview
- `docs/ARCHITECTURE.md` — 4-tier architecture with composability model (~20 KB)
- `docs/PRINCIPLES.md` — 7 immutable design principles, operationalised in code
- `docs/COMPLIANCE.md` — PDPA + IRB dual-gate model (~7 KB)
- `docs/SULUH-PRD-ANALYSIS.md` — analysis of the original SULUH SWARM PRD v1.0
- `docs/REBRAND-KRAG-TO-ISRAG.md` — migration note
- `research/proposal/SULUH-ECOSYSTEM-PROPOSAL.md` — unified programme proposal (RM 285K budget)
- `research/papers/paper-1-israg.md` — IsRAG paper draft
- `research/papers/paper-2-council.md` — Dewan Council paper draft
- `research/papers/paper-3-suluh.md` — SULUH AI paper draft

### 2.2 What Is NOT Built

| Component | Status | Priority |
|---|---|---|
| SULUH FastAPI gateway (`suluh/gateway/`) | Zero code | P0 — Phase 0 deliverable |
| Query router (`suluh/router/`) | Zero code | P0 — Phase 0 deliverable |
| LangGraph Swarm Coordinator (`suluh/swarm/`) | Zero code | P1 — Phase 2 |
| Hybrid RAG (`suluh/rag/`) — pgvector + Text-to-SQL | Zero code | P0 — Phase 1 |
| Docling ingestion pipeline (`suluh/docling/`) | Zero code | P1 — Phase 1 |
| PDPA masking layer (`suluh/pdpa/`) | Zero code | P0 — Phase 1 |
| IRB ethics gate (`suluh/irb/`) | Zero code | P0 — Phase 0 |
| Agent registry (`suluh/registry/`) | Zero code | P1 — Phase 1 |
| Vue 3 Workbench UI | Zero code | P1 — Phase 1 |
| Golden evaluation set | Zero entries | P0 — Phase 0 |
| Vector search (replaces keyword matching) | Not implemented | P0 — Phase 1 |
| Persistent storage (replaces in-memory) | Not implemented | P0 — Phase 1 |
| Git history | No `.git` initialised | P0 — immediate |

---

## 3. Architecture Overview

### 3.1 Four-Tier Design

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 1 — USER LAYER                                                     │
│                                                                          │
│   Vue 3 AI Workbench · JupyterLab Extension · REST/SDK · Admin Console  │
│   Receives JWT from institutional SSO; speaks only to T2 (gateway).      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │  HTTPS · JWT
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 2 — APPLICATION LAYER (FastAPI AI Gateway)                         │
│                                                                          │
│   JWT validation · RBAC enforcement · Rate limiting                     │
│   SSE streaming · OpenAPI spec                                          │
│   Agent Registry endpoint                                               │
│   Audit log emitter (PDPA + IRB events)                                 │
│   Forwards to T3 with user context stripped of PII.                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 3 — ORCHESTRATION LAYER                                             │
│                                                                          │
│   Query Router          — PDPA classify → IRB pre-screen → complexity   │
│   Swarm Coordinator     — LangGraph v1.0, 6-step pipeline               │
│   Hybrid RAG            — pgvector HNSW + Text-to-SQL                   │
│   Multi-LLM Deliberation — Council (triggered on SWARM route)           │
│   Document Intelligence — IBM Docling (OCR, tables, figures)            │
│   PDPA Masking Layer    — Fail-closed PII detection                     │
│   IRB Ethics Gate       — Deterministic classifier + protocol matcher   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 4 — DATA LAYER                                                      │
│                                                                          │
│   PostgreSQL AI Replica (read-only) — pgvector/HNSW, audit log (immutable)│
│   MinIO / Internal NAS — Docling-processed artefacts                    │
│   LangFuse — self-hosted LLM observability                              │
│   Redis — agent state, conversation cache                                │
│   Debezium / pg_logical — production → AI replica streaming             │
└─────────────────────────────────────────────────────────────────────────┘

        ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
        OPTIONAL CLOUD QUALITY LAYER
          Anthropic Claude API
          Conditions: anonymised + non-human-subject + confidence < 0.72
          Target share: < 5% of all queries
          Hard-blocked for: RESTRICTED data, human-subject research
        ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
```

### 3.2 Package Composition

```
packages/suluh/ (orchestrator — depends on both leaf packages)
    │
    ├──► packages/israg/     (leaf — no dependency on suluh)
    │       Provides: KnowledgeEntry, TrustEngine, IsnadChain, CulturalContext
    │
    └──► packages/council/   (leaf — no dependency on suluh)
            Provides: CouncilMember, Opinion, Review, DeliberationResult
```

This separation is deliberate. A researcher can `pip install israg` standalone. A developer can `pip install council` standalone. A university IT team installs the whole ecosystem.

### 3.3 Query Routing Decision Tree

```
1. User submits query
      │
      ▼
2. Gateway validates JWT, applies RBAC, emits audit event
      │
      ▼
3. Router classifies:
   ├─ PDPA class: PUBLIC → INTERNAL → CONFIDENTIAL → RESTRICTED
   ├─ IRB indicator: yes / no
   └─ Complexity: LOW / MEDIUM / HIGH
      │
      ▼
4. IRB Gate (if flagged):
   ├─ matched protocol → pass
   ├─ no protocol match → block for human review
   └─ non-human-subject → continue
      │
      ▼
5. PDPA Masking:
   ├─ RESTRICTED → block from cloud, continue locally only
   └─ Other → continue
      │
      ▼
6. Route:
   ├─ FAST (~55%): israg.retrieve(vector) → Qwen 3.6 direct
   ├─ PRIMARY (~30%): israg.retrieve(vector+SQL) → Qwen extended
   ├─ SWARM (~10%): israg + council.deliberate
   └─ ESCALATE (<5%): anonymise → Anthropic → return
      │
      ▼
7. Synthesis + Isnad chain assembly → Response to user
```

### 3.4 Data Model: Cross-Package Types

IsRAG defines the **canonical data structures** that flow through the ecosystem:

```
KnowledgeEntry {
  content: str
  entry_id: str (hash-based)
  author: str
  author_type: str
  source_type: SourceType (8 types)
  verification_level: VerificationLevel (6 levels)
  cultural_context: CulturalContext | None
  trust_score: float (computed)
  provenance: list[ProvenanceStep]
  verifications: list[VerificationRecord]
  tags: list[str]
  created_at: datetime
}

TrustEngine computes 5-factor score:
  verification_level (30%) + source_credibility (25%) +
  verification_quality (20%) + cross_reference (15%) + freshness (10%)

SourceType: RESEARCH · INSTITUTIONAL · GOVERNMENT · ACADEMIC · NEWS ·
            EXPERT · COMMUNITY · AI_GENERATED · FIELD_DATA

VerificationLevel (0–5):
  UNVERIFIED → SELF_REPORTED → PEER_REVIEWED →
  INSTITUTION_VERIFIED → MULTI_SOURCE_CONFIRMED → FIELD_VALIDATED

CulturalFramework (14):
  GLOBAL · WESTERN · EAST_ASIAN · SOUTHEAST_ASIAN · SOUTH_ASIAN ·
  INDONESIAN · MALAYSIAN · THAI · VIETNAMESE · FILIPINO ·
  SINGAPOREAN · ISLAMIC · BUDDHIST · INDIGENOUS
```

Council **consumes** IsRAG types:

```
CouncilMember: name, role (chairman|member), model_id, specialty, trust_weight
Opinion: member, response, confidence, timestamp
Review: reviewer, reviewed, rating (1–10), feedback, issues_found
DeliberationResult: final_answer, isnad_chain, consensus_score, dissenting_views
```

SULUH **wraps** both:

```
QueryRequest: user_id_hash, routing_label, pdpa_classification,
              irb_flagged, query, context
QueryResponse: answer, isnad_chain, deliberation, pdpa_masking_applied,
               irb_gate_decision, confidence, citations, audit_log_entry
```

---

## 4. Package Specifications

### 4.1 IsRAG — Detailed API

**Location:** `packages/israg/src/israg/israg_engine.py` (783 lines)

```python
class IsRAGEngine:
    def __init__(self, storage_path: Optional[str] = None)
    def ingest(content, author, source_type, author_type="person",
               verification_level=UNVERIFIED, cultural_context=None,
               tags=None, metadata=None, entry_id=None) -> KnowledgeEntry
    def retrieve(query, min_trust_score=0.0, cultural_filter=None,
                 source_filter=None, limit=10, include_isnad=False) -> list[RetrievalResult]
    def add_verification(entry_id, verifier, verifier_type, level,
                         rating, feedback="", issues_found=None) -> KnowledgeEntry | None
    def get_entry(entry_id) -> KnowledgeEntry | None
    def list_entries(source_type=None, min_trust=0.0) -> list[KnowledgeEntry]
    def get_stats() -> dict
```

**RetrievalResult:**
```python
@dataclass
class RetrievalResult:
    content: str
    entry_id: str
    relevance_score: float
    trust_score: float
    confidence_level: str  # very_high, high, medium, low, unverified
    isnad_chain: IsnadChain | None
    source_type: SourceType
    cultural_context: CulturalContext | None

    def format_for_display(show_isnad=False) -> str
    def to_dict() -> dict
```

**Current limitations to address in Phase 1:**
- `_calculate_relevance()` uses naive keyword matching — replace with vector similarity (bge-m3 embeddings + pgvector HNSW)
- `knowledge_base` is an in-memory dict — replace with persistent store (PostgreSQL + pgvector)
- No embedding model integration yet — need `sentence-transformers` or `bge-m3` via HuggingFace

### 4.2 Dewan Council — Detailed API

**Location:** `packages/council/src/council/council_engine.py` (775 lines)

```python
class DewanCouncil:
    def __init__(self, api_key=None, members=None, provider="openrouter",
                 verbose=False)
    def deliberate(query, skip_reviews=False, max_reviewers=3) -> DeliberationResult

    # Internal stages
    def _stage1_get_opinions(query) -> list[Opinion]
    def _stage2_cross_review(query, opinions, max_reviewers) -> list[Review]
    def _stage3_synthesize(query, opinions, reviews) -> dict
    def _call_llm(member, prompt) -> str

# Mock mode: set no API key and council auto-generates plausible mock responses
# for testing the deliberation protocol without burning tokens.
```

**Reference Council (7 members, OpenRouter model IDs):**

| Role | Name | Model | Specialty |
|---|---|---|---|
| Chairman | Ketua Claude | `anthropic/claude-opus-4.7` | Synthesis, judgment |
| Member | Anggota GPT | `openai/gpt-5.5` | Deep reasoning |
| Member | Anggota Gemini | `google/gemini-3-flash-preview` | Data, multimodal |
| Member | Anggota Kimi | `moonshotai/kimi-k2.6` | Long context, multi-agent |
| Member | Anggota Deepseek | `deepseek/deepseek-v4-flash` | Chain-of-thought |
| Member | Anggota Qwen | `qwen/qwen3.6-plus` | Multilingual, Asia |
| Member | Anggota Nemotron | `nvidia/nemotron-3-super` | Open model, free tier |

**Current limitations to address:**
- Mock mode is helpful but should be extended with structured test data
- No streaming support — all deliberation is synchronous
- Chairman selection is hardcoded (first member with role="chairman")
- No learned chairman selection or dynamic council composition

### 4.3 SULUH AI — Planned Components

**Location:** `packages/suluh/` (skeleton only)

| Component | Path | Function | Phase |
|---|---|---|---|
| Gateway | `suluh/gateway/` | FastAPI, JWT, RBAC, audit, SSE | Phase 0 |
| Router | `suluh/router/` | Query classifier, complexity scorer | Phase 0 |
| IRB Gate | `suluh/irb/` | Deterministic ethics classifier | Phase 0 |
| Hybrid RAG | `suluh/rag/` | pgvector + Text-to-SQL | Phase 1 |
| PDPA Masking | `suluh/pdpa/` | PII detection, fail-closed | Phase 1 |
| Docling | `suluh/docling/` | Document intelligence pipeline | Phase 1 |
| Swarm | `suluh/swarm/` | LangGraph coordinator | Phase 2 |
| Registry | `suluh/registry/` | Agent catalogue | Phase 1 |
| Frontend | `frontend/` | Vue 3 Workbench | Phase 1 |

**Gateway API contract (planned):**

```
GET  /health
POST /query          — main query endpoint
GET  /sessions       — list user sessions
GET  /sessions/{id}  — get session with full audit trail
POST /sessions/{id}/stop — stop running session
GET  /models         — list available models
GET  /agents         — list registered agents
GET  /audit          — query audit log (admin)
```

**Router contract (planned):**

```python
class QueryRouter:
    def classify(query: str, user_context: UserContext) -> RouteDecision:
        """
        Returns:
            RouteDecision {
                pdpa_class: PDPAClass (PUBLIC|INTERNAL|CONFIDENTIAL|RESTRICTED)
                irb_flagged: bool
                complexity: ComplexityClass (LOW|MEDIUM|HIGH)
                route: Route (FAST|PRIMARY|SWARM|ESCALATE)
                confidence_threshold: float
            }
        """
```

**Swarm Coordinator — 6-step LangGraph pipeline (planned):**

```
1. query_analyzer    — understand intent, scope, domain
2. discovery         — identify relevant agents, tools, sources
3. decompose         — break into subtasks, assign to agents
4. execute           — run agent tasks in parallel subgraphs
5. consensus         — aggregate results, resolve conflicts
6. irb_gate          — ethics check before returning to user
```

---

## 5. Compliance Architecture

### 5.1 PDPA Data Classification

| Level | Examples | Cloud escalation | Retention |
|---|---|---|---|
| PUBLIC | Published papers, anonymised stats, open datasets | Permitted | Indefinite |
| INTERNAL | Research aggregates, non-PII project data | Permitted (anonymised) | 7 years |
| CONFIDENTIAL | Researcher profiles, grant apps, pre-publication manuscripts | Prohibited | 7 years |
| RESTRICTED | Participant IDs, interview transcripts, clinical data, IRB records | Prohibited | 10 years |

**Enforcement points:**
- `suluh.pdpa.classify()` — every document, query, and tool output is classified
- `suluh.pdpa.mask()` — CONFIDENTIAL and RESTRICTED data masked before processing
- RESTRICTED queries never leave the intranet regardless of any other condition
- **Fail-closed:** if the masker errors, the query is blocked, not passed through

### 5.2 IRB Research Ethics Controls

The IRB gate runs on **every query** before routing. It uses a deterministic decision layer — even when the underlying classifier is LLM-based, the decision rule is a Python function.

**Five-question pre-screen:**
1. Human participants involved? (directly or via their data)
2. Identifiable personal information?
3. Sensitive categories (health, religion, ethnicity, political opinion)?
4. Vulnerable populations?
5. Has an IRB protocol been approved for this research type?

Any "yes" on (1), (2), or (3) without an approved protocol → **IRB gate blocks**.

**Five research types for Phase 0 classifier:**
- Survey research (questionnaires, interviews)
- Clinical / medical research (patient data)
- Educational research (student data, classroom observation)
- Indigenous community research (adat, customary knowledge)
- Vulnerable population research (children, elderly, prisoners)

### 5.3 Audit Log (Immutable)

The `ai_audit_log` PostgreSQL table is append-only — UPDATE and DELETE are rejected by trigger. All events retained 7–10 years per PDPA.

Key events: AI query submitted, SQL executed, agent swarm invoked, Anthropic escalation, PDPA PII detection, IRB gate decision, document lifecycle change, routing config change, failed authentication.

### 5.4 Network Perimeter

- The EXO cluster, AI replica, MinIO, Redis, and LangFuse are on the institution's **intranet only**
- Edge DGX Spark nodes are on isolated faculty VLANs with firewall rules
- FastAPI gateway is accessible from campus network and VPN — **never internet-facing**
- Only outbound connection permitted: HTTPS to `api.anthropic.com` from quality router, and only when all conditions met
- All intra-service communication: TLS 1.3

---

## 6. Design Principles (7 Immutable)

These are **constraints, not preferences**. Any proposal that violates them requires a formal Steering Committee design amendment.

1. **Sovereign by default** — all data, state, model weights stay inside Malaysian jurisdiction and institutional network perimeter.
2. **Read-only by design** — agents recommend and synthesise; no write to production systems. Write capability requires Steering Committee approval.
3. **Hybrid retrieval, not pure RAG** — vector search for documents + SQL generation for structured data + deterministic rules for compliance. Pure semantic RAG will produce incorrect research outputs.
4. **Document intelligence is mandatory** — Docling-grade OCR, table extraction, figure extraction from day one, not a Phase 2 enhancement.
5. **Auditability over novelty** — every agent action is explainable, attributable to source agent + model version, and logged to immutable audit trail.
6. **Evaluation-driven deployment** — no model, config, prompt, or workflow change reaches production without passing the golden set regression gate.
7. **Model-agnostic architecture** — swap the inference model by updating one config value. No code changes in the orchestrator or retrieval layers.

Each principle is **operationalised in code** — it is enforced at the application level, not at the configuration level. A misconfigured environment variable cannot bypass a principle.

---

## 7. Development Roadmap

### 7.1 Phase 0: Foundation (Months 1–2)

**Validation sprint.** Answer three questions before committing to full build:

| Task | Priority | Deliverable |
|---|---|---|
| SSO bridge | P0 | UPSI SSO → JWT validated in FastAPI skeleton |
| Schema + FastAPI skeleton | P0 | `schema.yaml` merged, gateway passing health check |
| Bilingual model benchmark | P0 | Qwen vs Gemma vs Nemotron on 50 golden-set entries |
| IRB gate prototype | P0 | Keyword classifier for 5 research types, <500ms latency |
| Golden set v0.1 | P0 | 50 Malay/English research queries with ground truth |
| Git initialisation | P0 | Repository under version control |

**Phase 0 runs on a single developer machine** — a Mac (M-series, 64 GB) or single DGX Spark. The cluster is not required to start. All Tier 1–3 components are stubbed. Single SQLite or local Postgres for Tier 4.

**Exit gate:** SSO validated, schema merged, FastAPI skeleton passing, benchmark report accepted, IRB prototype validated, golden set at 50 entries.

### 7.2 Phase 1: Core Capabilities (Months 3–6)

| Component | Deliverable |
|---|---|
| IsRAG v0.2 | Vector search (bge-m3 + pgvector), persistent storage, embedding pipeline |
| Dewan Council v0.2 | Streaming support, async deliberation |
| Hybrid RAG | pgvector HNSW + Text-to-SQL with 5-stage sqlglot sandbox |
| Text-to-SQL | Table allowlist, statement-type allowlist, row-limit, query timeout |
| Docling pipeline | OCR, table, figure extraction; low-confidence flagging for HITL review |
| PDPA masking | presidio-based PII detection, bilingual Malay/English |
| IRB gate v1 | Fine-tuned classifier on 200 labelled queries |
| Agent Registry | Agent catalogue, capability manifests, signed agent deployment |
| Chat Workbench | Vue 3 UI: chat, file tree, editor, terminal, session history |
| LangFuse | Self-hosted observability, spans at every layer |
| Golden set v0.2 | 200 entries across 5 domains |

**Exit gate:** All Tier 1–3 components on staging, Month 6 metrics: accuracy 80%, adoption 25%, latency < 4s, PDPA 100%.

### 7.3 Phase 2: Agentic Workflows (Months 7–10)

| Component | Deliverable |
|---|---|
| Multi-Agent Swarm | LangGraph v1.0, 6-step pipeline, max 15 steps/workflow |
| Research Experiment Automation | Agentic workflow for designing, running, and reporting experiments |
| IRB Compliance Auditing | Automated IRB workflow audit, 10% random sample review |
| Regression CI | Golden set gates every deployment; PR blocks on failure |
| IRB Audit Dashboard | Admin console showing gate decisions, flagged queries, protocol expiry |
| Golden set v1.0 | 200 entries, expanded to cover consortium domains |

**Exit gate:** 3 workflows live, Month 10 metrics: accuracy 88%, adoption 55%, latency < 3s, Text-to-SQL 85%, swarm success 80%, IRB gate 95%.

### 7.4 Phase 3: Full Production (Months 11–12)

| Activity | Target |
|---|---|
| Production rollout | 75% adoption across research staff and graduate students |
| Admin Console | Monitoring, user management, audit review |
| Consortium API | Federation spec documented and tested |
| Post-go-live monitoring | LangFuse dashboards, weekly IRB audit samples |
| Annual compliance attestation | Signed by IRB Chair, Legal/Compliance lead, Lead Architect |

**Exit gate:** 75% adoption, consortium API tested, all metrics at target: accuracy 93%, swarm success 90%, latency < 2.5s, IRB gate 98%, Anthropic escalation < 5%.

---

## 8. Golden Set & Evaluation Plan

### 8.1 Golden Set Specification

- **50 entries (Phase 0) → 200 entries (Phase 1) → 200+ entries (Phase 2+)**
- **5 domains:** agriculture, Islamic finance, indigenous land rights, public health, digital governance
- **Bilingual:** Malay and English
- **Authored by:** 30+ researchers from consortium institutions
- **Licence:** CC-BY 4.0 with author consent; no PII
- **Format:** JSONL with `query`, `golden_answer`, `domain`, `language`, `difficulty`, `requires_deliberation`, `irb_flagged`

### 8.2 Evaluation Metrics

| Metric | Method | Target |
|---|---|---|
| Answer accuracy | BERTScore vs golden answer | 93% (Month 12) |
| Trust calibration | Pre/post Likert survey (100+ users) | Effect size > 0.5 |
| Cultural appropriateness | Expert review, 3-point ordinal | 90% appropriate |
| Hallucination rate | Claimed citations that don't exist or are misattributed | < 5% |
| Provenance completeness | Does answer include full chain? | 100% |
| Text-to-SQL correctness | Execution match | 92% |
| Swarm task success | LangFuse trace review | 90% |
| PDPA compliance | Audit log review | 100% |
| IRB gate accuracy | IRB officer review | 98% |

### 8.3 Model Benchmark (Phase 0)

| Candidate | Size | Provider | Notes |
|---|---|---|---|
| Qwen 3.6 35B-A3B | 35B (3B active) | Alibaba | Primary candidate, MoE, bilingual |
| Gemma 4-31B | 31B | Google | Strong multilingual |
| Nemotron-3 Super | ? | NVIDIA | Strong tool-calling, open model |

Benchmark on 50 golden set entries, measuring BERTScore, latency, and token efficiency. Winner becomes the primary model; swap paths maintained for all three.

---

## 9. Hardware & Infrastructure

### 9.1 Target Cluster (Phase 1+)

| Node | Hardware | RAM | Role |
|---|---|---|---|
| 3× DGX Spark | NVIDIA Founders Edition | 128 GB each | Edge nodes, data-locality |
| 2× Mac Studio | M3 Ultra | 256 GB each | Core inference nodes |
| **Total** | **5 nodes** | **1,280 GB pooled** | |

- **Interconnect:** ConnectX-7 200GbE fabric
- **Disaggregation:** EXO — edge prefill, core decode split
- **All on-premise:** No cloud inference for primary models

### 9.2 Phase 0 Dev Environment

- Single Mac (M-series, 64 GB+) or single DGX Spark
- EXO configured for single-node inference
- SQLite or local Postgres for Tier 4
- LangFuse on `localhost:3000`
- Vue 3 Workbench via `npm run dev`

### 9.3 Software Stack

All open-source. RM 0 licensing:

| Layer | Technology |
|---|---|
| Models | Qwen 3.6, Nemotron-3 Super, Gemma 4, bge-m3 |
| Orchestration | LangGraph v1.0 |
| Gateway | FastAPI (Python) |
| Frontend | Vue 3 + Tailwind |
| Vector DB | pgvector (HNSW index) |
| Document | IBM Docling |
| Observability | LangFuse (self-hosted) |
| Cache/State | Redis |
| Disaggregation | EXO |
| CDC | Debezium / pg_logical |
| Object Store | MinIO |

---

## 10. Team & Resources

| Role | Allocation | Responsibilities |
|---|---|---|
| **Putra Nasution** — Lead Architect & PI | 1.0 FTE · 12 months | Programme design, all architecture and code, paper authorship |
| **Engineering team (remote)** | 0.5 FTE · 12 months | Frontend (Vue 3 Workbench), testing, documentation, LangFuse instrumentation |
| **Dr. Suzani Mohamad Samuri** — Oversight Director / Co-PI | 50% · 12 months | Architecture oversight, IRB gate validation, paper co-authorship, stakeholder engagement |
| **UPSI DBA Team** | 20% Phase 0–1 | PostgreSQL replication, AI read replica provisioning |
| **UPSI Research Community** | 20% Phase 0 | Golden set authorship, query validation, feedback |
| **UPSI IRB / Ethics Committee** | Milestone-based | Ethics workflow review, IRB gate validation |
| **UPSI Legal & Compliance** | Milestone-based | PDPA compliance sign-off, audit engagement |

### Budget: RM 285,000 (~USD 60,000)

| Category | RM |
|---|---|
| Hardware (3× DGX Spark + 2× Mac Studio + networking) | 175,000 |
| Software licensing (open source) | 0 |
| Cloud (Anthropic API, <5% queries) | 5,000 |
| Personnel (0.5 FTE × 12 months) | 60,000 |
| Training & change management | 15,000 |
| Travel & publication | 20,000 |
| Contingency (~3.5%) | 10,000 |

PI effort is in-kind. OpenRouter costs for Dewan Council research are covered by existing research credits.

---

## 11. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| SSO integration complexity | Medium | High | Phase 0 critical path, Week 1; Phase 1 cannot begin until validated |
| Model underperforms on bilingual | Medium | High | Phase 0 benchmark: Qwen vs Gemma vs Nemotron; swap paths maintained |
| Multi-agent consensus produces misleading outputs | Medium | High | Confidence-gated display, IRB gate, regression golden set gates |
| IRB gate adds latency | Medium | Medium | Async pre-screening, fast-path for non-human-subject; <500ms target |
| PI bandwidth split across programmes | High | High | Engineering team absorbs implementation; PI focuses on architecture + papers |
| Hardware procurement delay | Medium | High | Phase 0 runs on a single Mac if cluster slips; 6-week fast-track procurement |
| Academic adoption lower than forecast | Medium | Medium | Early adopter programme, researcher workshops, embedded support |
| Open-source model quality regression | Low | High | Model swap paths maintained; Claude API escalation as safety net |

---

## 12. Repository Structure

```
suluh-ecosystem/                          ← private monorepo
├── README.md                             ← ecosystem-level overview
├── pyproject.toml                        ← workspace root
├── LICENSE                               ← Apache 2.0
│
├── packages/
│   ├── israg/                            ← Package 1: provenance-aware RAG
│   │   ├── pyproject.toml
│   │   ├── README.md
│   │   ├── src/israg/
│   │   │   ├── __init__.py
│   │   │   └── israg_engine.py           ← 783 lines, working
│   │   ├── tests/
│   │   │   ├── test_engine.py            ← 10 tests, all passing
│   │   │   └── test_trust.py             ← 8 tests, all passing
│   │   └── examples/
│   │       ├── basic_usage.py
│   │       ├── trust_verification.py
│   │       ├── cultural_context.py
│   │       └── council_integration.py
│   │
│   ├── council/                          ← Package 2: multi-LLM deliberation
│   │   ├── pyproject.toml
│   │   ├── README.md
│   │   ├── src/council/
│   │   │   ├── __init__.py
│   │   │   └── council_engine.py         ← 775 lines, working
│   │   └── examples/
│   │
│   └── suluh/                            ← Package 3: orchestration platform
│       ├── pyproject.toml
│       ├── README.md
│       └── src/suluh/                    ← skeleton, zero implementation
│           ├── gateway/                  ← FastAPI: JWT, RBAC, audit, SSE
│           ├── router/                   ← Query classifier + complexity scorer
│           ├── swarm/                    ← LangGraph Swarm Coordinator
│           ├── rag/                      ← Hybrid RAG (vector + SQL)
│           ├── docling/                  ← Document intelligence
│           ├── pdpa/                     ← PDPA masking layer
│           ├── irb/                      ← IRB ethics gate
│           └── registry/                 ← Agent registry
│
├── docs/
│   ├── ARCHITECTURE.md                   ← ecosystem-level architecture
│   ├── PRINCIPLES.md                     ← 7 immutable design principles
│   ├── COMPLIANCE.md                     ← PDPA + IRB enforcement model
│   ├── SULUH-PRD-ANALYSIS.md             ← analysis of source PRD
│   ├── SULUH-README-ORIGINAL.md          ← preserved original
│   └── REBRAND-KRAG-TO-ISRAG.md          ← migration note
│
├── research/
│   ├── proposal/
│   │   └── SULUH-ECOSYSTEM-PROPOSAL.md   ← unified programme proposal
│   ├── papers/
│   │   ├── paper-1-israg.md
│   │   ├── paper-2-council.md
│   │   └── paper-3-suluh.md
│   └── golden-sets/                      ← (empty, Phase 0 deliverable)
│
├── benchmarks/                           ← (planned)
└── ops/                                  ← (planned)
```

---

## 13. Developer Quick Start

```bash
cd suluh-ecosystem
pip install -e "packages/israg[dev]"
pip install -e "packages/council[dev]"
pip install -e "packages/suluh[dev]"

# Test IsRAG
python -m pytest packages/israg/tests/ -v

# Run IsRAG engine
python -c "
from israg import IsRAGEngine, SourceType
e = IsRAGEngine()
e.ingest(content='ASEAN has 670M people', author='UN', source_type=SourceType.GOVERNMENT)
print(e.retrieve('ASEAN population'))
"

# Run Dewan Council (mock mode — no API key needed)
python -c "
from council import DewanCouncil
c = DewanCouncil()
result = c.deliberate('What is the best AI strategy for ASEAN higher education?')
print(result.final_answer)
"
```

---

## 14. Open Questions for OpenScience

These are the questions OpenScience should be aware of as it researches the project:

1. **Naming:** Is "SULUH" the final ecosystem name, or should we reserve space for a model-level branding (e.g., SULUH-EDU)?

2. **Training data ("100+ years of UPSI data"):** What is the actual composition? Academic content (theses, journals), institutional admin (PDPA-sensitive), Malay-language education corpus, or all three? The training pipeline, PDPA posture, and licensing all depend on this.

3. **Socratic AI features:** What does "Socratic" mean pedagogically? Dialogue-based guided inquiry, adaptive tutoring (Khanmigo-style), or lesson plan generation? The SFT dataset design and eval methodology change significantly.

4. **Model training strategy:** QLoRA (fast, 95% of full FT quality), continued pretraining (CPT) on UPSI corpus, or full fine-tune? QLoRA is the default recommendation for Phase 0 with escalation to CPT if results don't meet the accuracy bar.

5. **Consortium expansion:** Phase 3 federation design — is it a product line, a consulting offering, or a hosted inference service? Three very different operating models.

6. **Open-source licence:** The codebase is Apache 2.0. The model weights will need a separate licence decision (Apache-style, Llama-style restrictions, or open-weights-not-open-source).

7. **Phase 2+ budget:** The RM 285K covers Phase 0–3 (12 months). Phase 2 expansion (public inference, consortium launch) may need RM 5M — timeline and fundraising vehicle TBD.

---

## 15. Relationship to Other Projects

```
~/Documents/PROJECTS/
├── suluh-ecosystem/      ← THIS REPOSITORY (consolidated, private)
├── krag/                 ← legacy: superseded by packages/israg/
├── dewan-council/        ← legacy: superseded by packages/council/
├── suluh-ai/             ← legacy: superseded by packages/suluh/
└── INTELIGENSIA-English/ ← book; SULUH ecosystem referenced as Chapter 12
```

---

**End of PRD.** This document should be treated as the canonical product specification for the SULUH Ecosystem. The code, the architecture docs, and the papers all defer to this file. Update it when the architecture or scope changes.

---

*Putra Nasution — Lead Architect & Principal Investigator*  
*poetra@gmail.com*  
*July 2026*
