from crewai import Crew, Process
from typing import Dict, Any, List
import uuid
from datetime import datetime

from .resume_analyzer import ResumeAnalyzerAgent
from .interview_evaluator import InterviewEvaluatorAgent
from .scoring_agent import ScoringAgent
from ..models.candidate import Candidate, Resume, InterviewTranscript, EvaluationResult, EvaluationCriteria


class HiringEvaluationCrew:
    """Main crew manager that orchestrates the hiring evaluation process"""
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        
        # Initialize agents
        self.resume_analyzer = ResumeAnalyzerAgent(openai_api_key)
        self.interview_evaluator = InterviewEvaluatorAgent(openai_api_key)
        self.scoring_agent = ScoringAgent(openai_api_key)
        
        # Create the crew
        self.crew = Crew(
            agents=[
                self.resume_analyzer.agent,
                self.interview_evaluator.agent,
                self.scoring_agent.agent
            ],
            tasks=[],  # Tasks will be created dynamically
            process=Process.sequential,
            verbose=True
        )
    
    def evaluate_candidate(self, 
                          candidate: Candidate, 
                          resume: Resume, 
                          interview: InterviewTranscript) -> EvaluationResult:
        """
        Main method to evaluate a candidate using the multi-agent crew
        
        Args:
            candidate: Candidate information
            resume: Resume data
            interview: Interview transcript data
            
        Returns:
            EvaluationResult: Complete evaluation result
        """
        
        # Step 1: Analyze resume
        print("🔍 Analyzing resume...")
        resume_analysis = self.resume_analyzer.analyze_resume(
            resume.content, 
            candidate.position_applied
        )
        
        # Step 2: Evaluate interview
        print("🎤 Evaluating interview...")
        resume_summary = resume_analysis.get('structured_data', {}).get('overall_assessment', '')
        interview_evaluation = self.interview_evaluator.evaluate_interview(
            interview.content,
            candidate.position_applied,
            resume_summary
        )
        
        # Step 3: Generate final score and recommendation
        print("📊 Generating final score and recommendation...")
        final_scoring = self.scoring_agent.generate_final_score(
            resume_analysis,
            interview_evaluation,
            candidate.position_applied
        )
        
        # Step 4: Create evaluation result
        evaluation_result = self._create_evaluation_result(
            candidate,
            resume_analysis,
            interview_evaluation,
            final_scoring
        )
        
        return evaluation_result
    
    def _create_evaluation_result(self, 
                                 candidate: Candidate,
                                 resume_analysis: Dict[str, Any],
                                 interview_evaluation: Dict[str, Any],
                                 final_scoring: Dict[str, Any]) -> EvaluationResult:
        """Create the final evaluation result from all agent outputs"""
        
        # Extract data from agent outputs
        resume_data = resume_analysis.get('structured_data', {})
        interview_data = interview_evaluation.get('structured_data', {})
        scoring_data = final_scoring.get('structured_data', {})
        
        # Create evaluation criteria
        detailed_scores = scoring_data.get('detailed_scores', {})
        criteria = EvaluationCriteria(
            technical_skills=detailed_scores.get('technical_skills', 5.0),
            communication=detailed_scores.get('communication', 5.0),
            problem_solving=detailed_scores.get('problem_solving', 5.0),
            cultural_fit=detailed_scores.get('cultural_fit', 5.0),
            experience_relevance=detailed_scores.get('experience_relevance', 5.0)
        )
        
        # Determine recommendation
        recommendation = self._map_recommendation(scoring_data.get('recommendation', 'maybe'))
        
        # Compile strengths and weaknesses
        strengths = []
        strengths.extend(resume_data.get('strengths', []))
        strengths.extend(interview_data.get('strengths_demonstrated', []))
        strengths.extend(scoring_data.get('key_strengths', []))
        
        weaknesses = []
        weaknesses.extend(resume_data.get('weaknesses', []))
        weaknesses.extend(interview_data.get('areas_for_improvement', []))
        weaknesses.extend(scoring_data.get('main_concerns', []))
        
        # Create detailed feedback
        detailed_feedback = self._create_detailed_feedback(
            resume_analysis.get('raw_analysis', ''),
            interview_evaluation.get('raw_evaluation', ''),
            final_scoring.get('raw_scoring', '')
        )
        
        return EvaluationResult(
            candidate_id=candidate.id,
            evaluation_id=str(uuid.uuid4()),
            criteria=criteria,
            overall_score=scoring_data.get('overall_score', 5.0),
            recommendation=recommendation,
            strengths=list(set(strengths)),  # Remove duplicates
            weaknesses=list(set(weaknesses)),  # Remove duplicates
            detailed_feedback=detailed_feedback,
            evaluated_at=datetime.now(),
            evaluated_by="AI Hiring Evaluation Crew"
        )
    
    def _map_recommendation(self, recommendation: str) -> str:
        """Map recommendation string to standardized format"""
        recommendation_map = {
            'strong_hire': 'Strong Hire',
            'hire': 'Hire',
            'maybe': 'Maybe',
            'no_hire': 'No Hire',
            'strong_no_hire': 'Strong No Hire'
        }
        return recommendation_map.get(recommendation.lower(), 'Maybe')
    
    def _create_detailed_feedback(self, 
                                 resume_analysis: str, 
                                 interview_evaluation: str, 
                                 final_scoring: str) -> str:
        """Create comprehensive detailed feedback"""
        return f"""
# COMPREHENSIVE CANDIDATE EVALUATION

## RESUME ANALYSIS
{resume_analysis}

## INTERVIEW EVALUATION
{interview_evaluation}

## FINAL SCORING AND RECOMMENDATION
{final_scoring}

---
*This evaluation was generated by the AI Hiring Evaluation System using CrewAI multi-agent framework.*
        """.strip()
    
    def get_evaluation_summary(self, evaluation_result: EvaluationResult) -> Dict[str, Any]:
        """Get a summary of the evaluation result"""
        return {
            "candidate_id": evaluation_result.candidate_id,
            "evaluation_id": evaluation_result.evaluation_id,
            "overall_score": evaluation_result.overall_score,
            "recommendation": evaluation_result.recommendation,
            "criteria_scores": {
                "technical_skills": evaluation_result.criteria.technical_skills,
                "communication": evaluation_result.criteria.communication,
                "problem_solving": evaluation_result.criteria.problem_solving,
                "cultural_fit": evaluation_result.criteria.cultural_fit,
                "experience_relevance": evaluation_result.criteria.experience_relevance
            },
            "strengths": evaluation_result.strengths,
            "weaknesses": evaluation_result.weaknesses,
            "evaluated_at": evaluation_result.evaluated_at.isoformat(),
            "evaluated_by": evaluation_result.evaluated_by
        }

