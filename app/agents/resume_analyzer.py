from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List
import json
import re


class ResumeAnalyzerAgent:
    """Agent responsible for analyzing resumes and extracting key information"""
    
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            api_key=openai_api_key
        )
        
        self.agent = Agent(
            role="Senior HR Resume Analyst",
            goal="Analyze resumes thoroughly and extract structured information about candidates",
            backstory="""You are an expert HR professional with 15+ years of experience in 
            resume analysis and candidate evaluation. You excel at identifying key skills, 
            experience patterns, and potential red flags in resumes. You provide detailed, 
            objective analysis that helps hiring teams make informed decisions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_analysis_task(self, resume_content: str, position: str) -> Task:
        """Create a task for resume analysis"""
        return Task(
            description=f"""
            Analyze the following resume for a {position} position:
            
            RESUME CONTENT:
            {resume_content}
            
            Please provide a comprehensive analysis including:
            1. Years of relevant experience
            2. Key technical skills and their proficiency levels
            3. Educational background and certifications
            4. Work experience with focus on relevant roles
            5. Notable achievements and projects
            6. Potential red flags or concerns
            7. Overall assessment of candidate fit for the position
            
            Format your response as a detailed JSON object with the following structure:
            {{
                "experience_years": <number>,
                "skills": [
                    {{"name": "<skill_name>", "proficiency": "<beginner/intermediate/advanced/expert>", "evidence": "<supporting evidence>"}}
                ],
                "education": [
                    {{"degree": "<degree>", "institution": "<institution>", "year": <year>, "relevance": "<high/medium/low>"}}
                ],
                "work_experience": [
                    {{"company": "<company>", "position": "<position>", "duration": "<duration>", "relevance": "<high/medium/low>", "achievements": ["<achievement1>", "<achievement2>"]}}
                ],
                "certifications": ["<cert1>", "<cert2>"],
                "achievements": ["<achievement1>", "<achievement2>"],
                "red_flags": ["<flag1>", "<flag2>"],
                "overall_assessment": "<detailed assessment>",
                "strengths": ["<strength1>", "<strength2>"],
                "weaknesses": ["<weakness1>", "<weakness2>"]
            }}
            """,
            expected_output="A detailed JSON analysis of the resume with structured information",
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
                    "experience_years": 0,
                    "skills": [],
                    "education": [],
                    "work_experience": [],
                    "certifications": [],
                    "achievements": [],
                    "red_flags": [],
                    "overall_assessment": analysis_result,
                    "strengths": [],
                    "weaknesses": []
                }
        except json.JSONDecodeError:
            return {
                "experience_years": 0,
                "skills": [],
                "education": [],
                "work_experience": [],
                "certifications": [],
                "achievements": [],
                "red_flags": [],
                "overall_assessment": analysis_result,
                "strengths": [],
                "weaknesses": []
            }
    
    def analyze_resume(self, resume_content: str, position: str) -> Dict[str, Any]:
        """Main method to analyze a resume"""
        task = self.create_analysis_task(resume_content, position)
        
        # Execute the task
        result = self.agent.execute_task(task)
        
        # Extract structured data
        structured_data = self.extract_structured_data(result)
        
        return {
            "raw_analysis": result,
            "structured_data": structured_data
        }

