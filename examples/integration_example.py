"""
Example: KRAG + Dewan Council Integration
=========================================

Shows how KRAG retrieval feeds into Dewan Council deliberation
for complex, knowledge-grounded answers.

Run: python examples/integration_example.py
"""

import os
from krag import KRAGEngine, SourceType, VerificationLevel, CulturalContext, CulturalFramework
from dewan_council import DewanCouncil


def main():
    print("🔬 KRAG + DEWAN COUNCIL INTEGRATION DEMO\n")

    # Step 1: Build a knowledge base with KRAG
    print("📥 Building knowledge base...")
    krag = KRAGEngine()

    krag.ingest(
        content="Indonesia's digital economy reached $77 billion in 2024, growing 18% YoY.",
        author="Google, Temasek, Bain & Company",
        source_type=SourceType.RESEARCH,
        verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        tags=["indonesia", "digital-economy"],
    )

    krag.ingest(
        content="Local language models (e.g., Qwen, SeaLLM) reduce inference costs by 40-60% "
                "compared to Western models for Southeast Asian languages.",
        author="AI Research Lab Indonesia",
        source_type=SourceType.RESEARCH,
        verification_level=VerificationLevel.PEER_REVIEWED,
        tags=["local-llm", "cost", "southeast-asia"],
    )

    krag.ingest(
        content="Data sovereignty policies in Indonesia require critical data to be stored "
                "within national borders under Government Regulation No. 71 of 2019.",
        author="Ministry of Communication and Informatics",
        source_type=SourceType.GOVERNMENT,
        verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        cultural_context=CulturalContext(
            framework=CulturalFramework.INDONESIAN,
            language_original="Indonesian",
            applicability=["Indonesia"],
            limitations=["National regulation, not applicable to other ASEAN countries"],
        ),
        tags=["indonesia", "data-sovereignty", "regulation"],
    )

    print(f"✅ Ingested {len(krag.knowledge_base)} entries\n")

    # Step 2: Retrieve relevant knowledge
    query = "How can Indonesia achieve AI sovereignty while keeping costs low?"
    print(f"🔍 KRAG Query: {query}")

    krag_results = krag.retrieve(
        query,
        min_trust_score=0.5,
        include_isnad=True,
    )

    print(f"   Retrieved {len(krag_results)} entries with trust >= 0.5\n")

    # Build context from KRAG results
    context = "\n\n".join([
        f"[{r.confidence_level}] {r.content}\n"
        f"   Source: {r.source_type.value} | Trust: {r.trust_score:.2f}"
        for r in krag_results
    ])

    # Step 3: Feed to Dewan Council
    print("🕌 Sending to Dewan Council for deliberation...\n")

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    council = DewanCouncil(api_key=api_key or "mock")

    deliberation_query = (
        f"Question: {query}\n\n"
        f"Grounding Knowledge (from KRAG retrieval):\n\n{context}\n\n"
        f"Please deliberate on this question using the provided knowledge as grounding. "
        f"Note the trust scores and cultural context of each piece of knowledge."
    )

    mock_mode = not api_key
    if mock_mode:
        print("📝 Running in MOCK mode (no API calls)")
        print("   To use real LLMs: export OPENROUTER_API_KEY=sk-or-...")
        print()

    result = council.deliberate(deliberation_query)

    print("=" * 60)
    print("🎯 SYNTHESIZED ANSWER")
    print("=" * 60)
    print(result.final_answer)
    print()

    print(f"✅ Consensus: {result.isnad_chain.consensus_score:.2f}")
    print(f"👥 Council deliberated with {len(result.isnad_chain.stage1_opinions)} members")
    print(f"🔄 {len(result.isnad_chain.stage2_reviews)} cross-reviews performed")

    # Show provenance
    print("\n📜 KNOWLEDGE PROVENANCE:")
    for r in krag_results:
        print(f"   • {r.entry_id}: {r.source_type.value} | Trust {r.trust_score:.2f}")


if __name__ == "__main__":
    main()
