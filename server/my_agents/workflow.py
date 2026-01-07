from my_agents.orchestrator_agent import orchestrator_agent
from agents import Runner, trace
from agents.extensions.memory import AdvancedSQLiteSession
from openai import OpenAI
import io
from dotenv import load_dotenv
# --- Load Environment Variables ---
load_dotenv()

client = OpenAI()

session = AdvancedSQLiteSession(
    session_id="user_123",
    db_path="db/conversations.db",
    create_tables=True
)

async def get_voice_response(data):
    # Speech to Text
    audio_file = io.BytesIO(data)
    audio_file.name = "audio.wav"
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )
    # Get Response
    with trace("Car assistant") as t:
        run_result = await Runner.run(orchestrator_agent, transcription, session=session)
    await session.store_run_usage(run_result)
    text = run_result.final_output
    # Text to Speech
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format="wav",
    )
    audio = response.content
    return text, audio

async def get_message_response(message):
    # Get Response
    with trace("Car assistant") as t:
        run_result = await Runner.run(orchestrator_agent, message, session=session)
    await session.store_run_usage(run_result)
    text = run_result.final_output
    # # Text to Speech
    # response = client.audio.speech.create(
    #     model="tts-1",
    #     voice="alloy",
    #     input=text,
    #     response_format="wav",
    # )
    #audio = response.content
    return text