import { useQuery } from "@tanstack/react-query";
import { getAircraft } from "./getAircraft";
import type { AircraftParams } from "../types";

export const useAircraft = (params: AircraftParams) => {
  return useQuery({
    queryKey: ["aircraft", params],
    queryFn: () => getAircraft(params),
    refetchInterval: 7000,
  });
};
