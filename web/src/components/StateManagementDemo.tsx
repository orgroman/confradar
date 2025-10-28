/**
 * State Management Demo Component
 * 
 * Demonstrates the usage of both TanStack Query (server state) 
 * and Zustand (client state) in the ConfRadar application.
 */

import { useUpcomingConferences } from '../hooks';
import { useConferenceFilters, useUserPreferences, useUIState } from '../stores';

export function StateManagementDemo() {
  // Server State (TanStack Query)
  const { data: upcomingData, isLoading, error } = useUpcomingConferences(5);
  // Example of filtered query - uncomment when needed
  // const { data: filteredData } = useConferences({
  //   year: 2025,
  //   limit: 10,
  // });

  // Client State (Zustand)
  const { filters, setSearchQuery, setSortBy, resetFilters } = useConferenceFilters();
  const { preferences, setTheme, toggleFavorite } = useUserPreferences();
  const { sidebarOpen, toggleSidebar, setError } = useUIState();

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <h1>ConfRadar State Management Demo</h1>
      
      <div style={{ marginBottom: '2rem', padding: '1rem', background: '#f5f5f5', borderRadius: '8px' }}>
        <h2>🎯 Configuration Status</h2>
        <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
          <li>✅ TanStack Query configured for server state</li>
          <li>✅ Zustand stores configured for client state</li>
          <li>✅ Conference data queries available</li>
          <li>✅ Filter state management active</li>
          <li>✅ User preferences with localStorage persistence</li>
          <li>✅ UI state management ready</li>
        </ul>
      </div>

      {/* Server State Demo */}
      <section style={{ marginBottom: '2rem' }}>
        <h2>📡 Server State (TanStack Query)</h2>
        <div style={{ padding: '1rem', border: '1px solid #ddd', borderRadius: '8px' }}>
          <h3>Upcoming Conferences</h3>
          {isLoading && <p>Loading conferences...</p>}
          {error && <p style={{ color: 'red' }}>Error: {error.message}</p>}
          {upcomingData && (
            <div>
              <p>Total conferences: {upcomingData.total}</p>
              <p>Fetched: {upcomingData.conferences.length}</p>
              <p style={{ fontSize: '0.875rem', color: '#666' }}>
                Note: Connect to backend API to see real data
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Filter State Demo */}
      <section style={{ marginBottom: '2rem' }}>
        <h2>🔍 Filter State (Zustand)</h2>
        <div style={{ padding: '1rem', border: '1px solid #ddd', borderRadius: '8px' }}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>
              Search Query:
              <input
                type="text"
                value={filters.searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search conferences..."
                style={{ marginLeft: '0.5rem', padding: '0.25rem 0.5rem' }}
              />
            </label>
          </div>
          
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>
              Sort By:
              <select
                value={filters.sortBy}
                onChange={(e) => setSortBy(e.target.value as typeof filters.sortBy)}
                style={{ marginLeft: '0.5rem', padding: '0.25rem 0.5rem' }}
              >
                <option value="deadline">Deadline</option>
                <option value="name">Name</option>
                <option value="date">Date</option>
                <option value="updated">Last Updated</option>
              </select>
            </label>
          </div>

          <button 
            onClick={resetFilters}
            style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}
          >
            Reset Filters
          </button>

          <div style={{ marginTop: '1rem', fontSize: '0.875rem', color: '#666' }}>
            <strong>Current filters:</strong>
            <pre style={{ background: '#f9f9f9', padding: '0.5rem', borderRadius: '4px' }}>
              {JSON.stringify(filters, null, 2)}
            </pre>
          </div>
        </div>
      </section>

      {/* User Preferences Demo */}
      <section style={{ marginBottom: '2rem' }}>
        <h2>⚙️ User Preferences (Zustand + localStorage)</h2>
        <div style={{ padding: '1rem', border: '1px solid #ddd', borderRadius: '8px' }}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>
              Theme:
              <select
                value={preferences.theme}
                onChange={(e) => setTheme(e.target.value as typeof preferences.theme)}
                style={{ marginLeft: '0.5rem', padding: '0.25rem 0.5rem' }}
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="system">System</option>
              </select>
            </label>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <button
              onClick={() => toggleFavorite('demo-conference-1')}
              style={{ padding: '0.5rem 1rem', cursor: 'pointer', marginRight: '0.5rem' }}
            >
              Toggle Favorite (Demo Conference)
            </button>
            <span>
              {preferences.favoriteConferences.includes('demo-conference-1') ? '❤️ Favorited' : '🤍 Not Favorited'}
            </span>
          </div>

          <div style={{ fontSize: '0.875rem', color: '#666' }}>
            <p>✨ Preferences are persisted to localStorage</p>
            <p>Favorites: {preferences.favoriteConferences.length}</p>
          </div>
        </div>
      </section>

      {/* UI State Demo */}
      <section style={{ marginBottom: '2rem' }}>
        <h2>🎨 UI State (Zustand)</h2>
        <div style={{ padding: '1rem', border: '1px solid #ddd', borderRadius: '8px' }}>
          <div style={{ marginBottom: '1rem' }}>
            <button
              onClick={toggleSidebar}
              style={{ padding: '0.5rem 1rem', cursor: 'pointer', marginRight: '0.5rem' }}
            >
              Toggle Sidebar
            </button>
            <span>Sidebar is: {sidebarOpen ? 'Open 📖' : 'Closed 📕'}</span>
          </div>

          <div>
            <button
              onClick={() => setError('This is a demo error message')}
              style={{ padding: '0.5rem 1rem', cursor: 'pointer', marginRight: '0.5rem' }}
            >
              Trigger Error
            </button>
            <button
              onClick={() => setError(null)}
              style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}
            >
              Clear Error
            </button>
          </div>
        </div>
      </section>

      <div style={{ marginTop: '2rem', padding: '1rem', background: '#e8f5e9', borderRadius: '8px' }}>
        <h3>✅ State Management Setup Complete!</h3>
        <p>
          The ConfRadar frontend is now configured with:
        </p>
        <ul>
          <li><strong>TanStack Query</strong> for server state (conference data from API)</li>
          <li><strong>Zustand</strong> for client state (filters, preferences, UI state)</li>
          <li>Clear separation between server and client state</li>
          <li>Automatic caching, refetching, and error handling</li>
          <li>LocalStorage persistence for user preferences</li>
        </ul>
      </div>
    </div>
  );
}
