"use client";

import { useQuery } from "@tanstack/react-query";
import { getStats } from "../api/records";
import type { StatsResponse } from "../types";

export const statsQueryKey = ["stats"] as const;

export function useStats() {
  return useQuery<StatsResponse>({
    queryKey: statsQueryKey,
    queryFn: getStats,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // Refetch every minute
  });
}
