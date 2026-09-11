"""LiveKit Agents entrypoint: Success bud oral interview coach.

Realtime duplex voice via Gemini Live (GOOGLE_API_KEY). No ElevenLabs,
and no Google Cloud STT/TTS service-account path.
"""

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession
from livekit.plugins import google

from instructions import GREETING_INSTRUCTIONS, SUCCESS_BUD_INSTRUCTIONS

load_dotenv(".env")
load_dotenv(".env.local", override=True)

AGENT_NAME = "success-bud-oral"

# Gemini Developer API Live model. Pin 2.5 native audio: generate_reply
# works here, unlike gemini-3.1-flash-live-preview. Native audio picks
# language from the conversation; French is pinned in instructions.
GEMINI_LIVE_MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"

# Firm interviewer timbre. Swap to Charon / Aoede / Puck if needed.
GEMINI_LIVE_VOICE = "Kore"


class SuccessBudOral(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SUCCESS_BUD_INSTRUCTIONS)


server = AgentServer()


@server.rtc_session(agent_name=AGENT_NAME)
async def success_bud_oral(ctx: agents.JobContext) -> None:
    session = AgentSession(
        llm=google.realtime.RealtimeModel(
            model=GEMINI_LIVE_MODEL,
            voice=GEMINI_LIVE_VOICE,
            temperature=0.7,
        ),
    )

    await session.start(
        room=ctx.room,
        agent=SuccessBudOral(),
    )

    await session.generate_reply(instructions=GREETING_INSTRUCTIONS)


if __name__ == "__main__":
    agents.cli.run_app(server)
