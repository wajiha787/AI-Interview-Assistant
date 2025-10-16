from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SessionStatus(str, Enum):
    """Interview session status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InterviewRound(BaseModel):
    """Individual interview round within a session"""
    round_id: str = Field(..., description="Unique round identifier")
    round_number: int = Field(..., description="Round number (1, 2, 3, etc.)")
    questions: List[Dict[str, Any]] = Field(default_factory=list, description="Questions asked")
    answers: List[Dict[str, Any]] = Field(default_factory=list, description="Candidate answers")
    score: Optional[float] = Field(None, ge=0, le=100, description="Round score (0-100)")
    status: SessionStatus = Field(default=SessionStatus.PENDING, description="Round status")
    started_at: Optional[datetime] = Field(None, description="Round start time")
    completed_at: Optional[datetime] = Field(None, description="Round completion time")
    feedback: Optional[str] = Field(None, description="Feedback for this round")


class CVAnalysis(BaseModel):
    """CV analysis result"""
    user_id: str = Field(..., description="User identifier")
    analysis_id: str = Field(..., description="Unique analysis identifier")
    cv_content: str = Field(..., description="Raw CV content")
    profession: str = Field(..., description="User's profession/field")
    
    # Gap analysis results
    current_level: str = Field(..., description="Current experience level")
    overall_readiness_score: float = Field(..., ge=0, le=100, description="Readiness score (0-100)")
    technical_skills_gaps: List[Dict[str, Any]] = Field(default_factory=list)
    missing_certifications: List[Dict[str, Any]] = Field(default_factory=list)
    experience_gaps: List[Dict[str, Any]] = Field(default_factory=list)
    soft_skills_gaps: List[Dict[str, Any]] = Field(default_factory=list)
    educational_gaps: List[Dict[str, Any]] = Field(default_factory=list)
    
    strengths: List[str] = Field(default_factory=list, description="Identified strengths")
    priority_improvements: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Recommendations
    recommendations: Optional[Dict[str, Any]] = Field(None, description="Learning recommendations")
    
    analyzed_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class InterviewSession(BaseModel):
    """Interview session tracking multiple rounds"""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User identifier")
    profession: str = Field(..., description="Profession being interviewed for")
    
    # Session metadata
    total_rounds: int = Field(default=0, description="Total interview rounds")
    current_round: int = Field(default=0, description="Current round number")
    rounds: List[InterviewRound] = Field(default_factory=list, description="All interview rounds")
    
    # Performance tracking
    overall_score: Optional[float] = Field(None, ge=0, le=100, description="Overall session score")
    best_score: float = Field(default=0, ge=0, le=100, description="Best round score")
    improvement_rate: Optional[float] = Field(None, description="Score improvement percentage")
    
    # Weak areas and practice topics
    weak_topics: List[Dict[str, Any]] = Field(default_factory=list, description="Topics needing practice")
    practice_plan: Optional[Dict[str, Any]] = Field(None, description="Structured practice plan")
    
    # Session status
    status: SessionStatus = Field(default=SessionStatus.PENDING, description="Session status")
    is_ready_for_next_round: bool = Field(default=True, description="Ready for next interview")
    next_round_scheduled_at: Optional[datetime] = Field(None, description="Next round schedule")
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class QuestionAnswer(BaseModel):
    """A single question-answer pair with evaluation"""
    question_id: str = Field(..., description="Question identifier")
    question_text: str = Field(..., description="The question asked")
    question_type: str = Field(..., description="Question type (technical/behavioral/etc)")
    difficulty: str = Field(..., description="Question difficulty")
    
    answer_text: str = Field(..., description="Candidate's answer")
    answer_timestamp: datetime = Field(default_factory=datetime.now)
    
    # Evaluation
    score: Optional[float] = Field(None, ge=0, le=10, description="Answer score (0-10)")
    strengths: List[str] = Field(default_factory=list, description="Answer strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Answer weaknesses")
    missing_points: List[str] = Field(default_factory=list, description="Missing key points")
    feedback: Optional[str] = Field(None, description="Detailed feedback")
    improvement_suggestions: List[str] = Field(default_factory=list)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class User(BaseModel):
    """User profile for the career development system"""
    user_id: str = Field(..., description="Unique user identifier")
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email")
    profession: str = Field(..., description="User's profession/field")
    experience_level: str = Field(default="junior", description="Experience level")
    
    # Career development tracking
    cv_analysis_id: Optional[str] = Field(None, description="Latest CV analysis ID")
    current_session_id: Optional[str] = Field(None, description="Current interview session ID")
    completed_sessions: List[str] = Field(default_factory=list, description="Completed session IDs")
    
    # Progress tracking
    total_interviews: int = Field(default=0, description="Total interviews taken")
    average_score: float = Field(default=0, ge=0, le=100, description="Average interview score")
    skill_improvement: Dict[str, float] = Field(default_factory=dict, description="Skill-wise improvement")
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

