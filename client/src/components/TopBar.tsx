import React, { useState } from 'react';

interface TopBarProps {
    isScenariosOpen: boolean;
    setIsScenariosOpen: (isOpen: boolean) => void;
    lowBatteryMessage: () => void;
    heavyTrafficMessage: () => void;
    lowTrafficMessage: () => void;
    batteryLevel: number;
    setBatteryLevel: (level: number) => void;
    speed: number;
    setSpeed: (speed: number) => void;
    temperature: number;
    setTemperature: (temp: number) => void;
}

const TopBar: React.FC<TopBarProps> = ({
    isScenariosOpen,
    setIsScenariosOpen,
    lowBatteryMessage,
    heavyTrafficMessage,
    lowTrafficMessage,
    batteryLevel,
    setBatteryLevel,
    speed,
    setSpeed,
    temperature,
    setTemperature,
}) => {
    const [isBatteryOpen, setIsBatteryOpen] = useState(false);
    const [isSpeedOpen, setIsSpeedOpen] = useState(false);
    const [isTempOpen, setIsTempOpen] = useState(false);

    return (
        <div className="row p-3 border-bottom border-secondary m-0">
            <div className="col d-flex justify-content-start gap-3">
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

                {/* Battery Dropdown */}
                <div className="dropdown">
                    <button
                        className="btn btn-secondary dropdown-toggle"
                        type="button"
                        id="batteryDropdown"
                        onClick={() => setIsBatteryOpen(!isBatteryOpen)}
                        aria-expanded={isBatteryOpen}
                    >
                        Battery
                    </button>
                    <div className={`dropdown-menu p-3 ${isBatteryOpen ? 'show' : ''}`} aria-labelledby="batteryDropdown" style={{ backgroundColor: '#1e1e1e', border: '1px solid #444', minWidth: '200px' }}>
                        <label htmlFor="batteryRange" className="form-label text-white">Level: {batteryLevel}%</label>
                        <input
                            type="range"
                            className="form-range"
                            id="batteryRange"
                            min="0"
                            max="100"
                            value={batteryLevel}
                            onChange={(e) => setBatteryLevel(Number(e.target.value))}
                        />
                    </div>
                </div>

                {/* Speed Dropdown */}
                <div className="dropdown">
                    <button
                        className="btn btn-secondary dropdown-toggle"
                        type="button"
                        id="speedDropdown"
                        onClick={() => setIsSpeedOpen(!isSpeedOpen)}
                        aria-expanded={isSpeedOpen}
                    >
                        Speed
                    </button>
                    <div className={`dropdown-menu p-3 ${isSpeedOpen ? 'show' : ''}`} aria-labelledby="speedDropdown" style={{ backgroundColor: '#1e1e1e', border: '1px solid #444', minWidth: '200px' }}>
                        <label htmlFor="speedRange" className="form-label text-white">Speed: {speed} km/h</label>
                        <input
                            type="range"
                            className="form-range"
                            id="speedRange"
                            min="0"
                            max="120"
                            value={speed}
                            onChange={(e) => setSpeed(Number(e.target.value))}
                        />
                    </div>
                </div>

                {/* Temperature Dropdown */}
                <div className="dropdown">
                    <button
                        className="btn btn-secondary dropdown-toggle"
                        type="button"
                        id="tempDropdown"
                        onClick={() => setIsTempOpen(!isTempOpen)}
                        aria-expanded={isTempOpen}
                    >
                        Temp
                    </button>
                    <div className={`dropdown-menu p-3 ${isTempOpen ? 'show' : ''}`} aria-labelledby="tempDropdown" style={{ backgroundColor: '#1e1e1e', border: '1px solid #444', minWidth: '200px' }}>
                        <label htmlFor="tempRange" className="form-label text-white">Temp: {temperature}°C</label>
                        <input
                            type="range"
                            className="form-range"
                            id="tempRange"
                            min="-10"
                            max="40"
                            value={temperature}
                            onChange={(e) => setTemperature(Number(e.target.value))}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TopBar;
