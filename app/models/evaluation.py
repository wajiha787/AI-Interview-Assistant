from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class EvaluationScore(BaseModel):
    """Individual evaluation score model"""
    category: str = Field(..., description="Evaluation category")
    score: float = Field(..., ge=0, le=10, description="Score from 0-10")
    weight: float = Field(default=1.0, ge=0, le=1, description="Weight for this category")
    reasoning: str = Field(..., description="Reasoning for this score")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")


class EvaluationFeedback(BaseModel):
    """Detailed feedback model"""
    category: str = Field(..., description="Feedback category")
    feedback: str = Field(..., description="Detailed feedback text")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    examples: List[str] = Field(default_factory=list, description="Specific examples from evaluation")


class RecommendationType(str, Enum):
    """Recommendation types"""
    STRONG_HIRE = "strong_hire"
    HIRE = "hire"
    MAYBE = "maybe"
    NO_HIRE = "no_hire"
    STRONG_NO_HIRE = "strong_no_hire"


class EvaluationSummary(BaseModel):
    """Summary of evaluation results"""
    candidate_id: str = Field(..., description="Associated candidate ID")
    overall_score: float = Field(..., ge=0, le=10, description="Overall score")
    recommendation: RecommendationType = Field(..., description="Final recommendation")
    confidence: float = Field(..., ge=0, le=1, description="Confidence in recommendation")
    key_highlights: List[str] = Field(default_factory=list, description="Key positive highlights")
    concerns: List[str] = Field(default_factory=list, description="Key concerns or red flags")
    next_steps: List[str] = Field(default_factory=list, description="Recommended next steps")
    created_at: datetime = Field(default_factory=datetime.now)

