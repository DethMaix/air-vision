import { apiClient } from "../../../shared/api/client";

import type { AircraftParams, AircraftResponse } from "../types";

export const getAircraft = async ({ lat, lon, radius }: AircraftParams) => {
  const { data } = await apiClient.get<AircraftResponse>(
    `/v1/flights/point/${lat}/${lon}/${radius}`,
  );

  return data;
};
