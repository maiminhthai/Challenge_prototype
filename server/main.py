from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import uvicorn
from extensions import sio
from my_agents.workflow import get_voice_response, get_message_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

# --- SocketIO Events ---
@sio.event
async def connect(sid, environ, auth):
    """Handles new client connections."""
    print(f'Client {sid} connected')
    try:
        await sio.emit('message', {'user': 'Bot', 'text': "Client connected"}, to=sid)
    except Exception as e:
        print("Exception: ", e)
        await sio.emit('message', {'user': 'Bot', 'text': "Sorry, I'm having trouble responding right now."}, to=sid)

@sio.event
async def disconnect(sid):
    """Handles client disconnections."""
    print(f'Client {sid} disconnected')

@sio.on('send_message')
async def handle_user_message(sid, data):
    """
    Handles a message sent from the React client.
    'data' is expected to be {'text': 'user message content'}
    """
    user_message = data.get('text', '')
    print(f"Received message: {user_message}")

    try:
        bot_response, audio = await get_message_response(user_message)
        print(f"Bot response: {bot_response}")
        
        await sio.emit('audio', audio, to=sid)
        await sio.emit('message', {'user': 'Bot', 'text': bot_response}, to=sid)
    except Exception as e:
        print("Exception: ", e)
        await sio.emit('message', {'user': 'Bot', 'text': "Sorry, I'm having trouble responding right now."}, to=sid)


@sio.on('send_audio')
async def handle_audio(sid, data):
    """
    Handles audio data sent from the client.
    """
    print("Received audio data")
    try:
        bot_response, audio = await get_voice_response(data)
        await sio.emit('message', {'user': 'Bot', 'text': bot_response}, to=sid)
        await sio.emit('audio', audio, to=sid)
    except Exception as e:
        print(f"Error processing audio: {e}")
        await sio.emit('message', {'user': 'System', 'text': f"Error processing audio: {e}"}, to=sid)


#--- Run Server ---
if __name__ == '__main__':
    uvicorn.run("main:socket_app", host="127.0.0.1", port=5000, reload=True)
