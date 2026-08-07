"""
Example: Dewan Council — Multi-LLM Deliberation
================================================

Shows how Dewan Council deliberates on complex questions.
Requires OPENROUTER_API_KEY or run with --mock.

Run: python examples/dewan_demo.py
"""

import os
from dewan_council import DewanCouncil


def main():
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    mock_mode = not api_key

    if mock_mode:
        print("📝 Running in MOCK mode (no API calls)\n")
        print("   To use real LLMs: export OPENROUTER_API_KEY=sk-or-...")
        print()
    else:
        print("🧠 Running with real LLMs via OpenRouter\n")

    council = DewanCouncil(api_key=api_key or "mock")

    # Simple question
    query = "What is the most effective strategy for AI sovereignty in Southeast Asia?"
    print(f"🕌 DEWAN COUNCIL deliberating: {query}\n")

    result = council.deliberate(query)

    print("=" * 60)
    print("🎯 FINAL ANSWER (Chairman Synthesis)")
    print("=" * 60)
    print(result.final_answer)
    print()

    print(f"✅ Consensus Score: {result.isnad_chain.consensus_score:.2f}")
    print(f"👥 Council Members: {len(result.isnad_chain.stage1_opinions)}")
    print(f"🔄 Cross-Reviews: {len(result.isnad_chain.stage2_reviews)}")

    if result.isnad_chain.dissenting_views:
        print(f"⚠️  Dissenting Views: {len(result.isnad_chain.dissenting_views)}")
        for view in result.isnad_chain.dissenting_views:
            print(f"   - {view[:100]}...")


if __name__ == "__main__":
    main()
