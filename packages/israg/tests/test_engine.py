"""
Tests for IsRAG Engine
=====================

Run: pytest tests/test_engine.py
"""

import pytest
from israg import (
    IsRAGEngine,
    SourceType,
    VerificationLevel,
    CulturalContext,
    CulturalFramework,
)


class TestIsRAGEngine:
    """Test suite for IsRAG Engine."""

    @pytest.fixture
    def engine(self):
        return IsRAGEngine()

    def test_ingest_basic(self, engine):
        entry = engine.ingest(
            content="Test content",
            author="Test Author",
            source_type=SourceType.RESEARCH,
        )
        assert entry.content == "Test content"
        assert entry.author == "Test Author"
        assert entry.source_type == SourceType.RESEARCH
        assert entry.entry_id is not None

    def test_ingest_with_verification(self, engine):
        entry = engine.ingest(
            content="Verified content",
            author="Institution",
            source_type=SourceType.GOVERNMENT,
            verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        )
        trust = engine.trust_engine.calculate_trust_score(entry)
        assert trust > 0.5
        assert len(entry.verifications) == 1

    def test_ingest_with_cultural_context(self, engine):
        entry = engine.ingest(
            content="Gotong royong is cooperation.",
            author="Dr. Test",
            source_type=SourceType.ACADEMIC,
            cultural_context=CulturalContext(
                framework=CulturalFramework.INDONESIAN,
                language_original="Indonesian",
                applicability=["Indonesia"],
                limitations=["Cultural concept"],
            ),
        )
        assert entry.cultural_context is not None
        assert entry.cultural_context.framework == CulturalFramework.INDONESIAN

    def test_retrieve_basic(self, engine):
        engine.ingest(
            content="ASEAN population is 670 million",
            author="UN",
            source_type=SourceType.GOVERNMENT,
            verification_level=VerificationLevel.INSTITUTION_VERIFIED,
            tags=["asean", "population"],
        )
        results = engine.retrieve("ASEAN population", include_isnad=True)
        assert len(results) > 0
        assert results[0].content == "ASEAN population is 670 million"

    def test_retrieve_trust_filter(self, engine):
        engine.ingest(
            content="High trust fact",
            author="Government",
            source_type=SourceType.GOVERNMENT,
            verification_level=VerificationLevel.INSTITUTION_VERIFIED,
        )
        engine.ingest(
            content="Low trust rumor",
            author="Anonymous",
            source_type=SourceType.COMMUNITY,
            verification_level=VerificationLevel.UNVERIFIED,
        )
        results = engine.retrieve("trust", min_trust_score=0.5)
        assert all(r.trust_score >= 0.5 for r in results)

    def test_retrieve_cultural_filter(self, engine):
        engine.ingest(
            content="Indonesian concept",
            author="Dr. A",
            source_type=SourceType.ACADEMIC,
            cultural_context=CulturalContext(
                framework=CulturalFramework.INDONESIAN,
                language_original="Indonesian",
                applicability=["Indonesia"],
                limitations=[],
            ),
        )
        engine.ingest(
            content="Global concept",
            author="Dr. B",
            source_type=SourceType.ACADEMIC,
        )
        results = engine.retrieve(
            "concept",
            cultural_filter=CulturalFramework.INDONESIAN,
        )
        assert len(results) > 0
        assert all(
            r.cultural_context.framework == CulturalFramework.INDONESIAN
            for r in results if r.cultural_context
        )

    def test_add_verification(self, engine):
        entry = engine.ingest(
            content="Test",
            author="A",
            source_type=SourceType.COMMUNITY,
        )
        initial_trust = engine.trust_engine.calculate_trust_score(entry)

        engine.add_verification(
            entry_id=entry.entry_id,
            verifier="Reviewer B",
            verifier_type="person",
            level=VerificationLevel.SELF_REPORTED,
            rating=8.0,
        )

        updated = engine.get_entry(entry.entry_id)
        new_trust = engine.trust_engine.calculate_trust_score(updated)
        assert new_trust > initial_trust
        assert len(updated.verifications) == 1

    def test_get_stats(self, engine):
        engine.ingest(content="A", author="A", source_type=SourceType.GOVERNMENT)
        engine.ingest(content="B", author="B", source_type=SourceType.RESEARCH)

        stats = engine.get_stats()
        assert stats["total_entries"] == 2
        assert "avg_trust_score" in stats
        assert "sources" in stats

    def test_retrieval_result_display(self, engine):
        engine.ingest(
            content="Display test",
            author="Test",
            source_type=SourceType.GOVERNMENT,
        )
        results = engine.retrieve("display", include_isnad=True)
        display = results[0].format_for_display(show_isnad=True)
        assert "Display test" in display
        assert "Trust:" in display

    def test_empty_retrieval(self, engine):
        results = engine.retrieve("nonexistent query")
        assert results == []

    def test_provenance_tracking(self, engine):
        entry = engine.ingest(
            content="Provenance test",
            author="Creator",
            source_type=SourceType.RESEARCH,
        )
        assert len(entry.provenance) > 0
        assert "Created" in entry.provenance[0].action


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
