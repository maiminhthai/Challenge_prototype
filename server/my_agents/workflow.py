from my_agents.graph import builder
from langgraph.checkpoint.sqlite import SqliteSaver
from openai import OpenAI
import os
import io
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_voice_response(data, session_id):
    # Speech to Text
    audio_file = io.BytesIO(data)
    audio_file.name = "audio.wav"
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    # Get Response
    with SqliteSaver.from_conn_string("db/conversations.db") as memory:
        app = builder.compile(checkpointer=memory)
        messages = [{"role": "user", "content": transcription}]
        config = {"configurable": {"thread_id": session_id}}
        result = app.invoke({"messages": messages}, config)

    text = result["messages"][-1].content
    # Text to Speech
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format="wav",
    )
    audio = response.content
    return text, audio

def get_message_response(message, session_id):
    # Get Response
    with SqliteSaver.from_conn_string("db/conversations.db") as memory:
        app = builder.compile(checkpointer=memory)
        messages = [{"role": "user", "content": message}]
        config = {"configurable": {"thread_id": session_id}}
        result = app.invoke({"messages": messages}, config)

    text = result["messages"][-1].content
    # Text to Speech
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format="wav",
    )
    audio = response.content
    return text, audio