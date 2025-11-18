from flask_socketio import SocketIO, emit
from flask import Flask
from flask_cors import CORS
from agents.workflow import agent, config

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

    # 2. Get the bot's response
    bot_response =agent.invoke({"messages": {"role": "user", "content": user_message}}, config=config)
    print(f"Bot response: {bot_response['messages'][-1].content}")

    # 3. Send the bot's response back to the user
    emit('message', {'user': 'Bot', 'text': bot_response['messages'][-1].content}, broadcast=False)


#--- Run Server ---
if __name__ == '__main__':
    socketio.run(app, debug=True)
