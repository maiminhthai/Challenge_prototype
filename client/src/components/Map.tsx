import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine';
import 'leaflet-routing-machine/dist/leaflet-routing-machine.css';
import { OpenStreetMapProvider } from 'leaflet-geosearch';

// Fix for default Leaflet icons in Webpack/Vite
// @ts-ignore
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Routing Control Component
const RoutingControl: React.FC<{ start: [number, number]; end: [number, number] | null }> = ({ start, end }) => {
    const map = useMap();

    useEffect(() => {
        if (!start || !end) return;

        const routingControl = L.Routing.control({
            waypoints: [
                L.latLng(start[0], start[1]),
                L.latLng(end[0], end[1])
            ],
            routeWhileDragging: false,
            showAlternatives: true,
            fitSelectedRoutes: true,
            lineOptions: {
                styles: [{ color: '#6FA1EC', weight: 4 }],
                extendToWaypoints: false,
                missingRouteTolerance: 0
            },
            // @ts-ignore
            createMarker: function () { return null; }
        }).addTo(map);

        return () => {
            map.removeControl(routingControl);
        };
    }, [map, start, end]);

    return null;
};

interface MapProps {
    destination: string;
}

const Map: React.FC<MapProps> = ({ destination }) => {
    // Default center position (Turin, Italy)
    const startPosition: [number, number] = [45.0624332, 7.6596305];
    const [destCoords, setDestCoords] = useState<[number, number] | null>(null);

    // Geocode destination when it changes
    useEffect(() => {
        if (!destination) return;

        const geocodeDestination = async () => {
            // @ts-ignore
            const provider = new OpenStreetMapProvider();
            const results = await provider.search({ query: destination });
            if (results && results.length > 0) {
                setDestCoords([Number(results[0].y), Number(results[0].x)]);
            }
        };

        geocodeDestination();
    }, [destination]);

    return (
        <MapContainer center={startPosition} zoom={13} scrollWheelZoom={true} style={{ height: '100%', width: '100%' }}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {/* Start Marker */}
            <Marker position={startPosition}>
                <Popup>Start Position</Popup>
            </Marker>

            {/* Destination Marker */}
            {destCoords && (
                <Marker position={destCoords}>
                    <Popup>{destination}</Popup>
                </Marker>
            )}

            {/* Routing */}
            {destCoords && <RoutingControl start={startPosition} end={destCoords} />}

        </MapContainer>
    );
};

export default Map;
