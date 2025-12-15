import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import './App.css';
import { WavRecorder } from './WavRecorder';


interface ChatMessage {
  user: string;
  text: string;
}

const socket = io('http://127.0.0.1:5000');

const App: React.FC = () => {

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState<string>('');
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [isScenariosOpen, setIsScenariosOpen] = useState<boolean>(false);


  useEffect(() => {
    socket.on('message', (message: ChatMessage) => {
      setMessages((prevMessages) => [...prevMessages, message]);
    });

    socket.on('audio', (audioData: ArrayBuffer) => {
      console.log("Received audio back from server");
      const blob = new Blob([audioData], { type: 'audio/wav' });
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

  // Use a ref to hold the WavRecorder instance
  const wavRecorderRef = useRef<WavRecorder | null>(null);

  const startRecording = async () => {
    try {
      const recorder = new WavRecorder();
      await recorder.start();
      wavRecorderRef.current = recorder;
      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
    }
  };

  const stopRecording = async () => {
    if (wavRecorderRef.current && isRecording) {
      const audioBlob = await wavRecorderRef.current.stop();
      setIsRecording(false);

      // Emit the blob directly; socket.io client handles it
      socket.emit('send_audio', audioBlob);
      console.log("Sent audio to server");

      // Reset ref
      wavRecorderRef.current = null;
    }
  };

  const lowBatteryMessage = () => {
    const lowBatteryMessage = 'User battery is running low, help him find a charging station';
    socket.emit('send_message', { text: 'SYSTEM: ' + lowBatteryMessage });
    setMessages((prevMessages) => [...prevMessages, { user: 'SYSTEM', text: lowBatteryMessage }]);
    setInput('');
    setIsScenariosOpen(false);
  };

  const heavyTrafficMessage = () => {
    const heavyTrafficMessage = 'Heavy traffic incoming, help him drive efficiently';
    socket.emit('send_message', { text: 'SYSTEM: ' + heavyTrafficMessage });
    setMessages((prevMessages) => [...prevMessages, { user: 'SYSTEM', text: heavyTrafficMessage }]);
    setInput('');
    setIsScenariosOpen(false);
  };

  const lowTrafficMessage = () => {
    const lowTrafficMessage = 'Low traffic incoming, help him drive efficiently';
    socket.emit('send_message', { text: 'SYSTEM: ' + lowTrafficMessage });
    setMessages((prevMessages) => [...prevMessages, { user: 'SYSTEM', text: lowTrafficMessage }]);
    setInput('');
    setIsScenariosOpen(false);
  };

  return (
    <div className="container-fluid vh-100 d-flex flex-column bg-dark text-white">
      {/* Top Bar with Dropdowns */}
      <div className="row p-3 border-bottom border-secondary">
        <div className="col d-flex justify-content-start gap-3">
          {/* Chat Dropdown */}
          <div className="dropdown chat-dropdown-hover">
            <button className="btn btn-secondary dropdown-toggle" type="button" id="chatDropdown" aria-expanded="false">
              Chat
            </button>
            <div className="dropdown-menu p-0" aria-labelledby="chatDropdown" style={{ width: '400px', backgroundColor: '#1e1e1e', border: '1px solid #444' }}>
              <div className='chat-box' style={{ height: '400px', overflowY: 'scroll', padding: '10px' }}>
                {messages.map((msg, index) => (
                  <div key={index} className="text-white mb-1">
                    <strong>{msg.user}:</strong> {msg.text}
                  </div>
                ))}
              </div>
              <form onSubmit={sendMessage} className='p-2 border-top border-secondary d-flex'>
                <input
                  className='form-control me-2 bg-dark text-white border-secondary'
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type a message..."
                />
                <button type="submit" className="btn btn-primary">Send</button>
              </form>
            </div>
          </div>

          {/* Scenarios Dropdown */}
          <div className="dropdown">
            <button
              className="btn btn-secondary dropdown-toggle"
              type="button"
              id="scenariosDropdown"
              onClick={() => setIsScenariosOpen(!isScenariosOpen)}
              aria-expanded={isScenariosOpen}
            >
              Scenarios
            </button>
            <ul className={`dropdown-menu ${isScenariosOpen ? 'show' : ''}`} aria-labelledby="scenariosDropdown">
              <li><button onClick={lowBatteryMessage} className="dropdown-item">Low Battery</button></li>
              <li><button onClick={heavyTrafficMessage} className="dropdown-item">Heavy Traffic</button></li>
              <li><button onClick={lowTrafficMessage} className="dropdown-item">Low Traffic</button></li>
            </ul>
          </div>
        </div>
      </div>

      {/* Main Content - Centered Record Button */}
      <div className="row flex-grow-1 align-items-center justify-content-center">
        <div className="col-auto text-center">
          {!isRecording ? (
            <button
              onClick={startRecording}
              className="btn btn-success rounded-circle d-flex align-items-center justify-content-center shadow-lg"
              style={{ width: '150px', height: '150px', fontSize: '3rem', border: '5px solid #28a745' }}
            >
              <i className="bi bi-mic-fill"></i>
            </button>
          ) : (
            <button
              onClick={stopRecording}
              className="btn btn-danger rounded-circle d-flex align-items-center justify-content-center shadow-lg spinning-border"
              style={{ width: '150px', height: '150px', fontSize: '3rem', border: '5px solid #dc3545' }}
            >
              <i className="bi bi-stop-fill"></i>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
