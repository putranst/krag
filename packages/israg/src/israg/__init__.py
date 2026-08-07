"""
IsRAG - Isnad-chain Retrieval Augmented Generation
=======================================================

An evolution of RAG that adds provenance chains, trust scoring, and cultural context.
Inspired by the Isnad (إسناد) framework from Islamic scholarship.

Usage:
    from israg import IsRAGEngine, SourceType, VerificationLevel
    
    krag = IsRAGEngine()
    entry = krag.ingest(content="...", author="...", source_type=SourceType.GOVERNMENT)
    results = krag.retrieve("query", include_isnad=True)
"""

from .israg_engine import (
    IsRAGEngine,
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
    "IsRAGEngine",
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
