# SULUH Ecosystem — Consolidated Research Proposal

**Programme:** Sovereign Multi-Agent AI for Higher Education Research: The SULUH Ecosystem
**Principal Investigator:** Putra Nasution
**Academic Lead / Co-PI:** Dr. Suzani binti Mohamad Samuri (Universiti Pendidikan Sultan Idris, Faculty of Meta)
**Programme duration:** 12 months (with 12-month extension option)
**Total budget request:** RM 285,000 (~USD 60,000)
**Submission target:** UPSI DVC R&I, MOHE Fundamental Research Grant Scheme (FRGS), ASEAN higher-education consortium

---

## Executive Summary

Malaysian universities cannot legally process research data through foreign cloud AI services under PDPA 2010, yet they need AI to remain competitive. The SULUH Ecosystem solves this paradox by providing a sovereign, on-premise, multi-agent AI platform purpose-built for higher education research.

The Ecosystem integrates three open-source packages developed in this programme:

- **IsRAG** (*Isnad-chain Retrieval Augmented Generation*) — provenance-tracked, trust-scored, culturally-aware retrieval
- **Dewan Council** — multi-LLM deliberation with auditable dissent
- **SULUH AI** — the orchestration platform: gateway, router, LangGraph workflows, PDPA + IRB gates, Vue 3 Workbench

All three packages are open-source (Apache 2.0), composable, and designed for institutional reuse. The programme produces 1 unified proposal, 3 peer-reviewed papers, 1 working 12-month pilot at UPSI, and a reusable consortium expansion model for partner institutions.

---

## 1. Research Problem

### 1.1 The sovereignty paradox
Higher education institutions in Malaysia face a regulatory paradox:
- Research data (participant records, ethics approvals, pre-publication manuscripts, indigenous knowledge) cannot legally be processed by foreign cloud AI services
- Without AI, research productivity, reproducibility, and competitiveness decline
- Local GPU workstations are underutilised, fragmented, and produce irreproducible results

### 1.2 What is missing
There is no open, sovereign, PDPA-compliant multi-agent AI platform designed for higher education research. Existing solutions are:
- Foreign cloud (regulatory risk)
- Vendor-managed (institutional lock-in, opaque)
- Ad-hoc local (unsustainable, irreproducible)

### 1.3 Research questions
The programme answers four research questions:

| # | Question | Addressed by |
|---|---|---|
| RQ1 | Does provenance-tracked retrieval (IsRAG) measurably improve trust calibration, accuracy, and cultural appropriateness over standard RAG? | Paper 1 |
| RQ2 | Does multi-LLM deliberation with structured dissent (Dewan Council) produce more auditable and more accurate answers than single-LLM or naive-aggregation baselines? | Paper 2 |
| RQ3 | Can a reference architecture for sovereign multi-agent AI be deployed in a public university in 12 months, satisfying PDPA and IRB by design? | Paper 3 |
| RQ4 | Can the architecture federate across institutions without data centralisation? | Phase 3 consortium spec |

---

## 2. Programme Objectives

### 2.1 Primary objective
Develop, deploy, and evaluate a sovereign multi-agent AI platform for Malaysian higher education research, validated through a 12-month pilot at UPSI, with three peer-reviewed paper contributions and a consortium expansion roadmap.

### 2.2 Specific objectives

1. **Develop IsRAG** as a working open-source package with full provenance chains, trust scoring, and cultural context. Validate against standard RAG baselines.
2. **Develop Dewan Council** as a working open-source multi-LLM deliberation protocol with auditable dissent. Validate against single-LLM and majority-vote baselines.
3. **Develop SULUH AI** as the composition platform: FastAPI gateway, query router, LangGraph swarm coordinator, PDPA + IRB gates, Vue 3 Workbench.
4. **Deploy at UPSI** for 12 months across 275 research staff and 2,400+ graduate students. Measure adoption, accuracy, compliance, latency.
5. **Publish 3 peer-reviewed papers** targeting ACL/EMNLP/FAccT, AAMAS/NeurIPS, and FAccT/AIES.
6. **Document a consortium expansion model** so partner institutions (UTM, UM, NTU, others) can deploy their own instances and federate.

---

## 3. Methodology

### 3.1 Build-first, validate-second approach
The programme follows a disciplined build-validate-deploy cadence. No phase begins until the previous phase's exit gate is passed.

| Phase | Months | Focus | Exit gate |
|---|---|---|---|
| **Phase 0** | 1–2 | Foundation: SSO, schema, FastAPI skeleton, bilingual benchmark, IRB prototype, 50-entry golden set | SSO validated, schema.yaml merged, FastAPI skeleton passing, Phase 0 benchmark report accepted, IRB workflow prototype validated, golden set v0.1 at 50 entries |
| **Phase 1** | 3–6 | Core capabilities: IsRAG, Dewan Council, hybrid RAG, Text-to-SQL, Docling, Agent Registry, Chat Workbench, LangFuse | All Tier 1–3 components on staging, Month 6 metrics gate passed |
| **Phase 2** | 7–10 | Agentic workflows: all three LangGraph workflows, 200-entry golden set, regression CI, IRB Audit Dashboard | Three workflows live, Month 10 metrics passed |
| **Phase 3** | 11–12 | Full production: 75% adoption, Admin Console, consortium API documented, post-go-live monitoring | 75% adoption achieved, consortium API tested, Month 12 metrics passed |

### 3.2 Evaluation infrastructure
- **Golden set** (200 entries): 30+ researchers author queries across 5 domains (agriculture, Islamic finance, indigenous land rights, public health, digital governance), bilingual Malay/English
- **BERTScore evaluator**: automated accuracy scoring
- **SQL correctness evaluator**: text-to-SQL validation
- **Swarm success evaluator**: LangFuse workflow trace review
- **PDPA compliance score**: audit log review (target: 100% every month)
- **IRB gate accuracy**: IRB officer review of gate decisions (target: 98% by Month 12)
- **User study**: pre/post trust calibration with 100+ participants

### 3.3 Theoretical framework
The programme draws on three theoretical traditions:
1. **Islamic epistemology (Isnad/Chain of Transmission):** the 1,000-year tradition of knowledge validation through documented, rated transmission chains
2. **Decolonial AI theory:** the critique that AI systems embed Western epistemological assumptions and exclude non-Western knowledge systems
3. **Trust calibration in information systems:** research on how users calibrate trust in algorithmic systems and why provenance transparency increases appropriate reliance

---

## 4. The Ecosystem (technical contribution)

### 4.1 Three packages, one research programme

| Package | Type | Function | Paper |
|---|---|---|---|
| **IsRAG** | Retrieval | Provenance + trust + cultural context | Paper 1 |
| **Dewan Council** | Deliberation | Multi-LLM with auditable dissent | Paper 2 |
| **SULUH AI** | Platform | Orchestration + compliance + UX | Paper 3 |

### 4.2 The 4-tier architecture
Tier 1 (user) → Tier 2 (FastAPI gateway) → Tier 3 (orchestration: router, swarm, RAG, deliberation, PDPA, IRB) → Tier 4 (data: pgvector, MinIO, LangFuse, Redis). Cloud quality layer is optional, <5% of traffic, anonymised only, never RESTRICTED data.

### 4.3 The 7 immutable design principles
Sovereign by default · Read-only by design · Hybrid retrieval · Document intelligence mandatory · Auditability over novelty · Evaluation-driven deployment · Model-agnostic architecture. These are operationalised in code, not configuration.

### 4.4 Hardware
5-node EXO cluster: 3× NVIDIA DGX Spark (128 GB each, edge) + 2× Apple Mac Studio M3 Ultra (256 GB each, core). 896 GB aggregate memory (512 GB Mac Studio + 384 GB DGX Spark). EXO layer parallelism distributes inference across nodes; memory is not pooled into a single coherent space. 10GbE Ethernet backbone. All on-premise.

### 4.5 Open-source stack
Qwen3.6-35B-A3B (sovereign teacher, MoE, Apache 2.0) · Gemma 4:31b (production SLM, dense, multimodal) · Qwen3.5:9b (agent SLM, multilingual) · bge-m3 (embedding, 567M, 100+ languages) · LangGraph v1.0 · Docling · pgvector · LangFuse · Vue 3 · FastAPI · EXO · vLLM. RM 0 licensing.

---

## 5. Team

| Role | Allocation | Responsibilities |
|---|---|---|
| **Putra Nasution** — Lead Architect & PI | 1.0 FTE · 12 months | Programme design, all architecture and code, paper authorship |
| **Engineering team (remote)** | 0.5 FTE · 12 months | Frontend (Vue 3 Workbench), testing, documentation, LangFuse instrumentation |
| **Dr. Suzani Mohamad Samuri** — Oversight Director / Co-PI | 50% · 12 months | Technical architecture oversight, IRB gate validation, paper co-authorship, stakeholder engagement |
| **Agentic Engineering Platform** | Continuous | Schema introspection, scaffolding, test generation across all workstreams |
| **UPSI DBA Team** | 20% Phase 0–1 | PostgreSQL replication setup, AI read replica provisioning |
| **UPSI Research Community** | 20% Phase 0 | Golden set authorship, query validation, feedback |
| **UPSI IRB / Ethics Committee** | Milestone-based | Ethics workflow review, IRB gate validation, compliance attestation |
| **UPSI Legal & Compliance** | Milestone-based | PDPA compliance sign-off, audit engagement |

---

## 6. Budget

| Category | Component | Timing | Nature | RM |
|---|---|---|---|---|
| **Hardware (one-time)** | 3× NVIDIA DGX Spark Founders Edition (128 GB, 4 TB each) — edge | Phase 0 | CAPEX | 90,000 |
| **Hardware (one-time)** | 2× Apple Mac Studio M3 Ultra (256 GB) — core | Phase 0 | CAPEX | 60,000 |
| **Hardware (one-time)** | Networking (ConnectX-7 200GbE), rack, UPS, storage upgrade | Phase 0 | CAPEX | 25,000 |
| **Software** | Open-source stack (RM 0 licensing) | Ongoing | OPEX | 0 |
| **Cloud (optional)** | Anthropic Claude API (<5% queries, anonymised) | Phase 1+ | OPEX | 5,000 |
| **Personnel** | Engineering team (0.5 FTE × 12 months) | 12 months | Professional fees | 60,000 |
| **Training & Change** | Researcher workshops, user documentation, IRB training | Phase 2–3 | OPEX | 15,000 |
| **Travel & Publication** | Conference fees, open-access publication fees | 12 months | OPEX | 20,000 |
| **Contingency** | ~3.5% | — | — | 10,000 |
| **TOTAL** | | | | **285,000** |

**Note:** PI effort is in-kind. OpenRouter API costs for Dewan Council research are covered by existing research credits.

---

## 7. Timeline

```
Month:  1    2    3    4    5    6    7    8    9   10   11   12
        │    │    │    │    │    │    │    │    │    │    │    │
Phase 0 ████████▌
              │ IsRAG MVP  │Dewan v0.1│SULUH GW│Bench│
              │            │          │       │mark │
        ─────┼────────────┼──────────┼───────┼─────┤
Phase 1               ████████████▌
                            │Hybrid RAG │SQL│Docling│Reg│Workbench│
                            │           │  │       │ist│         │
        ─────────────────────┼──────────┼──┼───────┼───┼─────────┤
Phase 2                              ████████████▌
                                         │Swarm│Exp│IRB│Eval│
                                         │WFs  │Auto│Aud│Har │
        ──────────────────────────────────┼─────┼───┼───┼────┤
Phase 3                                          ████████████▌
                                                      │Prod│Adopt│Conso│
                                                      │roll│ion  │rtium│
        ───────────────────────────────────────────────┼─────┼─────┼────┤
Papers    Paper 1 draft (M4)        Paper 1 submit (M7) │Paper 2 (M9)  Paper 3 (M12)
```

---

## 8. Expected Outcomes

### 8.1 Academic outputs
- 3 peer-reviewed papers (target venues: ACL/EMNLP/FAccT, AAMAS/NeurIPS, FAccT/AIES)
- 1 open-source ecosystem (3 packages, Apache 2.0)
- 1 reusable 200-entry bilingual golden set (CC-BY 4.0)
- 2–3 supervised Master's/PhD theses
- 1 consortium expansion playbook

### 8.2 Institutional impact
- 15,000–35,000 productive hours returned to UPSI research community per year (8–18 FTE equivalent)
- 75% adoption rate among research staff and graduate students
- 100% PDPA compliance, 98% IRB gate accuracy
- 90% swarm task success rate
- Position UPSI as the first Malaysian university to deploy a sovereign, PDPA-compliant multi-agent AI research platform on a 1,280 GB distributed cluster

### 8.3 Strategic impact
- Reference implementation for Malaysia National AI Agenda 2026–2030
- Template for SEA consortium expansion (UTM, UM, NTU, others)
- Foundation for ASEAN sovereign AI research infrastructure
- Provenance-aware, culturally-grounded AI as a contribution to the global decolonial AI movement

---

## 9. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| SSO integration complexity | Medium | High | Phase 0 critical path, Week 1; Phase 1 cannot begin until validated |
| Model underperforms on bilingual | Medium | High | Phase 0 benchmark: Qwen3.6 vs Gemma4 vs Qwen3.5; architecture swap path maintained |
| Multi-agent consensus produces misleading outputs | Medium | High | Confidence-gated display, IRB gate, regression golden set gates every deployment |
| IRB gate adds latency | Medium | Medium | Async pre-screening, fast-path for non-human-subject, <500ms target benchmarked in Phase 0 |
| PI bandwidth split across programmes | High | High | Engineering team absorbs implementation; PI focuses on architecture + papers |
| Hardware procurement delay | Medium | High | 6-week fast-track; Phase 0 runs on a single Mac if cluster slips |

---

## 10. Why now

Four forces converge in 2026:
1. **Open-source AI crossed the commercial threshold.** Qwen3.6-35B-A3B, Gemma 4:31b, and Qwen3.5:9b are production-viable. Self-hosted is no longer a compromise.
2. **Multi-agent orchestration matured.** LangGraph v1.0 (October 2025) is production-deployed at LinkedIn, Replit, Elastic. The pattern is now well-understood.
3. **PDPA enforcement is tightening.** On-premise AI is the durable answer. Waiting until enforcement catches up means rushed, expensive retrofitting.
4. **Malaysia National AI Agenda 2026–2027 funding window is open.** First-mover institutions with documented architecture receive priority consideration. Delay risks losing the matched funding.

---

## 11. Ethical considerations

- The programme is reviewed by the UPSI IRB Committee at every phase gate
- All human-subject research workflows are IRB-gated in the system itself, not just in policy
- The golden set is CC-BY 4.0 with author consent; no PII in any test data
- The pilot study on adoption and trust calibration has its own IRB approval (separate submission)
- The codebase, golden set, and architecture documents are released under Apache 2.0 and CC-BY 4.0 respectively, for institutional reuse

---

## 12. Conclusion

The SULUH Ecosystem is a single research programme with three paper-level contributions and one institutional pilot. It addresses a real and growing problem — the sovereignty gap in higher education AI — with a complete, deployable, open-source solution. The architecture is grounded in a 1,000-year-old epistemology (Isnad) and 21st-century compliance requirements (PDPA, IRB). The 12-month timeline is disciplined, the budget is capital-light, the team is in place, and the impact is institutional, national, and regional.

We seek approval to begin Phase 0 immediately.

---

## Appendices (available separately)

- A. Architecture diagrams (4-tier, swarm workflow, query routing, cluster topology)
- B. Code repository structure (suluh-ecosystem monorepo)
- C. Golden set authoring protocol
- D. IRB pre-screen model training plan
- E. Cost model: sovereign vs cloud
- F. Letters of support (UPSI DVC R&I, consortium partners)

---

**Submitted by:**
Putra Nasution — Lead Architect & Principal Investigator
poetra@gmail.com · +62 81***0629

**Co-signed by:**
Dr. Suzani binti Mohamad Samuri — Oversight Director & Co-Principal Investigator
Universiti Pendidikan Sultan Idris, Faculty of Meta
