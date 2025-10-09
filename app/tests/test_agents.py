import pytest
import os
from unittest.mock import Mock, patch
from app.agents.resume_analyzer import ResumeAnalyzerAgent
from app.agents.interview_evaluator import InterviewEvaluatorAgent
from app.agents.scoring_agent import ScoringAgent


class TestResumeAnalyzerAgent:
    """Test cases for ResumeAnalyzerAgent"""
    
    @pytest.fixture
    def agent(self):
        """Create a ResumeAnalyzerAgent instance for testing"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            return ResumeAnalyzerAgent('test-key')
    
    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly"""
        assert agent is not None
        assert agent.agent is not None
        assert agent.llm is not None
    
    def test_create_analysis_task(self, agent):
        """Test task creation"""
        resume_content = "John Doe\nSoftware Engineer\n5 years experience"
        position = "Senior Developer"
        
        task = agent.create_analysis_task(resume_content, position)
        
        assert task is not None
        assert position in task.description
        assert resume_content in task.description
    
    def test_extract_structured_data_valid_json(self, agent):
        """Test extraction of structured data from valid JSON"""
        valid_json = '{"experience_years": 5, "skills": [{"name": "Python", "proficiency": "expert"}]}'
        
        result = agent.extract_structured_data(valid_json)
        
        assert result["experience_years"] == 5
        assert len(result["skills"]) == 1
        assert result["skills"][0]["name"] == "Python"
    
    def test_extract_structured_data_invalid_json(self, agent):
        """Test extraction with invalid JSON fallback"""
        invalid_json = "This is not valid JSON"
        
        result = agent.extract_structured_data(invalid_json)
        
        assert result["experience_years"] == 0
        assert result["overall_assessment"] == invalid_json


class TestInterviewEvaluatorAgent:
    """Test cases for InterviewEvaluatorAgent"""
    
    @pytest.fixture
    def agent(self):
        """Create an InterviewEvaluatorAgent instance for testing"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            return InterviewEvaluatorAgent('test-key')
    
    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly"""
        assert agent is not None
        assert agent.agent is not None
        assert agent.llm is not None
    
    def test_create_evaluation_task(self, agent):
        """Test task creation"""
        transcript = "Interviewer: Tell me about yourself. Candidate: I am a software engineer..."
        position = "Senior Developer"
        resume_summary = "5 years experience in Python"
        
        task = agent.create_evaluation_task(transcript, position, resume_summary)
        
        assert task is not None
        assert position in task.description
        assert transcript in task.description
        assert resume_summary in task.description
    
    def test_extract_structured_data_valid_json(self, agent):
        """Test extraction of structured data from valid JSON"""
        valid_json = '{"communication_score": 8, "problem_solving_score": 7}'
        
        result = agent.extract_structured_data(valid_json)
        
        assert result["communication_score"] == 8
        assert result["problem_solving_score"] == 7
    
    def test_extract_structured_data_invalid_json(self, agent):
        """Test extraction with invalid JSON fallback"""
        invalid_json = "This is not valid JSON"
        
        result = agent.extract_structured_data(invalid_json)
        
        assert result["communication_score"] == 5
        assert result["overall_assessment"] == invalid_json


class TestScoringAgent:
    """Test cases for ScoringAgent"""
    
    @pytest.fixture
    def agent(self):
        """Create a ScoringAgent instance for testing"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            return ScoringAgent('test-key')
    
    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly"""
        assert agent is not None
        assert agent.agent is not None
        assert agent.llm is not None
    
    def test_create_scoring_task(self, agent):
        """Test task creation"""
        resume_analysis = {"structured_data": {"experience_years": 5}}
        interview_evaluation = {"structured_data": {"communication_score": 8}}
        position = "Senior Developer"
        
        task = agent.create_scoring_task(resume_analysis, interview_evaluation, position)
        
        assert task is not None
        assert position in task.description
    
    def test_extract_structured_data_valid_json(self, agent):
        """Test extraction of structured data from valid JSON"""
        valid_json = '{"overall_score": 8.5, "recommendation": "hire"}'
        
        result = agent.extract_structured_data(valid_json)
        
        assert result["overall_score"] == 8.5
        assert result["recommendation"] == "hire"
    
    def test_extract_structured_data_invalid_json(self, agent):
        """Test extraction with invalid JSON fallback"""
        invalid_json = "This is not valid JSON"
        
        result = agent.extract_structured_data(invalid_json)
        
        assert result["overall_score"] == 5
        assert result["recommendation"] == "maybe"

