from crewai import Agent, Task, LLM
from typing import Dict, Any, List
import json
import re


class CVGapAnalyzerAgent:
    """Agent responsible for analyzing CVs and identifying gaps, weaknesses, and areas for improvement"""
    
    def __init__(self, google_api_key: str):
        self.llm = LLM(
            model="gemini-1.5-flash",
            provider="google",
            temperature=0.1,
            api_key=google_api_key
        )
        
        self.agent = Agent(
            role="Senior Career Development Advisor",
            goal="Analyze CVs to identify skill gaps, missing certifications, and areas for professional growth",
            backstory="""You are an expert career advisor with 20+ years of experience in 
            career development and talent assessment. You excel at identifying gaps in 
            professional profiles and understanding what skills, certifications, and experiences 
            are needed for career advancement in various fields. You provide actionable, 
            specific recommendations for professional growth.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_gap_analysis_task(self, cv_content: str, profession: str) -> Task:
        """Create a task for CV gap analysis"""
        return Task(
            description=f"""
            Analyze the following CV for a {profession} professional and identify gaps, weaknesses, 
            and areas for improvement:
            
            CV CONTENT:
            {cv_content}
            
            Please provide a comprehensive gap analysis including:
            1. Current skill level assessment
            2. Missing technical skills for the profession
            3. Lacking certifications and credentials
            4. Experience gaps (types of projects, roles, industries)
            5. Soft skills that need development
            6. Educational gaps or additional learning needed
            7. Industry-specific knowledge gaps
            8. Leadership and management experience gaps (if applicable)
            9. Overall readiness for the profession
            10. Priority areas for improvement (ranked)
            
            Format your response as a detailed JSON object with the following structure:
            {{
                "current_level": "<junior/mid-level/senior/expert>",
                "overall_readiness_score": <0-100>,
                "technical_skills_gaps": [
                    {{"skill": "<skill_name>", "importance": "<critical/high/medium/low>", "current_level": "<none/beginner/intermediate/advanced>", "required_level": "<beginner/intermediate/advanced/expert>"}}
                ],
                "missing_certifications": [
                    {{"certification": "<cert_name>", "importance": "<critical/high/medium/low>", "provider": "<provider>", "typical_duration": "<duration>"}}
                ],
                "experience_gaps": [
                    {{"gap_type": "<project_type/role/industry>", "description": "<description>", "importance": "<critical/high/medium/low>"}}
                ],
                "soft_skills_gaps": [
                    {{"skill": "<skill_name>", "importance": "<critical/high/medium/low>", "development_suggestions": "<suggestions>"}}
                ],
                "educational_gaps": [
                    {{"area": "<area>", "type": "<degree/course/bootcamp>", "importance": "<critical/high/medium/low>"}}
                ],
                "strengths": ["<strength1>", "<strength2>"],
                "priority_improvements": [
                    {{"area": "<area>", "priority": <1-10>, "rationale": "<rationale>", "estimated_time": "<time>"}}
                ],
                "career_stage_analysis": "<detailed analysis of where they are vs where they should be>",
                "recommendations_summary": "<summary of key recommendations>"
            }}
            """,
            expected_output="A detailed JSON analysis of CV gaps with specific recommendations",
            agent=self.agent
        )
    
    def extract_structured_data(self, analysis_result: str) -> Dict[str, Any]:
        """Extract structured data from the analysis result"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', analysis_result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: create basic structure
                return {
                    "current_level": "unknown",
                    "overall_readiness_score": 50,
                    "technical_skills_gaps": [],
                    "missing_certifications": [],
                    "experience_gaps": [],
                    "soft_skills_gaps": [],
                    "educational_gaps": [],
                    "strengths": [],
                    "priority_improvements": [],
                    "career_stage_analysis": analysis_result,
                    "recommendations_summary": "Unable to parse detailed recommendations"
                }
        except json.JSONDecodeError:
            return {
                "current_level": "unknown",
                "overall_readiness_score": 50,
                "technical_skills_gaps": [],
                "missing_certifications": [],
                "experience_gaps": [],
                "soft_skills_gaps": [],
                "educational_gaps": [],
                "strengths": [],
                "priority_improvements": [],
                "career_stage_analysis": analysis_result,
                "recommendations_summary": "Unable to parse detailed recommendations"
            }
    
    def analyze_cv_gaps(self, cv_content: str, profession: str) -> Dict[str, Any]:
        """Main method to analyze CV gaps"""
        task = self.create_gap_analysis_task(cv_content, profession)
        
        # Execute the task
        result = self.agent.execute_task(task)
        
        # Extract structured data
        structured_data = self.extract_structured_data(result)
        
        return {
            "raw_analysis": result,
            "structured_data": structured_data
        }

