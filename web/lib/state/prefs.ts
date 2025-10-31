import { create } from "zustand"
import { persist } from "zustand/middleware"

interface PrefsState {
  viewMode: "grid" | "list"
  timezoneMode: "local" | "aoe"
  setViewMode: (mode: "grid" | "list") => void
  setTimezoneMode: (mode: "local" | "aoe") => void
}

export const usePrefsStore = create<PrefsState>()(
  persist(
    (set) => ({
      viewMode: "grid",
      timezoneMode: "local",
      setViewMode: (mode) => set({ viewMode: mode }),
      setTimezoneMode: (mode) => set({ timezoneMode: mode }),
    }),
    {
      name: "confradar-prefs",
    },
  ),
)
