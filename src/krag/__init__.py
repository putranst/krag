"""
KRAG - Knowledge-chain Retrieval Augmented Generation
=======================================================

An evolution of RAG that adds provenance chains, trust scoring, and cultural context.
Inspired by the Isnad (إسناد) framework from Islamic scholarship.

Usage:
    from krag import KRAGEngine, SourceType, VerificationLevel
    
    krag = KRAGEngine()
    entry = krag.ingest(content="...", author="...", source_type=SourceType.GOVERNMENT)
    results = krag.retrieve("query", include_isnad=True)
"""

from .krag_engine import (
    KRAGEngine,
    KnowledgeEntry,
    ProvenanceStep,
    VerificationRecord,
    TrustEngine,
    IsnadChain,
    CulturalContext,
    RetrievalResult,
    SourceType,
    VerificationLevel,
    CulturalFramework,
)

__version__ = "0.1.0"
__author__ = "Putra Nasution"
__all__ = [
    "KRAGEngine",
    "KnowledgeEntry",
    "ProvenanceStep",
    "VerificationRecord",
    "TrustEngine",
    "IsnadChain",
    "CulturalContext",
    "RetrievalResult",
    "SourceType",
    "VerificationLevel",
    "CulturalFramework",
]
