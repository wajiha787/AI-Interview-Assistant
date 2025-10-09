import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.api.main import app


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def mock_hiring_crew():
    """Mock the hiring evaluation crew"""
    with patch('app.api.main.get_hiring_crew') as mock:
        mock_crew = Mock()
        mock_crew.evaluate_candidate.return_value = Mock(
            candidate_id="test-candidate-id",
            evaluation_id="test-evaluation-id",
            overall_score=8.5,
            recommendation="Hire",
            strengths=["Strong technical skills", "Good communication"],
            weaknesses=["Limited leadership experience"],
            detailed_feedback="Comprehensive evaluation feedback"
        )
        mock_crew.get_evaluation_summary.return_value = {
            "candidate_id": "test-candidate-id",
            "evaluation_id": "test-evaluation-id",
            "overall_score": 8.5,
            "recommendation": "Hire"
        }
        mock.return_value = mock_crew
        yield mock_crew


class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_create_candidate(self, client):
        """Test candidate creation"""
        response = client.post(
            "/api/candidates",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "position_applied": "Software Engineer",
                "phone": "123-456-7890"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "candidate_id" in data
        assert data["message"] == "Candidate created successfully"
    
    def test_create_candidate_missing_required_fields(self, client):
        """Test candidate creation with missing required fields"""
        response = client.post(
            "/api/candidates",
            data={
                "name": "John Doe",
                # Missing email and position_applied
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_upload_resume_candidate_not_found(self, client):
        """Test resume upload for non-existent candidate"""
        fake_file = ("test.pdf", b"fake pdf content", "application/pdf")
        response = client.post(
            "/api/candidates/non-existent-id/resume",
            files={"file": fake_file}
        )
        assert response.status_code == 404
        assert "Candidate not found" in response.json()["detail"]
    
    def test_upload_interview_candidate_not_found(self, client):
        """Test interview upload for non-existent candidate"""
        fake_file = ("test.pdf", b"fake pdf content", "application/pdf")
        response = client.post(
            "/api/candidates/non-existent-id/interview",
            files={"file": fake_file}
        )
        assert response.status_code == 404
        assert "Candidate not found" in response.json()["detail"]
    
    def test_evaluate_candidate_not_found(self, client):
        """Test evaluation for non-existent candidate"""
        response = client.post("/api/candidates/non-existent-id/evaluate")
        assert response.status_code == 404
        assert "Candidate not found" in response.json()["detail"]
    
    def test_evaluate_candidate_missing_resume(self, client):
        """Test evaluation when resume is missing"""
        # First create a candidate
        create_response = client.post(
            "/api/candidates",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "position_applied": "Software Engineer"
            }
        )
        candidate_id = create_response.json()["candidate_id"]
        
        # Try to evaluate without resume
        response = client.post(f"/api/candidates/{candidate_id}/evaluate")
        assert response.status_code == 400
        assert "Resume not found" in response.json()["detail"]
    
    def test_list_candidates_empty(self, client):
        """Test listing candidates when none exist"""
        response = client.get("/api/candidates")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_evaluations_empty(self, client):
        """Test listing evaluations when none exist"""
        response = client.get("/api/evaluations")
        assert response.status_code == 200
        assert response.json() == []
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_evaluate_candidate_success(self, client, mock_hiring_crew):
        """Test successful candidate evaluation"""
        # Create candidate
        create_response = client.post(
            "/api/candidates",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "position_applied": "Software Engineer"
            }
        )
        candidate_id = create_response.json()["candidate_id"]
        
        # Upload resume
        fake_resume = ("resume.pdf", b"fake resume content", "application/pdf")
        client.post(
            f"/api/candidates/{candidate_id}/resume",
            files={"file": fake_resume}
        )
        
        # Upload interview
        fake_interview = ("interview.pdf", b"fake interview content", "application/pdf")
        client.post(
            f"/api/candidates/{candidate_id}/interview",
            files={"file": fake_interview}
        )
        
        # Evaluate candidate
        response = client.post(f"/api/candidates/{candidate_id}/evaluate")
        assert response.status_code == 200
        data = response.json()
        assert data["overall_score"] == 8.5
        assert data["recommendation"] == "Hire"
    
    def test_get_evaluation_not_found(self, client):
        """Test getting evaluation for non-existent candidate"""
        response = client.get("/api/candidates/non-existent-id/evaluation")
        assert response.status_code == 404
        assert "Evaluation not found" in response.json()["detail"]


class TestFileProcessing:
    """Test cases for file processing"""
    
    def test_unsupported_file_type(self, client):
        """Test upload of unsupported file type"""
        # Create candidate first
        create_response = client.post(
            "/api/candidates",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "position_applied": "Software Engineer"
            }
        )
        candidate_id = create_response.json()["candidate_id"]
        
        # Try to upload unsupported file
        fake_file = ("test.txt", b"fake content", "image/jpeg")
        response = client.post(
            f"/api/candidates/{candidate_id}/resume",
            files={"file": fake_file}
        )
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]

