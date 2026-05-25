"""
Dewan Council CLI — Command-line interface for LLM deliberation.

Requires OPENROUTER_API_KEY environment variable.
"""

import argparse
import json
import os
import sys

from .dewan_council import DewanCouncil


def main():
    parser = argparse.ArgumentParser(
        description="Dewan Council — Multi-LLM Deliberation System"
    )
    parser.add_argument("query", nargs="?", help="Question to deliberate")
    parser.add_argument(
        "--verbose", action="store_true", help="Show full deliberation log"
    )
    parser.add_argument(
        "--mock", action="store_true", help="Run in mock mode (no API calls)"
    )
    parser.add_argument(
        "--output", help="Save result to JSON file"
    )

    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY", "")

    if not args.mock and not api_key:
        print("❌ OPENROUTER_API_KEY not set. Set it or use --mock", file=sys.stderr)
        print("   export OPENROUTER_API_KEY=sk-or-...", file=sys.stderr)
        sys.exit(1)

    council = DewanCouncil(api_key=api_key or "mock")

    if args.query:
        query = args.query
    else:
        query = input("Enter your question: ")

    print(f"\n🕌 DEWAN COUNCIL — Deliberating: {query}\n")

    if args.mock:
        print("📝 Mock mode — no API calls\n")
        result = council.deliberate(query)
    else:
        result = council.deliberate(query)

    print("=" * 60)
    print("🎯 FINAL ANSWER")
    print("=" * 60)
    print(result.final_answer)
    print()

    if args.verbose:
        print("=" * 60)
        print("📜 ISNAD CHAIN")
        print("=" * 60)
        print(json.dumps(result.isnad_chain.to_dict(), indent=2, ensure_ascii=False))
        print()

        print("=" * 60)
        print("🗣️  STAGE 1 — FIRST OPINIONS")
        print("=" * 60)
        for opinion in result.isnad_chain.stage1_opinions:
            print(f"\n👤 {opinion.member.name} ({opinion.member.role})")
            print(f"   Confidence: {opinion.confidence}")
            print(f"   {opinion.response[:500]}...")

        print("\n" + "=" * 60)
        print("🔍 STAGE 2 — CROSS REVIEWS")
        print("=" * 60)
        for review in result.isnad_chain.stage2_reviews:
            print(f"\n{review.reviewer.name} → {review.reviewed.name}: {review.rating}/10")
            if review.feedback:
                print(f"   Feedback: {review.feedback[:200]}...")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        print(f"💾 Saved to {args.output}")

    print(f"\n✅ Consensus Score: {result.isnad_chain.consensus_score:.2f}")


if __name__ == "__main__":
    main()
