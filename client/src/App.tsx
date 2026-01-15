import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import './App.css';
import { WavRecorder } from './WavRecorder';
import Context from './contexts/Context';
import TopBar from './components/TopBar';
import BottomBar from './components/BottomBar';
import LeftPanel from './components/LeftPanel';
import Map from './components/Map';

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
  const [batteryLevel, setBatteryLevel] = useState<number>(100);
  const [speed, setSpeed] = useState<number>(63);
  const [destination, setDestination] = useState<string>('');


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

    socket.on('destination', (des: string) => {
      setDestination(des);
    });

    return () => {
      socket.off('message');
      socket.off('audio');
      socket.off('destination');
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
    setInput('');
    setIsScenariosOpen(false);
  };

  const heavyTrafficMessage = () => {
    const heavyTrafficMessage = 'Heavy traffic incoming, help him drive efficiently';
    socket.emit('send_message', { text: 'SYSTEM: ' + heavyTrafficMessage });
    setInput('');
    setIsScenariosOpen(false);
  };

  const lowTrafficMessage = () => {
    const lowTrafficMessage = 'Low traffic incoming, help him drive efficiently';
    socket.emit('send_message', { text: 'SYSTEM: ' + lowTrafficMessage });
    setInput('');
    setIsScenariosOpen(false);
  };

  const lastBatteryWarningTime = useRef<number>(0);

  // Monitor battery level and trigger warning at 20% or less (throttled to 5s)
  useEffect(() => {
    const now = Date.now();
    if (batteryLevel <= 20 && now - lastBatteryWarningTime.current > 5000) {
      lowBatteryMessage();
      lastBatteryWarningTime.current = now;
    }
  }, [batteryLevel]);

  return (
    <Context.Provider value={{ batteryLevel, setBatteryLevel }}>
      <div className="container-fluid vh-100 d-flex flex-column bg-dark text-white p-0">
        <TopBar
          isScenariosOpen={isScenariosOpen}
          setIsScenariosOpen={setIsScenariosOpen}
          lowBatteryMessage={lowBatteryMessage}
          heavyTrafficMessage={heavyTrafficMessage}
          lowTrafficMessage={lowTrafficMessage}
          batteryLevel={batteryLevel}
          setBatteryLevel={setBatteryLevel}
        />

        {/* Main Content Area */}
        <div className="row flex-grow-1 m-0 overflow-hidden">
          {/* Left Panel - Chat & Record */}
          <div className="col-4 p-0 h-100 border-end border-secondary">
            <LeftPanel
              messages={messages}
              input={input}
              setInput={setInput}
              sendMessage={sendMessage}
              isRecording={isRecording}
              startRecording={startRecording}
              stopRecording={stopRecording}
              speed={speed}
              batteryLevel={batteryLevel}
            />
          </div>

          {/* Right Panel - Map */}
          <div className="col p-0 h-100 d-flex align-items-center justify-content-center bg-dark">
            <Map destination={destination} />
          </div>
        </div>

        <BottomBar />
      </div>
    </Context.Provider>
  );
};

export default App;
