"""
Example: Cultural Context Filtering
=====================================

Shows how IsRAG handles culturally-specific knowledge.
Run: python examples/cultural_context.py
"""

from israg import IsRAGEngine, SourceType, VerificationLevel, CulturalContext, CulturalFramework


def main():
    krag = IsRAGEngine()

    print("📥 Ingesting culturally-contextualized knowledge...\n")

    # Indonesian cultural concept
    krag.ingest(
        content="Gotong royong is a communal cooperation practice where community members "
                "work together voluntarily for mutual benefit, deeply rooted in Indonesian tradition.",
        author="Dr. Siti Nurbaya",
        source_type=SourceType.ACADEMIC,
        verification_level=VerificationLevel.PEER_REVIEWED,
        cultural_context=CulturalContext(
            framework=CulturalFramework.INDONESIAN,
            language_original="Indonesian",
            applicability=["Indonesia", "Southeast Asia"],
            limitations=["Cultural concept; may not translate to individualistic societies"],
            local_terms={"gotong royong": "mutual assistance, communal cooperation"},
        ),
        tags=["culture", "indonesia", "cooperation"],
    )

    # Islamic finance concept
    krag.ingest(
        content="Mudarabah is a profit-sharing partnership in Islamic finance where one party "
                "provides capital and the other provides labor/management expertise.",
        author="Islamic Bank of Malaysia",
        source_type=SourceType.GOVERNMENT,
        verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        cultural_context=CulturalContext(
            framework=CulturalFramework.ISLAMIC,
            language_original="Arabic",
            applicability=["Muslim-majority countries", "Islamic finance institutions"],
            limitations=["Requires Shariah compliance framework"],
            local_terms={"mudarabah": "profit-sharing partnership"},
        ),
        tags=["islamic-finance", "cooperation", "investment"],
    )

    # Western corporate concept
    krag.ingest(
        content="Equity crowdfunding allows startups to raise capital from a large number of "
                "small investors in exchange for equity ownership.",
        author="SEC Office",
        source_type=SourceType.GOVERNMENT,
        verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        cultural_context=CulturalContext(
            framework=CulturalFramework.WESTERN,
            language_original="English",
            applicability=["US", "EU", "Common law jurisdictions"],
            limitations=["Requires securities regulation compliance"],
        ),
        tags=["crowdfunding", "investment", "startup"],
    )

    print("✅ Ingested 3 culturally-framed entries\n")

    # Retrieve with cultural filter
    print("🔍 Query: 'cooperation investment' | Filter: Islamic framework")
    results = krag.retrieve(
        "cooperation investment",
        cultural_filter=CulturalFramework.ISLAMIC,
        include_isnad=True,
    )

    for r in results:
        print(f"\n  📄 {r.entry_id}")
        print(f"     Framework: {r.cultural_context.framework.value}")
        print(f"     Trust: {r.trust_score:.2f}")
        print(f"     Content: {r.content[:100]}...")

    # Retrieve with Indonesian filter
    print("\n🔍 Query: 'community help' | Filter: Indonesian framework")
    results = krag.retrieve(
        "community help",
        cultural_filter=CulturalFramework.INDONESIAN,
        include_isnad=True,
    )

    for r in results:
        print(f"\n  📄 {r.entry_id}")
        print(f"     Framework: {r.cultural_context.framework.value}")
        print(f"     Local terms: {r.cultural_context.local_terms}")
        print(f"     Trust: {r.trust_score:.2f}")


if __name__ == "__main__":
    main()
