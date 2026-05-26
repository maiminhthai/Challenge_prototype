from flask_socketio import emit
from extensions import socketio
from flask import Flask, request
from flask_cors import CORS
import asyncio
from my_agents.workflow import get_voice_response, get_message_response
from my_agents.memory_manager import extract_and_store_memory


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
socketio.init_app(app, cors_allowed_origins="http://localhost:5173")


# --- SocketIO Events ---
@socketio.on('connect')
def handle_connect():
    """Handles new client connections."""
    print('Client connected')
    try:
        emit('message', {'user': 'Bot', 'text': "Client connected"}, broadcast=False)
    except Exception as e:
        print("Exception: ", e)
        emit('message', {'user': 'Bot', 'text': "Sorry, I'm having trouble responding right now."}, broadcast=False)

@socketio.on('disconnect')
def handle_disconnect():
    """Handles client disconnections."""
    print('Client disconnected')
    session_id = request.sid
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(extract_and_store_memory(session_id))
        print("Memory extraction completed.")
    except Exception as e:
        print(f"Error extracting memory: {e}")

@socketio.on('send_message')
def handle_user_message(data):
    """
    Handles a message sent from the React client.
    'data' is expected to be {'text': 'user message content'}
    """
    user_message = data.get('text', '')
    print(f"Received message: {user_message}")

    session_id = request.sid
    try:
        loop = asyncio.new_event_loop()
        bot_response, audio = loop.run_until_complete(
            get_message_response(user_message, session_id)
        )
        print(f"Bot response: {bot_response}")
        # 3. Send the bot's response back to the user
        emit('audio', audio, broadcast=False)
        emit('message', {'user': 'Bot', 'text': bot_response}, broadcast=False)
    except Exception as e:
        print("Exception: ", e)
        emit('message', {'user': 'Bot', 'text': "Sorry, I'm having trouble responding right now."}, broadcast=False)


@socketio.on('send_audio')
def handle_audio(data):
    """
    Handles audio data sent from the client.
    Echoes the audio back to the client.
    """
    print("Received audio data")
    session_id = request.sid
    try:
        loop = asyncio.new_event_loop()
        bot_response, audio = loop.run_until_complete(
            get_voice_response(data, session_id)
        )
        emit('message', {'user': 'Bot', 'text': bot_response}, broadcast=False)
        emit('audio', audio, broadcast=False)
    except Exception as e:
        print(f"Error processing audio: {e}")
        emit('message', {'user': 'System', 'text': f"Error processing audio: {e}"}, broadcast=False)


#--- Run Server ---
if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
