import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents } from 'react-leaflet';
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-geosearch/dist/geosearch.css';
import 'leaflet-routing-machine';
import 'leaflet-routing-machine/dist/leaflet-routing-machine.css';

// Fix for default Leaflet icons in Webpack/Vite
// @ts-ignore
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Search Control Component
const SearchControl: React.FC<{ onResult: (pos: [number, number]) => void }> = ({ onResult }) => {
    const map = useMap();

    useEffect(() => {
        // @ts-ignore
        const provider = new OpenStreetMapProvider();

        // @ts-ignore
        const searchControl = new GeoSearchControl({
            provider: provider,
            style: 'bar',
            showMarker: true,
            showPopup: false,
            autoClose: true,
            retainZoomLevel: false,
            animateZoom: true,
            keepResult: true,
            searchLabel: 'Enter address',
        });

        map.addControl(searchControl);

        // Listen for search results
        const handleShowLocation = (e: any) => {
            if (e.location && e.location.y && e.location.x) {
                onResult([Number(e.location.y), Number(e.location.x)]);
            }
        };

        map.on('geosearch/showlocation', handleShowLocation);

        return () => {
            map.removeControl(searchControl);
            map.off('geosearch/showlocation', handleShowLocation);
        };
    }, [map, onResult]);

    return null;
};

// Routing Control Component
const RoutingControl: React.FC<{ start: [number, number]; end: [number, number] }> = ({ start, end }) => {
    const map = useMap();

    useEffect(() => {
        if (!map) return;

        const routingOptions: any = {
            waypoints: [
                L.latLng(start[0], start[1]),
                L.latLng(end[0], end[1])
            ],
            routeWhileDragging: true,
            showAlternatives: true,
            fitSelectedRoutes: true,
            lineOptions: {
                styles: [{ color: '#6FA1EC', weight: 4 }],
                extendToWaypoints: true,
                missingRouteTolerance: 0
            },
            show: false, // Hide the textual itinerary helper
            addWaypoints: false,
            createMarker: function () { return null; }
        };

        const routingControl = L.Routing.control(routingOptions).addTo(map);

        return () => {
            map.removeControl(routingControl);
        };
    }, [map, start, end]);

    return null;
};

// Map Click Handler Component
const MapClickHandler: React.FC<{ setDestination: React.Dispatch<React.SetStateAction<[number, number] | null>> }> = ({ setDestination }) => {
    useMapEvents({
        click: (e) => {
            setDestination([e.latlng.lat, e.latlng.lng]);
        },
    });
    return null;
};

const Map: React.FC = () => {
    // Start Address
    const startAddress = "Corso Duca degli Abruzzi, 24, 10129 Torino TO";
    const [startCoords, setStartCoords] = useState<[number, number] | null>(null);
    const [destination, setDestination] = useState<[number, number] | null>(null);

    // Geocode start address on mount
    useEffect(() => {
        const geocodeAddress = async (address: string) => {
            // @ts-ignore
            const provider = new OpenStreetMapProvider();
            const results = await provider.search({ query: address });
            if (results && results.length > 0) {
                setStartCoords([Number(results[0].y), Number(results[0].x)]);
            }
        };

        geocodeAddress(startAddress);
    }, []);

    if (!startCoords) return <div className="text-white p-3">Loading map...</div>;

    return (
        <MapContainer center={startCoords} zoom={13} scrollWheelZoom={true} style={{ height: '100%', width: '100%' }}>
            <SearchControl onResult={setDestination} />
            <MapClickHandler setDestination={setDestination} />
            {destination && <RoutingControl start={startCoords} end={destination} />}

            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {/* Start Marker */}
            <Marker position={startCoords}>
                <Popup>Start: {startAddress}</Popup>
            </Marker>

            {/* Destination Marker */}
            {destination && (
                <Marker position={destination}>
                    <Popup>Destination</Popup>
                </Marker>
            )}
        </MapContainer>
    );
};

export default Map;
