from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List
import json
import re


class InterviewEvaluatorAgent:
    """Agent responsible for evaluating interview transcripts"""
    
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            api_key=openai_api_key
        )
        
        self.agent = Agent(
            role="Senior Interview Evaluator",
            goal="Evaluate interview performance and assess candidate communication, problem-solving, and cultural fit",
            backstory="""You are an expert interview evaluator with extensive experience in 
            behavioral and technical interviews. You excel at analyzing communication patterns, 
            problem-solving approaches, and cultural fit indicators from interview transcripts. 
            You provide objective, detailed assessments that help hiring teams make informed decisions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_evaluation_task(self, transcript_content: str, position: str, resume_summary: str = "") -> Task:
        """Create a task for interview evaluation"""
        return Task(
            description=f"""
            Evaluate the following interview transcript for a {position} position:
            
            RESUME SUMMARY (for context):
            {resume_summary}
            
            INTERVIEW TRANSCRIPT:
            {transcript_content}
            
            Please provide a comprehensive evaluation including:
            1. Communication skills assessment
            2. Problem-solving ability demonstration
            3. Technical knowledge application
            4. Cultural fit indicators
            5. Leadership and teamwork examples
            6. Areas of concern or red flags
            7. Overall interview performance
            
            Format your response as a detailed JSON object with the following structure:
            {{
                "communication_score": <0-10>,
                "problem_solving_score": <0-10>,
                "technical_knowledge_score": <0-10>,
                "cultural_fit_score": <0-10>,
                "leadership_score": <0-10>,
                "questions_answered_well": ["<question1>", "<question2>"],
                "questions_struggled_with": ["<question1>", "<question2>"],
                "key_insights": ["<insight1>", "<insight2>"],
                "red_flags": ["<flag1>", "<flag2>"],
                "strengths_demonstrated": ["<strength1>", "<strength2>"],
                "areas_for_improvement": ["<area1>", "<area2>"],
                "overall_assessment": "<detailed assessment>",
                "recommendation_notes": "<notes for final recommendation>"
            }}
            """,
            expected_output="A detailed JSON evaluation of the interview performance",
            agent=self.agent
        )
    
    def extract_structured_data(self, evaluation_result: str) -> Dict[str, Any]:
        """Extract structured data from the evaluation result"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', evaluation_result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: create basic structure
                return {
                    "communication_score": 5,
                    "problem_solving_score": 5,
                    "technical_knowledge_score": 5,
                    "cultural_fit_score": 5,
                    "leadership_score": 5,
                    "questions_answered_well": [],
                    "questions_struggled_with": [],
                    "key_insights": [],
                    "red_flags": [],
                    "strengths_demonstrated": [],
                    "areas_for_improvement": [],
                    "overall_assessment": evaluation_result,
                    "recommendation_notes": ""
                }
        except json.JSONDecodeError:
            return {
                "communication_score": 5,
                "problem_solving_score": 5,
                "technical_knowledge_score": 5,
                "cultural_fit_score": 5,
                "leadership_score": 5,
                "questions_answered_well": [],
                "questions_struggled_with": [],
                "red_flags": [],
                "strengths_demonstrated": [],
                "areas_for_improvement": [],
                "overall_assessment": evaluation_result,
                "recommendation_notes": ""
            }
    
    def evaluate_interview(self, transcript_content: str, position: str, resume_summary: str = "") -> Dict[str, Any]:
        """Main method to evaluate an interview transcript"""
        task = self.create_evaluation_task(transcript_content, position, resume_summary)
        
        # Execute the task
        result = self.agent.execute_task(task)
        
        # Extract structured data
        structured_data = self.extract_structured_data(result)
        
        return {
            "raw_evaluation": result,
            "structured_data": structured_data
        }

