# SULUH Ecosystem — A Sovereign Multi-Agent AI Platform with Provenance-Tracked Retrieval and Multi-LLM Deliberation for Higher Education Research

## Preliminary Paper · July 2026

**Putra Nasution** (Lead Author, Corresponding Author)  
*Lead Architect & Principal Investigator*  
poetra@gmail.com

**Dr. Suzani binti Mohamad Samuri**  
*Universiti Pendidikan Sultan Idris, Faculty of Meta*  
*Oversight Director & Co-Principal Investigator*

---

## Abstract

Higher education institutions in Southeast Asia face a regulatory paradox: research data — participant records, ethics approvals, pre-publication manuscripts, indigenous knowledge — cannot legally be processed by foreign cloud AI services under data protection regimes like Malaysia's PDPA 2010, yet universities must adopt AI to remain competitive. Existing solutions are either foreign cloud (regulatory risk), vendor-managed (institutional lock-in), or ad-hoc local (unsustainable and irreproducible).

We present the **SULUH Ecosystem**, a sovereign, on-premise multi-agent AI platform purpose-built for higher education research in Southeast Asia. The ecosystem consists of three composable open-source packages: (1) **IsRAG** (*Isnad-chain Retrieval Augmented Generation*), which embeds full provenance chains, multi-factor trust scoring, and cultural-context tagging into every retrieved knowledge unit — adapting the 1,000-year-old Islamic Isnad (إسناد) framework for knowledge validation to modern AI retrieval; (2) **Dewan Council**, a three-stage multi-LLM deliberation protocol in which seven models produce independent opinions, cross-review each other, and synthesise a consensus answer with explicit dissent visibility and full audit trail; and (3) **SULUH AI**, the orchestration platform comprising a FastAPI gateway, LangGraph-based swarm coordinator, hybrid RAG (vector + SQL), PDPA and IRB compliance gates enforced in code rather than configuration, and a Vue 3 research workbench.

The architecture follows a four-tier design (user, application, orchestration, data) governed by seven immutable design principles including sovereignty-by-default, read-only-by-design, and evaluation-driven deployment. Compliance with PDPA 2010 and institutional IRB requirements is enforced through deterministic application-code gates — not configurable feature flags — making the platform deployable in regulated research environments where standard AI tools are currently unsafe.

We report the design, the current implementation state (IsRAG and Dewan Council are operational at v0.1 with 18/18 passing tests; SULUH AI is in planning with a validated architecture), the evaluation methodology (200-entry bilingual golden set across five research domains), and the 12-month pilot deployment plan at Universiti Pendidikan Sultan Idris, Malaysia, serving approximately 275 research staff and 2,400 graduate students.

**Keywords:** sovereign AI, retrieval-augmented generation, provenance, multi-agent systems, multi-LLM deliberation, PDPA compliance, IRB, higher education, Islamic epistemology, Isnad, Southeast Asia

---

## 1. Introduction

### 1.1 The Sovereignty Gap

The adoption of AI in higher education is accelerating globally, but the distribution of that adoption is highly uneven — and the governance of it is often non-existent. Universities in middle-income countries face a structural disadvantage: their research data cannot legally leave their jurisdiction, yet the AI tools that would accelerate their research are overwhelmingly cloud-based and foreign-operated.

Consider a typical Malaysian public university. Its researchers generate participant interview transcripts, ethics approvals, pre-publication manuscripts, indigenous community knowledge records, and clinical data. Under the Personal Data Protection Act 2010 (PDPA), much of this data cannot be processed by foreign cloud AI services. Institutional Review Boards (IRBs) require auditable, attributable decision trails for any research involving human subjects. Yet the AI tools available to these researchers — ChatGPT, Claude, Gemini, Copilot — process data on foreign servers with opaque provenance and no IRB-compatible audit trail.

The result is a fragmented landscape: well-resourced institutions build private AI clusters; under-resourced ones either use foreign cloud services and accept the regulatory risk, or forgo AI altogether. This is the **sovereignty gap**.

### 1.2 Three Research Questions

The SULUH Ecosystem addresses this gap through three integrated research contributions, each corresponding to one package in the ecosystem:

| # | Research Question | Package | Contribution |
|---|---|---|---|
| **RQ1** | Does provenance-tracked retrieval with multi-factor trust scoring and cultural-context tagging measurably improve trust calibration, factual accuracy, and cultural appropriateness over standard RAG? | IsRAG | A retrieval architecture that makes provenance, trust, and cultural context first-class citizens of every knowledge unit |
| **RQ2** | Does a structured multi-LLM deliberation protocol with explicit dissent recording produce more auditable, more comprehensive, and more internally consistent answers than single-LLM or naive-aggregation baselines? | Dewan Council | A three-stage deliberation protocol that produces auditable consensus with dissent visibility |
| **RQ3** | Can a reference architecture for sovereign multi-agent AI be deployed in a public university in 12 months, satisfying PDPA and IRB compliance by architectural design rather than post-hoc configuration? | SULUH AI | A four-tier, seven-principle reference architecture validated through a working pilot |

### 1.3 Contributions

The SULUH Ecosystem makes four contributions:

1. **A provenance-aware retrieval model (IsRAG)** that adapts a 1,000-year-old knowledge-validation framework — the Islamic Isnad — to modern AI retrieval. Every piece of retrieved knowledge carries: an immutable provenance chain, a 5-factor trust score, and a cultural-context tag drawn from a 14-framework registry. This is, to our knowledge, the first RAG system to treat provenance and cultural epistemology as architectural primitives rather than post-hoc features.

2. **A multi-LLM deliberation protocol (Dewan Council)** that produces both better answers (on multi-perspective queries) and more auditable answers (in all cases). The protocol surfaces dissent rather than absorbing it, names a consensus score, and produces a complete provenance chain for every deliberation.

3. **A reference architecture (SULUH AI)** for sovereign, PDPA/IRB-compliant multi-agent AI in higher education, governed by seven immutable design principles operationalised in application code rather than configuration.

4. **A 12-month pilot deployment** at a Malaysian public university, providing empirical data on adoption, accuracy, compliance, and the practical costs of sovereignty.

---

## 2. Related Work

### 2.1 Retrieval-Augmented Generation

RAG (Lewis et al., 2020) has become the dominant architecture for grounding LLMs in external knowledge. Subsequent work has explored retrieval quality (REALM, RETRO, Atlas), hybrid retrieval (vector + keyword + SQL), and agentic RAG patterns. However, the vast majority of RAG systems treat all retrieved documents as epistemically equivalent: a peer-reviewed journal article and an unverified blog post carry the same retrieval weight. Citation-based approaches (e.g., Perplexity, You.com) surface sources but do not score their trustworthiness. Our work extends RAG by embedding provenance, trust, and cultural context directly into the retrieval data model.

### 2.2 Provenance in Information Systems

Provenance tracking has a long history in databases (Buneman et al., 2001), scientific workflows (W3C PROV, 2013), and knowledge graphs. However, these systems have not been integrated into the LLM-generation loop. The W3C PROV model records `wasGeneratedBy`, `wasDerivedFrom`, and `wasAttributedTo` relations but has no notion of trust scoring, cultural context, or dynamic retrieval-time provenance assembly. IsRAG builds on PROV concepts but operationalises them for LLM retrieval: every retrieval operation constructs a live provenance chain, not a static annotation.

### 2.3 The Islamic Isnad Framework

The Isnad (إسناد) system, developed by Islamic scholars in the 2nd century AH (8th century CE), is arguably history's first systematic knowledge-validation methodology. Every transmitted report (*hadith*) was evaluated not by its content alone but by the complete chain of transmitters (*isnad*) who carried it: each transmitter was named, their reliability was rated, their contemporaneity with the previous transmitter was verified, and the resulting chain was classified on a spectrum from *sahih* (sound) to *mawdu'* (fabricated). The system produced a graded, auditable knowledge corpus that has survived for over a millennium.

We argue that this 1,000-year-old epistemology maps directly onto the modern AI trust problem. The RAG equivalent: an LLM produces a claim (the *matn*, or content), and the user needs to know the chain (*isnad*) of sources, their credibility, and who verified them. Our adaptation is not metaphorical — it is structural: the IsRAG `KnowledgeEntry`, `ProvenanceChain`, `TrustEngine`, and `IsnadChain` types map directly onto the Isnad data model.

### 2.4 Multi-LLM Ensembles and Deliberation

Multi-LLM patterns have emerged from both research and practice. Karpathy's LLM Council (2024) proposed a three-stage deliberation; Wang et al. (2023) introduced self-consistency through multiple sampling; Du et al. (2024) explored debate between LLMs. Commercial systems increasingly use "best-of-N" sampling or majority voting. However, these approaches discard dissent. A majority vote hides minority opinions. A confidence-weighted average produces an artificial consensus. Our approach differs in two ways: (1) dissent is explicitly recorded and surfaced, not absorbed, and (2) the deliberation is grounded in provenance-tracked knowledge from IsRAG, so every opinion carries a verifiable trust chain.

### 2.5 Sovereign and Decolonial AI

Recent work in decolonial AI (Mohamed et al., 2020; Birhane et al., 2022) has critiqued the universalising assumptions of Western AI frameworks and called for culturally-grounded, epistemologically-plural AI systems. Our cultural-context registry — 14 frameworks ranging from Global to Indigenous, operationalised as a first-class data structure in the retrieval pipeline — is a direct response to this call. Sovereignty in our architecture means not just data locality but epistemological plurality: the system explicitly tags knowledge with its cultural framework of origin, its applicability boundaries, and its limitations.

### 2.6 Compliance-Enforcing Architectures

The concept of "compliance by architecture" — enforcing regulatory requirements through code paths rather than configuration — draws from the privacy-by-design literature (Cavoukian, 2009) and from secure systems engineering. Our contribution is to operationalise this for AI research platforms: PDPA classification and IRB ethics gating are not feature flags that can be toggled off by an operator; they are hard code paths in the query routing pipeline with fail-closed semantics.

---

## 3. The SULUH Ecosystem

The ecosystem consists of three packages designed as a single research programme. `israg` and `council` are **leaf packages** — they have no dependency on `suluh` and can be used standalone. `suluh` is the **composition package** — it depends on both leaves and orchestrates them into a unified platform.

### 3.1 IsRAG: Isnad-Chain Retrieval Augmented Generation

#### 3.1.1 Data Model

IsRAG defines five primary data structures that together form the provenance backbone of the ecosystem:

**KnowledgeEntry.** A single piece of ingested knowledge with full provenance metadata:

```
KnowledgeEntry {
  content: str           — the knowledge claim itself
  entry_id: str          — SHA-256 content hash, truncated to 16 chars
  author: str            — who created this knowledge
  author_type: str       — "person", "institution", "ai"
  source_type: SourceType — RESEARCH, GOVERNMENT, ACADEMIC, etc. (9 types)
  verification_level: VerificationLevel — UNVERIFIED → FIELD_VALIDATED (6 levels)
  cultural_context: CulturalContext | None
  provenance: list[ProvenanceStep]
  verifications: list[VerificationRecord]
  tags: list[str]
  created_at: datetime
}
```

**ProvenanceStep.** One hop in the chain of custody:

```
ProvenanceStep {
  step_type: str         — "creation", "verification", "storage", "retrieval", "adaptation"
  entity: str            — who or what performed this step
  entity_type: str       — "person", "institution", "system"
  timestamp: datetime
  action: str            — human-readable description
  metadata: dict
}
```

**TrustEngine.** Computes a 0.0–1.0 composite trust score from five weighted factors:

| Factor | Weight | Description |
|---|---|---|
| Verification level | 0.30 | The highest verification level across all verifiers (normalised: level/5) |
| Source credibility | 0.25 | Base credibility of the source type, with institutional bonus |
| Verification quality | 0.20 | Average rating from verifiers plus count bonus (diminishing returns) |
| Cross-references | 0.15 | Number of other entries that reference this one (via metadata) |
| Freshness | 0.10 | Age in days; decays from 1.0 at <30 days to 0.6 at >730 days |

The trust score is mapped to a human-readable confidence level: `very_high` (≥0.9), `high` (≥0.75), `medium` (≥0.5), `low` (≥0.3), `unverified` (<0.3).

**CulturalContext.** Tags knowledge with its epistemological framework:

```
CulturalContext {
  framework: CulturalFramework  — 14 options: GLOBAL, WESTERN, EAST_ASIAN,
                                   SOUTHEAST_ASIAN, SOUTH_ASIAN, INDONESIAN,
                                   MALAYSIAN, THAI, VIETNAMESE, FILIPINO,
                                   SINGAPOREAN, ISLAMIC, BUDDHIST, INDIGENOUS
  language_original: str
  applicability: list[str]      — where does this knowledge apply?
  limitations: list[str]        — what are the boundaries?
  local_terms: dict[str, str]   — local terminology with translations
  adaptation_notes: str
}
```

**IsnadChain.** The complete human-readable provenance trail for a single knowledge entry, assembled at retrieval time:

```
IsnadChain {
  entry_id, provenance_steps, verifications,
  cultural_context, trust_score, confidence_level
}
```

The chain can be rendered for display with `format_for_display()`, producing a structured terminal output showing the full provenance, verifications, and cultural context in both English and Bahasa Malaysia ("Rantai Asal-Usul Pengetahuan").

#### 3.1.2 Retrieval Pipeline

```python
engine.retrieve(
    query: str,
    min_trust_score: float = 0.0,
    cultural_filter: CulturalFramework = None,
    source_filter: SourceType = None,
    limit: int = 10,
    include_isnad: bool = False
) -> list[RetrievalResult]
```

Each `RetrievalResult` carries: content, relevance score, trust score, confidence level, full isnad chain (if requested), source type, and cultural context. Results are sorted by a combined score: `relevance_score × 0.6 + trust_score × 0.4`.

The current implementation uses keyword-based relevance scoring; the Phase 1 upgrade replaces this with vector similarity (bge-m3 embeddings indexed in pgvector with HNSW).

#### 3.1.3 Current Implementation Status

IsRAG is operational at v0.1 alpha with **18/18 tests passing** (pytest, 0.03 seconds). The core engine is 783 lines of Python with a full CLI interface. Key capabilities demonstrated: ingest with provenance, keyword retrieval with trust filtering, cultural-context-aware retrieval, verification chaining, and knowledge base statistics. The implementation is in-memory with no persistent storage or vector search — these are Phase 1 deliverables.

### 3.2 Dewan Council: Multi-LLM Deliberation

#### 3.2.1 The Three-Stage Protocol

Dewan Council implements a structured deliberation protocol inspired by Karpathy's LLM Council (2024) and the Islamic tradition of scholarly consultation (*shura*):

**Stage 1: First Opinions.** Each of N council members is queried independently with the same prompt. Each member produces an `Opinion` carrying: the response text, a self-assessed confidence score (1–10), and the model identifier. Stage 1 produces N opinions.

**Stage 2: Cross-Review.** Each member reviews every other member's Stage 1 opinion. For N members, this produces N × (N−1) = N² − N reviews. Each `Review` carries: reviewer identity, reviewed member identity, rating (1–10), free-text feedback, and a list of issues found (factual errors, missing context, unsupported claims, bias). Stage 2 produces a complete review matrix.

**Stage 3: Chairman Synthesis.** A designated chairman LLM receives the original query, all Stage 1 opinions, all Stage 2 reviews, and the review matrix summary. The chairman produces: `final_answer` (the synthesised response), `consensus_score` (0.0–1.0), `dissenting_views` (list of opinions that disagreed with the majority), and a full `isnad_chain` (complete audit trail).

The chairman is the member with `role="chairman"` (Claude Opus 4.7 in the reference council). The chairman's trust weight is 1.2×; all other members are weighted at 1.0–1.1×.

#### 3.2.2 The Reference Council

The reference council used in all experiments consists of seven members spanning four model families, accessed via a single OpenRouter API:

| # | Role | Model (OpenRouter ID) | Specialty | Weight |
|---|---|---|---|---|
| 1 | Chairman | `anthropic/claude-opus-4.7` | Synthesis, judgment, nuanced analysis | 1.2 |
| 2 | Member | `openai/gpt-5.5` | Deep reasoning, multi-step logic | 1.1 |
| 3 | Member | `google/gemini-3-flash-preview` | Data analysis, multimodal, fast reasoning | 1.0 |
| 4 | Member | `moonshotai/kimi-k2.6` | Long context, multi-agent perspective | 1.0 |
| 5 | Member | `deepseek/deepseek-v4-flash` | Chain-of-thought, mathematical rigour | 1.1 |
| 6 | Member | `qwen/qwen3.6-plus` | Agentic coding, multilingual, Asian market context | 1.0 |
| 7 | Member | `nvidia/nemotron-3-super` | Open model, hardware-software integration | 1.0 |

Council composition is configurable — any set of `CouncilMember` objects with arbitrary model IDs and trust weights can be passed at initialisation.

#### 3.2.3 Integration with IsRAG

Dewan Council is designed to ground its deliberation in IsRAG-retrieved knowledge. When integrated, Stage 1 opinions are constrained to cite specific `KnowledgeEntry` objects; the chairman's synthesis inherits the trust scores of the cited entries. This produces a two-layer provenance chain: the knowledge provenance (from IsRAG) and the deliberation provenance (from Dewan Council), linked together in a single `DeliberationResult`.

#### 3.2.4 When to Use Deliberation vs. Direct Retrieval

Deliberation is triggered for approximately 10% of queries — those classified as SWARM-route by the SULUH query router. The routing decision considers query complexity, multi-perspective nature, and the presence of heterogeneous sources. Simple single-fact queries are routed to IsRAG directly (FAST or PRIMARY lanes). Deliberation is most valuable when: (a) the query has multiple defensible framings, (b) the sources are heterogeneous in quality, and (c) the downstream user benefits from seeing the reasoning and dissent.

#### 3.2.5 Current Implementation Status

Dewan Council is operational at v0.1 alpha with a 775-line core engine. Key capabilities demonstrated: full three-stage deliberation with configurable members, OpenRouter API integration, mock mode for testing without API keys, and structured output with dissent recording. The implementation uses synchronous, sequential API calls — streaming and async deliberation are Phase 1 deliverables.

### 3.3 SULUH AI: The Sovereign Orchestration Platform

SULUH AI is the composition layer that integrates IsRAG and Dewan Council into a unified platform with gateways, routing, compliance enforcement, and user interfaces. Unlike the two leaf packages, SULUH AI is in the planning phase with a validated architecture but zero implementation code.

#### 3.3.1 Component Architecture

```
packages/suluh/
├── gateway/     FastAPI: JWT validation, RBAC, rate limiting, SSE, audit logging
├── router/      Query classifier: PDPA level, IRB indicator, complexity scorer
├── swarm/       LangGraph v1.0: 6-step pipeline, subgraph composition
├── rag/         Hybrid RAG: pgvector HNSW + Text-to-SQL with sqlglot sandbox
├── docling/     IBM Docling: OCR, table extraction, figure extraction
├── pdpa/        PDPA masking: presidio-based PII detection, fail-closed
├── irb/         IRB ethics gate: deterministic classifier, protocol matcher
└── registry/    Agent registry: capability manifests, signed agent deployment
```

#### 3.3.2 The Query Routing Decision Tree

Every user query traverses the following decision path:

1. **Gateway** validates JWT, enforces RBAC, emits audit event.
2. **Router** classifies the query on three axes: PDPA level (PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED), IRB relevance (human-subject indicators), and complexity (LOW/MEDIUM/HIGH).
3. **IRB Gate** checks: if human-subject indicators are detected, cross-reference against approved IRB protocols. No protocol match → blocked for human review. Fail-closed.
4. **PDPA Masking** applies: RESTRICTED data is blocked from any cloud escalation. CONFIDENTIAL data is masked. Fail-closed.
5. **Route Decision**: FAST (55% of queries: vector retrieval + Qwen 3.6 direct), PRIMARY (30%: vector + SQL + Qwen extended), SWARM (10%: IsRAG + Council deliberation), ESCALATE (<5%: anonymised → Anthropic Claude API, only when all conditions met).
6. **Synthesis** assembles the response with full IsnadChain and returns to user.

#### 3.3.3 The Swarm Coordinator (Planned)

The LangGraph-based swarm coordinator implements a 6-step pipeline for multi-agent research tasks:

1. **Query Analyzer** — understand intent, scope, domain
2. **Discovery** — identify relevant agents, tools, data sources
3. **Decompose** — break into subtasks, assign to agents
4. **Execute** — run agent tasks in parallel subgraphs (max 15 steps/workflow, 10-second tool timeout)
5. **Consensus** — aggregate results, resolve conflicts via Council deliberation
6. **IRB Gate** — final ethics check before returning to user

All agent actions are read-only in Phase 2. Write capability requires Steering Committee approval and is reserved for Phase 3+.

---

## 4. Architecture & Design Principles

### 4.1 The Four Tiers

The SULUH ecosystem follows a four-tier architecture inherited from the SULUH SWARM PRD v1.0 (July 2026):

- **Tier 1 (User Layer):** Vue 3 AI Workbench, JupyterLab extension, REST/SDK, Admin Console. Receives JWT from institutional SSO; communicates only with Tier 2.
- **Tier 2 (Application Layer):** FastAPI AI Gateway handling JWT validation, RBAC, rate limiting, SSE streaming, and audit log emission. Strips PII from user context before forwarding to Tier 3.
- **Tier 3 (Orchestration Layer):** Query router, LangGraph swarm coordinator, hybrid RAG, multi-LLM deliberation, PDPA masking, IRB ethics gate, document intelligence, agent registry.
- **Tier 4 (Data Layer):** PostgreSQL AI read replica with pgvector/HNSW and immutable audit log, MinIO for document artefacts, LangFuse for LLM observability, Redis for agent state and caching, Debezium for CDC from production systems.

An optional cloud quality layer routes <5% of queries to Anthropic Claude API, but only when: the query is anonymised, does not involve human subjects, the local model confidence is below 0.72, and the data classification is PUBLIC or INTERNAL. RESTRICTED data is hard-blocked from all cloud escalation.

### 4.2 The Seven Immutable Design Principles

The ecosystem is governed by seven principles that are **constraints enforced in application code**, not preferences or configuration settings:

1. **Sovereign by default.** All research data, agent state, model weights, and institutional documents remain within the deploying institution's network perimeter and national jurisdiction. No raw research data traverses the public internet under any condition.

2. **Read-only by design.** AI agents can recommend, analyse, synthesise, and generate — but cannot write to production research databases, ethics systems, or institutional records. Write capability requires a formal Steering Committee design amendment.

3. **Hybrid retrieval, not pure RAG.** Research systems require vector search for documents, SQL generation for structured data, and deterministic controls for compliance. Pure semantic RAG will produce incorrect research outputs in database-backed environments.

4. **Document intelligence is mandatory.** Document OCR, table extraction, and figure extraction from research papers, grant proposals, and scanned documents are first-class requirements — not Phase 2 enhancements.

5. **Auditability over novelty.** Every agent action must be explainable, attributable to a source agent and model version, and logged to the immutable audit trail. IRB and reproducibility compliance is non-negotiable.

6. **Evaluation-driven deployment.** No model, retrieval configuration, prompt change, or agent workflow reaches production without passing the regression gate against the golden evaluation set.

7. **Model-agnostic architecture.** Switching the primary inference model requires updating one config value — not rewiring the orchestration or retrieval layers. Swap paths are maintained for all candidate models.

### 4.3 Package Composition and Dependency Flow

```
suluh (orchestrator — depends on both leaves)
  │
  ├──► israg (leaf — zero dependencies)
  │       Exports: KnowledgeEntry, TrustEngine, IsnadChain, CulturalContext
  │
  └──► council (leaf — zero dependencies)
          Exports: CouncilMember, Opinion, Review, DeliberationResult
```

This separation is deliberate. Researchers can use IsRAG standalone for provenance-tracked retrieval. Developers can use Dewan Council standalone for multi-LLM deliberation. Only when both are needed together — for multi-agent research orchestration with compliance enforcement — is the full SULUH platform required.

---

## 5. Compliance by Architecture

A core claim of this work is that compliance — with data protection law (PDPA) and research ethics requirements (IRB) — should be enforced in application code, not in configuration, policy documents, or operator training.

### 5.1 The Dual-Gate Model

Two compliance gates run on every query, in sequence, before routing:

```
Query enters
    │
    ▼
[PDPA Gate]     ← runs first; data classification
    │
    ├── RESTRICTED → local only, no cloud escalation
    │
    ▼
[IRB Gate]      ← runs second; human-subject check
    │
    ├── Human-subject + approved protocol → pass
    ├── Human-subject + no protocol → block for human review
    └── Non-human-subject → pass
    │
    ▼
[Routing]       ← only reached if both gates pass
```

Both gates are **hard-coded Python functions**, not configuration values. The PDPA classification gate is `suluh.pdpa.gate()`, not a feature flag. The IRB gate is a LangGraph node in the workflow graph, not a runtime toggle. The RESTRICTED-data cloud-escalation block is a hard `if/raise` in the router, not a settings file entry. Both gates **fail closed**: if the classifier errors, the query is blocked with an audit event, not passed through.

### 5.2 The PDA Classification System

Four levels, enforced at both ingest and runtime:

| Level | Description | Cloud Escalation | Retention |
|---|---|---|---|
| PUBLIC | Published papers, anonymised stats, open datasets | Permitted | Indefinite |
| INTERNAL | Research aggregates, non-PII project data | Permitted (anonymised) | 7 years |
| CONFIDENTIAL | Researcher profiles, grant applications, pre-publication manuscripts | Prohibited | 7 years |
| RESTRICTED | Participant IDs, interview transcripts, clinical data, IRB investigation records | Prohibited | 10 years |

### 5.3 The IRB Pre-Screen

The IRB gate uses a five-question pre-screen classifier, initially keyword-based (Phase 0) and later fine-tuned on 200 labelled research queries (Phase 1):

1. Does the research involve human participants (directly or via their data)?
2. Does it involve identifiable personal information?
3. Does it involve sensitive categories (health, religion, ethnicity, political opinion)?
4. Does it involve vulnerable populations?
5. Has an IRB protocol been approved for this research type?

Any "yes" on questions 1, 2, or 3 without an approved protocol triggers the IRB gate — the workflow pauses, the reviewer is notified, and no AI response is returned to the user until the gate is cleared.

### 5.4 The Immutable Audit Log

The `ai_audit_log` PostgreSQL table is protected by a database trigger that rejects any UPDATE or DELETE operation. All AI operations — queries, SQL executions, agent swarm invocations, cloud escalations, PDPA detections, IRB gate decisions, document lifecycles — are logged with retention periods of 7–10 years. All user and IP identifiers are hashed (SHA-256 with per-deployment salts); plaintext identifiers are never logged.

---

## 6. Evaluation Plan

### 6.1 The Golden Evaluation Set

A 200-entry bilingual (Malay/English) golden set authored by 30+ researchers from consortium institutions, covering five domains:

- **Agriculture:** crop science, palm oil sustainability, food security
- **Islamic finance:** shariah-compliant instruments, waqf, takaful
- **Indigenous land rights:** adat law, community mapping, customary tenure
- **Public health:** epidemiology, vaccination policy, health systems
- **Digital governance:** data sovereignty, AI regulation, e-government

Each entry includes: query text, golden answer, domain label, language, difficulty rating, whether it requires multi-LLM deliberation, whether it is IRB-flagged, and the expected trust score range for correctly retrieved sources.

The golden set is expanded in three phases: 50 entries (Phase 0, for model benchmarking), 200 entries (Phase 1, for regression testing), and ongoing expansion with consortium contributions (Phase 2+).

### 6.2 Evaluation Metrics

| Metric | Method | Phase 0 Target | Phase 3 Target |
|---|---|---|---|
| Answer accuracy | BERTScore vs golden answer | ≥75% | ≥93% |
| Trust calibration | Pre/post Likert survey (100+ participants) | Baseline established | Effect size >0.5 |
| Cultural appropriateness | Expert review, 3-point ordinal | Baseline established | ≥90% appropriate |
| Hallucination rate | Claimed citations verified against source DB | <10% | <5% |
| Provenance completeness | Binary: does response include full IsnadChain? | 100% | 100% |
| Text-to-SQL correctness | Execution result matches expected | — | ≥92% |
| Swarm task success | LangFuse trace review against expected outcome | — | ≥90% |
| PDPA compliance | Monthly audit log review | 100% | 100% |
| IRB gate accuracy | IRB officer review of gate decisions | — | ≥98% |
| Average response latency | End-to-end (gateway → response) | <5s | <2.5s |

### 6.3 Baselines

IsRAG is evaluated against:
- Standard RAG (LangChain default, LlamaIndex default)
- RAG with citations only (no trust scoring)
- RAG with cultural context only (no trust scoring)
- IsRAG (full: provenance + trust + cultural context)

Dewan Council is evaluated against:
- Single-LLM (Claude Opus alone)
- Best-of-N (N=7 samples from Claude, highest self-assessed confidence)
- Majority vote (independent sampling, modal answer)
- Dewan Council (full 3-stage protocol)

SULUH AI is evaluated against:
- Pre-pilot baseline: current research productivity and AI tool usage at UPSI
- Phased adoption metrics across the 12-month pilot
- Comparison with institutional cloud AI usage patterns at peer universities

### 6.4 Hypotheses

We hypothesise that:

1. **IsRAG** will match baseline RAG on simple factual queries and outperform on multi-perspective, trust-sensitive queries by 5–10% BERTScore, while reducing hallucination rate by ≥30% and significantly improving user trust calibration (effect size >0.5).

2. **Dewan Council** will match single-LLM on simple queries, outperform on multi-perspective synthesis queries by 10–15% on comprehensiveness, have lower internal inconsistency, and surface dissent that baselines silently absorb.

3. **SULUH AI** will demonstrate that a sovereign, PDPA/IRB-compliant multi-agent AI platform is deployable in a public university within 12 months on a capital-light budget, achieving 75% adoption, 100% PDPA compliance, and 90% swarm task success.

---

## 7. Expected Contributions

### 7.1 Academic Contributions

1. **IsRAG:** A provenance-aware retrieval architecture that adapts the 1,000-year-old Islamic Isnad framework to modern AI, demonstrating that trust scoring, cultural context, and provenance chains measurably improve RAG output quality and trust calibration. Target venues: ACL, EMNLP, FAccT, JCDL.

2. **Dewan Council:** A three-stage multi-LLM deliberation protocol that produces both better and more auditable answers, with structured dissent recording and provenance-grounding via IsRAG. Target venues: AAMAS, NeurIPS (workshops), ACL (workshops).

3. **SULUH AI:** A reference architecture for sovereign multi-agent AI in higher education, governed by seven immutable design principles operationalised in code, tested through a 12-month pilot. Target venues: FAccT, AIES, IEEE Security & Privacy.

### 7.2 Institutional Impact

- 15,000–35,000 productive research hours returned to UPSI per year (8–18 FTE equivalent)
- 75% adoption rate among research staff and graduate students
- 100% PDPA compliance, 98% IRB gate accuracy
- Position UPSI as the first Malaysian university to deploy a sovereign, PDPA-compliant multi-agent AI research platform on a 1,280 GB distributed cluster
- Reusable consortium expansion model for partner institutions (UTM, UM, NTU, others)

### 7.3 Strategic Contributions

- Reference implementation for Malaysia National AI Agenda 2026–2030
- Foundation for ASEAN sovereign AI research infrastructure
- A provenance-aware, culturally-grounded AI system as a contribution to the global decolonial AI movement
- Demonstration that Islamic epistemology (Isnad) provides a formal, operationalisable framework for AI trust that generalises beyond any single culture or religion

---

## 8. Limitations and Future Work

### 8.1 Current Limitations

1. **IsRAG's retrieval is keyword-based in v0.1.** The Phase 1 upgrade to vector search (bge-m3 + pgvector HNSW) is architecturally specified but not implemented. The current trust scoring weights are hand-tuned; future work should learn them from user feedback.

2. **Dewan Council is fully synchronous.** A seven-member council with full cross-review requires 43 sequential LLM calls per query. Streaming and parallelisation are Phase 1 priorities.

3. **SULUH AI has zero implementation code.** The architecture is validated, the data model is specified, and the principles are codified — but no gateway, router, swarm, or compliance gate code exists yet. This introduces execution risk for the 12-month timeline.

4. **The cultural framework registry (14 frameworks) is curated,** not discovered. Automated cultural-context detection from document content is future work.

5. **Single-site pilot.** The evaluation is at one Malaysian university. Multi-institution validation with consortium partners is a Phase 3 deliverable.

6. **The golden set is small.** 200 entries across 5 domains is sufficient for Phase 0–1 regression testing but not for publication-grade evaluation. 1,000+ entries are needed for the final paper submissions.

### 8.2 Future Work

- **Automated trust weight learning:** replace hand-tuned TrustEngine weights with learned weights from user trust calibration feedback.
- **Dynamic council composition:** learned chairman selection and council composition based on query type and domain.
- **Cultural-context auto-detection:** classify documents into the CulturalFramework registry automatically.
- **Consortium federation:** signed manifest exchange, capability-based access, no shared data plane. Full spec in Phase 3.
- **Longitudinal adoption study:** 24-month follow-up measuring sustained adoption, productivity impact, and quality of research outputs.
- **Public inference service:** in Phase 3+, open the platform as a hosted inference service for SEA universities that cannot deploy their own infrastructure.

---

## 9. Conclusion

The SULUH Ecosystem addresses a real and growing problem — the sovereignty gap in higher education AI — with a complete, deployable, open-source solution. The architecture is grounded in a 1,000-year-old epistemology (the Islamic Isnad) and 21st-century compliance requirements (PDPA, IRB).

We have presented: (1) IsRAG, a provenance-tracked retrieval system that makes trust, provenance, and cultural context first-class architectural concerns; (2) Dewan Council, a multi-LLM deliberation protocol that produces auditable consensus with dissent visibility; and (3) SULUH AI, a reference architecture for sovereign, compliant multi-agent AI in higher education.

The three components form a single research programme: IsRAG defines *what every retrieved fact looks like*, Council defines *how multiple models deliberate*, and SULUH defines *how agents coordinate and execute in a regulated environment*. Together, they offer a path toward deploying AI in institutional research contexts where standard AI tools are currently unsafe.

The 12-month pilot at UPSI will provide the first empirical data on whether a sovereign, provenance-aware, deliberation-grounded multi-agent AI platform can be deployed in a public university in a middle-income country — and whether it measurably improves research productivity, trust, and compliance.

---

## References

1. Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS 2020*.
2. Karpathy, A. (2024). LLM Council: A Three-Stage Multi-LLM Deliberation Pattern. *Blog post*.
3. Wang, X., et al. (2023). Self-Consistency Improves Chain of Thought Reasoning in Language Models. *ICLR 2023*.
4. Du, Y., et al. (2024). Improving Factuality and Reasoning in Language Models through Multiagent Debate. *ICML 2024*.
5. Buneman, P., Khanna, S., & Tan, W. C. (2001). Why and Where: A Characterization of Data Provenance. *ICDT 2001*.
6. W3C (2013). PROV-Overview: An Overview of the PROV Family of Documents.
7. Mohamed, S., Png, M. T., & Isaac, W. (2020). Decolonial AI: Decolonial Theory as Sociotechnical Foresight in Artificial Intelligence. *Philosophy & Technology*.
8. Birhane, A., et al. (2022). The Values Encoded in Machine Learning Research. *FAccT 2022*.
9. Cavoukian, A. (2009). Privacy by Design: The 7 Foundational Principles.
10. Malaysia Personal Data Protection Act 2010 (Act 709).
11. LangGraph v1.0 (2025). LangChain Inc. Production-grade agent orchestration framework.
12. IBM Docling. Document understanding and conversion toolkit.
13. EXO. Distributed inference for open-weight models.
14. pgvector. Open-source vector similarity search for PostgreSQL.
15. OpenRouter. Unified API for accessing multiple LLM providers.

---

## Reproducibility Appendix

- **Codebase:** `~/Documents/PROJECTS/suluh-ecosystem/` — private monorepo (Apache 2.0)
- **IsRAG engine:** `packages/israg/src/israg/israg_engine.py` (783 lines, Python)
- **Dewan Council engine:** `packages/council/src/council/council_engine.py` (775 lines, Python)
- **Tests:** 18 passing (pytest), covering all IsRAG and TrustEngine functionality
- **Architecture documentation:** `docs/ARCHITECTURE.md`, `docs/PRINCIPLES.md`, `docs/COMPLIANCE.md`
- **Research proposal:** `research/proposal/SULUH-ECOSYSTEM-PROPOSAL.md`
- **Academic papers (drafts):** `research/papers/paper-1-israg.md`, `paper-2-council.md`, `paper-3-suluh.md`
- **Golden set:** `research/golden-sets/` (Phase 0 deliverable: 50 entries in JSONL format)
- **Evaluation scripts:** `benchmarks/` (Phase 0 deliverable)

---

*Submitted for preliminary review. July 2026.*
