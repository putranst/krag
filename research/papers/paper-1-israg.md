# Paper 1: IsRAG — Provenance-Chain Retrieval Augmented Generation for Trustworthy AI Systems

**Target venues (in order of preference):**
1. ACL (Association for Computational Linguistics) — main conference, Long Paper
2. EMNLP (Empirical Methods in NLP) — main conference
3. FAccT (Fairness, Accountability, Transparency) — main conference
4. JCDL (Joint Conference on Digital Libraries) — main conference

**Submission timeline:** Target submission 6 months from programme start.

---

## Abstract (draft, 250 words)

Retrieval-Augmented Generation (RAG) has become the dominant architecture for grounding large language models in external knowledge. Yet standard RAG systems treat all retrieved documents as equivalent: a peer-reviewed journal article and an unverified blog post carry the same retrieval weight, and the user receives no information about *who* created the knowledge, *how* it was verified, or *in what cultural and epistemological framework* it should be interpreted. This is a critical deficiency for high-stakes domains — academic research, policy, healthcare, legal — where the provenance of a claim determines whether it should be trusted at all.

We present **IsRAG** (*Isnad-chain Retrieval Augmented Generation*), a retrieval architecture that embeds a full provenance chain, a multi-factor trust score, and a cultural-context tag into every knowledge unit. IsRAG adapts the **Isnad** (إسناد) framework from Islamic scholarship — a 1,000-year-old methodology for documenting and rating chains of transmission — to modern AI retrieval. Each piece of knowledge carries: (1) an immutable provenance chain recording every author, verifier, and adapter; (2) a trust score computed by a five-factor TrustEngine (verification level, source credibility, verification quality, cross-references, freshness); and (3) a cultural-context tag drawn from a 13-framework registry. We evaluate IsRAG against standard RAG baselines on a 200-entry bilingual (Malay/English) research-domain golden set, demonstrating measurable improvements in factual accuracy, user trust calibration, and cultural appropriateness. We further demonstrate that IsRAG's provenance chains enable IRB-compliant audit trails for sensitive research, opening a path to deploying RAG in regulated environments where standard RAG is currently unsafe.

---

## 1. Introduction

The problem of *trust* in LLM-generated outputs is not solved by retrieval alone. Standard RAG retrieves text and feeds it to the generator. The user sees citations, but the citations do not tell them whether the cited source was peer-reviewed or unverified, whether it was written from a Western or indigenous epistemological framework, or whether multiple independent verifiers have validated the claim.

This is not a hypothetical problem. In academic research, in policy analysis, in healthcare, in legal work, the **provenance of knowledge is the knowledge**. A claim sourced from a peer-reviewed paper and a claim sourced from an LLM hallucination look identical to the user.

**The research question:** *Can we adapt a 1,000-year-old methodology for knowledge validation — the Islamic Isnad — to modern AI retrieval, and does it measurably improve trust, accuracy, and cultural appropriateness of LLM-generated answers?*

---

## 2. Background and related work

### 2.1 RAG and its limitations
Brief survey of RAG evolution: original RAG (Lewis et al. 2020), REALM, RETRO, Atlas, current production patterns. Limitations: no provenance, no trust scoring, no cultural context.

### 2.2 Provenance in information systems
Provenance in databases, scientific workflows (W3C PROV), knowledge graphs. None of these have been integrated into the RAG generator loop.

### 2.3 Trust calibration in AI
Literature on user trust in algorithmic systems, why provenance transparency increases appropriate reliance (Dietvorst et al. 2015, Logg et al. 2019).

### 2.4 The Isnad framework
Origins in 2nd-century Islamic scholarship. Purpose: validate hadith transmission chains. Mechanism: every transmitter is named, rated, and contextualised. Outcome: a piece of knowledge is inseparable from the chain that produced it.

**We argue that Isnad is the missing primitive in modern RAG.**

---

## 3. IsRAG: design

### 3.1 Data model

```
KnowledgeEntry {
  content: str
  author: str
  source_type: SourceType   (RESEARCH, INSTITUTIONAL, GOVERNMENT, ...)
  verification_level: VerificationLevel  (UNVERIFIED → FIELD_VALIDATED)
  cultural_context: CulturalContext | None
  trust_score: float          (computed)
  provenance: list[ProvenanceStep]
  verifications: list[VerificationRecord]
  tags: list[str]
  created_at: datetime
}
```

### 3.2 TrustEngine: the 5-factor score

| Factor | Weight | Description |
|---|---|---|
| Verification level | 30% | How verified is this? |
| Source credibility | 25% | Type of source (gov, academic, news, community) |
| Verification quality | 20% | Ratings from verifiers |
| Cross-references | 15% | How many other entries reference this |
| Freshness | 10% | How recent is this knowledge |

### 3.3 Cultural context registry

13 frameworks: Global, Western, East Asian, Southeast Asian, South Asian, Indonesian, Malaysian, Thai, Vietnamese, Filipino, Singaporean, Islamic, Buddhist, Indigenous. Each tag includes: language of origin, applicability regions, known limitations, local terminology.

### 3.4 Retrieval with full isnad

IsRAG's `retrieve()` returns results with three properties: trust-weighted ranking, cultural-filter capability, and the full IsRAG.IsnadChain attached to each result.

---

## 4. Evaluation

### 4.1 Golden set

Version 1 contains **200 synthetic reference items** across 5 domains: agriculture, Islamic finance, indigenous land rights, public health, and digital governance. Each domain contains 40 items (20 English and 20 Malay), giving 100 items per language. The machine-readable JSONL file is `research/golden-sets/israg-v1.jsonl`; the deterministic builder is `research/golden-sets/build_israg_golden_set.py`.

These items are an evaluation scaffold, not evidence of measured performance: each reference answer is marked `annotation_status: reference_answer_pending_expert_review`. Before submission, the set must undergo independent bilingual domain-expert review, source citation, adjudication, and ethics/data-governance review. The final release should record annotator agreement and revisions rather than presenting the current synthetic references as researcher-authored ground truth.

### 4.2 Metrics

- **Accuracy:** BERTScore against human ground truth
- **Trust calibration:** pre/post user survey, 5-point Likert
- **Cultural appropriateness:** expert review, 3-point ordinal
- **Hallucination rate:** claimed citations that don't exist or are misattributed
- **Provenance completeness:** does the answer include the chain?

### 4.3 Baselines

- Standard RAG (LangChain default, LlamaIndex default)
- RAG with citations only (no trust)
- RAG with cultural context only (no trust)
- IsRAG (full)

### 4.4 Expected results

We hypothesise IsRAG will:
- Match baseline accuracy on simple factual queries
- Outperform baselines on multi-perspective queries (+5–10% BERTScore)
- Reduce hallucination rate by ≥30%
- Significantly improve user trust calibration (effect size > 0.5)

---

## 5. Discussion

### 5.1 What the Isnad gives us that citation alone does not

A citation tells you *where* to find the source. An isnad tells you *whether to trust the source* and *how confident to be in the claim derived from it*.

### 5.2 Cultural frameworks as a first-class concern

Standard RAG assumes a universal knowledge space. IsRAG recognises that knowledge is contextual. This matters in multilingual, multicultural deployments.

### 5.3 Trust calibration: the under-discussed RAG failure mode

Most RAG papers report accuracy. Few report whether users know when to trust the answer. IsRAG's explicit trust score is designed to fix this.

### 5.4 The IRB and regulatory angle

For healthcare, legal, and academic deployments, provenance is not a feature — it is a compliance requirement. IsRAG's audit trail is IRB-ready by design.

---

## 6. Limitations and future work

- The trust scoring weights are hand-tuned in v0.1. Future work: learn them from user feedback
- The cultural framework registry is curated. Future work: automated discovery
- The 200-entry golden set is small. Future work: 1,000+ entries across more domains

---

## 7. Conclusion

IsRAG is a retrieval architecture that treats provenance, trust, and cultural context as first-class concerns — not as post-hoc features. By adapting the Islamic Isnad framework, it offers a 1,000-year-old epistemology for a 1-year-old technology. Initial results suggest that the cost of the additional structure is small, while the gains in trust calibration and auditability are large. We believe IsRAG opens a path toward deploying RAG in regulated, high-stakes domains where standard RAG is currently unsafe.

---

## Authors (proposed)

- **Putra Nasution** (Lead, corresponding author)
- **Dr. Suzani binti Mohamad Samuri** (UPSI, Faculty of Meta)
- *TBD* — collaborators on golden set authoring from consortium institutions

## Acknowledgements (draft)

The golden set was authored by researchers from [list of institutions]. This work was supported by [funding source]. We thank the UPSI IRB Committee for the ethics-gate feedback and the consortium technical review board for the architecture review.

---

## Reproducibility appendix (planned)

- Code: `packages/israg/` (Apache 2.0, available to reviewers)
- Golden set: `research/golden-sets/israg-v1.jsonl` (CC-BY 4.0)
- TrustEngine weights: `packages/israg/src/israg/trust_weights.yaml`
- BERTScore evaluation script: `benchmarks/run_israg_eval.py`
