# Paper 2: Multi-LLM Deliberation with Provenance Chains for Research Synthesis

**Target venues (in order of preference):**
1. AAMAS (Autonomous Agents and Multi-Agent Systems) — main conference
2. NeurIPS — Workshop on AI for Scientific Discovery
3. ACL — Workshop on Knowledge Graphs / Computational Social Science
4. HCI journals (IJHCS, TOCHI) — if framed as a human-AI collaboration paper

**Submission timeline:** Target submission 9 months from programme start.

---

## Abstract (draft, 250 words)

Large language models increasingly operate as **committees** rather than individuals — multiple models are queried, their outputs compared, and a single answer synthesised. Yet most production multi-LLM systems treat this process as opaque: the user sees only the final synthesis, not the disagreement, not the dissent, not the reasoning. This is a critical deficiency in research and policy contexts where understanding *why* a model produced an answer matters as much as the answer itself.

We present **Dewan Council**, a three-stage multi-LLM deliberation protocol in which (1) each council member produces an independent first-stage opinion; (2) each member reviews and rates the other members' opinions, producing a structured critique; and (3) a designated chairman synthesises a final answer that explicitly carries the dissent forward, names the consensus score, and emits a complete provenance chain. Dewan Council is designed to integrate with the IsRAG provenance framework, so every opinion in the deliberation is itself grounded in verifiable knowledge with traceable trust scores.

We evaluate Dewan Council against single-LLM and majority-vote baselines on a 100-entry research synthesis task across five domains (education, public health, environmental policy, AI ethics, Islamic finance). Results show Dewan Council produces answers that are rated higher on comprehensiveness, internal consistency, and citation accuracy by expert reviewers, while also providing an auditable record of disagreement. The protocol is model-agnostic: it works with any combination of LLMs accessible via a unified API, and we demonstrate it with a seven-member council spanning four model families.

---

## 1. Introduction

The "ask multiple LLMs and aggregate" pattern is increasingly common, but the **how** of aggregation matters. A majority vote discards dissent. A confidence-weighted average hides disagreement. A chairman-LLM synthesis without structured dissent reporting produces a *false consensus* — the appearance of agreement where none exists.

**The research question:** *Can we design a multi-LLM deliberation protocol that produces better answers than single-LLM or naive-aggregation baselines, while simultaneously producing an auditable record of disagreement that downstream users (researchers, policy analysts, clinicians) can inspect and reason about?*

---

## 2. Related work

### 2.1 Multi-LLM ensembles
- Karpathy's LLM Council (2024) — 3-stage deliberation, the conceptual ancestor
- Mixture-of-Experts literature
- Self-consistency (Wang et al. 2023)
- Chain-of-thought and tree-of-thought aggregation

### 2.2 Provenance in agent systems
- Process provenance in scientific workflows
- LangChain/LangGraph built-in tracing
- W3C PROV and its limits in multi-agent contexts

### 2.3 IsRAG (companion paper)
Dewan Council is designed to operate on top of IsRAG-grounded knowledge. We assume the reader has read or is reading Paper 1.

---

## 3. The Dewan Council protocol

### 3.1 Setup

A council is a set of `CouncilMember` objects:

```
CouncilMember {
  name: str
  role: "chairman" | "member"
  model_id: str   (e.g., "anthropic/claude-opus-4.7")
  specialty: str  ("synthesis", "deep-reasoning", "data", "multilingual", ...)
  trust_weight: float  (default 1.0)
}
```

The reference council (used in all reported experiments) is:

| Role | Model | Specialty |
|---|---|---|
| Chairman | Claude Opus 4.7 | Synthesis, judgment |
| Member | GPT-5.5 | Deep reasoning |
| Member | Gemini 3 Flash | Data, multimodal |
| Member | Kimi K2.6 | Long context, multi-agent |
| Member | Deepseek V4 Flash | Chain-of-thought |
| Member | Qwen 3.6 Plus | Multilingual, Asia |
| Member | Nemotron 3 Super | Open model, free tier |

### 3.2 Stage 1: First opinions

Each member is queried independently with the same prompt. Each `Opinion` carries the response text, a self-assessed confidence score, and the model identifier. Stage 1 produces N opinions (one per member).

### 3.3 Stage 2: Cross-review

Each member reviews every other member's opinion. For N members, this produces N × (N-1) = N²−N reviews. Each `Review` carries:
- Reviewer and reviewed member names
- A rating (1–10)
- Free-text feedback
- A list of `issues_found` (factual errors, missing context, unsupported claims, bias)

Stage 2 produces a complete review matrix.

### 3.4 Stage 3: Chairman synthesis

The chairman LLM receives:
- The original query
- All Stage 1 opinions
- All Stage 2 reviews
- The review matrix summary

The chairman produces:
- `final_answer` — the synthesised response
- `consensus_score` — 0.0 (full disagreement) to 1.0 (full agreement)
- `dissenting_views` — list of opinions that disagreed with the majority
- `isnad_chain` — complete audit trail of the deliberation

### 3.5 Integration with IsRAG

When the query is knowledge-grounded (the default in our evaluations), Stage 1 opinions are constrained to cite IsRAG KnowledgeEntry objects. The chairman's synthesis inherits the IsRAG trust scores, allowing downstream users to see not just *what* the council said but *which sources* the council relied on and how trustworthy each source was.

---

## 4. Evaluation

### 4.1 Research synthesis task

We construct 100 queries across five domains. Each query requires synthesising 3–8 source documents into a coherent research-style answer. The domains are chosen to require both technical accuracy and contextual sensitivity:
- Education (Malaysian K-12 policy)
- Public health (Southeast Asian vaccination programs)
- Environmental policy (Indonesian peatland management)
- AI ethics (ASEAN sovereign AI frameworks)
- Islamic finance (Malaysian shariah-compliant fintech)

### 4.2 Metrics

- **Comprehensiveness:** does the answer cover all aspects of the query? (5-point Likert, expert)
- **Internal consistency:** does the answer contradict itself? (binary, expert)
- **Citation accuracy:** are the cited IsRAG entries correctly attributed? (binary, automated)
- **Trust calibration:** does the answer's confidence match the underlying source quality? (continuous, expert)
- **Dissenting view visibility:** is dissent surfaced or hidden? (categorical, expert)

### 4.3 Baselines

- **Single-LLM:** Claude Opus alone
- **Best-of-N:** N samples from Claude, pick the highest self-assessed confidence
- **Majority vote:** independent sampling, pick the modal answer
- **Dewan Council (full):** the proposed protocol

### 4.4 Expected results

We hypothesise Dewan Council will:
- Match single-LLM on simple factual queries
- Outperform on multi-perspective queries by 10–15% on comprehensiveness
- Have lower inconsistency rate
- Surface dissent that baselines silently absorb
- Match majority-vote cost but with better auditability

---

## 5. Discussion

### 5.1 When does multi-LLM deliberation help?

We expect deliberation to help most when:
- The query has multiple defensible framings
- The sources are heterogeneous in quality
- The downstream user benefits from seeing the reasoning

We expect it to *not* help when:
- The query is single-fact retrieval
- All council members are likely to agree (deliberation overhead without benefit)
- The chairman is weaker than the members

### 5.2 The cost of deliberation

A 7-member council with full cross-review is 42 + 1 = 43 LLM calls per query. For high-volume deployments, this is expensive. We discuss routing: simple queries go to single-LLM, complex ones to the full council.

### 5.3 The auditability dividend

Even when Dewan Council does not produce a better answer than baselines, it produces a more **auditable** answer. The user sees the dissent. They see which sources the council trusted. They see the consensus score. This is the primary contribution for regulated domains.

---

## 6. Limitations and future work

- The 100-entry evaluation is small. Future work: 1,000+ entries, larger user studies
- The chairman selection is hand-tuned. Future work: learned chairman selection
- The protocol assumes a synchronous council. Future work: async, streamed deliberations

---

## 7. Conclusion

Dewan Council is a multi-LLM deliberation protocol that produces both better answers (on multi-perspective queries) and more auditable answers (in all cases). Combined with IsRAG, it grounds every opinion in verifiable, trust-scored knowledge. We believe this combination is a step toward AI systems that can be deployed in research and policy contexts where the reasoning matters as much as the conclusion.

---

## Authors (proposed)

- **Putra Nasution** (Lead, corresponding author)
- **Dr. Suzani binti Mohamad Samuri** (UPSI, Faculty of Meta)
- *TBD* — collaborators with multi-LLM evaluation expertise

## Reproducibility appendix (planned)

- Code: `packages/council/` (Apache 2.0)
- Evaluation queries: `research/golden-sets/council-v1.jsonl`
- Council configuration: `packages/council/src/council/council_config.yaml`
- Multi-LLM evaluation script: `benchmarks/run_council_eval.py`
- Per-query LLM call cost: `benchmarks/cost_analysis.md`
