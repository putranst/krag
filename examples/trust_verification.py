"""
Example: Trust Scoring & Verification Workflow
==============================================

Shows how knowledge evolves as more verifications are added.
Run: python examples/trust_verification.py
"""

from krag import KRAGEngine, SourceType, VerificationLevel


def main():
    krag = KRAGEngine()

    print("📥 Ingesting unverified claim...")

    # Step 1: Unverified claim
    entry = krag.ingest(
        content="Indonesia will be the world's 4th largest economy by 2045.",
        author="Policy Analyst A",
        source_type=SourceType.BLOG,
        verification_level=VerificationLevel.UNVERIFIED,
        tags=["indonesia", "economy", "projection"],
    )
    print(f"   Initial trust: {krag.trust_engine.calculate_trust_score(entry):.2f}")

    # Step 2: Verified by a journalist
    print("\n📝 Adding journalist verification...")
    krag.add_verification(
        entry_id=entry.entry_id,
        verifier="Senior Journalist B",
        verifier_type="person",
        level=VerificationLevel.SELF_REPORTED,
        rating=6.5,
        feedback="Source is a credible policy analyst but projection is speculative.",
    )
    entry = krag.get_entry(entry.entry_id)
    print(f"   Updated trust: {krag.trust_engine.calculate_trust_score(entry):.2f}")

    # Step 3: Verified by a research institution
    print("\n🎓 Adding research institution verification...")
    krag.add_verification(
        entry_id=entry.entry_id,
        verifier="Center for Strategic and International Studies (CSIS)",
        verifier_type="institution",
        level=VerificationLevel.INSTITUTION_VERIFIED,
        rating=8.5,
        feedback="Consistent with McKinsey Global Institute projections for ASEAN growth.",
    )
    entry = krag.get_entry(entry.entry_id)
    print(f"   Updated trust: {krag.trust_engine.calculate_trust_score(entry):.2f}")

    # Step 4: Peer-reviewed
    print("\n📚 Adding peer review...")
    krag.add_verification(
        entry_id=entry.entry_id,
        verifier="Journal of Southeast Asian Economies",
        verifier_type="institution",
        level=VerificationLevel.PEER_REVIEWED,
        rating=9.0,
        feedback="Methodology sound. Growth assumptions validated against historical data.",
    )
    entry = krag.get_entry(entry.entry_id)
    print(f"   Final trust: {krag.trust_engine.calculate_trust_score(entry):.2f}")

    # Show Isnad
    print("\n📜 Full Isnad Chain:")
    print("   " + "=" * 50)
    for step in entry.provenance:
        print(f"   Step: {step.action} | By: {step.actor} | Time: {step.timestamp}")
    for v in entry.verifications:
        print(f"   Verified: {v.verifier} ({v.level.value}) | Rating: {v.rating}/10")
    print("   " + "=" * 50)

    print("\n✅ Knowledge graduated from 'unverified' to 'high trust' through layered verification.")


if __name__ == "__main__":
    main()
