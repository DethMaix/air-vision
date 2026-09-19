export interface Aircraft {
  registration: string;
  aircraft_type: string;
  true_heading: number;
  latitude: number;
  longitude: number;
}

export type AircraftResponse = Aircraft[];

export interface AircraftParams {
  lat: number;
  lon: number;
  radius: number;
}
