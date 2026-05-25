# CONCEPT PAPER
## KRAG: Knowledge-chain Retrieval Augmented Generation
### A Culturally-Grounded, Trust-Scored Approach to AI Knowledge Retrieval

**Prepared for:** Associate Professor Dr. Suzani binti Mohamad Samuri, Faculty of Meta (UPSI)
**Prepared by:** Putra Nasution, Research Collaborator & Principal Investigator
**Date:** May 2026

---

## 1. RESEARCH BACKGROUND AND MOTIVATION

### 1.1 The Problem with Current RAG Systems

Retrieval-Augmented Generation (RAG) has become the dominant architecture for grounding Large Language Models (LLMs) in external knowledge. However, standard RAG systems suffer from three critical limitations:

1. **No provenance tracking:** Users cannot verify WHERE a piece of retrieved knowledge came from, WHO created it, or HOW it was validated
2. **No trust scoring:** All retrieved documents are treated equally — a peer-reviewed journal article and an unverified blog post carry the same weight
3. **No cultural context:** Knowledge is treated as universal, ignoring that facts, interpretations, and terminologies vary dramatically across cultural and linguistic frameworks

These limitations are especially acute in Southeast Asian contexts, where:
- Knowledge systems (adat, Islamic scholarship, indigenous oral traditions) have their own epistemological frameworks
- Misinformation spreads rapidly across multilingual, multi-ethnic populations
- Trust in AI systems is low due to Western-centric training data and validation methods
- Scholars and policymakers need transparent, auditable knowledge chains for decision-making

### 1.2 The Isnad Precedent

For over 1,000 years, Islamic scholarship has used **Isnad** (إسناد) — a chain of transmission that documents every person who transmitted a piece of knowledge, from the original source to the current scholar. This creates:
- **Traceability:** Every piece of knowledge has a documented lineage
- **Trust calibration:** Scholars rate the reliability of each transmitter
- **Contextual awareness:** Knowledge is understood within the framework of its transmitters, not as an isolated fact

KRAG adapts this provenance-first epistemology to modern AI retrieval systems.

---

## 2. RESEARCH OBJECTIVES

### Primary Objective
Develop and empirically validate KRAG (Knowledge-chain Retrieval Augmented Generation), a retrieval architecture that embeds provenance chains, trust scoring, and cultural context into every knowledge retrieval operation.

### Specific Objectives

1. **Architecture Development:** Finalize the KRAG engine with vector database integration (Pinecone/Weaviate), multi-language support, and graph-based cross-referencing
2. **Trust Scoring Validation:** Empirically test whether KRAG's trust-weighted retrieval produces measurably more reliable answers than standard RAG across Southeast Asian knowledge domains
3. **Cultural Context Efficacy:** Evaluate whether culturally-contextualized retrieval improves answer relevance and user trust for Indonesian, Malaysian, Thai, and Filipino users compared to culturally-neutral retrieval
4. **Dewan Council Integration:** Benchmark the KRAG + multi-LLM deliberation system (Dewan Council) against single-LLM RAG on complex, multi-faceted queries
5. **Misinformation Resistance:** Test KRAG's ability to detect and flag low-trust, contradictory, or unverified knowledge in politically and culturally sensitive domains

---

## 3. RESEARCH METHODOLOGY

### 3.1 System Architecture

KRAG consists of five integrated components:

| Component | Function |
|-----------|----------|
| **KnowledgeEntry** | Stores content with full provenance (author, source type, verification level, cultural framework) |
| **TrustEngine** | Calculates composite trust scores (verification level 30%, source credibility 25%, verification quality 20%, cross-references 15%, freshness 10%) |
| **CulturalContext** | Tags knowledge with cultural framework (Indonesian, Malaysian, Islamic, Buddhist, Indigenous, etc.) |
| **IsnadChain** | Generates human-readable provenance chains for every retrieved answer |
| **RetrievalEngine** | Performs trust-weighted, culturally-filtered retrieval with full Isnad output |

### 3.2 Experimental Design

**Phase 1: Baseline Benchmarking (Months 1-3)**
- Build test datasets across 5 SEA knowledge domains: agriculture, Islamic finance, indigenous land rights, public health, and digital governance
- Benchmark KRAG against standard RAG (LangChain, LlamaIndex) on accuracy, relevance, and trust metrics
- Measure with both automated metrics (BLEU, ROUGE, BERTScore) and human expert evaluation

**Phase 2: Cultural Context Testing (Months 3-5)**
- Recruit 100+ participants across Indonesia, Malaysia, Thailand, and Philippines
- A/B test: culturally-contextualized vs. culturally-neutral retrieval
- Measure: answer relevance (Likert scale), user trust (pre/post), perceived accuracy, willingness to act on information

**Phase 3: Misinformation Resistance (Months 5-7)**
- Inject known misinformation, contradictory claims, and unverified sources into test knowledge bases
- Measure KRAG's ability to flag, downrank, or transparently disclose low-trust information
- Compare to standard RAG's "hallucination" and "confabulation" rates

**Phase 4: Dewan Council Integration (Months 7-9)**
- Integrate KRAG with Dewan Council (7-LLM deliberation system)
- Benchmark complex queries requiring multi-perspective synthesis
- Measure: answer comprehensiveness, internal consistency, deliberation time, cost efficiency

**Phase 5: Publication & Dissemination (Months 9-12)**
- Submit to ACL/EMNLP or comparable AI/NLP venues
- Submit to Islamic Digital Humanities or Southeast Asian Studies journals
- Open-source final system with full documentation

### 3.3 Theoretical Framework

This research draws on three theoretical foundations:

1. **Islamic Epistemology (Isnad/Chain of Transmission):** The 1,000-year tradition of knowledge validation through documented, rated transmission chains
2. **Decolonial AI Theory:** The critique that AI systems embed Western epistemological assumptions and exclude non-Western knowledge systems
3. **Trust Calibration in Information Systems:** Research on how users calibrate trust in algorithmic systems and why provenance transparency increases appropriate reliance

---

## 4. EXPECTED OUTCOMES AND IMPACT

### Academic Outputs
- **2-3 peer-reviewed journal articles** (AI/NLP and Southeast Asian Studies venues)
- **1 conference paper** (ACL, EMNLP, or FAccT)
- **1 open-source software release** with documentation
- **2-3 Master's/PhD student theses** supervised under the project

### Practical Impact
- A retrieval system that Southeast Asian governments, NGOs, and researchers can trust for policy-relevant queries
- A methodological contribution: the "Isnad approach" to AI provenance that other researchers can adopt
- A training tool for students to understand both AI retrieval and indigenous/local knowledge systems

### Strategic Impact for UPSI
- Positions UPSI as a leader in culturally-grounded AI research in Malaysia and SEA
- Strengthens collaboration between Meta faculty and international AI practitioners
- Potential for MOHE/FRGS grant applications using this foundational work

---

## 5. COLLABORATION STRUCTURE

| Party | Contribution |
|-------|-------------|
| **Putra Nasution (Principal Investigator)** | System architecture, code development, Dewan Council integration, industry partnerships, project management |
| **Dr. Suzani binti Mohamad Samuri (Academic Lead)** | Research supervision, theoretical framing, student mentorship, publication guidance, grant applications |
| **UPSI Meta Faculty** | Research infrastructure, student recruitment, ethical approval, administrative support |
| **Students (2-3 Master's/PhD)** | Literature review, experiment execution, data collection, thesis production |

---

## 6. TIMELINE

| Phase | Duration | Key Milestone |
|-------|----------|---------------|
| Setup & Ethics Approval | Month 1 | Ethical clearance, student recruitment, dataset collection |
| Baseline Benchmarking | Months 2-4 | Working paper: KRAG vs. Standard RAG |
| Cultural Context Study | Months 4-6 | User study with 100+ SEA participants |
| Misinformation Resistance | Months 6-8 | Working paper: Trust-scored retrieval under adversarial conditions |
| Dewan Council Integration | Months 8-10 | Integrated system benchmark |
| Publication & Release | Months 10-12 | Journal submissions, open-source release |

---

## 7. RESOURCE REQUIREMENTS

| Resource | Source |
|----------|--------|
| LLM API costs (OpenRouter) | ~RM 5,000-8,000/year |
| Cloud compute (vector DB, hosting) | ~RM 3,000-5,000/year |
| Participant incentives (Phase 2) | ~RM 3,000 |
| Conference travel & publication fees | ~RM 5,000-10,000 |
| **Total (Year 1)** | **~RM 16,000-26,000** |

*Note: Putra Nasution will cover API and infrastructure costs from existing resources. UPSI support requested for participant incentives, conference travel, and student stipends.*

---

## 8. WHY THIS MATTERS NOW

AI retrieval systems are being deployed across Southeast Asian governments, courts, and universities. Without provenance, trust scoring, and cultural context, these systems will:
- Spread misinformation with the authority of "AI"
- Erase non-Western knowledge systems
- Undermine public trust in digital governance

KRAG offers a technically sound, culturally grounded alternative. It is not just an engineering project — it is an epistemological intervention.

---

*This concept paper is preliminary and open to revision based on faculty feedback and collaborative discussion.*
