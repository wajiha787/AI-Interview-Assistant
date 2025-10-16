from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Optional, Dict, Any
import os
import uuid
from datetime import datetime, timedelta
import json

from ..agents.cv_gap_analyzer import CVGapAnalyzerAgent
from ..agents.learning_recommender import LearningRecommenderAgent
from ..agents.interactive_interviewer import InteractiveInterviewerAgent
from ..agents.performance_analyzer import PerformanceAnalyzerAgent
from ..agents.job_match_analyzer import JobMatchAnalyzerAgent
from ..models.session import (
    User, CVAnalysis, InterviewSession, InterviewRound, 
    QuestionAnswer, SessionStatus
)
from ..utils.file_processor import FileProcessor

# Initialize FastAPI app
app = FastAPI(
    title="AI Career Development & Interview Preparation System",
    description="AI-powered career development platform with CV analysis, learning recommendations, and adaptive interview practice",
    version="2.0.0"
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
users_db = {}
cv_analyses_db = {}
interview_sessions_db = {}

# Initialize agents
cv_gap_analyzer = None
learning_recommender = None
interactive_interviewer = None
performance_analyzer = None
job_match_analyzer = None


def get_agents():
    """Get or initialize the AI agents"""
    global cv_gap_analyzer, learning_recommender, interactive_interviewer, performance_analyzer, job_match_analyzer
    
    if cv_gap_analyzer is None:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise HTTPException(
                status_code=500, 
                detail="GOOGLE_API_KEY environment variable not set"
            )
        
        # Set environment variable for litellm to use
        os.environ["GEMINI_API_KEY"] = google_api_key
        
        cv_gap_analyzer = CVGapAnalyzerAgent(google_api_key)
        learning_recommender = LearningRecommenderAgent(google_api_key)
        interactive_interviewer = InteractiveInterviewerAgent(google_api_key)
        performance_analyzer = PerformanceAnalyzerAgent(google_api_key)
        job_match_analyzer = JobMatchAnalyzerAgent(google_api_key)
    
    return {
        'cv_gap_analyzer': cv_gap_analyzer,
        'learning_recommender': learning_recommender,
        'interactive_interviewer': interactive_interviewer,
        'performance_analyzer': performance_analyzer,
        'job_match_analyzer': job_match_analyzer
    }


@app.get("/")
async def root():
    """Root endpoint - serve the frontend"""
    try:
        return HTMLResponse(content=open("app/frontend/index.html", encoding="utf-8").read())
    except FileNotFoundError:
        return {"message": "AI Career Development & Interview Preparation System API v2.0"}


# ============== USER MANAGEMENT ==============

@app.post("/api/users", response_model=dict)
async def create_user(
    name: str = Form(...),
    email: str = Form(...),
    profession: str = Form(...),
    experience_level: str = Form(default="junior")
):
    """Create a new user profile"""
    user_id = str(uuid.uuid4())
    user = User(
        user_id=user_id,
        name=name,
        email=email,
        profession=profession,
        experience_level=experience_level
    )
    users_db[user_id] = user
    return {
        "user_id": user_id,
        "message": "User profile created successfully",
        "user": user.dict()
    }


@app.get("/api/users/{user_id}", response_model=dict)
async def get_user(user_id: str):
    """Get user profile"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id].dict()


# ============== CV ANALYSIS & GAP IDENTIFICATION ==============

@app.post("/api/users/{user_id}/cv/upload", response_model=dict)
async def upload_and_analyze_cv(
    user_id: str,
    file: UploadFile = File(...),
    profession: Optional[str] = Form(None)
):
    """Upload CV and perform gap analysis"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    
    # Use provided profession or user's default
    target_profession = profession or user.profession
    
    try:
        # Process the uploaded CV
        cv_content = await file_processor.process_file(file)
        
        # Get agents
        agents = get_agents()
        
        # Perform gap analysis
        gap_analysis = agents['cv_gap_analyzer'].analyze_cv_gaps(cv_content, target_profession)
        structured_data = gap_analysis.get('structured_data', {})
        
        # Create CV analysis record
        analysis_id = str(uuid.uuid4())
        cv_analysis = CVAnalysis(
            user_id=user_id,
            analysis_id=analysis_id,
            cv_content=cv_content,
            profession=target_profession,
            current_level=structured_data.get('current_level', 'unknown'),
            overall_readiness_score=structured_data.get('overall_readiness_score', 50),
            technical_skills_gaps=structured_data.get('technical_skills_gaps', []),
            missing_certifications=structured_data.get('missing_certifications', []),
            experience_gaps=structured_data.get('experience_gaps', []),
            soft_skills_gaps=structured_data.get('soft_skills_gaps', []),
            educational_gaps=structured_data.get('educational_gaps', []),
            strengths=structured_data.get('strengths', []),
            priority_improvements=structured_data.get('priority_improvements', [])
        )
        
        # Store analysis
        cv_analyses_db[analysis_id] = cv_analysis
        user.cv_analysis_id = analysis_id
        user.updated_at = datetime.now()
        
        return {
            "analysis_id": analysis_id,
            "message": "CV analyzed successfully",
            "analysis": cv_analysis.dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CV analysis failed: {str(e)}")


@app.get("/api/cv-analysis/{analysis_id}", response_model=dict)
async def get_cv_analysis(analysis_id: str):
    """Get CV analysis results"""
    if analysis_id not in cv_analyses_db:
        raise HTTPException(status_code=404, detail="CV analysis not found")
    return cv_analyses_db[analysis_id].dict()


# ============== LEARNING RECOMMENDATIONS ==============

@app.post("/api/cv-analysis/{analysis_id}/recommendations", response_model=dict)
async def generate_learning_recommendations(
    analysis_id: str,
    available_time: str = Form(default="flexible")
):
    """Generate personalized learning recommendations based on CV analysis"""
    if analysis_id not in cv_analyses_db:
        raise HTTPException(status_code=404, detail="CV analysis not found")
    
    cv_analysis = cv_analyses_db[analysis_id]
    
    try:
        agents = get_agents()
        
        # Prepare gap analysis data
        gap_data = {
            "technical_skills_gaps": cv_analysis.technical_skills_gaps,
            "missing_certifications": cv_analysis.missing_certifications,
            "experience_gaps": cv_analysis.experience_gaps,
            "soft_skills_gaps": cv_analysis.soft_skills_gaps,
            "educational_gaps": cv_analysis.educational_gaps,
            "priority_improvements": cv_analysis.priority_improvements
        }
        
        # Generate recommendations
        recommendations = agents['learning_recommender'].generate_recommendations(
            gap_data, 
            cv_analysis.profession,
            available_time
        )
        
        # Store recommendations with the CV analysis
        cv_analysis.recommendations = recommendations.get('structured_data', {})
        cv_analysis.analyzed_at = datetime.now()
        
        return {
            "analysis_id": analysis_id,
            "message": "Learning recommendations generated successfully",
            "recommendations": recommendations.get('structured_data', {})
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")


# ============== JOB FIT ANALYSIS ==============

@app.post("/api/users/{user_id}/job-fit/analyze", response_model=dict)
async def analyze_job_fit(
    user_id: str,
    job_description: str = Form(...)
):
    """Analyze how well a user fits a specific job description"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    
    try:
        agents = get_agents()
        
        # Get CV analysis data if available
        cv_data = None
        if user.cv_analysis_id and user.cv_analysis_id in cv_analyses_db:
            cv_analysis = cv_analyses_db[user.cv_analysis_id]
            cv_data = {
                'profession': cv_analysis.profession,
                'current_level': cv_analysis.current_level,
                'overall_readiness_score': cv_analysis.overall_readiness_score,
                'strengths': cv_analysis.strengths,
                'technical_skills_gaps': cv_analysis.technical_skills_gaps,
                'experience_gaps': cv_analysis.experience_gaps,
                'missing_certifications': cv_analysis.missing_certifications
            }
        
        # Prepare user profile
        user_profile = {
            'name': user.name,
            'profession': user.profession,
            'experience_level': user.experience_level
        }
        
        # Perform job fit analysis
        job_fit_result = agents['job_match_analyzer'].analyze_job_fit(
            job_description=job_description,
            cv_data=cv_data,
            user_profile=user_profile
        )
        
        # Store the analysis result
        analysis_id = str(uuid.uuid4())
        
        return {
            "analysis_id": analysis_id,
            "user_id": user_id,
            "message": "Job fit analysis completed successfully",
            "analysis": job_fit_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job fit analysis failed: {str(e)}")


@app.post("/api/job-fit/extract-requirements", response_model=dict)
async def extract_job_requirements(
    job_description: str = Form(...)
):
    """Extract structured requirements from a job description (no user context needed)"""
    try:
        agents = get_agents()
        
        # Extract job requirements
        requirements = agents['job_match_analyzer'].extract_job_requirements(job_description)
        
        return {
            "message": "Job requirements extracted successfully",
            "requirements": requirements,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Requirements extraction failed: {str(e)}")


# ============== INTERVIEW SESSION MANAGEMENT ==============

@app.post("/api/users/{user_id}/interview-session/start", response_model=dict)
async def start_interview_session(
    user_id: str,
    profession: Optional[str] = Form(None),
    focus_areas: Optional[str] = Form(None)
):
    """Start a new interview session"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    target_profession = profession or user.profession
    
    # Parse focus areas
    focus_list = [area.strip() for area in focus_areas.split(',')] if focus_areas else []
    
    # Create new session
    session_id = str(uuid.uuid4())
    session = InterviewSession(
        session_id=session_id,
        user_id=user_id,
        profession=target_profession,
        status=SessionStatus.IN_PROGRESS
    )
    
    # Store session
    interview_sessions_db[session_id] = session
    user.current_session_id = session_id
    user.updated_at = datetime.now()
    
    return {
        "session_id": session_id,
        "message": "Interview session started",
        "session": session.dict()
    }


@app.post("/api/interview-session/{session_id}/round/start", response_model=dict)
async def start_interview_round(
    session_id: str,
    difficulty: str = Form(default="mixed"),
    focus_areas: Optional[str] = Form(None)
):
    """Start a new interview round and generate questions"""
    if session_id not in interview_sessions_db:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    session = interview_sessions_db[session_id]
    
    # Parse focus areas from weak topics if not provided
    if focus_areas:
        focus_list = [area.strip() for area in focus_areas.split(',')]
    else:
        focus_list = [topic.get('topic', '') for topic in session.weak_topics[:3]]
    
    try:
        agents = get_agents()
        
        # Generate interview questions
        questions_data = agents['interactive_interviewer'].generate_interview_questions(
            session.profession,
            users_db[session.user_id].experience_level,
            focus_list if focus_list else None,
            difficulty
        )
        
        # Create new round
        round_id = str(uuid.uuid4())
        round_number = session.current_round + 1
        
        interview_round = InterviewRound(
            round_id=round_id,
            round_number=round_number,
            questions=questions_data.get('questions', []),
            status=SessionStatus.IN_PROGRESS,
            started_at=datetime.now()
        )
        
        # Update session
        session.rounds.append(interview_round)
        session.current_round = round_number
        session.total_rounds = len(session.rounds)
        session.updated_at = datetime.now()
        
        return {
            "round_id": round_id,
            "round_number": round_number,
            "message": "Interview round started",
            "questions": questions_data.get('questions', []),
            "interview_structure": questions_data.get('interview_structure', {})
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start interview round: {str(e)}")


@app.post("/api/interview-session/{session_id}/round/{round_id}/answer", response_model=dict)
async def submit_answer(
    session_id: str,
    round_id: str,
    question_id: str = Form(...),
    answer: str = Form(...)
):
    """Submit an answer to a question"""
    if session_id not in interview_sessions_db:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    session = interview_sessions_db[session_id]
    
    # Find the round
    current_round = None
    for round_obj in session.rounds:
        if round_obj.round_id == round_id:
            current_round = round_obj
            break
    
    if not current_round:
        raise HTTPException(status_code=404, detail="Interview round not found")
    
    # Find the question
    question = None
    for q in current_round.questions:
        if str(q.get('id')) == question_id:
            question = q
            break
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    try:
        agents = get_agents()
        
        # Evaluate the answer
        evaluation = agents['interactive_interviewer'].evaluate_answer(
            question, 
            answer, 
            session.profession
        )
        
        # Store the answer with evaluation
        answer_data = {
            "question_id": question_id,
            "question": question,
            "answer": answer,
            "evaluation": evaluation,
            "timestamp": datetime.now().isoformat()
        }
        
        current_round.answers.append(answer_data)
        session.updated_at = datetime.now()
        
        return {
            "message": "Answer submitted and evaluated",
            "evaluation": evaluation,
            "answered_count": len(current_round.answers),
            "total_questions": len(current_round.questions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate answer: {str(e)}")


@app.post("/api/interview-session/{session_id}/round/{round_id}/complete", response_model=dict)
async def complete_interview_round(session_id: str, round_id: str):
    """Complete an interview round and analyze performance"""
    if session_id not in interview_sessions_db:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    session = interview_sessions_db[session_id]
    
    # Find the round
    current_round = None
    for round_obj in session.rounds:
        if round_obj.round_id == round_id:
            current_round = round_obj
            break
    
    if not current_round:
        raise HTTPException(status_code=404, detail="Interview round not found")
    
    try:
        agents = get_agents()
        
        # Prepare interview data for analysis
        interview_data = {
            "round_number": current_round.round_number,
            "questions": current_round.questions,
            "answers": current_round.answers,
            "profession": session.profession
        }
        
        # Analyze performance
        performance = agents['performance_analyzer'].analyze_interview_performance(
            interview_data,
            session.profession
        )
        
        # Update round
        current_round.score = performance.get('overall_score', 0)
        current_round.status = SessionStatus.COMPLETED
        current_round.completed_at = datetime.now()
        current_round.feedback = performance.get('detailed_feedback', '')
        
        # Update session
        session.overall_score = performance.get('overall_score', 0)
        session.best_score = max(session.best_score, current_round.score)
        session.weak_topics = performance.get('weak_topics', [])
        session.updated_at = datetime.now()
        
        # Check if score is 100%
        if current_round.score >= 100:
            session.is_ready_for_next_round = True
            session.status = SessionStatus.COMPLETED
            message = "Perfect score! You're ready for the next level interview."
        else:
            session.is_ready_for_next_round = False
            # Generate practice plan
            practice_plan = agents['performance_analyzer'].generate_practice_plan(
                performance.get('weak_topics', []),
                session.profession,
                "1 week"
            )
            session.practice_plan = practice_plan
            message = "Interview completed. Please review weak areas and practice before the next round."
        
        # Update user stats
        user = users_db[session.user_id]
        user.total_interviews += 1
        if user.average_score == 0:
            user.average_score = current_round.score
        else:
            user.average_score = (user.average_score + current_round.score) / 2
        user.updated_at = datetime.now()
        
        return {
            "message": message,
            "round_score": current_round.score,
            "overall_score": session.overall_score,
            "ready_for_next_round": session.is_ready_for_next_round,
            "performance_analysis": performance,
            "practice_plan": session.practice_plan if not session.is_ready_for_next_round else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete round: {str(e)}")


@app.get("/api/interview-session/{session_id}", response_model=dict)
async def get_interview_session(session_id: str):
    """Get interview session details"""
    if session_id not in interview_sessions_db:
        raise HTTPException(status_code=404, detail="Interview session not found")
    return interview_sessions_db[session_id].dict()


@app.get("/api/users/{user_id}/sessions", response_model=list)
async def get_user_sessions(user_id: str):
    """Get all sessions for a user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_sessions = [
        session.dict() 
        for session in interview_sessions_db.values() 
        if session.user_id == user_id
    ]
    
    return user_sessions


# ============== DASHBOARD & STATISTICS ==============

@app.get("/api/users/{user_id}/dashboard", response_model=dict)
async def get_user_dashboard(user_id: str):
    """Get user dashboard with statistics and progress"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    
    # Get CV analysis
    cv_analysis = None
    if user.cv_analysis_id and user.cv_analysis_id in cv_analyses_db:
        cv_analysis = cv_analyses_db[user.cv_analysis_id].dict()
    
    # Get current session
    current_session = None
    if user.current_session_id and user.current_session_id in interview_sessions_db:
        current_session = interview_sessions_db[user.current_session_id].dict()
    
    # Get completed sessions
    completed_sessions = [
        session.dict()
        for session in interview_sessions_db.values()
        if session.user_id == user_id and session.status == SessionStatus.COMPLETED
    ]
    
    return {
        "user": user.dict(),
        "cv_analysis": cv_analysis,
        "current_session": current_session,
        "completed_sessions": completed_sessions,
        "statistics": {
            "total_interviews": user.total_interviews,
            "average_score": user.average_score,
            "completed_sessions_count": len(completed_sessions)
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }


# Mount static files
try:
    app.mount("/static", StaticFiles(directory="app/frontend"), name="static")
except Exception:
    pass  # Frontend directory might not exist yet


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
