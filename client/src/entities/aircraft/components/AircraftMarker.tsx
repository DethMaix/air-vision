import { Marker } from "react-leaflet";
import type { Marker as LeafletMarker } from "leaflet";
import planeIcon from "@/shared/assets/plane.png";
import L from "leaflet";
import { useMemo, useEffect, useRef } from "react";
import { aircraftAnimator } from "../lib/aircraftAnimation";

interface AircraftMarkerProps {
  id: string;
  lat: number;
  lon: number;
  heading: number;
}

const createAircraftIcon = () => {
  return L.divIcon({
    className: "",
    html: `
      <img data-aircraft-icon src="${planeIcon}" style="transform: rotate(0deg); display: block; width: 32px; height: 32px; filter: invert(44%) sepia(96%) saturate(1800%) hue-rotate(345deg) brightness(96%) contrast(92%);" />
    `,
    iconSize: [16, 16],
    iconAnchor: [8, 8],
  });
};

export const AircraftMarker = ({
  id,
  lat,
  lon,
  heading,
}: AircraftMarkerProps) => {
  const markerRef = useRef<LeafletMarker | null>(null);

  const icon = useMemo(() => createAircraftIcon(), [heading]);

  useEffect(() => {
    const marker = markerRef.current;

    if (!marker) return;
    aircraftAnimator.update(id, marker, {
      lat,
      lon,
      heading,
    });
  }, [id, lat, lon, heading]);

  useEffect(() => {
    return () => {
      aircraftAnimator.remove(id);
    };
  }, [id]);

  return <Marker ref={markerRef} position={[lat, lon]} icon={icon} />;
};
