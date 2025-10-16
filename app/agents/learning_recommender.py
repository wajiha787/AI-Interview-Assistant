from crewai import Agent, Task, LLM
from typing import Dict, Any, List
import json
import re


class LearningRecommenderAgent:
    """Agent responsible for recommending specific learning resources, projects, certifications, and courses"""
    
    def __init__(self, google_api_key: str):
        self.llm = LLM(
            model="gemini-1.5-flash",
            provider="google",
            temperature=0.3,
            api_key=google_api_key
        )
        
        self.agent = Agent(
            role="Professional Learning & Development Specialist",
            goal="Recommend specific projects, certifications, courses, and learning resources tailored to individual career gaps",
            backstory="""You are a learning and development expert with deep knowledge of 
            professional certifications, online courses, bootcamps, and practical projects 
            across various industries. You stay updated with the latest learning platforms, 
            certification programs, and industry-recognized credentials. You excel at creating 
            personalized learning paths that efficiently address skill gaps and career goals.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_recommendation_task(self, gap_analysis: Dict[str, Any], profession: str, 
                                  available_time: str = "flexible") -> Task:
        """Create a task for generating learning recommendations"""
        
        gaps_summary = json.dumps(gap_analysis, indent=2)
        
        return Task(
            description=f"""
            Based on the following gap analysis for a {profession} professional, recommend specific 
            learning resources, certifications, courses, and projects to address the identified gaps:
            
            GAP ANALYSIS:
            {gaps_summary}
            
            AVAILABLE TIME: {available_time}
            
            Please provide detailed, actionable recommendations including:
            1. Recommended certifications (with providers, costs, duration, and priority)
            2. Online courses (with platforms, instructors, costs, and duration)
            3. Practical projects to build portfolio (with difficulty level and learning outcomes)
            4. Books and reading materials
            5. Communities and networking opportunities
            6. Free vs paid resources
            7. Learning path timeline (3 months, 6 months, 1 year)
            8. Budget-friendly alternatives
            
            Format your response as a detailed JSON object with the following structure:
            {{
                "certifications": [
                    {{
                        "name": "<certification_name>",
                        "provider": "<provider>",
                        "cost": "<cost_in_PKR>",
                        "duration": "<duration>",
                        "difficulty": "<beginner/intermediate/advanced>",
                        "priority": "<critical/high/medium/low>",
                        "description": "<description>",
                        "prerequisites": ["<prereq1>", "<prereq2>"],
                        "link": "<URL_if_available>",
                        "addresses_gaps": ["<gap1>", "<gap2>"]
                    }}
                ],
                "courses": [
                    {{
                        "title": "<course_title>",
                        "platform": "<platform>",
                        "instructor": "<instructor>",
                        "cost": "<cost_in_PKR>",
                        "duration": "<duration>",
                        "difficulty": "<beginner/intermediate/advanced>",
                        "priority": "<critical/high/medium/low>",
                        "description": "<description>",
                        "link": "<URL_if_available>",
                        "addresses_gaps": ["<gap1>", "<gap2>"]
                    }}
                ],
                "projects": [
                    {{
                        "title": "<project_title>",
                        "description": "<project_description>",
                        "difficulty": "<beginner/intermediate/advanced>",
                        "estimated_time": "<time>",
                        "technologies": ["<tech1>", "<tech2>"],
                        "learning_outcomes": ["<outcome1>", "<outcome2>"],
                        "priority": "<critical/high/medium/low>",
                        "addresses_gaps": ["<gap1>", "<gap2>"]
                    }}
                ],
                "books": [
                    {{
                        "title": "<book_title>",
                        "author": "<author>",
                        "type": "<technical/soft_skills/industry>",
                        "priority": "<high/medium/low>",
                        "description": "<description>",
                        "addresses_gaps": ["<gap1>", "<gap2>"]
                    }}
                ],
                "communities": [
                    {{
                        "name": "<community_name>",
                        "platform": "<platform>",
                        "type": "<forum/slack/discord/meetup>",
                        "focus": "<focus_area>",
                        "link": "<URL_if_available>"
                    }}
                ],
                "learning_paths": {{
                    "3_months": {{
                        "focus": "<focus_areas>",
                        "activities": ["<activity1>", "<activity2>"],
                        "expected_outcomes": ["<outcome1>", "<outcome2>"],
                        "estimated_cost": "<cost_in_PKR>"
                    }},
                    "6_months": {{
                        "focus": "<focus_areas>",
                        "activities": ["<activity1>", "<activity2>"],
                        "expected_outcomes": ["<outcome1>", "<outcome2>"],
                        "estimated_cost": "<cost_in_PKR>"
                    }},
                    "12_months": {{
                        "focus": "<focus_areas>",
                        "activities": ["<activity1>", "<activity2>"],
                        "expected_outcomes": ["<outcome1>", "<outcome2>"],
                        "estimated_cost": "<cost_in_PKR>"
                    }}
                }},
                "budget_breakdown": {{
                    "free_resources": ["<resource1>", "<resource2>"],
                    "low_cost": "<total_PKR>",
                    "medium_cost": "<total_PKR>",
                    "premium_path": "<total_PKR>"
                }},
                "quick_wins": ["<quick_action1>", "<quick_action2>"],
                "summary": "<overall_recommendation_summary>"
            }}
            
            Note: Provide costs in Pakistani Rupees (PKR).
            """,
            expected_output="A detailed JSON with specific, actionable learning recommendations",
            agent=self.agent
        )
    
    def extract_structured_data(self, recommendation_result: str) -> Dict[str, Any]:
        """Extract structured data from the recommendation result"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', recommendation_result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: create basic structure
                return {
                    "certifications": [],
                    "courses": [],
                    "projects": [],
                    "books": [],
                    "communities": [],
                    "learning_paths": {},
                    "budget_breakdown": {},
                    "quick_wins": [],
                    "summary": recommendation_result
                }
        except json.JSONDecodeError:
            return {
                "certifications": [],
                "courses": [],
                "projects": [],
                "books": [],
                "communities": [],
                "learning_paths": {},
                "budget_breakdown": {},
                "quick_wins": [],
                "summary": recommendation_result
            }
    
    def generate_recommendations(self, gap_analysis: Dict[str, Any], profession: str,
                                available_time: str = "flexible") -> Dict[str, Any]:
        """Main method to generate learning recommendations"""
        task = self.create_recommendation_task(gap_analysis, profession, available_time)
        
        # Execute the task
        result = self.agent.execute_task(task)
        
        # Extract structured data
        structured_data = self.extract_structured_data(result)
        
        return {
            "raw_recommendations": result,
            "structured_data": structured_data
        }

