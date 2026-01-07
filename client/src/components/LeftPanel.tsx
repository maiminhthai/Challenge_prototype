import React from 'react';

interface ChatMessage {
    user: string;
    text: string;
}

interface LeftPanelProps {
    messages: ChatMessage[];
    input: string;
    setInput: (value: string) => void;
    sendMessage: (e: React.FormEvent) => void;
    isRecording: boolean;
    startRecording: () => void;
    stopRecording: () => void;
    speed: number;
    batteryLevel: number;
}

const LeftPanel: React.FC<LeftPanelProps> = ({
    messages,
    input,
    setInput,
    sendMessage,
    isRecording,
    startRecording,
    stopRecording,
    speed,
    batteryLevel,
}) => {
    const getBatteryStatus = (level: number) => {
        if (level > 60) return { color: 'text-success', icon: 'bi-battery-full' };
        if (level > 20) return { color: 'text-warning', icon: 'bi-battery-half' };
        return { color: 'text-danger', icon: 'bi-battery' };
    };

    const { color, icon } = getBatteryStatus(batteryLevel);

    return (
        <div className="d-flex flex-column h-100 bg-white border-end border-light p-3">
            {/* Header: Speed and Battery */}
            <div className="d-flex justify-content-between align-items-start mb-4 text-dark">
                {/* Status Icons Left (Placeholder for P R N D) */}
                <div className="text-secondary small fw-bold">
                    P R N <span className="text-dark">D</span>
                </div>

                {/* Speed */}
                <div className="text-center">
                    <h1 className="display-1 fw-bold m-0" style={{ lineHeight: '0.8' }}>{speed}</h1>
                    <small className="text-secondary fw-bold">MPH</small>
                </div>

                {/* Battery */}
                <div className={`d-flex align-items-center ${color}`}>
                    <span className="me-1 fw-bold">{batteryLevel}%</span>
                    <i className={`bi ${icon} fs-4`}></i>
                </div>
            </div>

            <div className="border-bottom border-light mb-3"></div>

            {/* Chat History */}
            <div className="flex-grow-1 overflow-auto mb-3" style={{ border: '1px solid #dee2e6', borderRadius: '5px', padding: '10px', backgroundColor: '#f8f9fa' }}>
                {messages.map((msg, index) => (
                    <div key={index} className="text-dark mb-2">
                        <strong>{msg.user}:</strong> {msg.text}
                    </div>
                ))}
            </div>

            {/* Chat Input */}
            <form onSubmit={sendMessage} className="d-flex mb-4">
                <input
                    className="form-control me-2 bg-light text-dark border-secondary"
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                />
                <button type="submit" className="btn btn-primary">Send</button>
            </form>

            {/* Record Button */}
            <div className="d-flex justify-content-center mt-auto mb-3">
                {!isRecording ? (
                    <button
                        onClick={startRecording}
                        className="btn btn-secondary rounded-circle d-flex align-items-center justify-content-center shadow-sm"
                        style={{ width: '60px', height: '60px', fontSize: '1.5rem', border: 'none' }}
                    >
                        <i className="bi bi-mic-fill"></i>
                    </button>
                ) : (
                    <button
                        onClick={stopRecording}
                        className="btn btn-danger rounded-circle d-flex align-items-center justify-content-center shadow-sm spinning-border"
                        style={{ width: '60px', height: '60px', fontSize: '1.5rem', border: 'none' }}
                    >
                        <i className="bi bi-stop-fill"></i>
                    </button>
                )}
            </div>
        </div>
    );
};

export default LeftPanel;
