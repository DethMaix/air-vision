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
      <img src="${planeIcon}" style="transform: rotate(${heading}deg); width: 32px; height: 32px; filter: invert(44%) sepia(96%) saturate(1800%) hue-rotate(345deg) brightness(96%) contrast(92%);" />
    `,
    iconSize: [16, 16],
    iconAnchor: [8, 8],
  });
};

export const AircraftMarker = ({ lat, lon, heading }: AircraftMarkerProps) => {
  const icon = useMemo(() => createAircraftIcon(heading), [heading]);

  return <Marker position={[lat, lon]} icon={icon} />;
};
