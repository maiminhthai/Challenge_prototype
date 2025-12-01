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
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    socket.on('message', (message: ChatMessage) => {
      setMessages((prevMessages) => [...prevMessages, message]);
    });

    socket.on('audio', (audioData: ArrayBuffer) => {
      console.log("Received audio back from server");
      const blob = new Blob([audioData], { type: 'audio/webm' });
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      audio.play();
    });

    return () => {
      socket.off('message');
      socket.off('audio');
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

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        // Emit the blob directly; socket.io client handles it
        socket.emit('send_audio', audioBlob);
        console.log("Sent audio to server");
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      // Stop all tracks to release the microphone
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  return (
    <div className='container'>
      <h2>Car-Assistant</h2>
      <div className='chat-box' style={{ overflowY: 'scroll' }}>
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
      </form>
      <div style={{ marginTop: '10px' }}>
        {!isRecording ? (
          <button onClick={startRecording} style={{ backgroundColor: '#4CAF50' }}>Record Audio</button>
        ) : (
          <button onClick={stopRecording} style={{ backgroundColor: '#f44336' }}>Stop Recording</button>
        )}
      </div>
    </div>
  );
};

export default App;
