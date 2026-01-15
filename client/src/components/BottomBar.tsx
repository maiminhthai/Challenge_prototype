import React from 'react';

interface BottomBarProps {
    temperature: number;
}

const BottomBar: React.FC<BottomBarProps> = ({ temperature }) => {
    return (
        <div className="row bg-black p-3 mt-auto align-items-center justify-content-between text-white border-top border-secondary m-0 w-100">
            <div className="col-auto d-flex gap-4 align-items-center">
                <i className="bi bi-car-front-fill bottom-bar-icon"></i>
                <i className="bi bi-wind bottom-bar-icon"></i>
            </div>

            <div className="col d-flex justify-content-center gap-5 align-items-center">
                {/* Driver Temp */}
                <div className="temp-control text-white">
                    <i className="bi bi-chevron-up small"></i>
                    <span className="temp-text">{temperature}°</span>
                    <i className="bi bi-chevron-down small"></i>
                </div>

                {/* Fan */}
                <i className="bi bi-fan bottom-bar-icon" style={{ fontSize: '2rem', color: 'white' }}></i>

                {/* Passenger Temp */}
                <div className="temp-control text-white">
                    <i className="bi bi-chevron-up small"></i>
                    <span className="temp-text">{temperature}°</span>
                    <i className="bi bi-chevron-down small"></i>
                </div>
            </div>

            <div className="col-auto d-flex gap-4 align-items-center">
                <i className="bi bi-music-note-beamed bottom-bar-icon"></i>
                <i className="bi bi-telephone-fill bottom-bar-icon"></i>
                <i className="bi bi-volume-up-fill bottom-bar-icon"></i>
            </div>
        </div>
    );
};

export default BottomBar;

