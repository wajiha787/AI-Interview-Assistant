from crewai import Agent, Task, LLM
from typing import Dict, Any, List
import json
import re


class PerformanceAnalyzerAgent:
    """Agent responsible for analyzing interview performance and identifying weak areas"""
    
    def __init__(self, google_api_key: str):
        self.llm = LLM(
            model="gemini-1.5-flash",
            provider="google",
            temperature=0.1,
            api_key=google_api_key
        )
        
        self.agent = Agent(
            role="Senior Performance Assessment Specialist",
            goal="Analyze interview performance comprehensively and identify specific areas for improvement",
            backstory="""You are an expert in performance assessment and candidate evaluation 
            with deep understanding of competency frameworks and skill development. You excel at 
            identifying patterns in interview responses, pinpointing specific weaknesses, and 
            providing actionable feedback for improvement. You are thorough, objective, and 
            focused on helping candidates grow.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def analyze_interview_performance(self, interview_data: Dict[str, Any], 
                                     profession: str) -> Dict[str, Any]:
        """Analyze complete interview performance"""
        
        interview_summary = json.dumps(interview_data, indent=2)
        
        task = Task(
            description=f"""
            Analyze the complete interview performance for a {profession} position based on the 
            following interview data:
            
            INTERVIEW DATA:
            {interview_summary}
            
            Provide a comprehensive performance analysis including:
            1. Overall performance score (0-100)
            2. Category-wise scoring (technical, problem-solving, communication, etc.)
            3. Detailed strengths and weaknesses
            4. Specific topics/areas where candidate struggled
            5. Topics for focused practice before next interview
            6. Question types that need improvement
            7. Behavioral patterns observed
            8. Readiness for next interview level
            
            Format your response as a detailed JSON object:
            {{
                "overall_score": <0-100>,
                "performance_level": "<poor/below_average/average/good/excellent>",
                "category_scores": {{
                    "technical_knowledge": <0-100>,
                    "problem_solving": <0-100>,
                    "communication": <0-100>,
                    "analytical_thinking": <0-100>,
                    "practical_application": <0-100>,
                    "depth_of_understanding": <0-100>
                }},
                "strengths": [
                    {{
                        "area": "<area>",
                        "description": "<description>",
                        "evidence": "<evidence_from_interview>"
                    }}
                ],
                "weaknesses": [
                    {{
                        "area": "<area>",
                        "severity": "<critical/high/medium/low>",
                        "description": "<description>",
                        "evidence": "<evidence_from_interview>",
                        "impact": "<how_this_affects_overall_performance>"
                    }}
                ],
                "weak_topics": [
                    {{
                        "topic": "<topic_name>",
                        "current_level": "<none/beginner/intermediate/advanced>",
                        "required_level": "<beginner/intermediate/advanced/expert>",
                        "priority": "<critical/high/medium/low>",
                        "practice_recommendations": ["<recommendation1>", "<recommendation2>"]
                    }}
                ],
                "question_type_analysis": {{
                    "technical": {{"score": <0-100>, "notes": "<notes>"}},
                    "problem_solving": {{"score": <0-100>, "notes": "<notes>"}},
                    "behavioral": {{"score": <0-100>, "notes": "<notes>"}},
                    "situational": {{"score": <0-100>, "notes": "<notes>"}}
                }},
                "behavioral_patterns": [
                    {{
                        "pattern": "<pattern_description>",
                        "frequency": "<always/often/sometimes/rarely>",
                        "impact": "<positive/neutral/negative>",
                        "suggestions": "<improvement_suggestions>"
                    }}
                ],
                "preparation_plan": {{
                    "immediate_focus": ["<topic1>", "<topic2>"],
                    "short_term_goals": ["<goal1>", "<goal2>"],
                    "practice_exercises": [
                        {{
                            "topic": "<topic>",
                            "exercise": "<exercise_description>",
                            "estimated_time": "<time>",
                            "priority": "<critical/high/medium/low>"
                        }}
                    ],
                    "study_resources": [
                        {{
                            "topic": "<topic>",
                            "resource": "<resource_name>",
                            "type": "<video/article/course/book>",
                            "link": "<URL_if_available>"
                        }}
                    ],
                    "estimated_preparation_time": "<time_needed>"
                }},
                "next_interview_readiness": {{
                    "ready": <true/false>,
                    "confidence_level": "<low/medium/high>",
                    "recommended_wait_time": "<time>",
                    "areas_to_practice": ["<area1>", "<area2>"],
                    "expected_improvement": "<percentage>"
                }},
                "detailed_feedback": "<comprehensive_feedback>",
                "motivational_message": "<encouraging_message>"
            }}
            """,
            expected_output="A comprehensive JSON analysis of interview performance",
            agent=self.agent
        )
        
        result = self.agent.execute_task(task)
        return self._parse_analysis(result)
    
    def generate_practice_plan(self, weak_areas: List[Dict[str, Any]], 
                              profession: str, 
                              available_time: str = "1 week") -> Dict[str, Any]:
        """Generate a focused practice plan for weak areas"""
        
        weak_areas_summary = json.dumps(weak_areas, indent=2)
        
        task = Task(
            description=f"""
            Create a focused practice plan to address the following weak areas for a {profession} 
            professional. The candidate has {available_time} to prepare.
            
            WEAK AREAS:
            {weak_areas_summary}
            
            Create a structured practice plan with:
            1. Daily study schedule
            2. Specific topics to cover each day
            3. Practice questions and exercises
            4. Self-assessment checkpoints
            5. Resources for each topic
            6. Mock interview questions to practice
            
            Format as JSON:
            {{
                "total_duration": "{available_time}",
                "daily_schedule": [
                    {{
                        "day": <day_number>,
                        "date": "<suggested_date>",
                        "focus_topics": ["<topic1>", "<topic2>"],
                        "activities": [
                            {{
                                "time": "<time_slot>",
                                "activity": "<activity_description>",
                                "duration": "<duration>",
                                "resources": ["<resource1>", "<resource2>"]
                            }}
                        ],
                        "practice_questions": ["<question1>", "<question2>"],
                        "self_assessment": "<assessment_task>",
                        "daily_goal": "<goal>"
                    }}
                ],
                "mock_interview_questions": [
                    {{
                        "question": "<question>",
                        "topic": "<topic>",
                        "difficulty": "<easy/medium/hard>",
                        "time_limit": "<time>"
                    }}
                ],
                "progress_checkpoints": [
                    {{
                        "checkpoint": "<when>",
                        "topics_to_master": ["<topic1>", "<topic2>"],
                        "assessment_method": "<method>",
                        "success_criteria": "<criteria>"
                    }}
                ],
                "final_preparation": {{
                    "last_day_activities": ["<activity1>", "<activity2>"],
                    "quick_review_topics": ["<topic1>", "<topic2>"],
                    "confidence_boosters": ["<tip1>", "<tip2>"]
                }},
                "success_tips": ["<tip1>", "<tip2>"],
                "estimated_improvement": "<percentage>"
            }}
            """,
            expected_output="A detailed practice plan in JSON format",
            agent=self.agent
        )
        
        result = self.agent.execute_task(task)
        return self._extract_json(result)
    
    def _parse_analysis(self, text: str) -> Dict[str, Any]:
        """Parse analysis result"""
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                data['raw_analysis'] = text
                return data
            else:
                return {
                    "overall_score": 50,
                    "raw_analysis": text,
                    "error": "No JSON structure found"
                }
        except json.JSONDecodeError:
            return {
                "overall_score": 50,
                "raw_analysis": text,
                "error": "Invalid JSON"
            }
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON from text"""
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"raw_text": text, "error": "No JSON found"}
        except json.JSONDecodeError:
            return {"raw_text": text, "error": "Invalid JSON"}

