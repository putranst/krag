# SULUH SWARM PRD v1.0 — Analysis & Verdict

**Document under review:** `suluh_swarm_prd_v1.pdf` (UPSI internal, July 2026, 38 pages, INTERNAL · CONFIDENTIAL)
**Author of analysis:** Mes (for Putra Nasution, Lead Architect)
**Date:** May 2026
**Status:** Pre-fork review — before we write any code under the new `suluh-ai/` standalone project

---

## TL;DR (the honest version)

This is a **strong, well-structured proposal** — clearly written by someone who has shipped production AI systems (you, sir). The 7 design principles are correct, the four-tier architecture is sound, the PDPA-first posture is non-negotiable and well-architected for it, the "fail closed on IRB/PDPA" rule is the right call, and the Phase 0 → Phase 3 gate structure is professionally de-risked.

**However.** It is also a **1.0 proposal that has not been built yet** — the spec describes a target state, not a working system. There is no `src/`, no schema, no swarm, no Vue 3 Workbench, no EXO cluster yet. It is a 12-month delivery plan waiting for Phase 0 to begin.

**My recommendation:** **Fork it as `suluh-ai`** as a new standalone project at `~/Documents/PROJECTS/suluh-ai/`, with three deliberate adjustments to the original PRD before we start coding:

1. **Strip the institutional voice** — the PDF is written for UPSI DVC sign-off. The standalone repo needs a developer-facing README and architecture doc written for engineers who will contribute, not for steering committees.
2. **Decouple the cluster from the dream** — the 1,280 GB 5-node EXO cluster is a Phase 0+ target. Phase 0 must run on a single Mac (M-series, 64 GB+) or a single DGX Spark, with the same code that will later spread across the cluster. Otherwise we cannot start until procurement clears.
3. **Treat IsRAG and Dewan Council as already-solved primitives** — the PRD does not name them, but the provenance/transparency claims of Suluh Swarm are exactly what IsRAG (Isnad chains) and Dewan Council (multi-LLM deliberation) provide. Reusing them saves us from rebuilding what already exists.

Everything else in the PRD is good. The analysis below is the line-by-line.

---

## 1. What the PRD is actually proposing

| Section | Substance | Verdict |
|---|---|---|
| **Strategic Summary** | 12-month programme, 4 phases, sovereign on-prem AI for UPSI research. Returns 15K–35K productive hrs/yr (8–18 FTE). 75% adoption target, 90% swarm success, 100% PDPA coverage. | Reasonable. The "8–18 FTE returned" headline is the kind of number DVC R&I will quote in steering meetings. Keep it. |
| **Executive Briefing** | PDPA + IRB compliance by architecture (not config). 4-tier intranet-first. 5-node, 1,280 GB EXO cluster. Open-source stack (RM 0 licensing). Existing team delivers. | The "by architecture, not configuration" line is the single strongest argument in the entire document. Honour it. |
| **Business Case** | 2,428 addressable hrs/wk → realistic case = 26,500 hrs/yr reclaimed (~13.8 FTE). | Defensible ranges, but they are illustrative. The PRD honestly says so in §"A note on methodology." Phase 0 should include a time-and-motion study to lock these numbers. |
| **Why Now** | 4 forces: open-source crossed commercial threshold, LangGraph v1.0 (Oct 2025) productionised, PDPA tightening, Malaysia National AI Agenda 2026–2027 funding window. | All four are real. The National AI Agenda window is the strongest forcing function — if missed, the institutional investment doubles. |
| **Design Principles** (7) | Sovereign by default, read-only by design, hybrid retrieval (vector+SQL), document intelligence mandatory, auditability over novelty, evaluation-driven deployment, model-agnostic. | These are correct, complete, and not negotiable. They are the guardrails every PR will be tested against. |
| **Four-Tier Architecture** | T1 User Layer (Vue 3 Workbench, Jupyter ext, CLI/SDK, Admin Console) → T2 FastAPI Gateway (JWT/RBAC/rate/audit/SSE) → T3 Orchestration (Query Router, Swarm Coordinator, Hybrid RAG, PDPA Masking) → T4 Data (pgvector AI replica, MinIO, LangFuse, Redis). Cloud quality layer is optional, <5%, anonymised only. | Architecturally clean. Tier boundaries are real — a fault in T3 should not cascade into T4 (and the graceful-degradation matrix in §10.3 enforces this). |
| **Query Routing** | FAST LANE (Qwen 3.6 35B-A3B, ~55% of queries) / PRIMARY (Qwen extended context, ~30%) / SWARM (Nemotron-3 Super + Agent Mesh, ~10%) / ESCALATE (Anthropic, <5%, anonymised, non-human-subject only). | Three cost levers in one diagram. The 0.72 confidence threshold and the "RESTRICTED never escalates" rule are the only two numbers that must be in code review every time. |
| **Hardware** | 3× DGX Spark (128 GB each) + 2× Mac Studio M3 Ultra (256 GB each) = 1,280 GB pooled via EXO. ConnectX-7 200GbE fabric. Edge prefill / core decode split. | This is the proposal's biggest real-world risk: hardware procurement. DGX Spark Founders Edition has constrained supply. 6-week delivery is optimistic. We will need a Phase 0 plan that runs on a single node. |
| **Models** | Qwen 3.6 35B-A3B (primary), Nemotron-3 Super (agentic/tool-call), Gemma 4-31B (alt), bge-m3 (embed), Claude API (anonymised fallback). All open-weights except the cloud escalation. | The model-agnostic principle (§7) means swap paths must be maintained for all four. Fine — but the Phase 0 benchmark (Qwen vs Gemma vs Nemotron) is the right move, not jumping to a winner. |
| **Hybrid RAG + Docling** | pgvector with HNSW, no separate vector DB. Docling for OCR/table/figure extraction. Text-to-SQL over a PostgreSQL AI read replica. | Pragmatic. pgvector eliminates one infrastructure dependency. Docling is the right tool. Text-to-SQL with sqlglot sandbox is the right discipline. |
| **Agentic Workflows (3)** | (1) Multi-Agent Swarm Orchestration, (2) Research Experiment Automation, (3) IRB Compliance Auditing. All on LangGraph v1.0, Nemotron-3 Super for tool-calling, Qwen for synthesis. Max 15 steps/workflow, 10-sec tool timeout, no write tools in Phase 2. | The guardrails table is the most important operational section. "No write tools in Phase 2" is wise — we earn write capability later, after trust is built. |
| **Security & Compliance** | 4-level PDPA classification (PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED), IRB gate runs on every human-subject workflow, fail-closed on both PDPA and IRB, immutable audit log. | Strongest part of the document. The "FAIL CLOSED" posture on PDPA masking and IRB gate is exactly right. |
| **Roadmap** | Phase 0 (M1–M2, validation only) → Phase 1 (M3–M6, core capabilities) → Phase 2 (M7–M10, workflows) → Phase 3 (M11–M12, production + consortium). 10 priority tasks. 8 success metrics with explicit targets. | Disciplined. The 10 priority tasks are well-scoped. Phase 0's three validation questions (SSO, model benchmark, IRB gate latency) are the right ones. |
| **Risk Register** | 8 risks, all Medium × {Medium/High}, all with active mitigations. None accepted as residual. | Honest. The fact that there are zero "accepted residual risks" is a bit aggressive for a 12-month programme — in reality, one or two should be on a watch list. But the discipline is correct. |
| **Appendix** | Glossary, 7 open questions (with owners + target dates), 13-component tech track record, alternatives analysis (Do Nothing / Full Cloud / Vendor / Suluh). | The "Why this approach vs alternatives" appendix (Table 36) is exactly the kind of pre-emptive objection-handling that gets proposals approved. |

---

## 2. What's missing — gaps the PRD does not address

| Gap | Why it matters | What we should do |
|---|---|---|
| **No source code, no schema, no agents, no evaluation harness** | This is a proposal, not a system. We can show 38 pages of architecture to a DVC and still need 6+ months to deliver the first phase. | Build a working v0.1 prototype on a single laptop BEFORE the next DVC review. Concrete demo > more documentation. |
| **No consortium federation design** | §1 mentions "eventually, partner SEA institutions" but Tier 4 has no federation layer. How does UM/UTM/NTU connect without data centralisation? | Add a Tier 4.5 "Federation Layer" sketch: signed manifest exchange, no shared data plane, capability-based access. |
| **No data-ingestion story for legacy research** | Docling handles PDFs, but what about the decades of `.doc`, `.rtf`, scanned image-only files, and pre-digital research notes? | Add a Docling pre-processor that flags low-confidence extractions for human review (the PRD does mention this in passing in the risk register, but it should be a Phase 1 task). |
| **No observability dashboard mockups** | LangFuse is mentioned but there are no screenshots, no KPI tiles, no operator UX. | Phase 0 should include a single-screen "Admin Console v0" — even if it's a Grafana panel stitched together. |
| **No IRB pre-screen model training plan** | The IRB gate runs on a "fine-tuned Qwen 3.6 classifier" but the training data and labelling process are not specified. | Phase 0 should produce a labelled corpus of 200 research queries (the 5 common types Dr. Suzani's team will identify) with ground-truth IRB risk labels. This is doable in 2 weeks. |
| **No failure-mode validation** | §10.3 lists 7 graceful-degradation paths but does not say how they will be tested. | Add a "chaos day" to each phase gate: kill a component on staging, verify the user experience matches §10.3. |
| **No PDPA masking implementation detail** | The "PDPA masking layer" is mentioned as a dashed box but no algorithm is specified. PII detection in Malay/English mixed research text is non-trivial. | Phase 1 should pick a baseline (presidio + bge-m3, or a fine-tuned NER) and benchmark it on the golden set. |
| **No academic publication plan** | The proposal will produce novel architecture, but there is no paper plan. The IsRAG collaboration with Dr. Suzani exists separately. | Tie the two together: SULUH AI is the system, IsRAG is the provenance layer, Dewan Council is the consensus mechanism. Three papers, one programme. |

---

## 3. What we already have that the PRD does not name

This is the "read between the lines" part, sir. The PRD was written without reference to IsRAG or Dewan Council, but Suluh Swarm's claims **require** exactly what those two projects already provide:

| SULUH Swarm claim | Already implemented in | What we save |
|---|---|---|
| "Every agent action is logged, attributable, and reversible" | **IsRAG** — full Isnad provenance chains, verification levels, cultural context tagging | 3–6 months of custom audit-log work. IsRAG's `IsnadChain.format_for_display()` and `TrustEngine` map 1:1 onto the Suluh audit log spec. |
| "Read-only by design" | **IsRAG** — KnowledgeEntry with immutable provenance append | The "no write tools in Phase 2" rule is already enforced by IsRAG's architecture. |
| "Multi-agent workflows" | **Dewan Council** — 7-LLM deliberation with cross-review, chairman synthesis, isnad output | Dewan Council IS a working swarm. The Swarm Coordinator in §9 is a superset of what Dewan already does. We extend, not rebuild. |
| "Citations on every output" | **IsRAG** — citation chain via provenance | Native. |
| "Bilingual Malay/English" | **Dewan Council** already includes Qwen 3.6 Plus as the multilingual member | The primary-reasoning model in the PRD is Qwen 3.6 35B-A3B, which we have already validated. |
| "Trust calibration" | **IsRAG** — TrustEngine with 5-factor weighted scoring | Maps onto the routing confidence threshold. |

**This is the real architectural shortcut.** Suluh Swarm does not need to invent provenance, trust, or multi-LLM deliberation. It composes them:

```
SULUH AI = FastAPI gateway
         + LangGraph agent meshes
         + pgvector (hybrid RAG)
         + Docling (document intelligence)
         + IsRAG (provenance + trust + cultural context)
         + Dewan Council (consensus + multi-LLM deliberation)
         + LangFuse (observability)
         + EXO (disaggregated inference, when the cluster arrives)
```

Six of those nine are open source and exist. We are building the gateway, the agent meshes, the PDPA masking layer, the IRB gate, and the Vue 3 Workbench. The rest is assembly.

---

## 4. Fork plan: what `suluh-ai/` will look like

The new project at `~/Documents/PROJECTS/suluh-ai/` (just created) will be structured to **implement the PRD's Phase 0 deliverable on a single developer laptop**, not on a 5-node EXO cluster:

```
suluh-ai/
├── README.md                    ← standalone developer README (write next)
├── docs/
│   ├── PRD-ANALYSIS.md          ← THIS FILE
│   ├── architecture.md          ← developer-facing port of the 4-tier diagram
│   ├── agentic-workflows.md     ← the 3 LangGraph workflows
│   ├── pdpa-irb-controls.md     ← the security/compliance section, operationalised
│   ├── routing-spec.md          ← the query-routing decision tree
│   └── model-benchmarks.md      ← Phase 0 benchmark plan
├── src/
│   ├── suluh/                   ← the gateway + orchestration code (write first)
│   │   ├── gateway/             ← FastAPI skeleton, JWT, RBAC, audit log
│   │   ├── router/              ← query classifier + complexity scorer
│   │   ├── swarm/               ← LangGraph Swarm Coordinator
│   │   ├── rag/                 ← Hybrid RAG (vector + SQL)
│   │   ├── docling/             ← document ingestion
│   │   ├── pdpa/                ← masking layer
│   │   ├── irb/                 ← ethics gate
│   │   └── registry/            ← agent registry
│   └── README.md
├── research/
│   ├── golden-set-v0.1.jsonl    ← 50 Malay/English research queries (Phase 0 task #1)
│   └── irb-classifier-corpus.md ← the 5 common research types
├── benchmarks/
│   ├── qwen-vs-gemma-vs-nemotron.md  ← Phase 0 model benchmark
│   └── irb-gate-latency.md           ← <500ms target
└── tools/
    └── exo-single-node.yaml     ← EXO config that runs on 1 Mac for Phase 0
```

**Phase 0 path on a single laptop:**
- Single Mac (M-series, 64 GB) or single DGX Spark
- EXO configured for single-node disaggregated inference
- Qwen 3.6 35B-A3B served locally
- All Tier 1–3 components in `src/suluh/`
- Single SQLite or local Postgres for Tier 4 (replica setup deferred to Phase 1)
- LangFuse on `localhost:3000`
- Vue 3 Workbench as a `npm run dev` frontend

This gets us the **first 3 of the 10 priority tasks** (schema.yaml, FastAPI skeleton, hybrid RAG scaffold) running in 2 weeks, on hardware we already have. The cluster becomes a Phase 1 deployment target, not a Phase 0 dependency.

---

## 5. Honest scoring against the original "Approval Ask"

The PRD asks for approval to start **Phase 0 only** — a 2-month validation sprint that answers three questions:
1. Will the selected model perform well enough on bilingual research content?
2. Can we cleanly bridge institutional SSO into the Workbench JWTs?
3. Can we build an IRB gate with <500ms latency?

**My verdict on the three questions:**

| # | Question | Realistic? | Why |
|---|---|---|---|
| 1 | Bilingual model benchmark | **Yes, achievable in 2 weeks** | Qwen 3.6 35B-A3B is already in Dewan Council. Run on 50 golden-set entries, measure BERTScore. |
| 2 | SSO bridge | **Risk: medium** | Depends on whether UPSI SSO is OIDC or SAML (OQ-1 in the appendix). Without that answer in Week 1, Phase 1 slips. |
| 3 | IRB gate latency | **Yes, achievable in 3 weeks** | A small classifier + deterministic rules engine, with the latency benchmarked in LangFuse. <500ms is feasible. |

**The hidden fourth question the PRD does not ask:** "Can the existing team actually deliver this in 12 months, given that the Lead Architect is also running IsRAG, Dewan Council, the INTELIGENSIA book, and the UPSI AI Lab?" The PRD assumes 1.0 FTE for Lead Architect. Realistically that is 0.5 FTE at best. This is the single biggest risk to the whole programme, and it is invisible in the document.

---

## 6. What I will build first, sir — the next 7 days

If you say "go", here is the order:

1. **README.md** — standalone developer README for `suluh-ai/`, written for an engineer who has never read the UPSI PRD. Includes the architecture diagram and the Phase 0 plan.
2. **FastAPI skeleton** (`src/suluh/gateway/`) — JWT validation, RBAC stub, `/health`, `/query`, OpenAPI spec. Run on `localhost:8000`.
3. **Query router v0** (`src/suluh/router/`) — heuristic classifier (no LLM yet) that routes to FAST / PRIMARY / SWARM / ESCALATE. Logs to a JSONL audit file.
4. **Hybrid RAG stub** (`src/suluh/rag/`) — single-table pgvector or even just a JSONL lookup, with a `/retrieve` endpoint. Goal: prove the data flow.
5. **Golden set v0.1** (`research/golden-set-v0.1.jsonl`) — 20–30 Malay/English research queries drawn from the INTELIGENSIA Nusantara corpus and re-written for academic research. This is the first deliverable we can show Dr. Suzani.
6. **IRB gate prototype** (`src/suluh/irb/`) — keyword-based risk classifier for 5 research types, with the latency benchmarked in `benchmarks/irb-gate-latency.md`.
7. **Kicking off Phase 0 work that the PRD assumes but does not schedule** — the SSO protocol discovery email to UPSI ICT (this is a calendar action, not a code action).

---

## 7. Final verdict

**Fork it. Build it. Don't wait for DVC sign-off.**

The PRD is a sound target. The architecture is correct. The principles are right. But the gap between a 38-page PDF and a working system is the same gap that kills most institutional AI programmes: the people who wrote the proposal leave, the procurement takes 6 months, the cluster arrives in pieces, and the next administration has different priorities.

**The standalone `suluh-ai/` repo breaks that cycle.** A working v0.1 on a developer laptop, with IsRAG and Dewan Council as composition layers, can be demoed in 4 weeks. Once Dr. Suzani sees it work, the cluster procurement becomes "scale the working prototype" instead of "build the dream." That is a fundamentally easier decision for DVC R&I to make.

---

*Mes · for Putra Nasution · May 2026 · `suluh-ai/docs/PRD-ANALYSIS.md`*
