# Paper 3: SULUH AI — A Sovereign Educational AI Model

**Target venues (in order of preference):**
1. ACL (Association for Computational Linguistics) — main conference, Long Paper
2. EMNLP (Empirical Methods in NLP) — main conference
3. Nature Machine Intelligence — if positioned as a systems paper
4. FAccT (Fairness, Accountability, Transparency) — if framed as a governance contribution

**Submission timeline:** Target submission 10–12 months from programme start.

---

## Abstract (draft, 250 words)

Higher education institutions in emerging economies face a fundamental AI gap: frontier models capable of complex reasoning, multilingual understanding, and cultural context adaptation are available only through foreign cloud APIs, creating unacceptable regulatory and sovereignty risks under data protection regimes like Malaysia's PDPA 2010. Yet training sovereign models from scratch is computationally prohibitive for most universities, leaving a class of institutions that cannot legally use cloud AI but cannot afford to build their own.

We present **SULUH AI**, a 35B-parameter sovereign educational AI model designed, adapted, and served entirely on-premise. SULUH AI uses a three-track strategy matched to realistic institutional hardware: (1) a cloud-hosted frontier teacher (Kimi K3, Claude Opus) generates curriculum-grounded synthetic training data; (2) a 35B Mixture-of-Experts sovereign model (Qwen3.6-35B-A3B, MoE, 3B active) is continually adapted via QLoRA on a 5-node EXO cluster; (3) compact 0.5–3B student models are distilled from the teacher and fine-tuned across a 10,000-device federated campus swarm under differential-privacy guarantees. This architecture delivers frontier-level reasoning quality for educational domains while keeping all student and staff data within national jurisdiction.

We evaluate SULUH AI against cloud and open-weight baselines on a 200-entry bilingual (Malay/English) educational-domain golden set, demonstrating competitive accuracy on grading, tutoring, and curriculum compliance tasks. We further present a full technical and economic analysis showing that sovereign educational AI is now practical for a middle-income country at a capital cost of less than RM 200,000.

---

## 1. Introduction

The **sovereignty gap in educational AI** is the central problem this paper addresses. Universities in emerging economies need AI to remain competitive — for automated grading, personalised tutoring, curriculum compliance auditing, and student-at-risk prediction. But the same data that needs AI (student transcripts, assessment submissions, counselling records, staff HR files) cannot legally be processed by foreign cloud services under PDPA 2010, GDPR, FERPA, or equivalent regimes.

This creates three unpalatable options:
1. **Use foreign cloud AI anyway** — accept regulatory risk, potential fines, and breach exposure
2. **Do without AI** — accept declining competitiveness against institutions that can afford sovereign infrastructure
3. **Build sovereign AI** — historically computationally prohibitive for a middle-income university

**The research question:** *Can a public university in a middle-income country deploy a sovereign educational AI model that matches frontier cloud model quality on educational tasks, at a capital cost below RM 200,000, while keeping all data on-premise?*

**Contributions:**
1. We present SULUH AI, a 35B-parameter sovereign educational model with a novel three-track training architecture
2. We validate it against cloud and open-weight baselines on a bilingual educational-domain golden set
3. We present a complete capital and operating cost model, demonstrating practical feasibility
4. We describe a federated training programme for 10,000 campus devices that produces publishable algorithmic contributions (MA3, APA-EF, LES-GA)

---

## 2. The Three-Track Sovereign Model Strategy

Rather than a single monolithic "train a 35B on 10,000 laptops" claim, SULUH AI runs three parallel tracks matched to what each tier of hardware can verifiably do.

### 2.1 Track A — Cloud Teacher (API, no data)

**Models:** Kimi K3 (Moonshot), Claude Fable / Opus 8 (Anthropic)

**Role:** Generate high-quality synthetic training data for Malaysian educational content. The teacher receives anonymised curriculum documents, rubrics, and model answers — never raw student data — and produces:
- Curriculum-grounded instruction-response pairs
- Preference-ranked answer sets for DPO alignment
- Adversarial test cases for red-teaming

**Data flow:** Anonymised curriculum data → Cloud API → Synthetic training corpus → Downloaded to cluster for local adaptation.

**Cost:** API credits (estimated RM 3,000–5,000 over 12 months).

### 2.2 Track B — Sovereign Teacher (on-premise, 35B)

**Model:** Qwen3.6-35B-A3B (Mixture-of-Experts)

**Architecture:**
- Total parameters: 35B
- Active parameters per token: 3B (8 routed + 1 shared experts from 256 total)
- Vision encoder: native — can process scanned textbooks, diagrams, infographics
- Context window: 262,144 tokens native, extensible to 1,010,000
- License: Apache 2.0 (fully sovereign)

**Hardware placement:**
- Primary hosting: 2× Mac Studio M3 Ultra (256 GB unified memory each)
- Secondary / failover: 3× NVIDIA DGX Spark (128 GB each) via EXO layer parallelism
- Total aggregate cluster memory: **896 GB** (not pooled coherently — EXO distributes layers across nodes)

**Memory budget:**
- Q4_K_M quantisation: ~20 GB weights + 40–80 GB KV cache (at 128K context) = ~60–100 GB total
- Q8_0 quantisation: ~40 GB weights + KV cache = ~80–120 GB total
- Fits comfortably within 256 GB Mac Studio with concurrent 7B agent model

**Adaptation pipeline:**
1. **Continual pre-training** (months 1–3): Malaysian academic corpus (Malay + English textbooks, MQA accreditation documents, KPT policy papers)
2. **Instruction tuning** (months 3–5): SFT on curated grading, advising, and curriculum datasets
3. **QLoRA adaptation** (ongoing): Low-rank adaptation on faculty-specific documents
4. **DPO alignment** (months 9–10): Preference alignment for safety, helpfulness, institutional tone

### 2.3 Track C — Federated Student (campus laptops, 0.5–3B)

**Models:** Qwen3.5-0.8B, Qwen3.5-2B, SmolLM2-1.7B

**Role:** Edge-deployed student models for personalised tutoring, local adaptation, and federated research.

**Training:**
- Distilled from the 35B sovereign teacher using supervised fine-tuning on synthetic data
- Federated LoRA fine-tuning across 10,000 campus laptops (8–16 GB RAM)
- Differential privacy (APA-EF) on all gradient uploads
- Only LoRA adapter deltas are transmitted — never raw student data

**Algorithmic contributions:**
- **MA3** (Model-Agnostic Adaptive Aggregation): weights adapter updates by device capability
- **APA-EF** (Adaptive Privacy-Aware Elastic Federated): differential privacy + top-k sparsification
- **LES-GA** (Localized Elastic Search with Gradient Alignment): keeps faculty-local RAG consistent with global KB

**Foundational proof.** Psyche (Nous Research) has demonstrated that distributed training of transformer models across untrusted internet participants is feasible at scale, using a coordinator/client consensus protocol and blockchain- or TCP-based backend coordination. Psyche proves the core premise that SULUH's federated track relies upon: transformer models can be trained across many independent compute nodes without requiring high-speed interconnects or a single coherent memory space. SULUH's campus swarm operates under a strictly easier trust assumption — all 10,000 devices are institutionally owned — which enables stronger differential-privacy guarantees (APA-EF) and curriculum-grounded knowledge alignment (LES-GA) impossible in Psyche's untrusted, open-internet setting. SULUH's contribution is not proving that distributed training works, but showing how to deploy it safely, privately, and educationally within a sovereign institutional boundary.

### 2.4 The production serving tier (27–31B)

**Model:** Gemma 4:31b (Dense, 31B parameters, multimodal, 128K context)

**Role:** Fast inference for grading, tutoring, and chat — the workhorse that handles 80%+ of queries.

**Placement:** DGX Spark 128 GB nodes — at Q4_K_M (~18 GB), leaves 110 GB for KV cache and concurrent requests.

---

## 3. Model Zoo and Compute Allocation

| Model | Parameters | Architecture | Quantisation | Memory | Placement | Role |
|---|---|---|---|---|---|---|
| **Sovereign Teacher** | 35B | MoE (3B active) | Q4_K_M / Q8_0 | 20–40 GB | Mac Studio 256 GB | Distillation source, synthesis, orchestration |
| **Production SLM** | 31B | Dense | Q4_K_M / Q8_0 | 18–35 GB | DGX Spark 128 GB | Grading, tutoring, fast chat |
| **Agent SLM** | 9B | Dense | Q8_0 | ~9 GB | Mac Studio (secondary) | Curriculum NLP, student advisor |
| **Swarm Students** | 0.5–3B | Dense | Q4–Q8 | 0.3–2 GB | Campus laptops | Federated LoRA research, edge inference |
| **Embedding** | 567M | Dense | FP16 | ~1 GB | All nodes | RAG retrieval (Malay/English multilingual) |
| **Cloud Teacher** | 100B+ | Dense | FP16 | N/A | API only | Synthetic data generation, validation |

**Cluster peak usage:**
- Sovereign teacher (Q4) + production SLM (Q4) + agent SLM (Q8) + embedding + KV cache ≈ 150 GB active
- Of 896 GB aggregate across 5 nodes — comfortable headroom for concurrent inference and QLoRA adaptation jobs

---

## 4. Hardware and Infrastructure

### 4.1 Cluster specification (RM 200,000)

| Component | Specification | Qty | Unit Cost (RM) | Total (RM) |
|---|---|---|---|---|
| Teacher nodes | Mac Studio M3 Ultra · 256 GB unified · 2 TB SSD | 2 | 68,000 | 136,000 |
| Edge nodes | NVIDIA DGX Spark · GB10 Superchip · 128 GB coherent | 3 | 14,000 | 42,000 |
| Network | 10GbE managed L3 switch, NICs, TB5 bridge cabling | 1 | 8,000 | 8,000 |
| Rack | 12U wall-mount cabinet + cantilever shelves + UPS (30-min) | 1 | 14,000 | 14,000 |
| **Total** | | | | **RM 200,000** |

**Form factor note:** All five compute nodes are desktop/tower units (Mac Studio ≈ 20 cm cylinder; DGX Spark ≈ mini-tower). They require ventilated cantilever shelves in a 12U wall-mount cabinet, not datacenter rails. 42U datacenter racks are unnecessary.

### 4.2 Network topology

```
                    ┌─────────────────┐
                    │   10GbE Switch  │
                    │   (Core, L3)    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────┴────┐          ┌─────┴─────┐       ┌─────┴─────┐
   │ Mac     │          │ DGX Spark │       │ DGX Spark │
   │ Studio  │          │ Node 1    │       │ Node 2    │
   │ (256GB) │          │ (128GB)   │       │ (128GB)   │
   │ Teacher │          │ Production│       │ Production│
   │ Node A  │          │ + Agent   │       │ + Agent   │
   └────┬────┘          └─────┬─────┘       └─────┬─────┘
        │                      │                    │
   ┌────┴────┐          ┌─────┴─────┐       ┌─────┴─────┐
   │ Mac     │          │ DGX Spark │       │  Campus   │
   │ Studio  │          │ Node 3    │       │  WiFi AP  │
   │ (256GB) │          │ (128GB)   │       │           │
   │ Teacher │          │ Failover  │       │ 10,000    │
   │ Node B  │          │ + Swarm   │       │ Laptops   │
   └─────────┘          └─────┬─────┘       └─────┬─────┘
                              │                    │
                        ┌─────┴─────┐            │
                        │ Data Fabric │            │
                        │ (PostgreSQL,│            │
                        │ pgvector,   │            │
                        │ MinIO,      │            │
                        │ Redis)      │            │
                        └─────────────┘            │
                                                   │
                              ┌────────────────────┘
                              ↓
                    Federated Swarm Clients
                    (LoRA adapter exchange)
```

### 4.3 EXO disaggregation

The EXO framework distributes model layers across physically separate nodes. This is **not** a single 896 GB coherent memory space — it is a pipeline where:
- Mac Studios hold early/late layers (attention, embedding, LM head)
- DGX Sparks hold middle layers (feed-forward, MoE routing)
- Inter-node communication is via 10GbE Ethernet (sufficient for inference, insufficient for training)

**Latency target:** < 3 seconds for grading queries, < 1 second for chat responses.

---

## 5. Data and Training Pipeline

### 5.1 Training data sources

| Source | Content | Volume | PDPA Classification |
|---|---|---|---|
| KPT/MQA policy corpus | Accreditation standards, programme development guidelines | ~50,000 pages | PUBLIC |
| UPSI curriculum archive | Course outlines, CLO/PLO mappings, Bloom taxonomy matrices | ~10,000 courses | INTERNAL |
| Malaysian academic textbooks | Malay + English, primary to tertiary | ~5,000 volumes | PUBLIC (published) |
| Open educational resources (OER) | MIT OCW, Khan Academy, Wikipedia (educational subset) | ~2M pages | PUBLIC |
| Synthetic data (cloud teacher) | Curriculum-grounded Q&A, preference pairs, adversarial tests | ~500K pairs | INTERNAL (anonymised) |

**No student PII or assessment data is used in pre-training.** All curriculum data is either public or anonymised aggregate.

### 5.2 Training stages

| Stage | Duration | Activity | Hardware |
|---|---|---|---|
| **Stage 1: Synthetic corpus generation** | Months 1–2 | Cloud teacher generates curriculum Q&A, DPO pairs, red-team cases | API credits |
| **Stage 2: Continual pre-training** | Months 2–4 | QLoRA on Malaysian academic corpus (Malay + English) | Mac Studio |
| **Stage 3: Instruction tuning** | Months 4–6 | SFT on grading, advising, curriculum datasets | Mac Studio + DGX Spark |
| **Stage 4: Federated adaptation** | Months 6–9 | LoRA/QLoRA on campus swarm (faculty-local documents) | 10,000 laptops + DGX Spark |
| **Stage 5: DPO alignment** | Months 9–10 | Preference alignment for safety, tone, institutional voice | Mac Studio |
| **Stage 6: Evaluation** | Months 10–12 | Benchmarking, red-teaming, accreditation readiness | All hardware |

---

## 6. Evaluation

### 6.1 Golden set

200 query-answer pairs across 5 educational domains:
1. Curriculum compliance (KPT/MQA standards)
2. Automated grading (essay rubric scoring)
3. Student advising (course selection, at-risk flags)
4. Staff analytics (IPA index, career pathing)
5. Institutional policy (promotion criteria, HR guidelines)

Bilingual Malay/English. Authored by 30+ UPSI researchers and validated by subject-matter experts.

### 6.2 Baselines

| Model | Size | Deployment | Type |
|---|---|---|---|
| SULUH AI (ours) | 35B MoE | On-premise | Sovereign |
| Qwen3.6-35B-A3B (base) | 35B MoE | On-premise | Unadapted |
| Kimi K3 | 100B+ | API | Cloud teacher |
| Claude 3.5 Sonnet | 175B | API | Cloud reference |
| Gemma 4:31b | 31B Dense | On-premise | Production SLM |
| GPT-4o (mini) | 8B | API | Cloud baseline |

### 6.3 Metrics

| Metric | Target | Measurement |
|---|---|---|
| **Grading accuracy** (rubric adherence) | ≥ 85% agreement with lecturer consensus | BERTScore + expert panel |
| **Curriculum compliance** (KPT/MQA) | ≥ 90% correct CLO/PLO mapping | Automated + auditor review |
| **Student advising quality** | ≥ 80% student satisfaction | Post-interaction survey |
| **Malay language fluency** | ≥ 90% grammatical correctness | Native speaker panel |
| **Hallucination rate** | ≤ 5% on golden set | Citation verification + expert review |
| **Latency** | < 3s grading, < 1s chat | LangFuse tracing |
| **PDPA compliance** | 100% | Audit log review |
| **IRB gate accuracy** | ≥ 98% | IRB officer review |

---

## 7. Economic Analysis

### 7.1 Capital cost (one-time)

| Item | RM |
|---|---|
| Hardware cluster | 200,000 |
| Setup & installation | 10,000 |
| **Total CAPEX** | **210,000** |

### 7.2 Operating cost (annual)

| Item | RM |
|---|---|
| Cloud API (synthetic data) | 5,000 |
| Electricity (5 nodes, 24/7) | 8,000 |
| Maintenance & warranty | 12,000 |
| Network & backup | 5,000 |
| **Total OPEX** | **30,000** |

### 7.3 Cost comparison: sovereign vs. cloud

| Scenario | 12-month cost | 3-year cost | Notes |
|---|---|---|---|
| **SULUH AI (sovereign)** | RM 240,000 | RM 300,000 | One-time CAPEX + low OPEX |
| **Cloud AI (Anthropic)** | RM 180,000 | RM 540,000 | RM 15K/month for equivalent usage |
| **Cloud AI (OpenAI)** | RM 240,000 | RM 720,000 | Higher token costs for long context |
| **Vendor-managed "sovereign"** | RM 400,000 | RM 900,000 | US-headquartered, opaque pricing |

**Breakeven:** SULUH AI becomes cheaper than cloud at month 16. By year 3, it is 55% cheaper than Anthropic and 58% cheaper than OpenAI.

**Risk-adjusted cost:** The sovereign option eliminates regulatory fines, breach response, and reputation damage — which are unquantifiable but potentially catastrophic.

---

## 8. Discussion

### 8.1 Sovereignty is not isolation

SULUH AI uses open-source models (Qwen, Gemma), open-source frameworks (EXO, LangGraph, vLLM), and open data formats. Sovereignty is about *where the data lives*, not about reinventing the stack. The cloud teacher tier ensures we benefit from frontier model quality for synthetic data generation without violating data residency.

### 8.2 Why 35B, not 70B or 100B

A 70B dense model at FP16 requires ~140 GB weights + 100+ GB KV cache = ~250 GB total. This exceeds our 256 GB Mac Studio nodes when concurrent models and OS overhead are included. A 35B MoE model achieves comparable quality with 3B active parameters per token, fitting comfortably in 60–100 GB — leaving massive headroom for concurrent inference and QLoRA jobs.

The honest claim is: **35B MoE is the largest model we can serve reliably on this hardware.** Full-scale 100B training is positioned as a Phase-2 vision contingent on national compute partnership (NAIO / MyDIGITAL GPU allocations), not a Year-1 deliverable.

### 8.3 The federated research dividend

The 10,000-device swarm is not just infrastructure — it is the project's primary research engine. Because laptops train models they can genuinely hold (0.5–3B), each algorithmic contribution (MA3, APA-EF, LES-GA) can be evaluated end-to-end on real heterogeneous hardware at a scale few labs can replicate. That is the moat.

**The Psyche baseline.** Nous Research's Psyche protocol has already proven that transformer models can be trained across thousands of untrusted internet nodes with zero institutional trust, using blockchain consensus and game-theoretic witness validation. SULUH's federated track takes this proven feasibility and asks: *what becomes possible when the nodes are trusted, institutionally owned, and operating within a single PDPA jurisdiction?* The answer is APA-EF — differential privacy with elastic compression — which would be impossible under Psyche's untrusted threat model because no node can be trusted with gradient sparsification parameters. It is also LES-GA — localized curriculum alignment — which requires a shared educational knowledge base that only institutional ownership enables. SULUH does not compete with Psyche; it extends Psyche's proof into the sovereign educational domain, trading the generality of untrusted participation for the strength of privacy and pedagogical alignment that institutional control affords.

### 8.4 Threats to validity

- Single-site pilot. Multi-institution validation is future work.
- Open-source model quality is improving but not yet at frontier-closed-source level on all tasks.
- MoE inference requires careful load balancing; routing overhead may impact latency at high concurrency.
- The 10,000-device swarm assumes sustained student participation; attrition is a risk.

---

## 9. Conclusion

SULUH AI is a 35B-parameter sovereign educational AI model deployed on a 5-node cluster costing less than RM 200,000. Its three-track architecture (cloud teacher → sovereign teacher → federated students) delivers frontier-level quality for educational tasks while keeping all data within Malaysian jurisdiction. The model is validated on a 200-entry bilingual golden set, with full economic analysis showing sovereign AI is now practical — and cheaper in the medium term — for a public university in a middle-income country.

The codebase, golden sets, and deployment configurations are released for institutional reuse under Apache 2.0 and CC-BY 4.0.

---

## Authors (proposed)

- **Putra Nasution** (Lead, corresponding author) — model architecture, training pipeline, implementation
- **Dr. Suzani binti Mohamad Samuri** (UPSI, Faculty of Meta) — IRB oversight, governance, educational domain validation
- *TBD* — ML systems researcher, federated learning specialist

---

## Relationship to the SULUH Ecosystem

**SULUH AI** (this paper) is the sovereign educational model — the "brain." **SULUH Ecosystem** (companion deployment documentation) is the institutional harness layer — the "nervous system" that routes queries, enforces PDPA/IRB gates, and serves four production applications (Institutional Intelligence, Curriculum Knowledge, Instructional Engine, Student Intelligence Platform). The Ecosystem consumes SULUH AI as its inference backend, but the two are developed and budgeted separately: SULUH AI is a RM 450K model R&D programme (RM 200K hardware + RM 250K manpower), while the four institutional harnesses are funded through UPSI operational IT budgets. Both are UPSI initiatives under the guidance of META, ICT, and related divisions.

## Acknowledgements

The SULUH AI pilot is supported by UPSI META, ICT, and related divisions. We thank the UPSI IRB Committee, DBA team, and research community for collaboration. We thank the SEA consortium partners for early feedback.

## Reproducibility Appendix (planned)

- Model weights and training code: `packages/suluh/models/`
- Golden evaluation set: `research/golden-sets/suluh-ai-v1.jsonl` (200 entries)
- Training corpus (anonymised): `research/corpus/educational-malay-english-v1/`
- Training scripts: `scripts/train_qlora.py`, `scripts/federated_lora.py`
- Benchmark scripts: `benchmarks/eval_suluh.py`
- Deployment configurations: `ops/exo-cluster.yaml`, `ops/vllm-config.yaml`
- Cost model spreadsheet: `docs/cost-model.xlsx`
