from crewai import Agent, Task, LLM
from typing import Dict, Any, List
import json
import re


class InteractiveInterviewerAgent:
    """Agent responsible for conducting interactive interviews based on profession"""
    
    def __init__(self, google_api_key: str):
        self.llm = LLM(
            model="gemini-1.5-flash",
            provider="google",
            temperature=0.7,
            api_key=google_api_key
        )
        
        self.agent = Agent(
            role="Senior Technical Interviewer",
            goal="Conduct professional, adaptive interviews tailored to candidate's profession and experience level",
            backstory="""You are an experienced interviewer with expertise across multiple 
            domains including software engineering, data science, product management, and more. 
            You excel at asking relevant, challenging questions that assess both technical 
            knowledge and practical application. You adapt your questioning based on candidate 
            responses and maintain a professional, encouraging demeanor throughout interviews.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def generate_interview_questions(self, profession: str, experience_level: str, 
                                    focus_areas: List[str] = None, 
                                    difficulty: str = "mixed") -> Dict[str, Any]:
        """Generate interview questions based on profession and experience level"""
        
        focus_areas_str = ", ".join(focus_areas) if focus_areas else "general professional competencies"
        
        task = Task(
            description=f"""
            Generate a comprehensive set of interview questions for a {experience_level} level 
            {profession} professional.
            
            FOCUS AREAS: {focus_areas_str}
            DIFFICULTY LEVEL: {difficulty}
            
            Generate 15-20 questions covering:
            1. Technical knowledge questions (40%)
            2. Problem-solving scenarios (30%)
            3. Behavioral questions (20%)
            4. Situational questions (10%)
            
            Format your response as a JSON object:
            {{
                "questions": [
                    {{
                        "id": <question_number>,
                        "question": "<question_text>",
                        "type": "<technical/problem_solving/behavioral/situational>",
                        "difficulty": "<easy/medium/hard>",
                        "focus_area": "<focus_area>",
                        "time_limit_minutes": <time>,
                        "evaluation_criteria": ["<criteria1>", "<criteria2>"],
                        "follow_up_questions": ["<follow_up1>", "<follow_up2>"]
                    }}
                ],
                "interview_structure": {{
                    "total_questions": <number>,
                    "estimated_duration_minutes": <time>,
                    "difficulty_distribution": {{"easy": <count>, "medium": <count>, "hard": <count>}},
                    "recommended_order": "<order_strategy>"
                }},
                "introduction": "<interviewer_introduction>",
                "closing": "<interview_closing_message>"
            }}
            """,
            expected_output="A structured JSON with interview questions and metadata",
            agent=self.agent
        )
        
        result = self.agent.execute_task(task)
        return self._extract_json(result)
    
    def evaluate_answer(self, question: Dict[str, Any], answer: str, 
                       profession: str) -> Dict[str, Any]:
        """Evaluate a candidate's answer to a question"""
        
        question_text = question.get('question', '')
        evaluation_criteria = question.get('evaluation_criteria', [])
        
        task = Task(
            description=f"""
            Evaluate the following answer to an interview question for a {profession} position:
            
            QUESTION: {question_text}
            
            EVALUATION CRITERIA: {', '.join(evaluation_criteria)}
            
            CANDIDATE'S ANSWER:
            {answer}
            
            Provide a detailed evaluation in JSON format:
            {{
                "score": <0-10>,
                "strengths": ["<strength1>", "<strength2>"],
                "weaknesses": ["<weakness1>", "<weakness2>"],
                "missing_points": ["<point1>", "<point2>"],
                "technical_accuracy": <0-10>,
                "clarity_of_explanation": <0-10>,
                "depth_of_knowledge": <0-10>,
                "practical_application": <0-10>,
                "detailed_feedback": "<comprehensive_feedback>",
                "improvement_suggestions": ["<suggestion1>", "<suggestion2>"],
                "follow_up_needed": <true/false>,
                "recommended_follow_up": "<follow_up_question_if_needed>"
            }}
            """,
            expected_output="A detailed JSON evaluation of the candidate's answer",
            agent=self.agent
        )
        
        result = self.agent.execute_task(task)
        return self._extract_json(result)
    
    def generate_adaptive_question(self, previous_answers: List[Dict[str, Any]], 
                                  profession: str, focus_area: str) -> Dict[str, Any]:
        """Generate an adaptive follow-up question based on previous answers"""
        
        answers_summary = json.dumps(previous_answers[-3:], indent=2) if previous_answers else "No previous answers"
        
        task = Task(
            description=f"""
            Based on the candidate's previous answers, generate a targeted follow-up question 
            for a {profession} position, focusing on {focus_area}.
            
            PREVIOUS ANSWERS SUMMARY:
            {answers_summary}
            
            Generate a question that:
            1. Probes deeper into areas where the candidate showed weakness
            2. Validates strengths demonstrated in previous answers
            3. Explores practical application of concepts discussed
            
            Format as JSON:
            {{
                "question": "<question_text>",
                "rationale": "<why_this_question>",
                "type": "<technical/problem_solving/behavioral/situational>",
                "difficulty": "<easy/medium/hard>",
                "evaluation_criteria": ["<criteria1>", "<criteria2>"],
                "time_limit_minutes": <time>
            }}
            """,
            expected_output="An adaptive follow-up question in JSON format",
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
                return {"raw_text": text, "error": "No JSON found"}
        except json.JSONDecodeError:
            return {"raw_text": text, "error": "Invalid JSON"}

