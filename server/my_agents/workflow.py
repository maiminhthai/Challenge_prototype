from agents.voice import AudioInput, VoicePipeline,  SingleAgentVoiceWorkflow
from my_agents.orchestrator_agent import orchestrator_agent
from agents import Runner, OpenAIConversationsSession

from dotenv import load_dotenv
# --- Load Environment Variables ---
load_dotenv()


session = OpenAIConversationsSession()

workflow = SingleAgentVoiceWorkflow(
    agent=orchestrator_agent,
)

voice_pipeline = VoicePipeline(workflow=workflow, stt_model="whisper-1", tts_model="tts-1")

async def get_voice_response(data):
    audio_input = AudioInput(buffer=data)
    result = await voice_pipeline.run(audio_input, session=session)
    audio_output = []
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            audio_output.append(event.data)
    return audio_output

async def get_message_response(user_message):
    return await Runner.run(orchestrator_agent, user_message, session=session)