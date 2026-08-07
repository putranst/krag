# Dewan Council — Multi-LLM Deliberation

> *A council of models, reasoning together. The audit trail is the product.*

**Package:** `council` (in the SULUH Ecosystem monorepo)
**Status:** v0.1 alpha — working engine, in active development
**Paper:** See [`../../research/papers/paper-2-council.md`](../../research/papers/paper-2-council.md) for the full academic contribution.

---

## What this is

Dewan Council is a **three-stage multi-LLM deliberation protocol** in which:

1. Each council member produces an independent first-stage opinion
2. Each member reviews and rates the other members' opinions
3. A designated chairman synthesises a final answer that explicitly carries the dissent forward, names the consensus score, and emits a complete provenance chain

The protocol is **model-agnostic**: it works with any combination of LLMs accessible via a unified API. The reference implementation uses OpenRouter for single-API access to all major models.

The protocol is **designed to integrate with IsRAG**: each opinion in the deliberation is grounded in verifiable, trust-scored knowledge, and the chairman's synthesis inherits those trust scores.

---

## The reference council

| Role | Model | Specialty |
|---|---|---|
| 👑 Ketua (Chairman) | Claude Opus 4.7 | Synthesis, judgment |
| 🧠 Member | GPT-5.5 | Deep reasoning |
| 📊 Member | Gemini 3 Flash | Data, multimodal |
| 📖 Member | Kimi K2.6 | Long context, multi-agent |
| 🔢 Member | Deepseek V4 Flash | Chain-of-thought |
| 🌏 Member | Qwen 3.6 Plus | Multilingual, Asia |
| 💻 Member | Nemotron 3 Super | Open model, free tier |

All accessed via **OpenRouter** (single API key).

---

## Quick start

```python
import os
from council import DewanCouncil

council = DewanCouncil(api_key=os.environ["OPENROUTER_API_KEY"])

result = council.deliberate(
    "What is the best AI strategy for ASEAN higher education?"
)

print("=== FINAL ANSWER ===")
print(result.final_answer)

print(f"\n=== CONSENSUS: {result.consensus_score:.2f} ===")
print(f"=== DISSENTING VIEWS ({len(result.dissenting_views)}) ===")
for view in result.dissenting_views:
    print(f"  - {view[:200]}...")

print(f"\n=== ISNAD CHAIN ===")
print(result.isnad_chain)
```

### Mock mode (no API key)

```python
council = DewanCouncil()  # no key → mock mode for testing
result = council.deliberate("test question")
```

---

## The 3 stages

### Stage 1: First opinions
Each member is queried independently with the same prompt. Each `Opinion` carries the response text, a self-assessed confidence score, and the model identifier.

### Stage 2: Cross-review
Each member reviews every other member's opinion. For N members, this produces N²−N reviews. Each review carries a rating (1–10), free-text feedback, and a list of issues found.

### Stage 3: Chairman synthesis
The chairman receives the original query, all Stage 1 opinions, all Stage 2 reviews, and the review matrix summary. The chairman produces:
- `final_answer`
- `consensus_score` (0.0–1.0)
- `dissenting_views` (list)
- `isnad_chain` (full audit trail)

---

## When to use it

✅ **Use Dewan Council for:**
- Multi-perspective questions where seeing the reasoning matters
- Policy / research / clinical decisions where auditability is required
- Complex synthesis where multiple defensible framings exist
- When the downstream user benefits from seeing the dissent

❌ **Do NOT use Dewan Council for:**
- Simple single-fact retrieval (use IsRAG alone)
- High-volume low-stakes queries (use single-LLM)
- Time-sensitive tasks (deliberation is slow)
- When all members are likely to agree (overhead without benefit)

---

## Integration with IsRAG

```python
from israg import IsRAGEngine, SourceType
from council import DewanCouncil

israg = IsRAGEngine()
council = DewanCouncil(api_key="...")

# Ground the deliberation in verified, trust-scored knowledge
israg.ingest(content="...", author="...", source_type=SourceType.GOVERNMENT)
retrieved = israg.retrieve("Your question", include_isnad=True)

# Build grounded context with trust scores
context = "\n\n".join([
    f"[Source: {r.entry.author}, trust={r.entry.trust_score:.2f}]\n{r.entry.content}"
    for r in retrieved
])

result = council.deliberate("Your question", context=context)
```

The chairman's synthesis will inherit the trust scores, so downstream users see both the consensus answer and the trust-weighted grounding.

---

## License

Apache 2.0.

## Part of the SULUH Ecosystem

Dewan Council is one of three packages in the [SULUH Ecosystem](../../README.md):

- **`israg`** — provenance-aware retrieval
- **`council`** — multi-LLM deliberation (this package)
- **`suluh`** — multi-agent orchestration platform

See the [ecosystem README](../../README.md), the [architecture doc](../../docs/ARCHITECTURE.md), and the [research proposal](../../research/proposal/SULUH-ECOSYSTEM-PROPOSAL.md).
