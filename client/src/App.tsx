import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import './App.css';


interface ChatMessage {
  user: string;
  text: string;
}

const socket = io('http://localhost:5000');

const App: React.FC = () => {

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState<string>('');
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [status, setStatus] = useState<string>("Disconnected");
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    if (!socket) return;

    socket.on('connect', () => {
      setStatus("Connected");
    });
    socket.on('disconnect', () => {
      setStatus("Disconnected");
    });
    socket.on('message', (message: ChatMessage) => {
      setMessages((prevMessages) => [...prevMessages, message]);
    });

    return () => {
      socket.off('message');
      socket.off('connect');
      socket.off('disconnect');
    };
  }, []);

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      socket.emit('send_message', { text: input });
      setMessages((prevMessages) => [...prevMessages, { user: 'You', text: input }]);
      setInput('');
    }
  };

  return (
    <div className='container'>
      <h2>Car-Assistant</h2>
      <div className='chat-box' style={{ overflowY: 'scroll'}}>
        {messages.map((msg, index) => (
          <div key={index}>
            <strong>{msg.user}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage} id='text-form'>
        <input
          className='chat-messages'
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={status === 'Disconnected'}
          style={{ backgroundColor: isRecording ? '#d9534f' : '#5cb85c', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '5px' }}
        >
          {isRecording ? '🛑 Stop Streaming' : '🎙️ Start Streaming'}
        </button>
      </form>
    </div>
  );
};

export default App;
