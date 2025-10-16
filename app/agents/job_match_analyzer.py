from crewai import Agent, Task, LLM
from typing import Dict, Any, List, Optional
import json
import re


class JobMatchAnalyzerAgent:
    """Agent responsible for analyzing job descriptions and matching against user profiles"""
    
    def __init__(self, google_api_key: str):
        self.llm = LLM(
            model="gemini-1.5-flash",
            provider="google",
            temperature=0.2,
            api_key=google_api_key
        )
        
        self.agent = Agent(
            role="Senior Talent Acquisition & Job Matching Specialist",
            goal="Analyze job descriptions and assess candidate fit based on their profile, experience, and skills",
            backstory="""You are an expert recruiter and talent acquisition specialist with 15+ years 
            of experience in matching candidates to job requirements. You excel at parsing job descriptions, 
            identifying key requirements, and providing honest assessments of candidate fit. You understand 
            what skills are critical vs nice-to-have, and can provide actionable advice on how candidates 
            can improve their chances for specific roles.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def analyze_job_fit(self, job_description: str, cv_data: Optional[Dict[str, Any]] = None,
                       user_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze how well a candidate fits a job description
        
        Args:
            job_description: The job posting text
            cv_data: Optional CV analysis data from previous analysis
            user_profile: Optional user profile information
        """
        
        # Prepare candidate profile summary
        if cv_data:
            candidate_summary = f"""
            CANDIDATE PROFILE:
            - Profession: {cv_data.get('profession', 'Not specified')}
            - Current Level: {cv_data.get('current_level', 'Unknown')}
            - Overall Readiness Score: {cv_data.get('overall_readiness_score', 0)}/100
            - Strengths: {', '.join(cv_data.get('strengths', []))}
            - Technical Skills Gaps: {json.dumps(cv_data.get('technical_skills_gaps', []), indent=2)}
            - Experience Gaps: {json.dumps(cv_data.get('experience_gaps', []), indent=2)}
            - Missing Certifications: {json.dumps(cv_data.get('missing_certifications', []), indent=2)}
            """
        elif user_profile:
            candidate_summary = f"""
            CANDIDATE PROFILE:
            - Name: {user_profile.get('name', 'Not specified')}
            - Profession: {user_profile.get('profession', 'Not specified')}
            - Experience Level: {user_profile.get('experience_level', 'Not specified')}
            """
        else:
            candidate_summary = "CANDIDATE PROFILE: No CV or profile data provided. Analysis will be based solely on job requirements."
        
        task = Task(
            description=f"""
            Analyze the following job description and assess the candidate's fit for this role:
            
            JOB DESCRIPTION:
            {job_description}
            
            {candidate_summary}
            
            Provide a comprehensive job fit analysis including:
            1. Job role and seniority level identification
            2. Key required skills and qualifications extracted from job description
            3. Nice-to-have skills and qualifications
            4. Candidate eligibility score (0-100)
            5. Matching skills (what candidate has that job requires)
            6. Missing critical skills (must-have skills candidate lacks)
            7. Missing preferred skills (nice-to-have skills candidate lacks)
            8. Experience level match assessment
            9. Specific recommendations to improve candidacy
            10. Estimated preparation time needed
            11. Overall hiring probability (low/medium/high)
            12. Detailed rationale for the assessment
            
            Format your response as a JSON object:
            {{
                "job_analysis": {{
                    "job_title": "<extracted_job_title>",
                    "company": "<company_name_if_mentioned>",
                    "seniority_level": "<junior/mid-level/senior/lead/executive>",
                    "employment_type": "<full-time/part-time/contract>",
                    "location": "<location_if_mentioned>",
                    "salary_range": "<salary_if_mentioned>"
                }},
                "required_skills": [
                    {{
                        "skill": "<skill_name>",
                        "category": "<technical/soft/domain/tool>",
                        "importance": "<critical/high/medium>",
                        "years_required": "<years_if_mentioned>"
                    }}
                ],
                "preferred_skills": [
                    {{
                        "skill": "<skill_name>",
                        "category": "<technical/soft/domain/tool>",
                        "importance": "<medium/low>"
                    }}
                ],
                "required_qualifications": [
                    {{"qualification": "<qualification>", "type": "<education/certification/experience>"}}
                ],
                "eligibility_assessment": {{
                    "overall_fit_score": <0-100>,
                    "skills_match_percentage": <0-100>,
                    "experience_match_percentage": <0-100>,
                    "education_match_percentage": <0-100>,
                    "hiring_probability": "<low/medium/high>",
                    "confidence_level": "<low/medium/high>"
                }},
                "matching_qualifications": [
                    {{
                        "qualification": "<what_matches>",
                        "strength": "<strong/moderate/weak>",
                        "notes": "<additional_context>"
                    }}
                ],
                "missing_critical_skills": [
                    {{
                        "skill": "<skill_name>",
                        "gap_severity": "<critical/high/medium>",
                        "current_level": "<none/beginner/intermediate>",
                        "required_level": "<intermediate/advanced/expert>",
                        "estimated_learning_time": "<time_estimate>"
                    }}
                ],
                "missing_preferred_skills": [
                    {{
                        "skill": "<skill_name>",
                        "impact_on_candidacy": "<medium/low>",
                        "estimated_learning_time": "<time_estimate>"
                    }}
                ],
                "improvement_recommendations": [
                    {{
                        "area": "<area_to_improve>",
                        "priority": <1-10>,
                        "action_items": ["<action1>", "<action2>"],
                        "estimated_time": "<time_to_improve>",
                        "resources": ["<resource1>", "<resource2>"]
                    }}
                ],
                "preparation_timeline": {{
                    "minimum_time_needed": "<time>",
                    "recommended_time": "<time>",
                    "intensive_preparation": "<description>",
                    "part_time_preparation": "<description>"
                }},
                "application_advice": {{
                    "should_apply_now": <true/false>,
                    "readiness_percentage": <0-100>,
                    "key_points_to_highlight": ["<point1>", "<point2>"],
                    "resume_tips": ["<tip1>", "<tip2>"],
                    "cover_letter_focus_areas": ["<area1>", "<area2>"],
                    "interview_preparation_focus": ["<focus1>", "<focus2>"]
                }},
                "detailed_analysis": "<comprehensive_analysis_and_rationale>",
                "next_steps": ["<step1>", "<step2>", "<step3>"]
            }}
            """,
            expected_output="A detailed JSON analysis of job fit with specific recommendations and action items",
            agent=self.agent
        )
        
        result = self.agent.execute_task(task)
        return self._extract_json(result)
    
    def extract_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """Extract and structure job requirements from a job description"""
        
        task = Task(
            description=f"""
            Extract and structure all requirements from the following job description:
            
            JOB DESCRIPTION:
            {job_description}
            
            Extract and organize:
            1. Job title and level
            2. All technical skills mentioned
            3. All soft skills mentioned
            4. Educational requirements
            5. Experience requirements (years and types)
            6. Certifications mentioned
            7. Tools and technologies
            8. Responsibilities and duties
            
            Format as JSON:
            {{
                "job_title": "<title>",
                "seniority_level": "<level>",
                "technical_skills": ["<skill1>", "<skill2>"],
                "soft_skills": ["<skill1>", "<skill2>"],
                "education_required": ["<requirement1>"],
                "experience_required": {{
                    "years": "<years>",
                    "types": ["<type1>", "<type2>"]
                }},
                "certifications": ["<cert1>", "<cert2>"],
                "tools_and_technologies": ["<tool1>", "<tool2>"],
                "key_responsibilities": ["<resp1>", "<resp2>"]
            }}
            """,
            expected_output="Structured JSON of job requirements",
            agent=self.agent
        )
        
        result = self.agent.execute_task(task)
        return self._extract_json(result)
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON from text response"""
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {
                    "raw_text": text,
                    "error": "No JSON found in response",
                    "eligibility_assessment": {
                        "overall_fit_score": 50,
                        "hiring_probability": "medium"
                    }
                }
        except json.JSONDecodeError as e:
            return {
                "raw_text": text,
                "error": f"Invalid JSON: {str(e)}",
                "eligibility_assessment": {
                    "overall_fit_score": 50,
                    "hiring_probability": "medium"
                }
            }

