import React, { useState } from 'react';

interface TopBarProps {
    isScenariosOpen: boolean;
    setIsScenariosOpen: (isOpen: boolean) => void;
    lowBatteryMessage: () => void;
    heavyTrafficMessage: () => void;
    lowTrafficMessage: () => void;
    batteryLevel: number;
    setBatteryLevel: (level: number) => void;
}

const TopBar: React.FC<TopBarProps> = ({
    isScenariosOpen,
    setIsScenariosOpen,
    lowBatteryMessage,
    heavyTrafficMessage,
    lowTrafficMessage,
    batteryLevel,
    setBatteryLevel,
}) => {
    const [isBatteryOpen, setIsBatteryOpen] = useState(false);

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
            </div>
        </div>
    );
};

export default TopBar;
