# IsRAG — Provenance-Chain Retrieval Augmented Generation

> *Isnad-chain RAG. Every piece of knowledge has a traceable lineage.*

**Package:** `israg` (in the SULUH Ecosystem monorepo)
**Status:** v0.1 alpha — working engine, in active development
**Paper:** See [`../../research/papers/paper-1-israg.md`](../../research/papers/paper-1-israg.md) for the full academic contribution.

---

## What this is

IsRAG is a retrieval architecture that embeds a **full provenance chain**, a **multi-factor trust score**, and a **cultural-context tag** into every piece of knowledge it handles. It adapts the **Isnad** (إسناد) framework — a 1,000-year-old Islamic methodology for validating chains of knowledge transmission — to modern AI retrieval.

Standard RAG retrieves text and feeds it to the generator. IsRAG retrieves **KnowledgeEntry objects** that carry their own history, their own trust score, and their own cultural context. The user (or the downstream system) can then decide how much to trust each retrieved fact, and why.

---

## The 5 components

1. **KnowledgeEntry** — a single piece of ingested knowledge, with full provenance metadata
2. **ProvenanceChain** — the chain of custody: author → verifier → storage → retrieval
3. **TrustEngine** — calculates composite trust scores from 5 factors
4. **CulturalContext** — tags knowledge with its cultural framework (13 supported)
5. **RetrievalEngine** — performs trust-weighted, culturally-filtered retrieval with full isnad output

---

## Quick start

```python
from israg import IsRAGEngine, SourceType, VerificationLevel, CulturalContext, CulturalFramework

# Create engine
engine = IsRAGEngine()

# Ingest a piece of knowledge
engine.ingest(
    content="ASEAN has approximately 670 million people across 10 member states.",
    author="UN Population Division",
    source_type=SourceType.GOVERNMENT,
    verification_level=VerificationLevel.INSTITUTION_VERIFIED,
    tags=["asean", "demographics"],
)

engine.ingest(
    content="Indonesia's digital economy reached $77 billion in 2024, growing 18% YoY.",
    author="Google, Temasek, Bain & Company",
    source_type=SourceType.RESEARCH,
    verification_level=VerificationLevel.INSTITUTION_VERIFIED,
    cultural_context=CulturalContext(
        framework=CulturalFramework.INDONESIAN,
        language_original="English",
        applicability=["Indonesia", "Southeast Asia"],
        limitations=["Aggregated figure, not province-level"],
    ),
    tags=["indonesia", "digital-economy"],
)

# Retrieve with full isnad
results = engine.retrieve("ASEAN population and Indonesia digital economy", include_isnad=True)

for r in results:
    print(f"[trust={r.entry.trust_score:.2f}] {r.entry.content}")
    print(f"  source: {r.entry.author} ({r.entry.source_type.value})")
    print(f"  cultural: {r.entry.cultural_context.framework.value if r.entry.cultural_context else 'global'}")
    print()
```

## Trust scoring

The TrustEngine computes a 0.0–1.0 trust score from 5 weighted factors:

| Factor | Weight | What it measures |
|---|---|---|
| Verification level | 30% | UNVERIFIED → FIELD_VALIDATED (6 levels) |
| Source credibility | 25% | RESEARCH, INSTITUTIONAL, GOVERNMENT, etc. (8 types) |
| Verification quality | 20% | Average rating from verifiers |
| Cross-references | 15% | How many other entries reference this |
| Freshness | 10% | How recent is the knowledge |

## Cultural frameworks supported

`Global`, `Western`, `East Asian`, `Southeast Asian`, `South Asian`, `Indonesian`, `Malaysian`, `Thai`, `Vietnamese`, `Filipino`, `Singaporean`, `Islamic`, `Buddhist`, `Indigenous`

## Integration with Dewan Council

```python
from israg import IsRAGEngine, SourceType
from council import DewanCouncil

# Ground a council deliberation in verified knowledge
israg = IsRAGEngine()
council = DewanCouncil(api_key="sk-or-...")

# Ingest your knowledge base
israg.ingest(content="...", author="...", source_type=SourceType.GOVERNMENT)

# Query with grounding
retrieved = israg.retrieve("Your research question", include_isnad=True)
context = "\n".join([f"[trust={r.entry.trust_score:.2f}] {r.entry.content}" for r in retrieved])

# Deliberate with grounded context
result = council.deliberate("Your research question", context=context)
print(result.final_answer)
print(f"Consensus: {result.consensus_score}")
print(f"Dissent: {result.dissenting_views}")
```

## License

Apache 2.0.

## Part of the SULUH Ecosystem

IsRAG is one of three packages in the [SULUH Ecosystem](../../README.md):

- **`israg`** — provenance-aware retrieval (this package)
- **`council`** — multi-LLM deliberation
- **`suluh`** — multi-agent orchestration platform

See the [ecosystem README](../../README.md), the [architecture doc](../../docs/ARCHITECTURE.md), and the [research proposal](../../research/proposal/SULUH-ECOSYSTEM-PROPOSAL.md).
