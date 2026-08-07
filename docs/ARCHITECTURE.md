# SULUH ECOSYSTEM — Architecture

> The four-layer, three-package, one-research-programme design.

---

## 1. Layered view (Tier 1–4)

The ecosystem follows the four-tier intranet-first architecture inherited from the SULUH SWARM PRD v1.0 (July 2026), but is now decomposed cleanly across the three packages.

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 1 — USER LAYER                                                     │
│                                                                          │
│   Vue 3 AI Workbench · JupyterLab Extension · REST/SDK · Admin Console  │
│                                                                          │
│   Receives JWT from institutional SSO; speaks only to T2 (gateway).      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │  HTTPS · JWT
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 2 — APPLICATION LAYER (FastAPI AI Gateway)                         │
│                                                                          │
│   packages/suluh/gateway/                                                │
│   ├─ JWT validation · RBAC enforcement · Rate limiting                  │
│   ├─ SSE streaming · OpenAPI spec                                        │
│   ├─ Agent Registry endpoint                                             │
│   └─ Audit log emitter (PDPA + IRB events)                              │
│                                                                          │
│   Forwards to T3 with user context stripped of PII.                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 3 — ORCHESTRATION LAYER                                             │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │  Query Router          — packages/suluh/router/                   │ │
│   │  • PDPA classification (PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED) │ │
│   │  • IRB pre-screen classifier                                     │ │
│   │  • Complexity scorer → routes to FAST/PRIMARY/SWARM/ESCALATE     │ │
│   └──────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │  Swarm Coordinator      — packages/suluh/swarm/                   │ │
│   │  • LangGraph v1.0 state machine                                  │ │
│   │  • 6-step pipeline: query → discovery → decompose → exec →       │ │
│   │    consensus → IRB gate                                          │ │
│   │  • Subgraph composition for nested swarms                        │ │
│   └──────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │  Hybrid RAG             — packages/suluh/rag/ + packages/israg/  │ │
│   │  • Vector arm: pgvector HNSW over document corpus                │ │
│   │  • SQL arm: Text-to-SQL over PostgreSQL AI read replica          │ │
│   │  • Returns IsRAG KnowledgeEntry objects (provenance + trust)     │ │
│   └──────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │  Multi-LLM Deliberation — packages/council/                      │ │
│   │  • Triggered on SWARM route (10% of queries)                     │ │
│   │  • 3 stages: first opinions → cross-review → chairman synthesis │ │
│   │  • Returns DeliberationResult with IsnadChain                    │ │
│   └──────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │  Document Intelligence — packages/suluh/docling/                 │ │
│   │  • IBM Docling for OCR, table extraction, figure captions       │ │
│   │  • Output stored in Tier 4 with document lifecycle state        │ │
│   └──────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │  PDPA Masking Layer    — packages/suluh/pdpa/                    │ │
│   │  • Pre-routing: blocks RESTRICTED from cloud escalation          │ │
│   │  • Per-tool-output: scans every tool response for PII            │ │
│   │  • Fail-closed: query blocked if masker fails                   │ │
│   └──────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │  IRB Ethics Gate       — packages/suluh/irb/                     │ │
│   │  • Deterministic classifier: human-subject indicators → gate     │ │
│   │  • Protocol matcher: cross-refs against approved IRB protocols   │ │
│   │  • <500ms target latency (Phase 0 benchmark)                    │ │
│   └──────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ TIER 4 — DATA LAYER                                                      │
│                                                                          │
│   PostgreSQL AI Replica (read-only) — production logical replication    │
│   ├─ pgvector / HNSW index (IsRAG embeddings)                           │
│   ├─ ai_audit_log (immutable, append-only, 7-10 yr retention)           │
│   └─ irb_protocols, agent_registry, golden_set, schema.yaml             │
│                                                                          │
│   MinIO / Internal NAS — Docling-processed document artefacts           │
│   LangFuse — self-hosted LLM observability                              │
│   Redis — agent state, conversation history, swarm coordination cache    │
│   Debezium / pg_logical — production → AI replica change streaming     │
└─────────────────────────────────────────────────────────────────────────┘

        ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
        OPTIONAL CLOUD QUALITY LAYER
          Anthropic Claude API
          Conditions: anonymised + non-human-subject + confidence < 0.72
          Target share: < 5% of all queries
          Hard-blocked for: RESTRICTED data, human-subject research
        ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
```

---

## 2. Package composition (the "what calls what" view)

```
┌──────────────────────────────────────────────────────────────┐
│                       packages/suluh/                        │
│                                                              │
│  suluh.gateway ──► suluh.router ──► suluh.swarm              │
│       │                  │              │                    │
│       │                  │              ├──► suluh.rag        │
│       │                  │              │      │             │
│       │                  │              │      ▼             │
│       │                  │              │   israg.IsRAGEngine│
│       │                  │              │      │             │
│       │                  │              │      ▼             │
│       │                  │              │   pgvector / SQL  │
│       │                  │              │                    │
│       │                  │              └──► council.DewanCouncil
│       │                  │                      │            │
│       │                  │                      ▼            │
│       │                  │                  OpenRouter      │
│       │                  │                                  │
│       │                  └──► suluh.pdpa (masking)           │
│       │                                                    │
│       │                  ┌──► suluh.irb (ethics gate)       │
│       │                  │                                 │
│       └──► suluh.registry (agent catalogue)                 │
│                                                              │
│  suluh.docling (ingestion pipeline)                          │
└──────────────────────────────────────────────────────────────┘
```

**Key insight:** `israg` and `council` are **leaf packages** — they have no dependency on `suluh`. They can be used standalone. `suluh` is the **composition package** — it depends on both and orchestrates them.

This means:
- A researcher can `pip install israg` and use IsRAG in their own pipeline
- A developer can `pip install council` and run a multi-LLM deliberation without the rest
- A university IT team installs the whole `suluh-ecosystem` to get the sovereign platform

---

## 3. Data model: how the three packages share types

IsRAG defines the **canonical data structures** that flow through the ecosystem:

```
IsRAG data model
├── KnowledgeEntry         (a single piece of ingested knowledge)
│   ├── content: str
│   ├── author: str
│   ├── source_type: SourceType
│   ├── verification_level: VerificationLevel
│   ├── cultural_context: CulturalContext | None
│   ├── trust_score: float       (computed by TrustEngine)
│   └── tags: list[str]
│
├── ProvenanceStep         (one hop in the chain: author → verifier → …)
├── VerificationRecord     (one verifier's rating)
├── TrustEngine            (computes the 5-factor score)
│
└── IsnadChain             (the human-readable provenance trail)
    ├── entries: list[KnowledgeEntry]
    ├── verifications: list[VerificationRecord]
    ├── total_trust: float
    └── format_for_display() → str
```

Council **consumes** IsRAG types:

```
Council data model
├── Opinion                (one member's first-stage answer)
├── Review                 (one member's second-stage review of another)
├── DeliberationResult
│   ├── final_answer: str
│   ├── isnad_chain: list[IsRAG.IsnadChain]   ← cross-package ref
│   ├── stage1_opinions: list[Opinion]
│   ├── stage2_reviews: list[Review]
│   ├── stage3_synthesis: str
│   ├── consensus_score: float
│   └── dissenting_views: list[str]
```

SULUH **wraps** both:

```
SULUH request/response model
├── QueryRequest
│   ├── user_id_hash: str
│   ├── routing_label: Literal["FAST", "PRIMARY", "SWARM", "ESCALATE"]
│   ├── pdpa_classification: PDPAClass
│   ├── irb_flagged: bool
│   ├── query: str
│   └── context: dict | None
│
└── QueryResponse
    ├── answer: str
    ├── isnad_chain: IsRAG.IsnadChain
    ├── deliberation: Council.DeliberationResult | None
    ├── pdpa_masking_applied: bool
    ├── irb_gate_decision: Literal["PASS", "BLOCK", "REVIEW"]
    ├── confidence: float
    ├── citations: list[Citation]
    └── audit_log_entry: str
```

This way, every answer that leaves the ecosystem carries a complete chain — authorship, verification, deliberation history, compliance decisions.

---

## 4. The provenance flow (end to end)

What happens when a researcher types a question:

```
1. User submits query
        │
        ▼
2. Gateway validates JWT, applies RBAC, emits audit event
        │
        ▼
3. Router classifies:
   ├─ PDPA class (PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED)
   ├─ IRB indicator (yes / no)
   └─ Complexity (LOW / MEDIUM / HIGH)
        │
        ▼
4. If IRB flagged → IRB gate (suluh.irb)
   ├─ matched protocol → pass
   ├─ no protocol match → block for human review
   └─ non-human-subject → continue
        │
        ▼
5. PDPA Masking (suluh.pdpa)
   ├─ RESTRICTED → block from cloud, continue locally only
   └─ Other → continue
        │
        ▼
6. Route decision:
   ├─ FAST → israg.retrieve (vector) → Qwen 3.6 35B-A3B direct
   ├─ PRIMARY → israg.retrieve (vector + SQL) → Qwen 3.6 extended
   ├─ SWARM → israg.retrieve + council.deliberate
   └─ ESCALATE → anonymise, send to Anthropic, return
        │
        ▼
7. Synthesis & IsRAG chain assembly
   │
   ▼
8. Response to user with full provenance + audit log entry
```

Every step is logged. The audit log is the system's memory. PDPA fail-closed. IRB fail-closed. Cloud only when safe.

---

## 5. The 7 immutable design principles (carried over from SULUH SWARM PRD)

1. **Sovereign by default** — all data, state, model weights stay inside Malaysian jurisdiction
2. **Read-only by design** — agents recommend and synthesise; no write to production systems
3. **Hybrid retrieval, not pure RAG** — vector search + SQL + deterministic rules
4. **Document intelligence is mandatory** — Docling-grade OCR/table/figure extraction from day one
5. **Auditability over novelty** — every action attributable to source agent + model version
6. **Evaluation-driven deployment** — golden set gates every change to production
7. **Model-agnostic architecture** — swap the model, not the orchestrator

These are constraints, not preferences. Any PR that violates them requires a Steering Committee design amendment.

---

## 6. Cross-cutting concerns

### Observability
LangFuse spans at every layer. Every LLM call, retrieval operation, routing decision, agent action → traceable span. All data on-premise.

### Security
- All intra-service communication: TLS 1.3
- The FastAPI gateway: VPN-only, never internet-facing
- The only outbound internet connection permitted: HTTPS to api.anthropic.com from the quality router, and only when all conditions met
- Production PostgreSQL: network group allows inbound only from the replication source IP

### Reproducibility
Every workflow is versioned, containerised, and logged. `experiment_id` ties together: agent config + prompt versions + retrieved documents + model weights + output + audit log. Replayable end-to-end.

### Federation (consortium-ready)
For the SEA consortium expansion (UTM, UM, NTU, etc.):
- Each partner deploys their own `suluh` instance
- Agents are registered via signed manifests
- No shared data plane — only capability + manifest exchange
- Encryption: per-tenant keys, no plaintext cross-tenant traffic

(Federation is a Phase 3 deliverable. Spec lives in `docs/federation/` once written.)

---

*This document is the canonical architecture reference. Update it when the architecture changes. The code, the PRDs, and the papers all defer to this file.*
