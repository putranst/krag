"""
KRAG CLI — Command-line interface for the Knowledge-chain RAG engine.
"""

import argparse
import json
import sys

from .krag_engine import KRAGEngine, SourceType, VerificationLevel


def main():
    parser = argparse.ArgumentParser(
        description="KRAG — Knowledge-chain Retrieval Augmented Generation"
    )
    parser.add_argument(
        "action",
        choices=["demo", "ingest", "query", "stats"],
        help="Action to perform",
    )
    parser.add_argument("--content", help="Content to ingest")
    parser.add_argument("--author", help="Author name")
    parser.add_argument(
        "--source",
        default="RESEARCH",
        choices=[st.name for st in SourceType],
        help="Source type",
    )
    parser.add_argument("--query", help="Query string")
    parser.add_argument(
        "--isnad", action="store_true", help="Show Isnad chain in output"
    )
    parser.add_argument(
        "--min-trust", type=float, default=0.0, help="Minimum trust score filter"
    )

    args = parser.parse_args()
    krag = KRAGEngine()

    if args.action == "demo":
        run_demo(krag)
    elif args.action == "ingest":
        if not args.content:
            print("❌ --content is required for ingest", file=sys.stderr)
            sys.exit(1)
        entry = krag.ingest(
            content=args.content,
            author=args.author or "Unknown",
            source_type=SourceType[args.source],
        )
        print(f"✅ Ingested: {entry.entry_id}")
    elif args.action == "query":
        if not args.query:
            print("❌ --query is required for query", file=sys.stderr)
            sys.exit(1)
        results = krag.retrieve(
            args.query,
            min_trust_score=args.min_trust,
            include_isnad=args.isnad,
        )
        for r in results:
            print(r.format_for_display(show_isnad=args.isnad))
            print()
    elif args.action == "stats":
        print(json.dumps(krag.get_stats(), indent=2))


def run_demo(krag: KRAGEngine):
    """Run an interactive demo."""
    print("\n🔬 KRAG DEMO — Knowledge-chain RAG\n")

    print("📥 Ingesting knowledge entries...\n")

    krag.ingest(
        content="ASEAN's total population is approximately 670 million people as of 2024.",
        author="UN Population Division",
        source_type=SourceType.GOVERNMENT,
        author_type="institution",
        verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        tags=["asean", "population"],
    )

    krag.ingest(
        content="Indonesia has 64.2 million MSMEs (UMKM), contributing 61% to GDP.",
        author="Ministry of Cooperative and SME Indonesia",
        source_type=SourceType.GOVERNMENT,
        author_type="institution",
        verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        tags=["indonesia", "umkm", "economy"],
    )

    krag.ingest(
        content="The AI market in Southeast Asia is projected to reach $24.9 billion by 2030.",
        author="IDC Asia Pacific",
        source_type=SourceType.RESEARCH,
        author_type="institution",
        verification_level=VerificationLevel.PEER_REVIEWED,
        tags=["ai", "market", "asean"],
    )

    krag.ingest(
        content="Gotong royong is a foundational principle in Indonesian society.",
        author="Dr. Siti Nurbaya",
        source_type=SourceType.ACADEMIC,
        author_type="person",
        verification_level=VerificationLevel.PEER_REVIEWED,
        tags=["culture", "indonesia", "cooperation"],
    )

    print(f"✅ Ingested {len(krag.knowledge_base)} entries\n")

    print("🔍 Query: 'ASEAN population and economy'\n")
    results = krag.retrieve("ASEAN population economy", include_isnad=True)

    for r in results[:3]:
        print(r.format_for_display(show_isnad=True))
        print()

    print("📊 Knowledge Base Stats:")
    print(json.dumps(krag.get_stats(), indent=2))
    print()


if __name__ == "__main__":
    main()
