from agents.voice import AudioInput, VoicePipeline,  SingleAgentVoiceWorkflow
from my_agents.orchestrator_agent import orchestrator_agent
from agents import Runner, OpenAIConversationsSession
from openai import OpenAI, AsyncOpenAI
import io
from dotenv import load_dotenv
# --- Load Environment Variables ---
load_dotenv()

client = OpenAI()

session = OpenAIConversationsSession()

async def get_voice_response(data):
    audio_file = io.BytesIO(data)
    audio_file.name = "audio.wav"
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )

    run_result = await Runner.run(orchestrator_agent, transcription, session=session)
    text = run_result.final_output

    response = client.audio.speech.create(
        model="tts-1",
        voice="coral",
        input=text,
        response_format="wav",
    )
    audio = response.content
    return text, audio

async def get_message_response(message):
    run_result = await Runner.run(orchestrator_agent, message, session=session)
    text = run_result.final_output
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="coral",
        input=text,
        response_format="wav",
    )
    audio = response.content
    return text, audio