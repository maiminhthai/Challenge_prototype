from flask_socketio import emit
from extensions import socketio, set_current_sid
from flask import Flask, request
from flask_cors import CORS
import os
from my_agents.workflow import get_voice_response, get_message_response
from my_agents.memory_manager import extract_and_store_memory

os.makedirs("db", exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
socketio.init_app(app, cors_allowed_origins="http://localhost:5173")


# --- SocketIO Events ---
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    try:
        emit('message', {'user': 'Bot', 'text': "Client connected"}, broadcast=False)
    except Exception as e:
        print("Exception: ", e)
        emit('message', {'user': 'Bot', 'text': "Sorry, I'm having trouble responding right now."}, broadcast=False)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    session_id = request.sid
    try:
        extract_and_store_memory(session_id)
        print("Memory extraction completed.")
    except Exception as e:
        print(f"Error extracting memory: {e}")

@socketio.on('send_message')
def handle_user_message(data):
    user_message = data.get('text', '')
    print(f"Received message: {user_message}")

    session_id = request.sid
    set_current_sid(session_id)
    try:
        bot_response, audio = get_message_response(user_message, session_id)
        print(f"Bot response: {bot_response}")
        emit('message', {'user': 'Bot', 'text': bot_response}, broadcast=False)
        emit('audio', audio, broadcast=False)
    except Exception as e:
        print("Exception: ", e)
        emit('message', {'user': 'Bot', 'text': "Sorry, I'm having trouble responding right now."}, broadcast=False)


@socketio.on('send_audio')
def handle_audio(data):
    print("Received audio data")
    session_id = request.sid
    set_current_sid(session_id)
    try:
        bot_response, audio = get_voice_response(data, session_id)
        emit('message', {'user': 'Bot', 'text': bot_response}, broadcast=False)
        emit('audio', audio, broadcast=False)
    except Exception as e:
        print(f"Error processing audio: {e}")
        emit('message', {'user': 'Bot', 'text': "Sorry, I'm having trouble processing your audio right now."}, broadcast=False)


#--- Run Server ---
if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
