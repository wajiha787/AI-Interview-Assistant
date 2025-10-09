from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List
import json
import re


class ScoringAgent:
    """Agent responsible for final scoring and recommendation"""
    
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            api_key=openai_api_key
        )
        
        self.agent = Agent(
            role="Senior Hiring Manager",
            goal="Provide final scoring and hiring recommendation based on comprehensive candidate evaluation",
            backstory="""You are a senior hiring manager with 20+ years of experience in 
            making critical hiring decisions. You excel at synthesizing information from 
            multiple sources (resume, interview) to make objective, data-driven hiring 
            recommendations. You consider both technical fit and cultural alignment in 
            your assessments.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_scoring_task(self, resume_analysis: Dict[str, Any], interview_evaluation: Dict[str, Any], position: str) -> Task:
        """Create a task for final scoring and recommendation"""
        return Task(
            description=f"""
            Based on the comprehensive evaluation data below, provide a final scoring and hiring recommendation for a {position} position:
            
            RESUME ANALYSIS SUMMARY:
            {json.dumps(resume_analysis.get('structured_data', {}), indent=2)}
            
            INTERVIEW EVALUATION SUMMARY:
            {json.dumps(interview_evaluation.get('structured_data', {}), indent=2)}
            
            Please provide a final assessment including:
            1. Overall score (0-10)
            2. Detailed scoring breakdown by category
            3. Final hiring recommendation (Strong Hire/Hire/Maybe/No Hire/Strong No Hire)
            4. Confidence level in the recommendation
            5. Key strengths that support the recommendation
            6. Main concerns or areas of improvement
            7. Detailed reasoning for the recommendation
            8. Suggested next steps
            
            Format your response as a detailed JSON object with the following structure:
            {{
                "overall_score": <0-10>,
                "detailed_scores": {{
                    "technical_skills": <0-10>,
                    "communication": <0-10>,
                    "problem_solving": <0-10>,
                    "cultural_fit": <0-10>,
                    "experience_relevance": <0-10>
                }},
                "recommendation": "<strong_hire/hire/maybe/no_hire/strong_no_hire>",
                "confidence": <0-1>,
                "key_strengths": ["<strength1>", "<strength2>"],
                "main_concerns": ["<concern1>", "<concern2>"],
                "detailed_reasoning": "<detailed reasoning for recommendation>",
                "next_steps": ["<step1>", "<step2>"],
                "risk_factors": ["<risk1>", "<risk2>"],
                "opportunity_factors": ["<opportunity1>", "<opportunity2>"]
            }}
            """,
            expected_output="A comprehensive final scoring and recommendation in JSON format",
            agent=self.agent
        )
    
    def extract_structured_data(self, scoring_result: str) -> Dict[str, Any]:
        """Extract structured data from the scoring result"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', scoring_result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: create basic structure
                return {
                    "overall_score": 5,
                    "detailed_scores": {
                        "technical_skills": 5,
                        "communication": 5,
                        "problem_solving": 5,
                        "cultural_fit": 5,
                        "experience_relevance": 5
                    },
                    "recommendation": "maybe",
                    "confidence": 0.5,
                    "key_strengths": [],
                    "main_concerns": [],
                    "detailed_reasoning": scoring_result,
                    "next_steps": [],
                    "risk_factors": [],
                    "opportunity_factors": []
                }
        except json.JSONDecodeError:
            return {
                "overall_score": 5,
                "detailed_scores": {
                    "technical_skills": 5,
                    "communication": 5,
                    "problem_solving": 5,
                    "cultural_fit": 5,
                    "experience_relevance": 5
                },
                "recommendation": "maybe",
                "confidence": 0.5,
                "key_strengths": [],
                "main_concerns": [],
                "detailed_reasoning": scoring_result,
                "next_steps": [],
                "risk_factors": [],
                "opportunity_factors": []
            }
    
    def generate_final_score(self, resume_analysis: Dict[str, Any], interview_evaluation: Dict[str, Any], position: str) -> Dict[str, Any]:
        """Main method to generate final score and recommendation"""
        task = self.create_scoring_task(resume_analysis, interview_evaluation, position)
        
        # Execute the task
        result = self.agent.execute_task(task)
        
        # Extract structured data
        structured_data = self.extract_structured_data(result)
        
        return {
            "raw_scoring": result,
            "structured_data": structured_data
        }

