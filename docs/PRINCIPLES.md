# Seven Immutable Design Principles

> Every technical decision in SULUH flows from these seven principles. They are not preferences — they are constraints. Any proposal that violates them requires a formal Steering Committee design amendment.

---

## 01 · Sovereign by default

All research data, agent state, model weights, and institutional documents remain within Malaysian jurisdiction and the deploying institution's network perimeter. No raw research data or participant records traverse the public internet under any condition.

**Operationalised in code:**
- `suluh.pdpa.masker.scan_at_ingress()` — runs on every query and every tool output
- `suluh.pdpa.fail_closed()` — if the masker errors, the query is blocked, not passed through
- `suluh.gateway.outbound_allowlist` — environment variable restricting outbound internet; only `api.anthropic.com` permitted, and only from the quality router

---

## 02 · Read-only by design

AI agents can recommend, analyse, synthesise, and generate — but they cannot write to production research databases, ethics systems, or institutional records. The only path to write capability is a formal design amendment with Steering Committee approval.

**Operationalised in code:**
- `suluh.registry.tools.yaml` — contains zero write-capable tool definitions in Phase 2
- Adding a write tool requires dual approval: Lead Architect + Oversight Director
- The AI read replica is enforced at the database role level, not at the application level

---

## 03 · Hybrid retrieval, not pure RAG

Research systems require vector search for documents AND SQL generation for structured data AND deterministic controls for compliance. Pure semantic RAG will produce incorrect research outputs.

**Operationalised in code:**
- `suluh.rag.hybrid_retrieve()` always runs vector + SQL in parallel, then merges
- `israg.IsRAGEngine.retrieve()` accepts a `mode` parameter: `vector | sql | hybrid`
- The Text-to-SQL engine has a 5-stage sandbox (sqlglot parse, table allowlist, statement-type allowlist, row-limit, query timeout)

---

## 04 · Document intelligence is mandatory

Document OCR, table extraction, figure extraction from research papers, grant proposals, and scanned documents are first-class requirements — not Phase 2 enhancements.

**Operationalised in code:**
- `suluh.docling` ships with the gateway, not as a separate service
- All uploaded documents pass through Docling before pgvector indexing
- Documents below 0.75 confidence are excluded from retrieval until human-approved (HITL review queue in Admin Console)

---

## 05 · Auditability over novelty

Every agent action must be explainable, attributable to a source agent and model version, and logged to the immutable audit trail. IRB and reproducibility compliance is non-negotiable.

**Operationalised in code:**
- `ai_audit_log` table is PostgreSQL-immutable (trigger blocks UPDATE/DELETE)
- Every LangGraph node emits a LangFuse span with: agent_id, model_version, prompt_version, retrieved_docs_hash, output_hash
- The IsRAG IsnadChain is attached to every response, not optional

---

## 06 · Evaluation-driven deployment

No model, retrieval configuration, prompt change, or agent workflow reaches production without passing the regression gate against the golden evaluation set.

**Operationalised in code:**
- `eval/golden_set.jsonl` is the single source of truth for "is this change safe?"
- CI pipeline blocks any PR that does not pass the golden set benchmark
- The golden set is expanded by the research community (50 → 200 → 500 entries across phases)

---

## 07 · Model-agnostic architecture

Switching the primary inference model requires updating one config value — not rewiring the orchestration or retrieval layers. Swap paths are maintained for all models.

**Operationalised in code:**
- `suluh.config.models.yaml` is the single config source
- The model identifier is passed to the inference backend, not hardcoded in code
- Phase 0 benchmark evaluates three candidates: Qwen3.6-35B-A3B (sovereign teacher), Gemma 4:31b (production SLM), Qwen3.5:9b (agent SLM)
- The OpenRouter adapter pattern (used by `council`) is the template for new model adapters

---

## How a change is reviewed

A pull request that touches any of these principles must:

1. Reference this document in the PR description
2. Include an explicit "Principle Compliance" section
3. Be approved by the Lead Architect AND the Oversight Director
4. Be recorded in the Steering Committee decision log

There are no exceptions. If a research use case seems to require violating a principle, the right answer is to amend the principle, not bypass it.

---

*This document is signed by the Lead Architect and the Oversight Director. It cannot be modified without a Steering Committee vote.*
