import { useQuery } from "@tanstack/react-query";
import { getAircraft } from "./getAircraft";
import type { AircraftParams } from "../types";

export const useAircraft = (params: AircraftParams) => {
  return useQuery({
    queryKey: ["aircraft"],
    queryFn: () => getAircraft(params),
    refetchInterval: 8000,
  });
};
