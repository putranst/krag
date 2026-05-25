"""
Dewan Council - LLM Deliberation System
=======================================

A council of multiple LLMs that deliberate together to answer complex questions.
Inspired by Karpathy's llm-council and the Isnad framework.

Usage:
    from dewan_council import DewanCouncil
    
    council = DewanCouncil(api_key="sk-or-...")
    result = council.deliberate("What is the best AI strategy for ASEAN?")
    print(result.final_answer)
"""

from .dewan_council import (
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
