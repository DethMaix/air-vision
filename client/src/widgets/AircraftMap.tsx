import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer } from "react-leaflet";
import { useAircraft } from "../entities/aircraft/api/queries";
import { AircraftMarker } from "../entities/aircraft/components/AircraftMarker";
import { MapController } from "./MapController";
import type { AircraftParams } from "../entities/aircraft/types";
import { useCallback, useState } from "react";

export function AircraftMap() {
  const [aircraftParams, setAircraftParams] = useState<AircraftParams>({
    lat: 53,
    lon: -6,
    radius: 500,
  });
  const { data, isPending, isError } = useAircraft(aircraftParams);

  const handleMapChange = useCallback((params: AircraftParams) => {
    setAircraftParams(params);
  }, []);

  if (!isPending && !isError && data) {
    console.log(data);
  }

  return (
    <div>
      <MapContainer
        center={[51.505, -0.09]}
        zoom={5}
        zoomAnimation={true}
        minZoom={3}
        maxZoom={10}
        maxBounds={[
          [-90, -180],
          [90, 180],
        ]}
        maxBoundsViscosity={1.0}
        style={{ height: "100vh" }}
      >
        <MapController onMapChange={handleMapChange} />
        <TileLayer
          url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png?api_key=ТВОЙ_КЛЮЧ"
          attribution="&copy; Stadia Maps &copy; OpenStreetMap contributors"
        />
        {data &&
          data.map((aircraft) => (
            <AircraftMarker
              key={aircraft.registration}
              lat={aircraft.latitude}
              lon={aircraft.longitude}
              heading={aircraft.true_heading}
            />
          ))}
      </MapContainer>
    </div>
  );
}
