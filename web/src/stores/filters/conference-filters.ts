/**
 * Conference Filter Store (Zustand)
 * 
 * Manages client-side filter state for conferences.
 * This includes search queries, year filters, sorting preferences, etc.
 * 
 * Usage:
 * ```tsx
 * function FilterPanel() {
 *   const { filters, setSearchQuery, resetFilters } = useConferenceFilters();
 *   
 *   return (
 *     <input 
 *       value={filters.searchQuery}
 *       onChange={(e) => setSearchQuery(e.target.value)}
 *     />
 *   );
 * }
 * ```
 */

import { create } from 'zustand';
import type { ConferenceFilters } from '../../types/conference';

interface ConferenceFiltersState {
  filters: ConferenceFilters;
  setSearchQuery: (query: string) => void;
  setYear: (year: number | undefined) => void;
  setLocation: (location: string | undefined) => void;
  toggleSeriesFilter: (seriesId: string) => void;
  setShowWorkshops: (show: boolean) => void;
  setSortBy: (sortBy: ConferenceFilters['sortBy']) => void;
  setSortOrder: (order: ConferenceFilters['sortOrder']) => void;
  resetFilters: () => void;
}

const initialFilters: ConferenceFilters = {
  searchQuery: '',
  year: undefined,
  location: undefined,
  seriesIds: [],
  showWorkshops: true,
  sortBy: 'deadline',
  sortOrder: 'asc',
};

/**
 * Zustand store for conference filter state
 */
export const useConferenceFilters = create<ConferenceFiltersState>((set) => ({
  filters: initialFilters,

  setSearchQuery: (query) =>
    set((state) => ({
      filters: { ...state.filters, searchQuery: query },
    })),

  setYear: (year) =>
    set((state) => ({
      filters: { ...state.filters, year },
    })),

  setLocation: (location) =>
    set((state) => ({
      filters: { ...state.filters, location },
    })),

  toggleSeriesFilter: (seriesId) =>
    set((state) => {
      const seriesIds = state.filters.seriesIds.includes(seriesId)
        ? state.filters.seriesIds.filter((id: string) => id !== seriesId)
        : [...state.filters.seriesIds, seriesId];
      return {
        filters: { ...state.filters, seriesIds },
      };
    }),

  setShowWorkshops: (show) =>
    set((state) => ({
      filters: { ...state.filters, showWorkshops: show },
    })),

  setSortBy: (sortBy) =>
    set((state) => ({
      filters: { ...state.filters, sortBy },
    })),

  setSortOrder: (order) =>
    set((state) => ({
      filters: { ...state.filters, sortOrder: order },
    })),

  resetFilters: () => set({ filters: initialFilters }),
}));
