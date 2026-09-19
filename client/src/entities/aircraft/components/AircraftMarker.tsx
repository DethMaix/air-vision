import { Marker } from "react-leaflet";
import planeIcon from "@/shared/assets/plane.png";
import L from "leaflet";
import { useMemo } from "react";

interface AircraftMarkerProps {
  lat: number;
  lon: number;
  heading: number;
}

const createAircraftIcon = (heading: number) => {
  return L.divIcon({
    className: "",
    html: `
      <img src="${planeIcon}" style="transform: rotate(${heading - 90}deg); width=16px; height=16px;" />
    `,
    iconSize: [16, 16],
    iconAnchor: [8, 8],
  });
};

export const AircraftMarker = ({ lat, lon, heading }: AircraftMarkerProps) => {
  const icon = useMemo(() => createAircraftIcon(heading), [heading]);

  return <Marker position={[lat, lon]} icon={icon} />;
};
