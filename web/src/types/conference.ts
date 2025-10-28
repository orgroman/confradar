/**
 * Conference Data Types
 * 
 * Core data structures for conference information.
 * These types align with the ConfRadar backend schema.
 */

export interface ConferenceSeries {
  id: string;
  name: string;
  acronym: string;
  description?: string;
  website?: string;
}

export interface Conference {
  id: string;
  seriesId: string;
  name: string;
  acronym: string;
  year: number;
  location?: string;
  website: string;
  submissionDeadline?: string; // ISO 8601 date string
  abstractDeadline?: string; // ISO 8601 date string
  notificationDate?: string; // ISO 8601 date string
  conferenceStartDate?: string; // ISO 8601 date string
  conferenceEndDate?: string; // ISO 8601 date string
  lastUpdated: string; // ISO 8601 timestamp
  isWorkshop: boolean;
  parentEventId?: string;
}

export interface ConferenceFilters {
  searchQuery: string;
  year?: number;
  location?: string;
  seriesIds: string[];
  showWorkshops: boolean;
  sortBy: 'deadline' | 'name' | 'date' | 'updated';
  sortOrder: 'asc' | 'desc';
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  favoriteConferences: string[]; // Conference IDs
  notificationSettings: {
    enabled: boolean;
    daysBeforeDeadline: number;
  };
  displaySettings: {
    dateFormat: 'relative' | 'absolute';
    timezone: string;
  };
}

export interface UIState {
  sidebarOpen: boolean;
  filterPanelOpen: boolean;
  selectedConferenceId: string | null;
  isLoading: boolean;
  error: string | null;
}
