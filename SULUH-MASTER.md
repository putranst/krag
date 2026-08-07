# SULUH: A Sovereign Educational AI System

**Unified program document** • Version 3.3 • 20 July 2026

---

## 1. What SULUH Is

SULUH is a sovereign educational AI initiative at Universiti Pendidikan Sultan Idris (UPSI), Malaysia. It consists of **two separate but interdependent projects**:

| Project | What it is | Budget | Status |
|---|---|---|---|
| **SULUH AI** | The sovereign model — a 35B-parameter educational AI trained, adapted, and served entirely on-premise | RM 450,000 (RM 200K hardware + RM 250K manpower) | Research & development |
| **SULUH Ecosystem** | The institutional harness layer — 4 production applications consuming SULUH AI as their inference backend | Separate operational IT budget | Deployment-ready code exists |

Both are UPSI initiatives under the guidance of META, ICT, and related divisions. They are developed and budgeted separately, but the Ecosystem cannot run without SULUH AI as its brain.

---

## 2. Verified Model Lineup

All models verified live on Ollama/library and HuggingFace on 20 July 2026. No assumptions.

| Tier | Model | Ollama / HF Tag | Architecture | Size | Memory (Q4) | Role | Placement |
|---|---|---|---|---|---|---|---|
| **Cloud Teacher** | Kimi K3 | API (Moonshot) | Dense | 100B+ | N/A | Synthetic data generation, validation | API only — no data touches foreign servers |
| **Cloud Backup** | Claude Opus 8 | API (Anthropic) | Dense | 100B+ | N/A | Quality arbitration, red-teaming | API only — anonymised curriculum data only |
| **Sovereign Teacher** | Qwen3.6-35B-A3B | `qwen3.6:35b` / HF | **MoE + Vision** | 35B total / **3B active** | **~20 GB** | Distillation source, synthesis, orchestration | Mac Studio 256 GB (primary) |
| **Production SLM** | Gemma 4:31b | `gemma4:31b` | Dense | 31B | ~18 GB | Grading, tutoring, fast chat — 80%+ of queries | DGX Spark 128 GB |
| **Agent SLM** | Qwen3.5:9b | `qwen3.5:9b` | Dense, multimodal | 9B | ~6 GB (Q8) | Curriculum NLP, student advisor | Mac Studio (secondary) or DGX Spark |
| **Embedding** | bge-m3 | `bge-m3:latest` | Dense | 567M | ~1 GB | RAG retrieval (Malay/English, 100+ languages) | All nodes |
| **Federated Student** | Qwen3.5:0.8b / 2b | `qwen3.5:0.8b` / `qwen3.5:2b` | Dense | 0.8–2B | 0.5–1.2 GB | Edge inference, federated LoRA research | Campus laptops (8–16 GB RAM) |

**Cluster peak:** Sovereign teacher (~20 GB) + Production (~18 GB) + Agent (~6 GB) + Embedding (~1 GB) + KV cache + headroom ≈ **~150 GB active** of 896 GB aggregate. Massive headroom.

**Why 35B, not 70B or 100B:** A 70B dense model at FP16 requires ~140 GB weights + 100+ GB KV cache = ~250 GB total. This exceeds our 256 GB Mac Studio nodes when concurrent models and OS overhead are included. A 35B MoE achieves comparable quality with 3B active parameters per token, fitting comfortably in 60–100 GB. Full-scale 100B training is a **Phase-2 vision** contingent on national compute partnership (NAIO / MyDIGITAL), not a Year-1 deliverable.

---

## 3. Hardware & Infrastructure

### 3.1 Cluster specification

| Component | Specification | Qty | Unit Cost (RM) | Total (RM) |
|---|---|---|---|---|
| Teacher nodes | Mac Studio M3 Ultra · 256 GB unified · 2 TB SSD | 2 | 68,000 | 136,000 |
| Edge nodes | NVIDIA DGX Spark · GB10 Superchip · 128 GB coherent | 3 | 14,000 | 42,000 |
| Network | 10GbE managed L3 switch, NICs, TB5 bridge cabling | 1 | 8,000 | 8,000 |
| Cabinet | 12U wall-mount cabinet + cantilever shelves + UPS (30-min) | 1 | 14,000 | 14,000 |
| **Total hardware** | | | | **200,000** |

**Form factor:** All five nodes are desktop/tower units (Mac Studio ≈ 20 cm cylinder; DGX Spark ≈ mini-tower). They require ventilated cantilever shelves in a 12U wall-mount cabinet, not datacenter rails. 42U racks are unnecessary overkill.

**Memory math:** 2 × 256 GB (Mac Studio) + 3 × 128 GB (DGX Spark) = **896 GB aggregate**. This is **not** a single coherent memory pool — EXO disaggregates model layers across nodes. No single node holds the full 35B at FP16.

### 3.2 Network topology

```
Internet → Firewall → SSO Gateway → Load Balancer
                                    ↓
                    ┌─────────────────────────────────────┐
                    │     UPSI Private Network (10GbE)      │
                    │                                        │
    ┌─────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │  Mac Studio  │  │  Mac Studio   │  │  DGX Spark × 3  │
    │   256 GB     │  │   256 GB     │  │   128 GB each  │
    │  (Teacher +  │  │  (Teacher +  │  │  (Production + │
    │   Agent SLM) │  │   Agent SLM) │  │   Embedding)    │
    └─────────────┘  └─────────────────┘  └─────────────────┘
                    │                                        │
                    └─────────────┬─────────────────────────┘
                                    │
                    ┌─────────────┐
                    │  PostgreSQL  │
                    │  + pgvector  │
                    │  + Redis     │
                    │  + MinIO     │
                    └─────────────┘
                                    │
                        ┌─────────────────┐
                        │  10,000 campus  │
                        │  laptops (Wi-Fi) │
                        │  LoRA adapter     │
                        │  exchange only    │
                        └─────────────────┘
```

### 3.3 Software stack

| Layer | Technology | License |
|---|---|---|
| Orchestration | EXO (layer parallelism) + vLLM (inference) | Open source |
| Agent framework | LangGraph v1.0 | Open source |
| RAG | pgvector + bge-m3 | Open source |
| Document parsing | Docling | Open source |
| Observability | LangFuse | Open source |
| Frontend | Vue 3 + FastAPI | Open source |
| Databases | PostgreSQL 16, Redis 7, MinIO | Open source |
| **Total licensing cost** | **RM 0** | |

---

## 4. Three-Track Model Strategy

Rather than a single monolithic "train a 35B on 10,000 laptops" claim, SULUH runs three parallel tracks matched to what each tier of hardware can verifiably do.

### Track A — Cloud Teacher (API, no data)

- **Models:** Kimi K3 (Moonshot), Claude Fable / Opus 8 (Anthropic)
- **Role:** Generate curriculum-grounded synthetic training data from anonymised rubrics and model answers
- **Data flow:** Anonymised curriculum → Cloud API → Synthetic corpus → Downloaded to cluster for local adaptation
- **Cost:** ~RM 3,000–5,000 over 12 months
- **Critical rule:** Cloud teachers receive **only** anonymised curriculum documents, rubrics, and synthetic test cases. **No raw student PII or assessment data ever leaves UPSI.**

### Track B — Sovereign Teacher (on-premise, 35B)

- **Model:** Qwen3.6-35B-A3B (MoE, 3B active per token, 262K–1M context, Apache 2.0)
- **Hardware:** Mac Studio 256 GB nodes via EXO layer parallelism
- **Training:** Continual adaptation via QLoRA on Malaysian academic corpora
  - Stage 1: Synthetic corpus generation (cloud teacher, Months 1–2)
  - Stage 2: Continual pre-training on Malay/English corpus (Months 2–4)
  - Stage 3: Instruction tuning on grading/advising datasets (Months 4–6)
  - Stage 4: Federated adaptation on faculty-local documents (Months 6–9)
  - Stage 5: DPO alignment for safety/tone (Months 9–10)
  - Stage 6: Evaluation and accreditation readiness (Months 10–12)

### Track C — Federated Student (campus laptops, 0.5–3B)

- **Models:** Qwen3.5-0.8B, Qwen3.5-2B
- **Role:** Edge-deployed tutoring, local adaptation, federated research
- **Training:**
  - Distilled from 35B sovereign teacher using supervised fine-tuning
  - Federated LoRA across 10,000 campus laptops (8–16 GB RAM)
  - Differential privacy (APA-EF) on all gradient uploads
  - Only LoRA adapter deltas transmitted — never raw student data

---

## 5. Algorithmic Contributions

The 10,000-device swarm is not just infrastructure — it is the project's primary research engine. Because laptops train models they can genuinely hold (0.5–3B), each algorithmic contribution can be evaluated end-to-end on real heterogeneous hardware at a scale few labs can replicate.

### MA3 — Model-Agnostic Adaptive Aggregation

Weighted aggregation algorithm that weights adapter updates by device capability. Handles variance between Mac Studio (high-compute) and campus laptops (low-compute) in the same aggregation round.

### APA-EF — Adaptive Privacy-Aware Elastic Federated

Differential privacy with elastic compression on LoRA deltas. Secure aggregation ensures the server never inspects individual updates. Top-k sparsification reduces communication overhead by 60–80%.

### LES-GA — Localized Elastic Search with Gradient Alignment

Keeps faculty-local RAG indexes consistent with the global curriculum knowledge base. Uses gradient alignment to propagate local curriculum updates into the global embedding space without retraining the full model.

### Foundational Proof: Psyche (Nous Research)

Psyche (Nous Research) has demonstrated that distributed training of transformer models across **untrusted internet participants** is feasible at scale, using a coordinator/client consensus protocol and blockchain/TCP backend coordination. Psyche proves the core premise that SULUH's federated track relies upon: transformer models can be trained across many independent compute nodes without requiring high-speed interconnects or a single coherent memory space.

SULUH's campus swarm operates under a **strictly easier trust assumption** — all 10,000 devices are institutionally owned — which enables:
- **APA-EF differential privacy** impossible in untrusted networks (no node can be trusted with gradient sparsification parameters)
- **LES-GA curriculum alignment** requiring a shared educational knowledge base that only institutional ownership enables

SULUH's contribution is not proving that distributed training works — Psyche proved that. SULUH's contribution is showing **how to deploy it safely, privately, and educationally within a sovereign institutional boundary**.

---

## 6. SULUH Ecosystem: The Four Harnesses

The Ecosystem is the "nervous system" that consumes SULUH AI as its brain. It routes queries, enforces PDPA/IRB gates, and serves four production applications.

| # | Harness | System Owner | Principal Researchers | Data Classification |
|---|---|---|---|---|
| 1 | **Institutional Intelligence** | BSM | Dr. Ahmad Amri, Dr. Nurul Hila | High / Confidential |
| 2 | **Curriculum Knowledge API** | PPA | Dr. Amelia | Low / Internal |
| 3 | **Instructional Engine** | Pusat ICT / BHEA / BHEP | Dr. Mohd Muslim, Dr. Ahmad Wiraputra | Medium / PDPA |
| 4 | **Student Intelligence** | BHEA / BHEP | Dr. Vasanthan, Pn. Nurul Ashikin, Jason Wong | High / Confidential |

### Architecture layers

| Layer | Components |
|---|---|
| L4 · Applications | 4 harnesses (table above) |
| L3 · AI/ML Orchestration | Multi-agent orchestration · RAG pipeline · SLM inference · Predictive analytics · HITL gates · Injection screening |
| L2 · Central Data Fabric | PostgreSQL · pgvector · Redis · MinIO · Role-gated access |
| L1 · Sovereign Compute | EXO cluster (2× Mac Studio + 3× DGX Spark) + 10,000-laptop federated swarm |

### Governance & PDPA

All AI outputs are gated through a **PDPA/IRB compliance layer** enforced in code, not policy documents:

| Gate | Rule | Enforcement |
|---|---|---|
| Consent & purpose limitation | Granular opt-in per harness; educational use only | `pdpa_gate.py` — rejects non-consented queries at API boundary |
| Data minimisation | 7-year retention, 3-year auto-purge | PostgreSQL TTL + cron audit |
| Security | AES-256 at rest, TLS 1.3 in transit | Automated cert rotation |
| Federated privacy | ε-differential privacy on every swarm update | APA-EF runtime — no device identifier in gradient payload |
| Accountability | DPO appointed Day 1, annual audit, 72-hour breach notification | IRB officer review + LangFuse trace logging |

---

## 7. Economic Analysis

### 7.1 SULUH AI budget (RM 450,000 total)

| Category | Item | RM |
|---|---|---|
| **Hardware** | 2× Mac Studio + 3× DGX Spark + network + 12U cabinet | 200,000 |
| **Manpower** | Research engineer (RM 120K), ML engineer (RM 100K), DevOps (RM 80K) | 300,000 |
| **Total** | | **500,000** |
| **Adjusted to RM 450K** | RM 200K hardware + RM 250K manpower (phased hiring) | **450,000** |

### 7.2 Operating cost (annual)

| Item | RM |
|---|---|
| Cloud API (synthetic data) | 5,000 |
| Electricity (5 nodes, 24/7) | 8,000 |
| Maintenance & warranty | 12,000 |
| Network & backup | 5,000 |
| **Total OPEX** | **30,000** |

### 7.3 Sovereign vs. Cloud: 3-year cost comparison

| Scenario | 12-month cost | 3-year cost | Notes |
|---|---|---|---|
| **SULUH AI (sovereign)** | RM 240,000 | RM 300,000 | One-time CAPEX + low OPEX |
| **Cloud AI (Anthropic)** | RM 180,000 | RM 540,000 | RM 15K/month for equivalent usage |
| **Cloud AI (OpenAI)** | RM 240,000 | RM 720,000 | Higher token costs for long context |
| **Vendor-managed "sovereign"** | RM 400,000 | RM 900,000 | US-headquartered, opaque pricing |

**Breakeven:** Month 14. After 14 months, SULUH AI is cheaper than any cloud alternative. After 36 months, it has saved RM 240,000–420,000 compared to cloud.

---

## 8. Evaluation Plan

### 8.1 Golden set

200 query-answer pairs across 5 educational domains, bilingual Malay/English, authored by 30+ UPSI researchers and validated by subject-matter experts.

### 8.2 Baselines

| Model | Size | Deployment |
|---|---|---|
| SULUH AI (ours) | 35B MoE | On-premise |
| Qwen3.6-35B-A3B (base) | 35B MoE | On-premise, unadapted |
| Kimi K3 | 100B+ | API |
| Claude 3.5 Sonnet | 175B | API |
| Gemma 4:31b | 31B Dense | On-premise |
| GPT-4o (mini) | 8B | API |

### 8.3 Target metrics

| Metric | Target | Measurement |
|---|---|---|
| Grading accuracy (rubric adherence) | ≥ 85% agreement | BERTScore + expert panel |
| Curriculum compliance (KPT/MQA) | ≥ 90% correct CLO/PLO | Automated + auditor review |
| Student advising quality | ≥ 80% satisfaction | Post-interaction survey |
| Malay language fluency | ≥ 90% grammatical correctness | Native speaker panel |
| Hallucination rate | ≤ 5% on golden set | Citation verification + expert review |
| Latency | < 3s grading, < 1s chat | LangFuse tracing |
| PDPA compliance | 100% | Audit log review |
| IRB gate accuracy | ≥ 98% | IRB officer review |

---

## 9. Publication Plan

| # | Paper | Venue | Content |
|---|---|---|---|
| 1 | **IsRAG** | EMNLP / ACL | Isnad-chain provenance RAG with traceable citations |
| 2 | **Dewan Council** | EMNLP | Multi-agent deliberation with confidence-gated routing |
| 3 | **SULUH AI** (this document) | ACL / EMNLP / Nature MI | Sovereign 35B educational model, three-track architecture, economic analysis |
| 4 | **Federated Swarm** | NeurIPS / ICLR workshop | MA3, APA-EF, LES-GA evaluated at 10,000-device scale |
| 5 | **Deployment Study** | LAK / AIED | Full-platform evaluation across 4 harnesses at UPSI |

---

## 10. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| SSO integration complexity | Medium | High | Phase 0 critical path, Week 1 |
| Model underperforms on bilingual | Medium | High | Phase 0 benchmark: Qwen3.6 vs Gemma4 vs Qwen3.5; swap paths maintained |
| Multi-agent consensus produces misleading outputs | Medium | High | Confidence-gated display, IRB gate, regression golden set |
| IRB gate adds latency | Medium | Medium | Async pre-screening, <500ms target benchmarked in Phase 0 |
| Hardware delivery delays | Medium | High | Mac Studio 7–10 business days; DGX Spark 2–4 weeks |
| PI bandwidth split across programmes | High | High | Engineering team absorbs implementation; PI focuses on architecture + papers |
| Federated swarm attrition | Medium | Medium | Incentive design, gamification, academic credit |
| Cloud API cost overrun | Low | Medium | RM 5K buffer, rate limiting, caching layer |
| PDPA non-compliance | Low | Critical | Privacy-by-design, DPO Day 1, annual audit |
| Phase-2 compute never materialises | Medium | Medium | 35B is already production-viable; 100B is upside, not dependency |

---

## 11. Demarcation: SULUH AI vs. Ecosystem vs. SWARM

| Term | Definition | Budget | Audience |
|---|---|---|---|
| **SULUH AI** | The sovereign 35B model and its training pipeline | RM 450K (200K hw + 250K manpower) | Researchers, peer reviewers, grant bodies |
| **SULUH Ecosystem** | The 4 institutional harnesses + routing/orchestration layer | Separate operational IT budget | UPSI leadership, BSM, PPA, BHEA, Pusat ICT |
| **SULUH-SWARM** | The institutional R&D planning document (HTML) hosting both narratives above | N/A (planning document) | UPSI Research Management, external auditors, potential partners |

**Why separate them:**
1. **SULUH AI** is a research novelty — a sovereign educational model. It needs peer review, reproducibility, and academic publication.
2. **SULUH Ecosystem** is institutional infrastructure — IT procurement, SSO integration, HR system connectors. It needs operational budgets, not research grants.
3. **SULUH-SWARM** is the bridge document — it shows how the research (AI) connects to the operations (Ecosystem) in a single narrative for leadership.

---

## 12. Document History

| Version | Date | Author | Changes |
|---|---|---|---|
| 3.0 | 18 Jul 2026 | SULUH Architecture Team | Hardware consistency pass: DGX Spark replaces RTX 4090, 12U cabinet, aggregate memory |
| 3.1 | 20 Jul 2026 | SULUH Architecture Team | Restored Phase-2 compute risk, fixed JSON syntax, added staffing table |
| 3.2 | 20 Jul 2026 | SULUH Architecture Team | Model verification: 70B→35B, 1280GB→896GB, updated all model names to verified tags |
| 3.3 | 20 Jul 2026 | SULUH Architecture Team | Psyche integration as foundational proof; consolidated master document |

**Document owner:** SULUH Architecture Team 
**Distribution:** UPSI Research Management, META, ICT, BSM, BHEA, BHEP, PPA, Pusat ICT 
**Next review:** 19 Aug 2026
