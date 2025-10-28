/**
 * Conference Query Hooks
 * 
 * TanStack Query hooks for managing server state (conference data).
 * These hooks handle caching, refetching, and loading states automatically.
 * 
 * Usage:
 * ```tsx
 * function ConferenceList() {
 *   const { data, isLoading, error } = useConferences();
 *   
 *   if (isLoading) return <div>Loading...</div>;
 *   if (error) return <div>Error: {error.message}</div>;
 *   
 *   return <div>{data.conferences.map(c => <div key={c.id}>{c.name}</div>)}</div>;
 * }
 * ```
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  fetchConferences,
  fetchConference,
  fetchConferenceSeries,
  fetchUpcomingConferences,
} from '../api/conferences';

/**
 * Query keys for conference-related queries
 * Used for caching and cache invalidation
 */
export const conferenceKeys = {
  all: ['conferences'] as const,
  lists: () => [...conferenceKeys.all, 'list'] as const,
  list: (filters?: Record<string, unknown>) => 
    [...conferenceKeys.lists(), filters] as const,
  details: () => [...conferenceKeys.all, 'detail'] as const,
  detail: (id: string) => [...conferenceKeys.details(), id] as const,
  upcoming: () => [...conferenceKeys.all, 'upcoming'] as const,
  series: ['series'] as const,
};

/**
 * Fetch all conferences with optional filters
 */
export function useConferences(params?: {
  year?: number;
  seriesId?: string;
  search?: string;
  limit?: number;
  offset?: number;
}) {
  return useQuery({
    queryKey: conferenceKeys.list(params),
    queryFn: () => fetchConferences(params),
  });
}

/**
 * Fetch a single conference by ID
 */
export function useConference(id: string) {
  return useQuery({
    queryKey: conferenceKeys.detail(id),
    queryFn: () => fetchConference(id),
    enabled: !!id, // Only run query if ID is provided
  });
}

/**
 * Fetch all conference series
 */
export function useConferenceSeries() {
  return useQuery({
    queryKey: conferenceKeys.series,
    queryFn: fetchConferenceSeries,
    staleTime: 10 * 60 * 1000, // Series data changes less frequently
  });
}

/**
 * Fetch upcoming conferences (with deadlines in the future)
 */
export function useUpcomingConferences(limit = 20) {
  return useQuery({
    queryKey: conferenceKeys.upcoming(),
    queryFn: () => fetchUpcomingConferences(limit),
    refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
  });
}

/**
 * Example mutation hook for favoriting a conference
 * Demonstrates optimistic updates and cache invalidation
 */
export function useFavoriteConference() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (conferenceId: string) => {
      // This would call an API endpoint to favorite/unfavorite
      // For now, it's a placeholder
      return { success: true, conferenceId };
    },
    onSuccess: () => {
      // Invalidate and refetch relevant queries
      queryClient.invalidateQueries({ queryKey: conferenceKeys.all });
    },
  });
}
