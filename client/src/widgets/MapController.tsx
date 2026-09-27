import { useEffect } from "react";
import { useMap } from "react-leaflet";
import type { AircraftParams } from "../entities/aircraft/types";
import { getRagiusFromZoom } from "../shared/lib/map/getRadiusFromZoom";

export function MapController({
  onMapChange,
}: {
  onMapChange: (params: AircraftParams) => void;
}) {
  const map = useMap();
  useEffect(() => {
    const handleMoveEnd = () => {
      const center = map.getCenter();
      const zoom = map.getZoom();
      const radius = getRagiusFromZoom(zoom);
      onMapChange({
        lat: center.lat,
        lon: center.lng,
        radius,
      });
    };

    map.on("moveend", handleMoveEnd);
    return () => {
      map.off("moveend", handleMoveEnd);
    };
  }, [map, onMapChange]);
  return null;
}
