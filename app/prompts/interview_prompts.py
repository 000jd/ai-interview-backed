# =============================================================================
# File: app/prompts/interview_prompts.py - Prompt Management System
# =============================================================================

from typing import Dict, List, Optional
from enum import Enum

class InterviewPhase(Enum):
    INTRODUCTION = "introduction"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    CLOSING = "closing"
    COMPLETED = "completed"

class PromptManager:
    """Centralized prompt management system"""
    
    def __init__(self):
        self.base_instructions = self._load_base_instructions()
        self.position_prompts = self._load_position_prompts()
        self.behavioral_questions = self._load_behavioral_questions()
        self.follow_up_prompts = self._load_follow_up_prompts()
    
    def _load_base_instructions(self) -> str:
        return """You are an AI interviewer conducting a professional job interview. Follow these guidelines:

                1. INTRODUCTION PHASE: 
                - Welcome the candidate warmly
                - Ask for their name and confirm the position they're applying for
                - Brief overview of the interview process (15-20 minutes)
                - Ask about their background and interest in the role

                2. TECHNICAL PHASE:
                - Ask 3-5 relevant technical questions based on their position
                - Listen for depth of knowledge and problem-solving approach
                - Ask follow-up questions for clarification
                - Score responses on technical competency

                3. BEHAVIORAL PHASE:
                - Ask 3-4 behavioral questions using STAR method
                - Focus on teamwork, leadership, problem-solving, and adaptability
                - Evaluate communication skills and cultural fit

                4. CLOSING PHASE:
                - Summarize key points discussed
                - Ask if candidate has questions
                - Explain next steps in the process
                - Thank them for their time

                SCORING GUIDELINES:
                - 5: Exceptional - Clear examples, deep understanding, excellent communication
                - 4: Strong - Good examples, solid understanding, clear communication
                - 3: Adequate - Basic understanding, meets minimum requirements
                - 2: Below Average - Limited understanding, unclear responses
                - 1: Poor - Inadequate knowledge, concerning responses

                IMPORTANT RULES:
                - Be conversational and professional
                - Allow natural conversation flow
                - Ask follow-up questions when needed
                - Keep responses concise but thorough
                - Use the provided functions to record information
                - Maintain consistency in scoring criteria"""

    def _load_position_prompts(self) -> Dict[str, Dict[str, List[str]]]:
        return {
            "software_engineer": {
                "technical": [
                    "Describe your approach to debugging a complex issue in production",
                    "How would you design a system to handle 1 million concurrent users?",
                    "What's your experience with different programming paradigms?",
                    "Tell me about a challenging technical problem you solved recently",
                    "How do you ensure code quality and maintainability in your projects?"
                ],
                "skills_focus": ["problem_solving", "system_design", "code_quality", "debugging", "scalability"]
            },
            "data_scientist": {
                "technical": [
                    "Walk me through your approach to a new machine learning project",
                    "How do you handle missing or inconsistent data in your datasets?",
                    "Explain the bias-variance tradeoff and how you manage it",
                    "What's your process for feature selection and engineering?",
                    "How do you validate and interpret your model results?"
                ],
                "skills_focus": ["data_analysis", "machine_learning", "statistics", "data_cleaning", "model_validation"]
            },
            "product_manager": {
                "technical": [
                    "How do you prioritize features when resources are limited?",
                    "Walk me through your process for gathering user requirements",
                    "How do you measure product success and user satisfaction?",
                    "Tell me about a product decision you had to make with incomplete information",
                    "How do you work with engineering teams to balance technical debt and new features?"
                ],
                "skills_focus": ["prioritization", "user_research", "metrics", "stakeholder_management", "technical_understanding"]
            },
            "designer": {
                "technical": [
                    "Walk me through your design process from concept to final product",
                    "How do you conduct user research and incorporate feedback?",
                    "Tell me about a design challenge where you had to balance user needs and business constraints",
                    "How do you ensure your designs are accessible to all users?",
                    "What's your approach to collaborating with developers during implementation?"
                ],
                "skills_focus": ["design_process", "user_research", "accessibility", "collaboration", "problem_solving"]
            },
            "marketing_manager": {
                "technical": [
                    "How do you develop and execute a go-to-market strategy?",
                    "What metrics do you use to measure campaign effectiveness?",
                    "Tell me about a time you had to pivot a marketing strategy based on data",
                    "How do you approach customer segmentation and targeting?",
                    "What's your experience with marketing automation and analytics tools?"
                ],
                "skills_focus": ["strategy", "analytics", "customer_understanding", "campaign_management", "tools_proficiency"]
            }
        }

    def _load_behavioral_questions(self) -> List[str]:
        return [
            "Tell me about a time you had to work with a difficult team member. How did you handle it?",
            "Describe a situation where you had to learn something completely new in a short timeframe",
            "Give me an example of when you had to make a decision with incomplete information",
            "Tell me about a time you failed at something. What did you learn?",
            "Describe a situation where you had to convince someone to see things your way",
            "Tell me about a time you had to meet a very tight deadline. How did you prioritize?",
            "Give me an example of when you went above and beyond what was expected",
            "Describe a time when you had to give constructive feedback to a colleague",
            "Tell me about a project you're particularly proud of and your role in its success",
            "Describe a situation where you had to adapt to significant changes at work"
        ]

    def _load_follow_up_prompts(self) -> List[str]:
        return [
            "Can you give me more specific details about that?",
            "What was the outcome of that situation?",
            "How did you measure success in that case?",
            "What would you do differently if faced with a similar situation?",
            "Can you walk me through your thought process?",
            "What challenges did you encounter during that process?",
            "How did others react to your approach?",
            "What did you learn from that experience?"
        ]

    def get_system_prompt(
        self, 
        position: str, 
        candidate_name: str,
        company_name: Optional[str] = None
    ) -> str:
        """Generate complete system prompt for the interview"""
        
        company_info = f" at {company_name}" if company_name else ""
        
        position_specific = ""
        if position.lower().replace(" ", "_") in self.position_prompts:
            position_data = self.position_prompts[position.lower().replace(" ", "_")]
            skills = ", ".join(position_data["skills_focus"])
            position_specific = f"""
                POSITION-SPECIFIC FOCUS for {position}:
                Key skills to assess: {skills}
                Pay special attention to their experience and knowledge in these areas.
                """

        return f"""
{self.base_instructions}

{position_specific}

INTERVIEW CONTEXT:
- Candidate: {candidate_name}
- Position: {position}{company_info}
- Duration: Aim for 15-20 minutes total
- Current phase: Introduction (you will advance through phases automatically)

Remember to use the provided functions to:
- record_candidate_info() - Capture basic details
- record_question() - Log each question asked
- record_response() - Score and log candidate responses
- add_interviewer_note() - Add observations
- advance_interview_phase() - Move to next phase
- complete_interview() - Finish with summary

Start with a warm welcome and introduction!"""

    def get_technical_questions(self, position: str) -> List[str]:
        """Get technical questions for specific position"""
        position_key = position.lower().replace(" ", "_")
        if position_key in self.position_prompts:
            return self.position_prompts[position_key]["technical"]
        return self.position_prompts["software_engineer"]["technical"]  # Default fallback

    def get_behavioral_questions(self, count: int = 5) -> List[str]:
        """Get random behavioral questions"""
        import random
        return random.sample(self.behavioral_questions, min(count, len(self.behavioral_questions)))

    def get_follow_up_prompt(self) -> str:
        """Get random follow-up prompt"""
        import random
        return random.choice(self.follow_up_prompts)

# Global prompt manager instance
prompt_manager = PromptManager()
