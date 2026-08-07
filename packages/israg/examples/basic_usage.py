"""
Example: Basic IsRAG Usage
=========================

Shows how to ingest knowledge and retrieve it with trust scoring.
Run: python examples/basic_usage.py
"""

from israg import IsRAGEngine, SourceType, VerificationLevel


def main():
    # Create engine
    krag = IsRAGEngine()

    # Ingest knowledge with provenance
    print("📥 Ingesting knowledge...")

    entry1 = krag.ingest(
        content="ASEAN has approximately 670 million people.",
        author="UN Population Division",
        source_type=SourceType.GOVERNMENT,
        verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        tags=["asean", "population"],
    )
    print(f"  ✅ {entry1.entry_id} | Trust: {krag.trust_engine.calculate_trust_score(entry1):.2f}")

    entry2 = krag.ingest(
        content="Indonesia's UMKM sector employs 97% of the workforce.",
        author="Ministry of Cooperatives and SMEs",
        source_type=SourceType.GOVERNMENT,
        verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        tags=["indonesia", "umkm", "employment"],
    )
    print(f"  ✅ {entry2.entry_id} | Trust: {krag.trust_engine.calculate_trust_score(entry2):.2f}")

    entry3 = krag.ingest(
        content="AI will replace all jobs by 2025.",
        author="Random Blogger",
        source_type=SourceType.BLOG,
        verification_level=VerificationLevel.UNVERIFIED,
        tags=["ai", "prediction"],
    )
    print(f"  ✅ {entry3.entry_id} | Trust: {krag.trust_engine.calculate_trust_score(entry3):.2f}")

    # Retrieve with trust filter
    print("\n🔍 Query: 'Indonesia workforce' (min trust 0.5)")
    results = krag.retrieve(
        "Indonesia workforce",
        min_trust_score=0.5,
        include_isnad=True,
    )

    for r in results:
        print(f"\n  📄 {r.entry_id}")
        print(f"     Trust: {r.trust_score:.2f} ({r.confidence_level})")
        print(f"     Content: {r.content[:80]}...")

    # Show stats
    print("\n📊 Knowledge Base Stats:")
    stats = krag.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")


if __name__ == "__main__":
    main()
