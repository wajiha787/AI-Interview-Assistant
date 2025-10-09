from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class Candidate(BaseModel):
    """Candidate information model"""
    id: str = Field(..., description="Unique candidate identifier")
    name: str = Field(..., description="Candidate's full name")
    email: str = Field(..., description="Candidate's email address")
    phone: Optional[str] = Field(None, description="Candidate's phone number")
    position_applied: str = Field(..., description="Position the candidate is applying for")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Resume(BaseModel):
    """Resume data model"""
    candidate_id: str = Field(..., description="Associated candidate ID")
    content: str = Field(..., description="Raw resume text content")
    file_name: str = Field(..., description="Original file name")
    file_type: str = Field(..., description="File type (pdf, docx, txt)")
    uploaded_at: datetime = Field(default_factory=datetime.now)
    
    # Extracted structured data
    experience_years: Optional[int] = Field(None, description="Years of experience")
    skills: List[str] = Field(default_factory=list, description="List of skills")
    education: List[Dict[str, Any]] = Field(default_factory=list, description="Education history")
    work_experience: List[Dict[str, Any]] = Field(default_factory=list, description="Work experience")
    certifications: List[str] = Field(default_factory=list, description="Certifications")


class InterviewTranscript(BaseModel):
    """Interview transcript data model"""
    candidate_id: str = Field(..., description="Associated candidate ID")
    content: str = Field(..., description="Raw interview transcript text")
    duration_minutes: Optional[int] = Field(None, description="Interview duration in minutes")
    interviewer: Optional[str] = Field(None, description="Interviewer name")
    interview_date: Optional[datetime] = Field(None, description="Date of interview")
    uploaded_at: datetime = Field(default_factory=datetime.now)
    
    # Extracted structured data
    questions_asked: List[str] = Field(default_factory=list, description="List of questions asked")
    candidate_responses: List[Dict[str, str]] = Field(default_factory=list, description="Q&A pairs")
    key_topics: List[str] = Field(default_factory=list, description="Key topics discussed")


class EvaluationCriteria(BaseModel):
    """Evaluation criteria model"""
    technical_skills: float = Field(..., ge=0, le=10, description="Technical skills score (0-10)")
    communication: float = Field(..., ge=0, le=10, description="Communication skills score (0-10)")
    problem_solving: float = Field(..., ge=0, le=10, description="Problem solving ability score (0-10)")
    cultural_fit: float = Field(..., ge=0, le=10, description="Cultural fit score (0-10)")
    experience_relevance: float = Field(..., ge=0, le=10, description="Experience relevance score (0-10)")
    
    @property
    def total_score(self) -> float:
        """Calculate total weighted score"""
        return sum([
            self.technical_skills,
            self.communication,
            self.problem_solving,
            self.cultural_fit,
            self.experience_relevance
        ]) / 5


class EvaluationResult(BaseModel):
    """Complete evaluation result model"""
    candidate_id: str = Field(..., description="Associated candidate ID")
    evaluation_id: str = Field(..., description="Unique evaluation identifier")
    criteria: EvaluationCriteria = Field(..., description="Detailed scoring criteria")
    overall_score: float = Field(..., ge=0, le=10, description="Overall evaluation score")
    recommendation: str = Field(..., description="Hire/No Hire/Maybe recommendation")
    strengths: List[str] = Field(default_factory=list, description="Candidate strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Areas for improvement")
    detailed_feedback: str = Field(..., description="Detailed evaluation feedback")
    evaluated_at: datetime = Field(default_factory=datetime.now)
    evaluated_by: str = Field(default="AI Evaluation System", description="System that performed evaluation")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

