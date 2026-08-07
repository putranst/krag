# Rebrand note: KRAG → IsRAG

**Effective:** May 2026
**Scope:** All packages, all docs, all papers, all public-facing material

---

## What changed

| Before | After | Why |
|---|---|---|
| `krag` (Knowledge-chain Retrieval Augmented Generation) | `israg` (*Isnad*-chain Retrieval Augmented Generation) | The Islamic *Isnad* framework is the conceptual heart of the system. Naming the project after the tradition makes the contribution legible, citable, and aligned with the academic framing of the paper. "IsRAG" also reads as a natural acronym next to the academic venues (ACL, EMNLP, FAccT) where the paper will be submitted. |
| `KRAGEngine` | `IsRAGEngine` | Match the new package name |
| `Knowledge-chain RAG` | `Isnad-chain RAG` | Same shift; both phrasings remain valid in academic text but "Isnad-chain" is the canonical form |
| PyPI / pip name `krag` | `israg` | Match the new package name |
| `from krag import ...` | `from israg import ...` | Match the new package name |
| GitHub repo `krag` (was planned public) | Private (no public repo; ecosystem is private) | Per the consortium decision, the SULUH Ecosystem is private and not for public distribution |

## What did NOT change

- The data model (KnowledgeEntry, ProvenanceChain, VerificationRecord, TrustEngine, CulturalContext, IsnadChain) — same names, same semantics
- The 5-factor trust scoring weights
- The 13 cultural frameworks supported
- The integration with Dewan Council (now: the `council` package)
- The Apache 2.0 license

## Migration

If you have existing code using `krag`:

```python
# Before
from krag import KRAGEngine, SourceType, VerificationLevel

krag = KRAGEngine()
entry = krag.ingest(content="...", author="...", source_type=SourceType.GOVERNMENT)
result = krag.retrieve("...", include_isnad=True)
```

```python
# After
from israg import IsRAGEngine, SourceType, VerificationLevel

israg = IsRAGEngine()
entry = israg.ingest(content="...", author="...", source_type=SourceType.GOVERNMENT)
result = israg.retrieve("...", include_isnad=True)
```

Variable name `krag` is unchanged (variable names are local; the class name changed).

## Rationale for the rebrand

1. **The "Knowledge-chain" framing was generic.** It did not communicate the unique contribution. "Isnad-chain" is specific, citable, and anchored in a 1,000-year-old scholarly tradition.
2. **The academic paper (Paper 1) is built on the Isnad concept.** Aligning the code name with the paper name reduces cognitive load and strengthens the contribution.
3. **"IsRAG" is short, pronounceable, and memorable.** It also evokes "is" — "this *is* RAG, but with provenance" — which is what the system is.
4. **Decolonial AI framing.** Naming the system after a non-Western knowledge-validation tradition is a small but explicit statement that AI retrieval can be grounded in non-Western epistemologies.

## Old name kept as alias (transitional)

For at least one release cycle, `KRAGEngine` remains importable as a deprecated alias:

```python
# Still works, but emits a DeprecationWarning
from israg import KRAGEngine  # → IsRAGEngine (preferred)
```

This will be removed in v0.3.

---

*This is a code, documentation, and paper-level rebrand. The underlying research contribution, the data model, and the integration architecture are unchanged.*
