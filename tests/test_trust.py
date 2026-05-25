"""
Tests for Trust Engine
======================

Run: pytest tests/test_trust.py
"""

import pytest
from krag import TrustEngine, VerificationLevel, SourceType
from krag.krag_engine import KnowledgeEntry, VerificationRecord, CulturalContext
from datetime import datetime


class TestTrustEngine:
    """Test suite for TrustEngine."""

    @pytest.fixture
    def trust_engine(self):
        return TrustEngine()

    @pytest.fixture
    def basic_entry(self):
        return KnowledgeEntry(
            content="Test",
            entry_id="test-001",
            author="Author",
            author_type="person",
            source_type=SourceType.RESEARCH,
            created_at=datetime.now(),
        )

    def test_unverified_score(self, trust_engine, basic_entry):
        score = trust_engine.calculate_trust_score(basic_entry)
        assert 0 <= score <= 1
        # Research source without verification is moderate, not high
        assert score < 0.6

    def test_peer_reviewed_score(self, trust_engine, basic_entry):
        basic_entry.add_verification(VerificationRecord(
            verifier="Journal",
            verifier_type="institution",
            level=VerificationLevel.PEER_REVIEWED,
            timestamp=datetime.now(),
            rating=9.0,
        ))
        score = trust_engine.calculate_trust_score(basic_entry)
        assert score > 0.65  # Peer reviewed should be high

    def test_multiple_verifications(self, trust_engine, basic_entry):
        basic_entry.add_verification(VerificationRecord(
            verifier="A",
            verifier_type="person",
            level=VerificationLevel.SELF_REPORTED,
            timestamp=datetime.now(),
            rating=7.0,
        ))
        basic_entry.add_verification(VerificationRecord(
            verifier="B",
            verifier_type="person",
            level=VerificationLevel.SELF_REPORTED,
            timestamp=datetime.now(),
            rating=8.0,
        ))
        score = trust_engine.calculate_trust_score(basic_entry)
        assert score > 0.5  # Multiple verifications boost score

    def test_government_source_boost(self, trust_engine, basic_entry):
        basic_entry.source_type = SourceType.GOVERNMENT
        basic_entry.add_verification(VerificationRecord(
            verifier="Gov",
            verifier_type="institution",
            level=VerificationLevel.INSTITUTION_VERIFIED,
            timestamp=datetime.now(),
            rating=8.5,
        ))
        score = trust_engine.calculate_trust_score(basic_entry)
        assert score > 0.6

    def test_confidence_levels(self, trust_engine):
        assert trust_engine.get_confidence_level(0.95) == "very_high"
        assert trust_engine.get_confidence_level(0.80) == "high"
        assert trust_engine.get_confidence_level(0.65) == "medium"
        assert trust_engine.get_confidence_level(0.45) == "low"
        assert trust_engine.get_confidence_level(0.20) == "unverified"

    def test_blog_source_low_trust(self, trust_engine, basic_entry):
        basic_entry.source_type = SourceType.COMMUNITY
        score = trust_engine.calculate_trust_score(basic_entry)
        assert score < 0.5  # Community source without verification is low-moderate trust

    def test_negative_feedback_penalty(self, trust_engine, basic_entry):
        basic_entry.add_verification(VerificationRecord(
            verifier="Critic",
            verifier_type="person",
            level=VerificationLevel.SELF_REPORTED,
            timestamp=datetime.now(),
            rating=3.0,
            feedback="Contains factual errors",
            issues_found=["error1"],
        ))
        score = trust_engine.calculate_trust_score(basic_entry)
        assert score < 0.55  # Negative feedback should not raise score significantly


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
