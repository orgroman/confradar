/**
 * UI State Store (Zustand)
 * 
 * Manages transient UI state like open/closed panels, loading states, errors, etc.
 * This state is ephemeral and should not be persisted.
 * 
 * Usage:
 * ```tsx
 * function Sidebar() {
 *   const { sidebarOpen, toggleSidebar } = useUIState();
 *   
 *   return (
 *     <aside className={sidebarOpen ? 'open' : 'closed'}>
 *       <button onClick={toggleSidebar}>Toggle</button>
 *     </aside>
 *   );
 * }
 * ```
 */

import { create } from 'zustand';
import type { UIState } from '../../types/conference';

interface UIStateStore {
  // State properties
  sidebarOpen: boolean;
  filterPanelOpen: boolean;
  selectedConferenceId: string | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  toggleFilterPanel: () => void;
  setFilterPanelOpen: (open: boolean) => void;
  setSelectedConference: (id: string | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
  resetUIState: () => void;
}

const initialState: UIState = {
  sidebarOpen: true,
  filterPanelOpen: false,
  selectedConferenceId: null,
  isLoading: false,
  error: null,
};

/**
 * Zustand store for UI state
 */
export const useUIState = create<UIStateStore>((set) => ({
  ...initialState,

  toggleSidebar: () =>
    set((state) => ({ sidebarOpen: !state.sidebarOpen })),

  setSidebarOpen: (open) =>
    set({ sidebarOpen: open }),

  toggleFilterPanel: () =>
    set((state) => ({ filterPanelOpen: !state.filterPanelOpen })),

  setFilterPanelOpen: (open) =>
    set({ filterPanelOpen: open }),

  setSelectedConference: (id) =>
    set({ selectedConferenceId: id }),

  setLoading: (loading) =>
    set({ isLoading: loading }),

  setError: (error) =>
    set({ error }),

  clearError: () =>
    set({ error: null }),

  resetUIState: () =>
    set(initialState),
}));
