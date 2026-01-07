import React, { type Dispatch, type SetStateAction } from "react";

interface ContextType {
    batteryLevel: number;
    setBatteryLevel: Dispatch<SetStateAction<number>>;
}

const Context = React.createContext<ContextType>({
    batteryLevel: 0,
    setBatteryLevel: () => { },
});

export default Context;