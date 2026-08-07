"""
IsRAG - Isnad-chain Retrieval Augmented Generation
=====================================================

An evolution of RAG that adds provenance chains, trust scoring, and cultural context.
Inspired by the Isnad framework - every piece of knowledge has a traceable lineage.

Core Components:
1. KnowledgeEntry - A piece of knowledge with full provenance
2. ProvenanceChain - The chain of custody (author → verifier → storage → retrieval)
3. TrustEngine - Calculates trust scores based on multiple factors
4. CulturalContext - Knowledge doesn't exist in vacuum - it has cultural framework
5. RetrievalEngine - IsRAG retrieval with trust-weighted results

Usage:
    from israg import IsRAGEngine
    
    krag = IsRAGEngine()
    
    # Store knowledge with provenance
    krag.ingest(
        content="ASEAN has 670 million people...",
        author="Research Team",
        source_type="research",
        verification_level="peer_reviewed",
        cultural_context="southeast_asian"
    )
    
    # Query with full isnad
    result = krag.retrieve("Population of ASEAN?", include_isnad=True)
    print(result.content)
    print(result.isnad_chain)  # Full provenance
    print(result.trust_score)  # 0.0 - 1.0
"""

import hashlib
import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


# =============================================================================
# ENUMS AND TYPES
# =============================================================================

class SourceType(Enum):
    """Types of knowledge sources."""
    RESEARCH = "research"
    INSTITUTIONAL = "institutional"
    GOVERNMENT = "government"
    ACADEMIC = "academic"
    NEWS = "news"
    EXPERT = "expert"
    COMMUNITY = "community"
    AI_GENERATED = "ai_generated"
    FIELD_DATA = "field_data"


class VerificationLevel(Enum):
    """How verified is this knowledge?"""
    UNVERIFIED = 0
    SELF_REPORTED = 1
    PEER_REVIEWED = 2
    INSTITUTION_VERIFIED = 3
    MULTI_SOURCE_CONFIRMED = 4
    FIELD_VALIDATED = 5


class CulturalFramework(Enum):
    """Cultural context for knowledge."""
    GLOBAL = "global"
    WESTERN = "western"
    EAST_ASIAN = "east_asian"
    SOUTHEAST_ASIAN = "southeast_asian"
    SOUTH_ASIAN = "south_asian"
    INDONESIAN = "indonesian"
    MALAYSIAN = "malaysian"
    THAI = "thai"
    VIETNAMESE = "vietnamese"
    FILIPINO = "filipino"
    SINGAPOREAN = "singaporean"
    ISLAMIC = "islamic"
    BUDDHIST = "buddhist"
    INDIGENOUS = "indigenous"


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class ProvenanceStep:
    """A single step in the provenance chain."""
    step_type: str  # creation, verification, storage, retrieval, adaptation
    entity: str  # Who/what performed this step
    entity_type: str  # person, institution, system
    timestamp: datetime
    action: str  # Description of what happened
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "step_type": self.step_type,
            "entity": self.entity,
            "entity_type": self.entity_type,
            "timestamp": self.timestamp.isoformat(),
            "action": self.action,
            "metadata": self.metadata
        }


@dataclass
class VerificationRecord:
    """Record of verification for a knowledge entry."""
    verifier: str
    verifier_type: str  # institution, peer, ai, community
    level: VerificationLevel
    timestamp: datetime
    rating: float  # 0-10 quality rating
    feedback: str = ""
    issues_found: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "verifier": self.verifier,
            "verifier_type": self.verifier_type,
            "level": self.level.name,
            "level_value": self.level.value,
            "timestamp": self.timestamp.isoformat(),
            "rating": self.rating,
            "feedback": self.feedback,
            "issues_found": self.issues_found
        }


@dataclass
class CulturalContext:
    """Cultural context for a knowledge entry."""
    framework: CulturalFramework
    language_original: str
    applicability: list[str]  # Where does this knowledge apply?
    limitations: list[str]  # What are the boundaries?
    local_terms: dict[str, str] = field(default_factory=dict)  # Local terminology
    adaptation_notes: str = ""
    
    def to_dict(self) -> dict:
        return {
            "framework": self.framework.value,
            "language_original": self.language_original,
            "applicability": self.applicability,
            "limitations": self.limitations,
            "local_terms": self.local_terms,
            "adaptation_notes": self.adaptation_notes
        }


@dataclass
class IsnadChain:
    """Complete Isnad (provenance chain) for a knowledge entry."""
    entry_id: str
    provenance_steps: list[ProvenanceStep]
    verifications: list[VerificationRecord]
    cultural_context: CulturalContext
    trust_score: float  # 0-1
    confidence_level: str  # low, medium, high, very_high
    
    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "provenance_chain": [s.to_dict() for s in self.provenance_steps],
            "verifications": [v.to_dict() for v in self.verifications],
            "cultural_context": self.cultural_context.to_dict(),
            "trust_score": self.trust_score,
            "confidence_level": self.confidence_level
        }
    
    def format_for_display(self) -> str:
        """Human-readable Isnad chain."""
        lines = [
            "╔════════════════════════════════════════════════════════════╗",
            "║                    ISNAD CHAIN                             ║",
            "║              Rantai Asal-Usul Pengetahuan                  ║",
            "╚════════════════════════════════════════════════════════════╝",
            f"\n📝 Entry ID: {self.entry_id}",
            f"🔒 Trust Score: {self.trust_score:.2f} ({self.confidence_level})",
        ]
        
        lines.append("\n" + "─" * 60)
        lines.append("📜 PROVENANCE CHAIN:")
        lines.append("─" * 60)
        
        for i, step in enumerate(self.provenance_steps, 1):
            lines.append(f"\n[{i}] {step.step_type.upper()}")
            lines.append(f"    Entity: {step.entity} ({step.entity_type})")
            lines.append(f"    Action: {step.action}")
            lines.append(f"    Date: {step.timestamp.strftime('%Y-%m-%d %H:%M')}")
        
        lines.append("\n" + "─" * 60)
        lines.append("✅ VERIFICATIONS:")
        lines.append("─" * 60)
        
        for v in self.verifications:
            lines.append(f"\n• {v.verifier} ({v.verifier_type})")
            lines.append(f"  Level: {v.level.name} | Rating: {v.rating}/10")
            if v.feedback:
                lines.append(f"  Feedback: {v.feedback[:100]}...")
        
        lines.append("\n" + "─" * 60)
        lines.append("🌏 CULTURAL CONTEXT:")
        lines.append("─" * 60)
        lines.append(f"\n• Framework: {self.cultural_context.framework.value}")
        lines.append(f"• Original Language: {self.cultural_context.language_original}")
        lines.append(f"• Applicable: {', '.join(self.cultural_context.applicability)}")
        if self.cultural_context.limitations:
            lines.append(f"• Limitations: {', '.join(self.cultural_context.limitations)}")
        
        return "\n".join(lines)


@dataclass
class KnowledgeEntry:
    """A piece of knowledge with full provenance tracking."""
    content: str
    entry_id: str
    author: str
    author_type: str  # person, institution, ai
    source_type: SourceType
    created_at: datetime
    provenance: list[ProvenanceStep] = field(default_factory=list)
    verifications: list[VerificationRecord] = field(default_factory=list)
    cultural_context: Optional[CulturalContext] = None
    tags: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        # Generate ID if not provided
        if not self.entry_id:
            content_hash = hashlib.sha256(self.content.encode()).hexdigest()[:16]
            self.entry_id = f"ke-{content_hash}"
        
        # Add creation step to provenance
        if not self.provenance:
            self.provenance.append(ProvenanceStep(
                step_type="creation",
                entity=self.author,
                entity_type=self.author_type,
                timestamp=self.created_at,
                action=f"Created knowledge entry from {self.source_type.value} source"
            ))
    
    def add_verification(self, verification: VerificationRecord):
        """Add a verification record."""
        self.verifications.append(verification)
    
    def add_provenance_step(self, step: ProvenanceStep):
        """Add a provenance step (e.g., adaptation, translation)."""
        self.provenance.append(step)
    
    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "content": self.content,
            "author": self.author,
            "author_type": self.author_type,
            "source_type": self.source_type.value,
            "created_at": self.created_at.isoformat(),
            "provenance": [p.to_dict() for p in self.provenance],
            "verifications": [v.to_dict() for v in self.verifications],
            "cultural_context": self.cultural_context.to_dict() if self.cultural_context else None,
            "tags": self.tags,
            "metadata": self.metadata
        }


# =============================================================================
# TRUST ENGINE
# =============================================================================

class TrustEngine:
    """
    Calculates trust scores for knowledge entries.
    
    Factors:
    1. Verification level (weight: 0.30)
    2. Source credibility (weight: 0.25)
    3. Verification count and quality (weight: 0.20)
    4. Cross-reference consistency (weight: 0.15)
    5. Age/freshness (weight: 0.10)
    """
    
    # Source type base credibility scores
    SOURCE_CREDIBILITY = {
        SourceType.GOVERNMENT: 0.85,
        SourceType.ACADEMIC: 0.90,
        SourceType.RESEARCH: 0.85,
        SourceType.INSTITUTIONAL: 0.80,
        SourceType.EXPERT: 0.75,
        SourceType.FIELD_DATA: 0.70,
        SourceType.COMMUNITY: 0.60,
        SourceType.NEWS: 0.50,
        SourceType.AI_GENERATED: 0.40,
    }
    
    # Weights for trust calculation
    WEIGHTS = {
        "verification_level": 0.30,
        "source_credibility": 0.25,
        "verification_quality": 0.20,
        "cross_reference": 0.15,
        "freshness": 0.10,
    }
    
    def calculate_trust_score(self, entry: KnowledgeEntry) -> float:
        """
        Calculate overall trust score (0-1) for a knowledge entry.
        """
        scores = {
            "verification_level": self._score_verification_level(entry),
            "source_credibility": self._score_source_credibility(entry),
            "verification_quality": self._score_verification_quality(entry),
            "cross_reference": self._score_cross_reference(entry),
            "freshness": self._score_freshness(entry),
        }
        
        # Weighted sum
        total = sum(
            scores[key] * self.WEIGHTS[key]
            for key in scores
        )
        
        return min(1.0, max(0.0, total))
    
    def _score_verification_level(self, entry: KnowledgeEntry) -> float:
        """Score based on highest verification level."""
        if not entry.verifications:
            return 0.3  # Some credit for existing
        
        max_level = max(v.level.value for v in entry.verifications)
        return max_level / 5.0  # Normalize to 0-1
    
    def _score_source_credibility(self, entry: KnowledgeEntry) -> float:
        """Score based on source type credibility."""
        base = self.SOURCE_CREDIBILITY.get(entry.source_type, 0.5)
        
        # Bonus for institutional author
        if entry.author_type == "institution":
            base = min(1.0, base + 0.1)
        
        return base
    
    def _score_verification_quality(self, entry: KnowledgeEntry) -> float:
        """Score based on verification ratings and count."""
        if not entry.verifications:
            return 0.2  # Low base score without verification
        
        # Average rating across verifications
        avg_rating = sum(v.rating for v in entry.verifications) / len(entry.verifications)
        rating_score = avg_rating / 10.0
        
        # Bonus for multiple verifications (diminishing returns)
        count_bonus = min(0.2, len(entry.verifications) * 0.05)
        
        return min(1.0, rating_score + count_bonus)
    
    def _score_cross_reference(self, entry: KnowledgeEntry) -> float:
        """Score based on cross-referencing with other entries."""
        # This would connect to a knowledge graph in full implementation
        # For now, check if entry has cross-reference metadata
        refs = entry.metadata.get("cross_references", [])
        if len(refs) >= 3:
            return 0.9
        elif len(refs) >= 1:
            return 0.7
        return 0.5
    
    def _score_freshness(self, entry: KnowledgeEntry) -> float:
        """Score based on how recent the knowledge is."""
        age_days = (datetime.now() - entry.created_at).days
        
        if age_days < 30:
            return 1.0
        elif age_days < 180:
            return 0.9
        elif age_days < 365:
            return 0.8
        elif age_days < 730:
            return 0.7
        else:
            return 0.6  # Older knowledge still has value
    
    def get_confidence_level(self, trust_score: float) -> str:
        """Convert trust score to human-readable confidence level."""
        if trust_score >= 0.9:
            return "very_high"
        elif trust_score >= 0.75:
            return "high"
        elif trust_score >= 0.5:
            return "medium"
        elif trust_score >= 0.3:
            return "low"
        else:
            return "unverified"


# =============================================================================
# IsRAG ENGINE
# =============================================================================

class IsRAGEngine:
    """
    Isnad-chain Retrieval Augmented Generation Engine.
    
    Extends traditional RAG with:
    - Full provenance tracking (Isnad)
    - Trust scoring
    - Cultural context awareness
    - Verification chain
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.knowledge_base: dict[str, KnowledgeEntry] = {}
        self.trust_engine = TrustEngine()
        self.storage_path = storage_path
    
    def ingest(
        self,
        content: str,
        author: str,
        source_type: SourceType,
        author_type: str = "person",
        verification_level: VerificationLevel = VerificationLevel.UNVERIFIED,
        cultural_context: Optional[CulturalContext] = None,
        tags: list[str] = None,
        metadata: dict = None,
        entry_id: Optional[str] = None,
    ) -> KnowledgeEntry:
        """
        Ingest knowledge with full provenance tracking.
        
        Returns the created KnowledgeEntry with calculated trust score.
        """
        entry = KnowledgeEntry(
            content=content,
            entry_id=entry_id or "",
            author=author,
            author_type=author_type,
            source_type=source_type,
            created_at=datetime.now(),
            cultural_context=cultural_context,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        # Add initial verification if provided
        if verification_level != VerificationLevel.UNVERIFIED:
            entry.add_verification(VerificationRecord(
                verifier=author,
                verifier_type=author_type,
                level=verification_level,
                timestamp=datetime.now(),
                rating=8.0  # Default rating for self-verified
            ))
        
        # Store
        self.knowledge_base[entry.entry_id] = entry
        
        return entry
    
    def add_verification(
        self,
        entry_id: str,
        verifier: str,
        verifier_type: str,
        level: VerificationLevel,
        rating: float,
        feedback: str = "",
        issues_found: list[str] = None
    ) -> Optional[KnowledgeEntry]:
        """Add a verification to an existing knowledge entry."""
        entry = self.knowledge_base.get(entry_id)
        if not entry:
            return None
        
        entry.add_verification(VerificationRecord(
            verifier=verifier,
            verifier_type=verifier_type,
            level=level,
            timestamp=datetime.now(),
            rating=rating,
            feedback=feedback,
            issues_found=issues_found or []
        ))
        
        return entry
    
    def retrieve(
        self,
        query: str,
        min_trust_score: float = 0.0,
        cultural_filter: Optional[CulturalFramework] = None,
        source_filter: Optional[SourceType] = None,
        limit: int = 10,
        include_isnad: bool = False
    ) -> list["RetrievalResult"]:
        """
        Retrieve knowledge entries matching query with trust filtering.
        
        Returns list of RetrievalResult sorted by relevance and trust.
        """
        results = []
        
        for entry in self.knowledge_base.values():
            # Simple keyword matching (would be vector search in production)
            relevance = self._calculate_relevance(query, entry)
            if relevance <= 0:
                continue
            
            # Calculate trust score
            trust_score = self.trust_engine.calculate_trust_score(entry)
            
            # Apply filters
            if trust_score < min_trust_score:
                continue
            
            if cultural_filter and entry.cultural_context:
                if entry.cultural_context.framework != cultural_filter:
                    continue
            
            if source_filter and entry.source_type != source_filter:
                continue
            
            # Build isnad chain
            isnad = self._build_isnad(entry, trust_score)
            
            results.append(RetrievalResult(
                content=entry.content,
                entry_id=entry.entry_id,
                relevance_score=relevance,
                trust_score=trust_score,
                confidence_level=self.trust_engine.get_confidence_level(trust_score),
                isnad_chain=isnad if include_isnad else None,
                source_type=entry.source_type,
                cultural_context=entry.cultural_context
            ))
        
        # Sort by combined relevance and trust
        results.sort(key=lambda r: (r.relevance_score * 0.6 + r.trust_score * 0.4), reverse=True)
        
        return results[:limit]
    
    def _calculate_relevance(self, query: str, entry: KnowledgeEntry) -> float:
        """Simple keyword relevance (would be vector similarity in production)."""
        query_lower = query.lower()
        content_lower = entry.content.lower()
        
        # Count keyword matches
        query_words = query_lower.split()
        matches = sum(1 for word in query_words if word in content_lower)
        
        if len(query_words) == 0:
            return 0.0
        
        # Also check tags
        tag_matches = sum(1 for word in query_words if word in " ".join(entry.tags).lower())
        
        return min(1.0, (matches + tag_matches * 2) / (len(query_words) * 2))
    
    def _build_isnad(self, entry: KnowledgeEntry, trust_score: float) -> IsnadChain:
        """Build complete Isnad chain for an entry."""
        return IsnadChain(
            entry_id=entry.entry_id,
            provenance_steps=entry.provenance,
            verifications=entry.verifications,
            cultural_context=entry.cultural_context or CulturalContext(
                framework=CulturalFramework.GLOBAL,
                language_original="unknown",
                applicability=["global"],
                limitations=[]
            ),
            trust_score=trust_score,
            confidence_level=self.trust_engine.get_confidence_level(trust_score)
        )
    
    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Get a knowledge entry by ID."""
        return self.knowledge_base.get(entry_id)
    
    def list_entries(
        self,
        source_type: Optional[SourceType] = None,
        min_trust: float = 0.0
    ) -> list[KnowledgeEntry]:
        """List all entries with optional filters."""
        entries = list(self.knowledge_base.values())
        
        if source_type:
            entries = [e for e in entries if e.source_type == source_type]
        
        if min_trust > 0:
            entries = [
                e for e in entries
                if self.trust_engine.calculate_trust_score(e) >= min_trust
            ]
        
        return entries
    
    def get_stats(self) -> dict:
        """Get statistics about the knowledge base."""
        entries = list(self.knowledge_base.values())
        
        if not entries:
            return {"total_entries": 0}
        
        trust_scores = [self.trust_engine.calculate_trust_score(e) for e in entries]
        
        return {
            "total_entries": len(entries),
            "avg_trust_score": sum(trust_scores) / len(trust_scores),
            "high_trust_count": sum(1 for t in trust_scores if t >= 0.75),
            "verified_count": sum(1 for e in entries if e.verifications),
            "sources": {
                st.value: sum(1 for e in entries if e.source_type == st)
                for st in SourceType
            },
            "cultural_frameworks": {
                cf.value: sum(1 for e in entries if e.cultural_context and e.cultural_context.framework == cf)
                for cf in CulturalFramework
                if any(e.cultural_context and e.cultural_context.framework == cf for e in entries)
            }
        }


@dataclass
class RetrievalResult:
    """Result from IsRAG retrieval."""
    content: str
    entry_id: str
    relevance_score: float
    trust_score: float
    confidence_level: str
    isnad_chain: Optional[IsnadChain]
    source_type: SourceType
    cultural_context: Optional[CulturalContext]
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "entry_id": self.entry_id,
            "relevance_score": self.relevance_score,
            "trust_score": self.trust_score,
            "confidence_level": self.confidence_level,
            "isnad_chain": self.isnad_chain.to_dict() if self.isnad_chain else None,
            "source_type": self.source_type.value,
            "cultural_context": self.cultural_context.to_dict() if self.cultural_context else None
        }
    
    def format_for_display(self, show_isnad: bool = False) -> str:
        """Format retrieval result for display."""
        lines = [
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"📄 {self.entry_id}",
            f"📊 Relevance: {self.relevance_score:.2f} | Trust: {self.trust_score:.2f} ({self.confidence_level})",
            f"📎 Source: {self.source_type.value}",
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"\n{self.content}\n"
        ]
        
        if show_isnad and self.isnad_chain:
            lines.append(self.isnad_chain.format_for_display())
        
        return "\n".join(lines)


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Demo CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="IsRAG - Isnad-chain RAG")
    parser.add_argument("action", choices=["demo", "ingest", "query", "stats"])
    parser.add_argument("--content", help="Content to ingest")
    parser.add_argument("--query", help="Query to search")
    parser.add_argument("--author", help="Author name")
    parser.add_argument("--source", default="research", help="Source type")
    parser.add_argument("--isnad", action="store_true", help="Show Isnad chain")
    
    args = parser.parse_args()
    
    krag = IsRAGEngine()
    
    if args.action == "demo":
        run_demo(krag)
    elif args.action == "ingest":
        entry = krag.ingest(
            content=args.content,
            author=args.author or "Unknown",
            source_type=SourceType[args.source.upper()]
        )
        print(f"✅ Ingested: {entry.entry_id}")
    elif args.action == "query":
        results = krag.retrieve(args.query, include_isnad=args.isnad)
        for r in results:
            print(r.format_for_display(show_isnad=args.isnad))
    elif args.action == "stats":
        print(json.dumps(krag.get_stats(), indent=2))


def run_demo(krag: IsRAGEngine):
    """Run a demo of IsRAG capabilities."""
    print("\n🔬 IsRAG DEMO - Isnad-chain RAG\n")
    
    # Ingest some knowledge
    print("📥 Ingesting knowledge entries...")
    
    krag.ingest(
        content="ASEAN's total population is approximately 670 million people as of 2024, "
                "making it the third most populous region in Asia after China and India.",
        author="UN Population Division",
        source_type=SourceType.GOVERNMENT,
        author_type="institution",
        verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        tags=["asean", "population", "demographics"]
    )
    
    krag.ingest(
        content="Indonesia has 64.2 million MSMEs (UMKM), contributing 61% to GDP "
                "and employing 97% of the workforce.",
        author="Ministry of Cooperative and SME Indonesia",
        source_type=SourceType.GOVERNMENT,
        author_type="institution",
        verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        tags=["indonesia", "umkm", "msme", "economy"]
    )
    
    krag.ingest(
        content="The AI market in Southeast Asia is projected to reach $24.9 billion by 2030, "
                "growing at a CAGR of 32.6% from 2024.",
        author="IDC Asia Pacific",
        source_type=SourceType.RESEARCH,
        author_type="institution",
        verification_level=VerificationLevel.PEER_REVIEWED,
        tags=["ai", "market", "asean", "growth"]
    )
    
    krag.ingest(
        content="Gotong royong (mutual assistance) is a foundational principle in Indonesian "
                "society that can be leveraged for cooperative AI development.",
        author="Dr. Siti Nurbaya",
        source_type=SourceType.ACADEMIC,
        author_type="person",
        verification_level=VerificationLevel.PEER_REVIEWED,
        cultural_context=CulturalContext(
            framework=CulturalFramework.INDONESIAN,
            language_original="Indonesian",
            applicability=["Indonesia", "Southeast Asia"],
            limitations=["Cultural concept, may not translate directly"],
            local_terms={"gotong royong": "mutual assistance, communal cooperation"}
        ),
        tags=["culture", "indonesia", "cooperation", "ai"]
    )
    
    print(f"✅ Ingested {len(krag.knowledge_base)} entries\n")
    
    # Query
    print("🔍 Query: 'ASEAN population and economy'\n")
    results = krag.retrieve("ASEAN population economy", include_isnad=True)
    
    for r in results[:2]:
        print(r.format_for_display(show_isnad=True))
        print()
    
    # Stats
    print("📊 Knowledge Base Stats:")
    print(json.dumps(krag.get_stats(), indent=2))


if __name__ == "__main__":
    main()
