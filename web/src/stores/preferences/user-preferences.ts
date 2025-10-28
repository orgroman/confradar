/**
 * User Preferences Store (Zustand)
 * 
 * Manages user preferences that should persist across sessions.
 * This store should be persisted to localStorage.
 * 
 * Usage:
 * ```tsx
 * function ThemeToggle() {
 *   const { theme, setTheme } = useUserPreferences();
 *   
 *   return (
 *     <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
 *       Toggle Theme
 *     </button>
 *   );
 * }
 * ```
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { UserPreferences } from '../../types/conference';

interface UserPreferencesState {
  preferences: UserPreferences;
  setTheme: (theme: UserPreferences['theme']) => void;
  toggleFavorite: (conferenceId: string) => void;
  setNotificationSettings: (settings: UserPreferences['notificationSettings']) => void;
  setDisplaySettings: (settings: UserPreferences['displaySettings']) => void;
  resetPreferences: () => void;
}

const initialPreferences: UserPreferences = {
  theme: 'system',
  favoriteConferences: [],
  notificationSettings: {
    enabled: false,
    daysBeforeDeadline: 7,
  },
  displaySettings: {
    dateFormat: 'relative',
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
  },
};

/**
 * Zustand store for user preferences with localStorage persistence
 */
export const useUserPreferences = create<UserPreferencesState>()(
  persist(
    (set) => ({
      preferences: initialPreferences,

      setTheme: (theme) =>
        set((state) => ({
          preferences: { ...state.preferences, theme },
        })),

      toggleFavorite: (conferenceId) =>
        set((state) => {
          const favoriteConferences = state.preferences.favoriteConferences.includes(conferenceId)
            ? state.preferences.favoriteConferences.filter((id: string) => id !== conferenceId)
            : [...state.preferences.favoriteConferences, conferenceId];
          return {
            preferences: { ...state.preferences, favoriteConferences },
          };
        }),

      setNotificationSettings: (settings) =>
        set((state) => ({
          preferences: {
            ...state.preferences,
            notificationSettings: settings,
          },
        })),

      setDisplaySettings: (settings) =>
        set((state) => ({
          preferences: {
            ...state.preferences,
            displaySettings: settings,
          },
        })),

      resetPreferences: () => set({ preferences: initialPreferences }),
    }),
    {
      name: 'confradar-preferences',
    }
  )
);
