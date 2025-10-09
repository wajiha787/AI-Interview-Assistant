from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List, Optional
import os
import uuid
from datetime import datetime
import json

from ..agents import HiringEvaluationCrew
from ..models.candidate import Candidate, Resume, InterviewTranscript, EvaluationResult
from ..utils.file_processor import FileProcessor

# Initialize FastAPI app
app = FastAPI(
    title="AI Hiring Evaluation System",
    description="Multi-agent AI system for automated candidate evaluation using CrewAI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize file processor
file_processor = FileProcessor()

# In-memory storage (in production, use a database)
candidates_db = {}
evaluations_db = {}

# Initialize the hiring evaluation crew
hiring_crew = None

def get_hiring_crew():
    """Get or initialize the hiring evaluation crew"""
    global hiring_crew
    if hiring_crew is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise HTTPException(
                status_code=500, 
                detail="OPENAI_API_KEY environment variable not set"
            )
        hiring_crew = HiringEvaluationCrew(openai_api_key)
    return hiring_crew

@app.get("/")
async def root():
    """Root endpoint - serve the frontend"""
    return HTMLResponse(content=open("app/frontend/index.html").read())

@app.post("/api/candidates", response_model=dict)
async def create_candidate(
    name: str = Form(...),
    email: str = Form(...),
    position_applied: str = Form(...),
    phone: Optional[str] = Form(None)
):
    """Create a new candidate"""
    candidate_id = str(uuid.uuid4())
    candidate = Candidate(
        id=candidate_id,
        name=name,
        email=email,
        position_applied=position_applied,
        phone=phone
    )
    candidates_db[candidate_id] = candidate
    return {"candidate_id": candidate_id, "message": "Candidate created successfully"}

@app.post("/api/candidates/{candidate_id}/resume", response_model=dict)
async def upload_resume(
    candidate_id: str,
    file: UploadFile = File(...)
):
    """Upload resume for a candidate"""
    if candidate_id not in candidates_db:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Process the uploaded file
    content = await file_processor.process_file(file)
    
    # Create resume object
    resume = Resume(
        candidate_id=candidate_id,
        content=content,
        file_name=file.filename,
        file_type=file.content_type or "unknown"
    )
    
    # Store resume (in production, save to database)
    candidates_db[candidate_id].resume = resume
    
    return {"message": "Resume uploaded successfully", "file_name": file.filename}

@app.post("/api/candidates/{candidate_id}/interview", response_model=dict)
async def upload_interview(
    candidate_id: str,
    file: UploadFile = File(...)
):
    """Upload interview transcript for a candidate"""
    if candidate_id not in candidates_db:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Process the uploaded file
    content = await file_processor.process_file(file)
    
    # Create interview transcript object
    interview = InterviewTranscript(
        candidate_id=candidate_id,
        content=content,
        file_name=file.filename
    )
    
    # Store interview (in production, save to database)
    candidates_db[candidate_id].interview = interview
    
    return {"message": "Interview transcript uploaded successfully", "file_name": file.filename}

@app.post("/api/candidates/{candidate_id}/evaluate", response_model=dict)
async def evaluate_candidate(candidate_id: str):
    """Evaluate a candidate using the AI system"""
    if candidate_id not in candidates_db:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    candidate = candidates_db[candidate_id]
    
    # Check if both resume and interview are available
    if not hasattr(candidate, 'resume') or not candidate.resume:
        raise HTTPException(status_code=400, detail="Resume not found. Please upload resume first.")
    
    if not hasattr(candidate, 'interview') or not candidate.interview:
        raise HTTPException(status_code=400, detail="Interview transcript not found. Please upload interview first.")
    
    try:
        # Get the hiring crew
        crew = get_hiring_crew()
        
        # Perform evaluation
        evaluation_result = crew.evaluate_candidate(
            candidate=candidate,
            resume=candidate.resume,
            interview=candidate.interview
        )
        
        # Store evaluation result
        evaluations_db[candidate_id] = evaluation_result
        
        # Return summary
        summary = crew.get_evaluation_summary(evaluation_result)
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@app.get("/api/candidates/{candidate_id}/evaluation", response_model=dict)
async def get_evaluation(candidate_id: str):
    """Get evaluation result for a candidate"""
    if candidate_id not in evaluations_db:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    evaluation = evaluations_db[candidate_id]
    return evaluation.dict()

@app.get("/api/candidates", response_model=List[dict])
async def list_candidates():
    """List all candidates"""
    return [
        {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "position_applied": candidate.position_applied,
            "created_at": candidate.created_at.isoformat(),
            "has_resume": hasattr(candidate, 'resume') and candidate.resume is not None,
            "has_interview": hasattr(candidate, 'interview') and candidate.interview is not None,
            "has_evaluation": candidate.id in evaluations_db
        }
        for candidate in candidates_db.values()
    ]

@app.get("/api/evaluations", response_model=List[dict])
async def list_evaluations():
    """List all evaluations"""
    return [
        {
            "candidate_id": evaluation.candidate_id,
            "evaluation_id": evaluation.evaluation_id,
            "overall_score": evaluation.overall_score,
            "recommendation": evaluation.recommendation,
            "evaluated_at": evaluation.evaluated_at.isoformat()
        }
        for evaluation in evaluations_db.values()
    ]

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Mount static files
app.mount("/static", StaticFiles(directory="app/frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

