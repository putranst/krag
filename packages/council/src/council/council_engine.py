"""
Dewan Council - LLM Deliberation System
========================================

A council of multiple LLMs that deliberate together to answer complex questions.
Inspired by Karpathy's llm-council and the Isnad framework.

All models accessed via OpenRouter (single API) with Huggingface as fallback.

Flow:
1. Stage 1: All council members give their first opinions
2. Stage 2: Members review and rank each other's responses  
3. Stage 3: Chairman synthesizes final response with full isnad chain

Usage:
    from dewan_council import DewanCouncil
    
    council = DewanCouncil(api_key="sk-or-...")
    result = council.deliberate("Apa strategi terbaik untuk kedaulatan data ASEAN?")
    print(result.final_answer)
    print(result.isnad_chain)
"""

import os
import json
import requests
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class CouncilMember:
    """Represents a member of the Dewan Council."""
    name: str
    role: str  # chairman, member
    model_id: str  # OpenRouter model ID (e.g., "anthropic/claude-opus-4.7")
    specialty: str
    trust_weight: float = 1.0  # base trust weight
    
    def describe(self) -> str:
        return f"{self.name} ({self.role}) - {self.specialty}"


@dataclass 
class Opinion:
    """A single council member's opinion."""
    member: CouncilMember
    response: str
    timestamp: datetime
    confidence: float = 0.0  # self-assessed confidence
    
    def to_dict(self) -> dict:
        return {
            "member": self.member.name,
            "role": self.member.role,
            "response": self.response,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class Review:
    """One member's review of another's opinion."""
    reviewer: CouncilMember
    reviewed: CouncilMember
    rating: float  # 1-10
    feedback: str
    issues_found: list = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "reviewer": self.reviewer.name,
            "reviewed": self.reviewed.name,
            "rating": self.rating,
            "feedback": self.feedback,
            "issues": self.issues_found
        }


@dataclass
class IsnadChain:
    """Complete provenance chain for the deliberation."""
    query: str
    stage1_opinions: list[Opinion]
    stage2_reviews: list[Review]
    stage3_synthesis: str
    consensus_score: float
    dissenting_views: list[str]
    
    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "stage1_opinions": [o.to_dict() for o in self.stage1_opinions],
            "stage2_reviews": [r.to_dict() for r in self.stage2_reviews],
            "stage3_synthesis": self.stage3_synthesis,
            "consensus_score": self.consensus_score,
            "dissenting_views": self.dissenting_views,
            "metadata": {
                "total_members": len(set(o.member.name for o in self.stage1_opinions)),
                "total_reviews": len(self.stage2_reviews),
                "generated_at": datetime.now().isoformat()
            }
        }
    
    def format_for_display(self) -> str:
        """Format the isnad chain for human-readable display."""
        lines = [
            "=" * 60,
            "ISNAD CHAIN - Rantai Asal-Usul",
            "=" * 60,
            f"\n📋 QUERY: {self.query}\n",
            "-" * 60,
            "STAGE 1: Opini Awal Council Members",
            "-" * 60,
        ]
        
        for i, opinion in enumerate(self.stage1_opinions, 1):
            lines.append(f"\n[{i}] {opinion.member.describe()}")
            lines.append(f"    Confidence: {opinion.confidence:.1f}/10")
            lines.append(f"    Response: {opinion.response[:200]}...")
        
        lines.extend([
            "\n" + "-" * 60,
            "STAGE 2: Cross-Review",
            "-" * 60,
        ])
        
        for review in self.stage2_reviews:
            lines.append(f"\n{review.reviewer.name} → {review.reviewed.name}: {review.rating}/10")
            lines.append(f"  Feedback: {review.feedback[:150]}...")
            if review.issues_found:
                lines.append(f"  Issues: {', '.join(review.issues_found)}")
        
        lines.extend([
            "\n" + "-" * 60,
            "STAGE 3: Sintesis Ketua Dewan",
            "-" * 60,
            f"\n{self.stage3_synthesis}",
            "\n" + "-" * 60,
            f"Consensus Score: {self.consensus_score:.1f}/10",
        ])
        
        if self.dissenting_views:
            lines.append("\n⚠️ DISSENTING VIEWS:")
            for view in self.dissenting_views:
                lines.append(f"  • {view}")
        
        return "\n".join(lines)


@dataclass
class DeliberationResult:
    """Complete result of a council deliberation."""
    final_answer: str
    isnad_chain: IsnadChain
    processing_time: float
    members_used: list[str]


# =============================================================================
# COUNCIL MEMBERS REGISTRY
# =============================================================================

DEFAULT_COUNCIL = [
    CouncilMember(
        name="Ketua Claude",
        role="chairman",
        model_id="anthropic/claude-opus-4.7",
        specialty="Synthesis, judgment, nuanced analysis",
        trust_weight=1.2
    ),
    CouncilMember(
        name="Anggota GPT",
        role="member",
        model_id="openai/gpt-5.5",
        specialty="Deep reasoning, multi-step logic",
        trust_weight=1.1
    ),
    CouncilMember(
        name="Anggota Gemini",
        role="member", 
        model_id="google/gemini-3-flash-preview",
        specialty="Data analysis, multimodal, fast reasoning",
        trust_weight=1.0
    ),
    CouncilMember(
        name="Anggota Kimi",
        role="member",
        model_id="moonshotai/kimi-k2.6",
        specialty="Long context, multi-agent, Chinese tech perspective",
        trust_weight=1.0
    ),
    CouncilMember(
        name="Anggota Deepseek",
        role="member",
        model_id="deepseek/deepseek-v4-flash",
        specialty="Chain-of-thought, MoE efficiency, mathematical rigor",
        trust_weight=1.1
    ),
    CouncilMember(
        name="Anggota Qwen",
        role="member",
        model_id="qwen/qwen3.6-plus",
        specialty="Agentic coding, multilingual, Asian market context",
        trust_weight=1.0
    ),
    CouncilMember(
        name="Anggota Nemotron",
        role="member",
        model_id="nvidia/nemotron-3-super",
        specialty="Open model, hardware-software integration, multi-agent",
        trust_weight=1.0
    ),
]


# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

STAGE1_PROMPT = """You are {member_name}, a member of the Dewan Council (AI Council).

Your specialty: {specialty}

Answer the following question with your best analysis. Be specific, cite reasoning, and note your confidence level.

QUESTION: {query}

Provide your response in this format:
RESPONSE: [your detailed analysis]
CONFIDENCE: [1-10, your confidence in this answer]
KEY_POINTS: [bullet points of main arguments]"""

STAGE2_PROMPT = """You are {reviewer_name}, reviewing responses from other council members.

Your specialty: {specialty}

QUESTION: {query}

RESPONSE TO REVIEW (by {reviewed_name}):
{reviewed_response}

Review this response on:
1. Factual accuracy (are claims supportable?)
2. Logical coherence (does reasoning hold?)
3. Completeness (what's missing?)
4. Bias detection (any obvious biases?)

Provide your review in this format:
RATING: [1-10]
FEEDBACK: [detailed feedback]
ISSUES: [list any issues found, or "none"]
STRENGTHS: [what's good about this response]"""

STAGE3_PROMPT = """You are the KETUA (Chairman) of the Dewan Council.

Your role: Synthesize all opinions and reviews into a final consensus answer.

QUESTION: {query}

ORIGINAL OPINIONS:
{opinions_summary}

REVIEW RESULTS:
{reviews_summary}

Your task:
1. Identify areas of CONSENSUS (where members agree)
2. Note DISSENTING views (where members disagree)
3. Weight opinions based on review scores
4. Produce a SYNTHESIZED FINAL ANSWER that represents the council's collective wisdom

Provide your synthesis in this format:
CONSENSUS: [areas where council agrees]
DISSENT: [areas of disagreement with reasoning]
FINAL_ANSWER: [your synthesized response that balances all views]
CONSENSUS_SCORE: [1-10, how much consensus exists]"""


# =============================================================================
# MAIN DEWAN COUNCIL CLASS
# =============================================================================

class DewanCouncil:
    """
    Dewan Council - A council of LLMs that deliberate together.
    
    All models accessed via OpenRouter for simplicity.
    Based on the Isnad principle: every opinion has a source,
    every synthesis has a chain of custody.
    """
    
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    HUGGINGFACE_BASE_URL = "https://api-inference.huggingface.co/models"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        members: Optional[list[CouncilMember]] = None,
        provider: str = "openrouter",  # openrouter or huggingface
        verbose: bool = False
    ):
        self.members = members or DEFAULT_COUNCIL
        self.verbose = verbose
        self.provider = provider
        
        # Get API key from env or parameter
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY") or os.getenv("HF_API_KEY")
        
        if not self.api_key:
            print("⚠️  No API key found. Using mock responses.")
            print("   Set OPENROUTER_API_KEY or pass api_key parameter.")
            self.use_mock = True
        else:
            self.use_mock = False
    
    def deliberate(
        self, 
        query: str,
        skip_reviews: bool = False,
        max_reviewers: int = 3
    ) -> DeliberationResult:
        """
        Run full council deliberation on a query.
        
        Args:
            query: The question to deliberate on
            skip_reviews: Skip stage 2 for faster results
            max_reviewers: Max number of reviewers per opinion
            
        Returns:
            DeliberationResult with final answer and isnad chain
        """
        start_time = datetime.now()
        
        if self.verbose:
            print(f"\n🏛️ DEWAN COUNCIL DELIBERATION")
            print(f"{'='*50}")
            print(f"Query: {query}")
            print(f"Members: {len(self.members)}")
        
        # STAGE 1: First Opinions
        if self.verbose:
            print(f"\n📝 Stage 1: Gathering opinions...")
        
        opinions = self._stage1_get_opinions(query)
        
        if self.verbose:
            for op in opinions:
                print(f"  ✓ {op.member.name}: confidence={op.confidence}")
        
        # STAGE 2: Cross-Review
        reviews = []
        if not skip_reviews:
            if self.verbose:
                print(f"\n🔍 Stage 2: Cross-reviewing...")
            
            reviews = self._stage2_cross_review(query, opinions, max_reviewers)
            
            if self.verbose:
                print(f"  ✓ {len(reviews)} reviews completed")
        
        # STAGE 3: Chairman Synthesis
        if self.verbose:
            print(f"\n👑 Stage 3: Chairman synthesis...")
        
        synthesis = self._stage3_synthesize(query, opinions, reviews)
        
        # Build Isnad Chain
        isnad = IsnadChain(
            query=query,
            stage1_opinions=opinions,
            stage2_reviews=reviews,
            stage3_synthesis=synthesis["final_answer"],
            consensus_score=synthesis["consensus_score"],
            dissenting_views=synthesis.get("dissenting", [])
        )
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        if self.verbose:
            print(f"\n✅ Deliberation complete in {elapsed:.1f}s")
            print(f"   Consensus Score: {isnad.consensus_score}/10")
        
        return DeliberationResult(
            final_answer=synthesis["final_answer"],
            isnad_chain=isnad,
            processing_time=elapsed,
            members_used=[m.name for m in self.members]
        )
    
    def _stage1_get_opinions(self, query: str) -> list[Opinion]:
        """Stage 1: Get initial opinions from all council members."""
        opinions = []
        
        for member in self.members:
            prompt = STAGE1_PROMPT.format(
                member_name=member.name,
                specialty=member.specialty,
                query=query
            )
            
            response = self._call_llm(member, prompt)
            parsed = self._parse_stage1_response(response)
            
            opinions.append(Opinion(
                member=member,
                response=parsed.get("response", response),
                timestamp=datetime.now(),
                confidence=parsed.get("confidence", 5.0)
            ))
        
        return opinions
    
    def _stage2_cross_review(
        self, 
        query: str, 
        opinions: list[Opinion],
        max_reviewers: int
    ) -> list[Review]:
        """Stage 2: Each member reviews other members' opinions."""
        reviews = []
        
        for target in opinions:
            # Other members review this opinion
            reviewers = [o for o in opinions if o.member.name != target.member.name]
            
            # Limit number of reviewers
            reviewers = reviewers[:max_reviewers]
            
            for reviewer_opinion in reviewers:
                prompt = STAGE2_PROMPT.format(
                    reviewer_name=reviewer_opinion.member.name,
                    specialty=reviewer_opinion.member.specialty,
                    query=query,
                    reviewed_name=target.member.name,
                    reviewed_response=target.response
                )
                
                response = self._call_llm(reviewer_opinion.member, prompt)
                parsed = self._parse_stage2_response(response)
                
                reviews.append(Review(
                    reviewer=reviewer_opinion.member,
                    reviewed=target.member,
                    rating=parsed.get("rating", 5.0),
                    feedback=parsed.get("feedback", response[:500]),
                    issues_found=parsed.get("issues", [])
                ))
        
        return reviews
    
    def _stage3_synthesize(
        self,
        query: str,
        opinions: list[Opinion],
        reviews: list[Review]
    ) -> dict:
        """Stage 3: Chairman synthesizes all opinions and reviews."""
        
        # Find chairman or use first member
        chairman = next(
            (m for m in self.members if m.role == "chairman"),
            self.members[0]
        )
        
        # Prepare summaries
        opinions_summary = "\n\n".join([
            f"**{op.member.name}** (confidence: {op.confidence}/10):\n{op.response}"
            for op in opinions
        ])
        
        reviews_summary = "\n\n".join([
            f"**{review.reviewer.name} reviews {review.reviewed.name}** (rating: {review.rating}/10):\n{review.feedback}"
            for review in reviews
        ])
        
        prompt = STAGE3_PROMPT.format(
            query=query,
            opinions_summary=opinions_summary,
            reviews_summary=reviews_summary
        )
        
        response = self._call_llm(chairman, prompt)
        parsed = self._parse_stage3_response(response)
        
        return parsed
    
    def _call_llm(self, member: CouncilMember, prompt: str) -> str:
        """Call an LLM via OpenRouter or Huggingface."""
        
        if self.use_mock:
            return self._mock_response(member, prompt)
        
        if self.provider == "huggingface":
            return self._call_huggingface(member, prompt)
        else:
            return self._call_openrouter(member, prompt)
    
    def _call_openrouter(self, member: CouncilMember, prompt: str) -> str:
        """Call model via OpenRouter API."""
        try:
            response = requests.post(
                self.OPENROUTER_BASE_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/inteligensia",
                    "X-Title": "Dewan Council"
                },
                json={
                    "model": member.model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 2000,
                    "reasoning": {"effort": "high"}  # Enable thinking/reasoning
                },
                timeout=120
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[Error calling {member.name} via OpenRouter: {str(e)}]"
    
    def _call_huggingface(self, member: CouncilMember, prompt: str) -> str:
        """Call model via Huggingface Inference API."""
        try:
            model_id = member.model_id.split("/")[-1]  # Get model name only
            response = requests.post(
                f"{self.HUGGINGFACE_BASE_URL}/{model_id}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 2000,
                        "return_full_text": False
                    }
                },
                timeout=120
            )
            response.raise_for_status()
            return response.json()[0]["generated_text"]
        except Exception as e:
            return f"[Error calling {member.name} via Huggingface: {str(e)}]"
    
    def _mock_response(self, member: CouncilMember, prompt: str) -> str:
        """Generate mock response for testing without API keys."""
        
        mock_responses = {
            "chairman": """RESPONSE: As the chairman, I synthesize the diverse perspectives from our council. The question of ASEAN data sovereignty requires balancing technological capability, economic incentives, and cultural preservation. Each member has contributed unique insights from their specialized perspectives.

CONFIDENCE: 8

KEY_POINTS:
- Regional cooperation creates collective bargaining power
- Technical infrastructure must be locally owned
- Cultural context cannot be outsourced
- Economic models must favor local value retention
- Cross-border data governance needs harmonization""",
            
            "openai": """RESPONSE: From a deep reasoning perspective, the multi-step logic here reveals structural dependencies that are often overlooked. The path to sovereignty requires understanding the full stack of AI infrastructure - from hardware to data to models.

CONFIDENCE: 8

KEY_POINTS:
- Dependency analysis must go beyond surface level
- Each layer of the AI stack presents different challenges
- Economic incentives currently favor dependency
- Policy intervention can reshape the landscape""",
            
            "google": """RESPONSE: Analyzing the data patterns across ASEAN nations reveals both challenges and opportunities. The quantitative reality shows massive value extraction, but also massive potential for local value creation if the right frameworks are in place.

CONFIDENCE: 7

KEY_POINTS:
- Data shows $200B+ potential extraction over decade
- Local AI development growing but needs support
- Multimodal data sovereignty is the next frontier
- Regional data sharing can create competitive advantage""",
            
            "moonshot": """RESPONSE: Examining this through a long-context lens, we see patterns that mirror historical colonial dynamics but in digital form. The Chinese tech perspective offers insights into how a nation can build sovereign AI capabilities while engaging globally.

CONFIDENCE: 7

KEY_POINTS:
- Historical parallels with trade colonialism
- China's experience shows sovereignty is achievable
- Long-term planning trumps quick adoption
- Research synthesis reveals common patterns""",
            
            "deepseek": """RESPONSE: Using chain-of-thought reasoning, let me work through this systematically. The question requires decomposing "sovereignty" into measurable components: data ownership, model ownership, compute ownership, and talent retention.

CONFIDENCE: 8

KEY_POINTS:
- Sovereignty has multiple dimensions
- Mathematical rigor shows current trajectory is unsustainable
- Counterfactual analysis: what if ASEAN kept its data?
- Logical framework for measuring progress""",
            
            "qwen": """RESPONSE: From a multilingual and Asian market perspective, the key insight is that Western AI models are not designed for Asian contexts. This creates both a vulnerability and an opportunity for regional development.

CONFIDENCE: 7

KEY_POINTS:
- Asian languages underrepresented in training data
- Market-specific models create local advantage
- Cultural context requires local training
- Regional cooperation amplifies small-market voices""",
            
            "nemotron": """RESPONSE: From a technical infrastructure perspective, the hardware-software integration challenge is significant. Sovereign AI requires not just models, but the entire stack - compute, storage, networking - to be locally可控.

CONFIDENCE: 7

KEY_POINTS:
- Hardware sovereignty is foundational
- Software without hardware is dependency
- Regional data center development is critical
- Technical standards need local input""",
        }
        
        if member.role == "chairman":
            return mock_responses["chairman"]
        elif "openai" in member.model_id:
            return mock_responses["openai"]
        elif "google" in member.model_id:
            return mock_responses["google"]
        elif "moonshot" in member.model_id:
            return mock_responses["moonshot"]
        elif "deepseek" in member.model_id:
            return mock_responses["deepseek"]
        elif "qwen" in member.model_id:
            return mock_responses["qwen"]
        elif "nvidia" in member.model_id:
            return mock_responses["nemotron"]
        else:
            return mock_responses["openai"]
    
    # =========================================================================
    # RESPONSE PARSERS
    # =========================================================================
    
    def _parse_stage1_response(self, response: str) -> dict:
        """Parse stage 1 response to extract structured data."""
        result = {"response": response, "confidence": 5.0}
        
        # Try to extract confidence
        if "CONFIDENCE:" in response:
            try:
                conf_line = response.split("CONFIDENCE:")[1].split("\n")[0]
                result["confidence"] = float(conf_line.strip().split("/")[0].split()[0])
            except:
                pass
        
        # Try to extract main response
        if "RESPONSE:" in response:
            try:
                result["response"] = response.split("RESPONSE:")[1].split("CONFIDENCE:")[0].strip()
            except:
                pass
        
        return result
    
    def _parse_stage2_response(self, response: str) -> dict:
        """Parse stage 2 review response."""
        result = {
            "rating": 5.0,
            "feedback": response,
            "issues": []
        }
        
        # Extract rating
        if "RATING:" in response:
            try:
                rating_line = response.split("RATING:")[1].split("\n")[0]
                result["rating"] = float(rating_line.strip().split("/")[0].split()[0])
            except:
                pass
        
        # Extract feedback
        if "FEEDBACK:" in response:
            try:
                result["feedback"] = response.split("FEEDBACK:")[1].split("ISSUES:")[0].strip()
            except:
                pass
        
        # Extract issues
        if "ISSUES:" in response:
            try:
                issues_text = response.split("ISSUES:")[1].split("STRENGTHS:")[0].strip()
                if issues_text.lower() not in ["none", "no issues", "-"]:
                    result["issues"] = [i.strip() for i in issues_text.split("\n") if i.strip()]
            except:
                pass
        
        return result
    
    def _parse_stage3_response(self, response: str) -> dict:
        """Parse stage 3 synthesis response."""
        result = {
            "final_answer": response,
            "consensus_score": 5.0,
            "dissenting": []
        }
        
        # Extract final answer
        if "FINAL_ANSWER:" in response:
            try:
                result["final_answer"] = response.split("FINAL_ANSWER:")[1].split("CONSENSUS_SCORE:")[0].strip()
            except:
                pass
        
        # Extract consensus score
        if "CONSENSUS_SCORE:" in response:
            try:
                score_line = response.split("CONSENSUS_SCORE:")[1].split("\n")[0]
                result["consensus_score"] = float(score_line.strip().split("/")[0].split()[0])
            except:
                pass
        
        # Extract dissenting views
        if "DISSENT:" in response:
            try:
                dissent_text = response.split("DISSENT:")[1].split("FINAL_ANSWER:")[0].strip()
                if dissent_text.lower() not in ["none", "no dissent", "-"]:
                    result["dissenting"] = [
                        line.strip().lstrip("-•").strip() 
                        for line in dissent_text.split("\n") 
                        if line.strip()
                    ]
            except:
                pass
        
        return result


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Simple CLI interface for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Dewan Council - LLM Deliberation")
    parser.add_argument("query", help="Question to deliberate on")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--skip-reviews", action="store_true", help="Skip stage 2")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    council = DewanCouncil(verbose=args.verbose)
    result = council.deliberate(args.query, skip_reviews=args.skip_reviews)
    
    if args.json:
        print(json.dumps(result.isnad_chain.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(result.isnad_chain.format_for_display())
        print("\n" + "=" * 60)
        print("FINAL ANSWER:")
        print("=" * 60)
        print(result.final_answer)


if __name__ == "__main__":
    main()
