import type { Marker } from "leaflet";

interface AircraftPosition {
  lat: number;
  lon: number;
  heading: number;
}

interface AnimationState {
  marker: Marker;
  current: AircraftPosition;
  from: AircraftPosition;
  to: AircraftPosition;
  startTime: number;
  duration: number;
  isAnimating: boolean;
}

const ANIMATION_DURATION = 6500;
const MIN_MOVEMENT_METERS = 20;

const lerp = (from: number, to: number, progress: number) => {
  return from + (to - from) * progress;
};

const lerpLongitude = (from: number, to: number, progress: number) => {
  const difference = ((to - from + 540) % 360) - 180;

  let longitude = from + difference * progress;

  if (longitude > 180) {
    longitude -= 360;
  }

  if (longitude < -180) {
    longitude += 360;
  }

  return longitude;
};

const lerpAngle = (from: number, to: number, progress: number) => {
  const difference = ((to - from + 540) % 360) - 180;

  return from + difference * progress;
};

const getDistanceMeters = (from: AircraftPosition, to: AircraftPosition) => {
  const earthRadius = 6_371_000;

  const lat1 = (from.lat * Math.PI) / 180;
  const lat2 = (to.lat * Math.PI) / 180;

  const deltaLat = ((to.lat - from.lat) * Math.PI) / 180;

  const deltaLon = ((to.lon - from.lon) * Math.PI) / 180;

  const a =
    Math.sin(deltaLat / 2) ** 2 +
    Math.cos(lat1) * Math.cos(lat2) * Math.sin(deltaLon / 2) ** 2;

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return earthRadius * c;
};

const setMarkerHeading = (marker: Marker, heading: number) => {
  const element = marker.getElement();

  if (!element) {
    return;
  }

  const image = element.querySelector<HTMLElement>("[data-aircraft-icon]");

  if (!image) {
    return;
  }

  image.style.transform = `rotate(${heading}deg)`;
};

class AircraftAnimator {
  private readonly items = new Map<string, AnimationState>();

  private animationFrameId: number | null = null;

  private readonly animate = (timestamp: number) => {
    let hasActiveAnimations = false;

    for (const item of this.items.values()) {
      if (!item.isAnimating) {
        continue;
      }

      const elapsed = timestamp - item.startTime;

      const progress = Math.min(elapsed / item.duration, 1);

      const lat = lerp(item.from.lat, item.to.lat, progress);

      const lon = lerpLongitude(item.from.lon, item.to.lon, progress);

      const heading = lerpAngle(item.from.heading, item.to.heading, progress);

      item.current = {
        lat,
        lon,
        heading,
      };

      item.marker.setLatLng([lat, lon]);

      setMarkerHeading(item.marker, heading);

      if (progress >= 1) {
        item.current = {
          ...item.to,
        };

        item.isAnimating = false;
      } else {
        hasActiveAnimations = true;
      }
    }

    if (hasActiveAnimations) {
      this.animationFrameId = requestAnimationFrame(this.animate);
    } else {
      this.animationFrameId = null;
    }
  };

  private startAnimationLoop() {
    if (this.animationFrameId !== null) {
      return;
    }

    this.animationFrameId = requestAnimationFrame(this.animate);
  }

  update(id: string, marker: Marker, target: AircraftPosition) {
    const existing = this.items.get(id);

    if (!existing) {
      const state: AnimationState = {
        marker,
        current: target,
        from: target,
        to: target,
        startTime: 0,
        duration: ANIMATION_DURATION,
        isAnimating: false,
      };

      this.items.set(id, state);

      marker.setLatLng([target.lat, target.lon]);

      setMarkerHeading(marker, target.heading);

      return;
    }

    existing.marker = marker;

    const distance = getDistanceMeters(existing.current, target);

    existing.from = {
      ...existing.current,
    };

    existing.to = {
      ...target,
    };

    existing.startTime = performance.now();

    existing.isAnimating = distance >= MIN_MOVEMENT_METERS;

    if (!existing.isAnimating) {
      existing.current = {
        ...target,
      };

      marker.setLatLng([target.lat, target.lon]);

      setMarkerHeading(marker, target.heading);

      return;
    }

    this.startAnimationLoop();
  }

  remove(id: string) {
    this.items.delete(id);

    if (this.items.size === 0 && this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);

      this.animationFrameId = null;
    }
  }
}

export const aircraftAnimator = new AircraftAnimator();
