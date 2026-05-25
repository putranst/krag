# KRAG — Knowledge-chain Retrieval Augmented Generation

> *Not just retrieval. Retrieval with provenance, trust, and cultural context.*

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)]()

KRAG is an evolution of RAG (Retrieval-Augmented Generation) that adds **provenance chains**, **trust scoring**, and **cultural context** to every piece of retrieved knowledge. Inspired by the **Isnad** (إسناد) tradition of Islamic scholarship — where every transmission of knowledge is documented and rated — KRAG makes AI retrieval transparent, accountable, and culturally aware.

```
Standard RAG:  Query → Retrieve → Generate → "Source: Document X"
KRAG:          Query → Retrieve + Provenance + Trust + Culture → 
               Generate → "Source: Author A → Institution B → Doc X | 
               Verified by C, D | Trust: 0.92 | Framework: Indonesian"
```

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/putranasution/krag.git
cd krag

# Install
pip install -e .

# Run the demo
krag demo

# Or in Python
python examples/basic_usage.py
```

---

## ✨ What Makes KRAG Different

### 1. Provenance Chain (Isnad)
Every knowledge entry carries a complete lineage: who created it, who verified it, how it was preserved, and how it reached you.

### 2. Trust Scoring
Not all sources are equal. KRAG calculates composite trust scores based on:
- **Verification level** (30%) — peer-reviewed, institutional, journalist, or unverified
- **Source credibility** (25%) — government, academic, research, news, or blog
- **Verification quality** (20%) — ratings from independent verifiers
- **Cross-references** (15%) — how many other entries confirm this
- **Freshness** (10%) — recency of the knowledge

### 3. Cultural Context
Knowledge is not universal. KRAG tags every entry with its cultural framework — Indonesian, Malaysian, Islamic, Buddhist, Indigenous, Western, or Global — so retrieval respects context, not just keywords.

### 4. Audit Trail
Every answer includes a full Isnad chain that humans can read, verify, and challenge.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      KRAG SYSTEM                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  User Query                                                  │
│     │                                                        │
│     ▼                                                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              KRAG RETRIEVAL ENGINE                   │    │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │    │
│  │  │   Content   │ │    Trust    │ │   Cultural  │   │    │
│  │  │  Matching   │ │   Scoring   │ │   Context   │   │    │
│  │  └─────────────┘ └─────────────┘ └─────────────┘   │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                     │
│            ┌────────────┴────────────┐                       │
│            ▼                         ▼                       │
│  ┌──────────────────┐   ┌──────────────────────────┐      │
│  │  KNOWLEDGE BASE  │   │    DEWAN COUNCIL          │      │
│  │                  │   │    (Optional)             │      │
│  │ • Entries        │   │                           │      │
│  │ • Provenance     │   │ • 7 LLM members           │      │
│  │ • Verifications  │   │ • Cross-review            │      │
│  │ • Cultural Tags  │   │ • Synthesis               │      │
│  └──────────────────┘   └──────────────────────────┘      │
│            │                         │                       │
│            └────────────┬────────────┘                       │
│                         ▼                                     │
│              INTEGRATED RESULT                                 │
│              ┌─────────────────────────────┐                  │
│              │  FINAL ANSWER             │                  │
│              │  + Complete Isnad Chain   │                  │
│              │  + Trust Score (0-1)       │                  │
│              │  + Confidence Level        │                  │
│              └─────────────────────────────┘                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🕌 Dewan Council (Multi-LLM Deliberation)

KRAG includes **Dewan Council**, a multi-LLM deliberation system inspired by [Karpathy's llm-council](https://github.com/karpathy/llm-council).

Instead of one LLM answering, Dewan Council convenes **7 specialist LLMs** to deliberate:

| Role | Model | Specialty |
|------|-------|-----------|
| 👑 Ketua (Chairman) | Claude Opus | Synthesis, judgment |
| 🧠 Member | GPT-5.5 | Deep reasoning |
| 📊 Member | Gemini Flash | Data, multimodal |
| 📖 Member | Kimi K2.6 | Long context, multi-agent |
| 🔢 Member | DeepSeek V4 | Chain-of-thought |
| 🌏 Member | Qwen 3.6 | Multilingual, Asia |
| 💻 Member | Nemotron 3 | Open model |

**Three stages:**
1. **First Opinions** — Each member answers independently
2. **Cross-Review** — Each member reviews and rates the others (21 reviews)
3. **Chairman Synthesis** — Final answer with full deliberation log

```bash
# Requires OPENROUTER_API_KEY
dewan "What is the best AI strategy for ASEAN?" --verbose
```

---

## 📚 Examples

| Example | What It Shows | Run |
|---------|---------------|-----|
| [`basic_usage.py`](examples/basic_usage.py) | Ingest, retrieve, trust filter | `python examples/basic_usage.py` |
| [`cultural_context.py`](examples/cultural_context.py) | Cultural framework filtering | `python examples/cultural_context.py` |
| [`trust_verification.py`](examples/trust_verification.py) | Knowledge evolving through verification | `python examples/trust_verification.py` |
| [`dewan_demo.py`](examples/dewan_demo.py) | Multi-LLM deliberation | `python examples/dewan_demo.py` |
| [`integration_example.py`](examples/integration_example.py) | KRAG + Dewan Council together | `python examples/integration_example.py` |

---

## 🧪 Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

---

## 📖 Research & Academic Use

KRAG is the subject of active academic research. A concept paper and collaboration framework are available in [`research-proposal/`](research-proposal/).

**Target venues:** ACL, EMNLP, FAccT, and regional journals on AI ethics and Southeast Asian digital humanities.

**Research questions:**
- How does provenance tracking reduce LLM hallucination?
- Does cultural framework encoding improve output relevance for non-Western contexts?
- What trust scoring mechanisms are appropriate for different knowledge domains?
- How does KRAG + multi-LLM deliberation compare to single-LLM RAG on complex queries?

If you are a researcher or student interested in collaborating, see [`research-proposal/CONCEPT-PAPER-UPSI.md`](research-proposal/CONCEPT-PAPER-UPSI.md) or contact **poetra@gmail.com**.

---

## 🔮 Roadmap

- [x] Core KRAG engine (trust scoring, provenance, cultural context)
- [x] Dewan Council (7-LLM deliberation)
- [x] CLI interfaces
- [x] Basic test suite
- [ ] Vector database integration (Qdrant, Weaviate, Pinecone)
- [ ] Multi-language knowledge entries
- [ ] Graph-based cross-referencing
- [ ] Blockchain anchoring for immutable provenance
- [ ] Automated verification pipelines
- [ ] REST API server
- [ ] Web dashboard for Isnad visualization

---

## 🤝 Contributing

This is an early-stage open-source project. Contributions welcome:

- **Code:** Vector DB integration, new cultural frameworks, performance improvements
- **Research:** Empirical studies, benchmarking, paper drafts
- **Data:** Curated, verified knowledge bases for Southeast Asian domains
- **Docs:** Translations, tutorials, case studies

Open an issue or PR. All contributions must include proper Isnad (provenance) attribution.

---

## 📜 License

MIT License — see [LICENSE](LICENSE).

---

## 🙏 Acknowledgments

- **Isnad tradition** — 1,000+ years of knowledge verification methodology
- **Andrej Karpathy** — llm-council inspiration
- **Islamic Digital Humanities community** — for keeping Isnad alive in the digital age
- **Southeast Asian knowledge keepers** — whose oral and written traditions inspire this work

---

**KRAG is not just retrieval. It is retrieval with accountability.**

Built with ❤️ in Southeast Asia by [Putra Nasution](https://linkedin.com/in/putranasution).
