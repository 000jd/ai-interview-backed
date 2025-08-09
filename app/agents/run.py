from livekit.agents import cli
from app.agents.interview_agent import entrypoint, prewarm_process

if __name__ == "__main__":
    cli.run_app(entrypoint, prewarm_process=prewarm_process)
