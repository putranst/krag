"""
Dewan Council — Multi-LLM Deliberation System
==============================================

A council of multiple LLMs that deliberate together to answer complex questions.
Inspired by Karpathy's llm-council and the Islamic Isnad framework.

Flow:
  Stage 1 — All council members give their first opinions
  Stage 2 — Members review and rate each other's responses
  Stage 3 — Chairman synthesizes the final response with full isnad chain

Designed to compose with IsRAG:
  - Each member's opinion can be grounded in IsRAG KnowledgeEntry objects
  - The chairman's synthesis inherits the IsRAG trust scores
  - The deliberation is auditable end-to-end via the isnad chain

Usage:
    from council import DewanCouncil
    council = DewanCouncil(api_key="sk-or-...")
    result = council.deliberate("What is the best AI strategy for ASEAN?")
    print(result.final_answer)
    print(result.consensus_score)
    print(result.dissenting_views)
"""

from .council_engine import (
    DewanCouncil,
    CouncilMember,
    Opinion,
    Review,
    IsnadChain,
    DeliberationResult,
)

__version__ = "0.1.0"
__author__ = "Putra Nasution"
__all__ = [
    "DewanCouncil",
    "CouncilMember",
    "Opinion",
    "Review",
    "IsnadChain",
    "DeliberationResult",
]
