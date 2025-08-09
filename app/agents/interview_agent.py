import asyncio
import logging
from typing import Dict, Any
from livekit import agents
from livekit.agents import Agent, AgentSession, function_tool, RunContext
from livekit.plugins import deepgram, cartesia, google, silero, elevenlabs
from app.core.logging_config import setup_logging
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from datetime import datetime
import json

from app.prompts.interview_prompts import prompt_manager, InterviewPhase
from app.core.config import settings

setup_logging()
logger = logging.getLogger("app")

class InterviewData:
    """Interview session data management"""
    def __init__(self):
        self.candidate_name = ""
        self.position = ""
        self.current_phase = InterviewPhase.INTRODUCTION
        self.questions_asked = []
        self.responses = []
        self.notes = []
        self.technical_score = 0
        self.behavioral_score = 0
        self.question_count = 0
        self.start_time = datetime.now()

class InterviewAgent(Agent):
    """AI Interview Agent with enhanced capabilities"""
    
    def __init__(self, interview_config: Dict[str, Any]):
        self.interview_data = InterviewData()
        self.max_questions_per_phase = 5
        self.interview_config = interview_config
        
        # Get system prompt
        system_prompt = prompt_manager.get_system_prompt(
            position=interview_config.get("position", "Software Engineer"),
            candidate_name=interview_config.get("candidate_name", "Candidate"),
            company_name=interview_config.get("company_name")
        )
        
        super().__init__(instructions=system_prompt)
    
    @function_tool()
    async def record_candidate_info(self, ctx: RunContext, name: str, position: str):
        """Record candidate's basic information"""
        logger.info(f"Recording candidate info - Name: {name}, Position: {position}")
        self.interview_data.candidate_name = name
        self.interview_data.position = position
        return f"Thank you, {name}! I've noted you're interviewing for the {position} position. Let's begin!"
    
    @function_tool()
    async def record_question(self, ctx: RunContext, question: str):
        """Record a question that was asked"""
        logger.info(f"Recording question: {question}")
        self.interview_data.questions_asked.append({
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "phase": self.interview_data.current_phase.value
        })
        self.interview_data.question_count += 1
        return "Question recorded."
    
    @function_tool()
    async def record_response(self, ctx: RunContext, response_summary: str, quality_score: int):
        """Record and score candidate's response"""
        if not 1 <= quality_score <= 5:
            return "Score must be between 1 and 5."
        
        logger.info(f"Recording response with score {quality_score}")
        self.interview_data.responses.append({
            "response_summary": response_summary,
            "quality_score": quality_score,
            "timestamp": datetime.now().isoformat(),
            "phase": self.interview_data.current_phase.value
        })
        
        # Update phase-specific scores
        if self.interview_data.current_phase == InterviewPhase.TECHNICAL:
            self.interview_data.technical_score += quality_score
        elif self.interview_data.current_phase == InterviewPhase.BEHAVIORAL:
            self.interview_data.behavioral_score += quality_score
        
        return f"Response recorded with score {quality_score}/5."
    
    @function_tool()
    async def add_interviewer_note(self, ctx: RunContext, note: str):
        """Add interviewer observation note"""
        logger.info(f"Adding note: {note}")
        self.interview_data.notes.append({
            "note": note,
            "timestamp": datetime.now().isoformat(),
            "phase": self.interview_data.current_phase.value
        })
        return "Note added."
    
    @function_tool()
    async def advance_interview_phase(self, ctx: RunContext):
        """Move to the next interview phase"""
        current = self.interview_data.current_phase
        
        if current == InterviewPhase.INTRODUCTION:
            self.interview_data.current_phase = InterviewPhase.TECHNICAL
            self.interview_data.question_count = 0
            return "Moving to technical questions. I'll now ask about your technical skills and experience."
        
        elif current == InterviewPhase.TECHNICAL:
            self.interview_data.current_phase = InterviewPhase.BEHAVIORAL
            self.interview_data.question_count = 0
            return "Great! Now let's discuss some behavioral questions to understand how you work in teams and handle challenges."
        
        elif current == InterviewPhase.BEHAVIORAL:
            self.interview_data.current_phase = InterviewPhase.CLOSING
            return "Thank you for those insights. Let me wrap up with some final questions."
        
        elif current == InterviewPhase.CLOSING:
            self.interview_data.current_phase = InterviewPhase.COMPLETED
            return "Interview completed successfully!"
        
        return "Interview phase already at maximum."
    
    @function_tool()
    async def get_interview_status(self, ctx: RunContext):
        """Get current interview status"""
        duration = datetime.now() - self.interview_data.start_time
        return {
            "candidate_name": self.interview_data.candidate_name,
            "position": self.interview_data.position,
            "current_phase": self.interview_data.current_phase.value,
            "duration_minutes": int(duration.total_seconds() / 60),
            "questions_asked": len(self.interview_data.questions_asked),
            "technical_score": self.interview_data.technical_score,
            "behavioral_score": self.interview_data.behavioral_score
        }
    
    @function_tool()
    async def complete_interview(self, ctx: RunContext, overall_impression: str):
        """Complete the interview with final assessment"""
        logger.info("Completing interview")
        self.interview_data.current_phase = InterviewPhase.COMPLETED
        
        # Calculate averages
        tech_responses = [r for r in self.interview_data.responses if r.get("phase") == "technical"]
        behavioral_responses = [r for r in self.interview_data.responses if r.get("phase") == "behavioral"]
        
        avg_technical = sum(r["quality_score"] for r in tech_responses) / len(tech_responses) if tech_responses else 0
        avg_behavioral = sum(r["quality_score"] for r in behavioral_responses) / len(behavioral_responses) if behavioral_responses else 0
        
        summary = {
            "candidate_name": self.interview_data.candidate_name,
            "position": self.interview_data.position,
            "duration_minutes": int((datetime.now() - self.interview_data.start_time).total_seconds() / 60),
            "questions_asked": len(self.interview_data.questions_asked),
            "avg_technical_score": round(avg_technical, 2),
            "avg_behavioral_score": round(avg_behavioral, 2),
            "overall_impression": overall_impression,
            "detailed_data": {
                "questions": self.interview_data.questions_asked,
                "responses": self.interview_data.responses,
                "notes": self.interview_data.notes
            }
        }
        
        logger.info(f"Interview completed: {summary}")
        return f"Interview completed! Thank you for your time, {self.interview_data.candidate_name}. We'll be in touch soon with next steps."

def prewarm_process(proc: agents.JobProcess):
    """Prewarm models for better performance"""
    logger.info("Prewarming AI models...")
    proc.userdata["vad"] = silero.VAD.load()
    logger.info("VAD model loaded")

async def entrypoint(ctx: agents.JobContext):
    """Main entrypoint for the interview agent"""
    logger.info("Starting AI Interview Agent")
    
    interview_config = {
        "candidate_name": "Candidate",
        "position": "Software Engineer",
        "company_name": "Your Company"
    }
    
    agent = InterviewAgent(interview_config)
    
    session = AgentSession(

        stt=deepgram.STT(
            model="nova-2-conversationalai",
            language="en",
            smart_format=True,
            interim_results=True,
            profanity_filter=False,
        ),
        
        llm=google.LLM(
            model="gemini-1.5-flash",
            api_key=settings.GOOGLE_API_KEY,
            temperature=0.7,
            max_output_tokens=1024,
        ),
        
        tts=elevenlabs.TTS(
            api_key=settings.ELEVENLABS_API_KEY,
            voice_id="pNInz6obpgDQGcFmaJgB",  
            model="eleven_multilingual_v2",
            streaming=True
        ),
        
        vad=ctx.proc.userdata.get("vad", silero.VAD.load()),
        
        turn_detection=MultilingualModel(),
    )
    
    await session.start(room=ctx.room, agent=agent)

    welcome_msg = "Hello! Welcome to your interview today. I'm excited to speak with you and learn more about your background. Could you please start by telling me your name and confirming the position you're interviewing for?"
