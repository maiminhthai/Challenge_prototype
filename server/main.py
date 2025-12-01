import numpy as np
from flask_socketio import SocketIO, emit
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import asyncio
from my_agents.workflow import get_voice_response, get_message_response
import io
import soundfile as sf

from dotenv import load_dotenv
# --- Load Environment Variables ---
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


# --- SocketIO Events ---
@socketio.on('connect')
def handle_connect():
    """Handles new client connections."""
    print('Client connected')
    emit('message', {'user': 'System', 'text': 'Welcome to the Chatbot!'}, broadcast=False)
    # Automatically send the first bot message
    emit('message', {'user': 'Bot', 'text': 'I am your real-time chat bot.'}, broadcast=False)

@socketio.on('disconnect')
def handle_disconnect():
    """Handles client disconnections."""
    print('Client disconnected')

@socketio.on('send_message')
def handle_user_message(data):
    """
    Handles a message sent from the React client.
    'data' is expected to be {'text': 'user message content'}
    """
    user_message = data.get('text', '')
    print(f"Received message: {user_message}")

    # 2. Get the bot's response4
    try:
        loop = asyncio.new_event_loop()
        bot_response = loop.run_until_complete(
            get_message_response(user_message)
        )
        print(f"Bot response: {bot_response.final_output}")
        # 3. Send the bot's response back to the user
        emit('message', {'user': 'Bot', 'text': bot_response.final_output}, broadcast=False)
    except RuntimeError:
        print("RuntimeError: Event loop is closed")
        emit('message', {'user': 'Bot', 'text': "Sorry, I'm having trouble responding right now."}, broadcast=False)


@socketio.on('send_audio')
def handle_audio(data):
    """
    Handles audio data sent from the client.
    Echoes the audio back to the client.
    """
    print("Received audio data")
    try:
        audio_file = io.BytesIO(data)
        audio_array, sample_rate = sf.read(audio_file, dtype='float32')
        loop = asyncio.new_event_loop()
        response = loop.run_until_complete(
            get_voice_response(audio_array)
        )
        # Ensure response is a flat numpy array
        if isinstance(response, list) and len(response) > 0:
            response = np.concatenate(response)
        elif isinstance(response, list):
            response = np.array([], dtype=np.float32)
            
        print(f"Response shape: {response.shape}")

        out_buffer = io.BytesIO()
        sf.write(out_buffer, response, sample_rate, format='WAV')
        bot_response = out_buffer.getvalue()
        
        emit('audio', bot_response, broadcast=False)

    except Exception as e:
        print(f"Error processing audio: {e}")
        emit('message', {'user': 'System', 'text': f"Error processing audio: {e}"}, broadcast=False)


#--- Run Server ---
if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
