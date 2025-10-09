import pytest
from datetime import datetime
from app.models.candidate import Candidate, Resume, InterviewTranscript, EvaluationResult, EvaluationCriteria
from app.models.evaluation import EvaluationScore, EvaluationFeedback, RecommendationType, EvaluationSummary


class TestCandidateModels:
    """Test cases for candidate-related models"""
    
    def test_candidate_creation(self):
        """Test candidate model creation"""
        candidate = Candidate(
            id="test-id",
            name="John Doe",
            email="john@example.com",
            position_applied="Software Engineer"
        )
        
        assert candidate.id == "test-id"
        assert candidate.name == "John Doe"
        assert candidate.email == "john@example.com"
        assert candidate.position_applied == "Software Engineer"
        assert candidate.phone is None
        assert isinstance(candidate.created_at, datetime)
    
    def test_candidate_with_optional_fields(self):
        """Test candidate model with optional fields"""
        candidate = Candidate(
            id="test-id",
            name="John Doe",
            email="john@example.com",
            position_applied="Software Engineer",
            phone="123-456-7890"
        )
        
        assert candidate.phone == "123-456-7890"
    
    def test_resume_creation(self):
        """Test resume model creation"""
        resume = Resume(
            candidate_id="test-candidate-id",
            content="John Doe\nSoftware Engineer\n5 years experience",
            file_name="resume.pdf",
            file_type="application/pdf"
        )
        
        assert resume.candidate_id == "test-candidate-id"
        assert resume.content == "John Doe\nSoftware Engineer\n5 years experience"
        assert resume.file_name == "resume.pdf"
        assert resume.file_type == "application/pdf"
        assert isinstance(resume.uploaded_at, datetime)
        assert resume.skills == []
        assert resume.education == []
    
    def test_interview_transcript_creation(self):
        """Test interview transcript model creation"""
        transcript = InterviewTranscript(
            candidate_id="test-candidate-id",
            content="Interviewer: Tell me about yourself. Candidate: I am a software engineer..."
        )
        
        assert transcript.candidate_id == "test-candidate-id"
        assert "Tell me about yourself" in transcript.content
        assert isinstance(transcript.uploaded_at, datetime)
        assert transcript.questions_asked == []
        assert transcript.candidate_responses == []


class TestEvaluationModels:
    """Test cases for evaluation-related models"""
    
    def test_evaluation_criteria_creation(self):
        """Test evaluation criteria model creation"""
        criteria = EvaluationCriteria(
            technical_skills=8.5,
            communication=7.0,
            problem_solving=9.0,
            cultural_fit=8.0,
            experience_relevance=7.5
        )
        
        assert criteria.technical_skills == 8.5
        assert criteria.communication == 7.0
        assert criteria.problem_solving == 9.0
        assert criteria.cultural_fit == 8.0
        assert criteria.experience_relevance == 7.5
        assert criteria.total_score == (8.5 + 7.0 + 9.0 + 8.0 + 7.5) / 5
    
    def test_evaluation_criteria_validation(self):
        """Test evaluation criteria validation"""
        with pytest.raises(ValueError):
            EvaluationCriteria(
                technical_skills=11.0,  # Should be <= 10
                communication=7.0,
                problem_solving=9.0,
                cultural_fit=8.0,
                experience_relevance=7.5
            )
        
        with pytest.raises(ValueError):
            EvaluationCriteria(
                technical_skills=-1.0,  # Should be >= 0
                communication=7.0,
                problem_solving=9.0,
                cultural_fit=8.0,
                experience_relevance=7.5
            )
    
    def test_evaluation_result_creation(self):
        """Test evaluation result model creation"""
        criteria = EvaluationCriteria(
            technical_skills=8.5,
            communication=7.0,
            problem_solving=9.0,
            cultural_fit=8.0,
            experience_relevance=7.5
        )
        
        result = EvaluationResult(
            candidate_id="test-candidate-id",
            evaluation_id="test-evaluation-id",
            criteria=criteria,
            overall_score=8.0,
            recommendation="Hire",
            strengths=["Strong technical skills", "Good problem solving"],
            weaknesses=["Communication could be improved"],
            detailed_feedback="Comprehensive evaluation feedback"
        )
        
        assert result.candidate_id == "test-candidate-id"
        assert result.evaluation_id == "test-evaluation-id"
        assert result.overall_score == 8.0
        assert result.recommendation == "Hire"
        assert len(result.strengths) == 2
        assert len(result.weaknesses) == 1
        assert isinstance(result.evaluated_at, datetime)
    
    def test_evaluation_score_creation(self):
        """Test evaluation score model creation"""
        score = EvaluationScore(
            category="Technical Skills",
            score=8.5,
            weight=0.3,
            reasoning="Strong background in Python and machine learning",
            evidence=["5 years Python experience", "ML certification"]
        )
        
        assert score.category == "Technical Skills"
        assert score.score == 8.5
        assert score.weight == 0.3
        assert len(score.evidence) == 2
    
    def test_evaluation_feedback_creation(self):
        """Test evaluation feedback model creation"""
        feedback = EvaluationFeedback(
            category="Communication",
            feedback="Good verbal communication but needs improvement in written communication",
            suggestions=["Practice technical writing", "Take communication course"],
            examples=["Clear explanation of technical concepts", "Some grammar issues in written responses"]
        )
        
        assert feedback.category == "Communication"
        assert "verbal communication" in feedback.feedback
        assert len(feedback.suggestions) == 2
        assert len(feedback.examples) == 2
    
    def test_evaluation_summary_creation(self):
        """Test evaluation summary model creation"""
        summary = EvaluationSummary(
            candidate_id="test-candidate-id",
            overall_score=8.0,
            recommendation=RecommendationType.HIRE,
            confidence=0.85,
            key_highlights=["Strong technical skills", "Good cultural fit"],
            concerns=["Limited leadership experience"],
            next_steps=["Schedule final interview", "Check references"]
        )
        
        assert summary.candidate_id == "test-candidate-id"
        assert summary.overall_score == 8.0
        assert summary.recommendation == RecommendationType.HIRE
        assert summary.confidence == 0.85
        assert len(summary.key_highlights) == 2
        assert len(summary.concerns) == 1
        assert len(summary.next_steps) == 2
        assert isinstance(summary.created_at, datetime)
    
    def test_recommendation_type_enum(self):
        """Test recommendation type enum values"""
        assert RecommendationType.STRONG_HIRE == "strong_hire"
        assert RecommendationType.HIRE == "hire"
        assert RecommendationType.MAYBE == "maybe"
        assert RecommendationType.NO_HIRE == "no_hire"
        assert RecommendationType.STRONG_NO_HIRE == "strong_no_hire"

