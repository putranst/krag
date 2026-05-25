# KRAG - Knowledge-chain Retrieval Augmented Generation

An evolution of RAG that adds provenance chains, trust scoring, and cultural context.
Inspired by the Isnad (إسناد) framework from Islamic scholarship.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        KRAG SYSTEM                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    USER QUERY                            │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              KRAG RETRIEVAL ENGINE                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │   Content   │  │    Trust    │  │   Cultural  │     │   │
│  │  │  Matching   │  │   Scoring   │  │   Context   │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                      │
│              ┌────────────┴────────────┐                        │
│              ▼                         ▼                         │
│  ┌────────────────────┐    ┌────────────────────────┐          │
│  │   KNOWLEDGE BASE   │    │   DEWAN COUNCIL        │          │
│  │                    │    │   (optional)            │          │
│  │ • Entries          │    │                         │          │
│  │ • Provenance       │    │ • 7 LLM members         │          │
│  │ • Verifications    │    │ • Cross-review          │          │
│  │ • Cultural Context │    │ • Synthesis             │          │
│  └────────────────────┘    └────────────────────────┘          │
│              │                         │                         │
│              └────────────┬────────────┘                        │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  INTEGRATED RESULT                       │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │              FINAL ANSWER                        │   │   │
│  │  │  + Complete Isnad Chain                          │   │   │
│  │  │  + Trust Score (0-1)                             │   │   │
│  │  │  + Confidence Level                              │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. KnowledgeEntry
A piece of knowledge with full provenance tracking:
- Content
- Author & source type
- Provenance chain (who created, verified, adapted)
- Verification records
- Cultural context

### 2. TrustEngine
Calculates trust scores based on:
- Verification level (30%)
- Source credibility (25%)
- Verification quality (20%)
- Cross-references (15%)
- Freshness (10%)

### 3. CulturalContext
Knowledge doesn't exist in vacuum:
- Cultural framework (Indonesian, Thai, Vietnamese, etc.)
- Original language
- Applicability regions
- Known limitations
- Local terminology

### 4. IsnadChain
Complete provenance chain for human display:
- All steps from creation to retrieval
- All verifications with ratings
- Cultural context
- Final trust score

## Usage

### Basic KRAG

```python
from krag import KRAGEngine, SourceType, VerificationLevel

krag = KRAGEngine()

# Ingest knowledge
entry = krag.ingest(
    content="ASEAN has 670 million people...",
    author="UN Population Division",
    source_type=SourceType.GOVERNMENT,
    verification_level=VerificationLevel.INSTITUTION_VERIFIED
)

# Query
results = krag.retrieve("ASEAN population", include_isnad=True)
for r in results:
    print(r.content)
    print(r.isnad_chain.format_for_display())
```

### With Dewan Council

```python
from integration import IntegratedEngine

engine = IntegratedEngine(openrouter_api_key="sk-or-...")

# Complex query - uses both KRAG and Dewan Council
result = engine.query(
    "What's the best AI strategy for ASEAN?",
    use_council=True
)

print(result.final_answer)
print(result.isnad_chain)
```

## Trust Score Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Verification Level | 30% | How verified is this? (peer-reviewed, institutional, etc.) |
| Source Credibility | 25% | Type of source (government, academic, news, etc.) |
| Verification Quality | 20% | Ratings from verifiers |
| Cross-Reference | 15% | How many other entries reference this |
| Freshness | 10% | How recent is this knowledge |

## Cultural Frameworks Supported

- Global
- Western
- East Asian
- Southeast Asian
- Indonesian
- Malaysian
- Thai
- Vietnamese
- Filipino
- Singaporean
- Islamic
- Buddhist
- Indigenous

## Running

```bash
# Demo
python krag/krag_engine.py demo

# Ingest
python krag/krag_engine.py ingest --content "..." --author "..." --source government

# Query
python krag/krag_engine.py query --query "ASEAN population" --isnad

# Stats
python krag/krag_engine.py stats
```

## Integration with Dewan Council

KRAG and Dewan Council work together:

1. **Simple queries**: KRAG only (fast, trust-scored)
2. **Complex queries**: KRAG + Dewan Council (comprehensive, deliberated)
3. **Output**: Answer with full Isnad chain from both systems

## Future Enhancements

- [ ] Vector database integration (Pinecone, Weaviate)
- [ ] Blockchain anchoring for immutable provenance
- [ ] Multi-language knowledge entries
- [ ] Graph-based cross-referencing
- [ ] Automated verification pipelines
