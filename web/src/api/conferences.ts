/**
 * Conference API Methods
 * 
 * API functions for fetching conference data from the backend.
 * These functions are used by TanStack Query hooks.
 */

import { api } from './client';
import type { Conference, ConferenceSeries } from '../types/conference';

export interface ConferencesResponse {
  conferences: Conference[];
  total: number;
}

export interface ConferenceSeriesResponse {
  series: ConferenceSeries[];
  total: number;
}

/**
 * Fetch all conferences with optional filters
 */
export async function fetchConferences(params?: {
  year?: number;
  seriesId?: string;
  search?: string;
  limit?: number;
  offset?: number;
}): Promise<ConferencesResponse> {
  const queryParams = new URLSearchParams();
  if (params?.year) queryParams.set('year', params.year.toString());
  if (params?.seriesId) queryParams.set('seriesId', params.seriesId);
  if (params?.search) queryParams.set('search', params.search);
  if (params?.limit) queryParams.set('limit', params.limit.toString());
  if (params?.offset) queryParams.set('offset', params.offset.toString());

  const query = queryParams.toString();
  return api.get<ConferencesResponse>(
    `/conferences${query ? `?${query}` : ''}`
  );
}

/**
 * Fetch a single conference by ID
 */
export async function fetchConference(id: string): Promise<Conference> {
  return api.get<Conference>(`/conferences/${id}`);
}

/**
 * Fetch all conference series
 */
export async function fetchConferenceSeries(): Promise<ConferenceSeriesResponse> {
  return api.get<ConferenceSeriesResponse>('/series');
}

/**
 * Fetch upcoming conferences (deadlines in the future)
 */
export async function fetchUpcomingConferences(
  limit = 20
): Promise<ConferencesResponse> {
  return api.get<ConferencesResponse>(
    `/conferences/upcoming?limit=${limit}`
  );
}
