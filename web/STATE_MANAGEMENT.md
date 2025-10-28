# ConfRadar Frontend - State Management Documentation

This document describes the state management architecture for the ConfRadar frontend application.

## Overview

The ConfRadar frontend uses a **dual-state management approach** that clearly separates concerns:

1. **TanStack Query (React Query)** - For **server state** (data from APIs)
2. **Zustand** - For **client state** (UI state, filters, user preferences)

This separation provides:
- Clear responsibility boundaries
- Optimized caching and refetching for server data
- Simple, performant client state management
- Type-safe state access with TypeScript

## Architecture

### Server State (TanStack Query)

**Purpose**: Manage data fetched from the backend API, including:
- Conference data
- Conference series
- Upcoming deadlines
- Search results

**Location**: `/src/hooks/use-conferences.ts`

**Key Features**:
- Automatic caching and background refetching
- Request deduplication
- Optimistic updates
- Loading and error states
- Stale-while-revalidate pattern

**Configuration**: `/src/lib/query/query-client.ts`
```typescript
{
  staleTime: 5 * 60 * 1000,    // Data fresh for 5 minutes
  gcTime: 10 * 60 * 1000,       // Cache garbage collection after 10 min
  retry: 1,                      // Retry failed requests once
  refetchOnWindowFocus: false    // Don't auto-refetch on window focus
}
```

### Client State (Zustand)

**Purpose**: Manage application-local state that doesn't come from the server:
- Filter state
- User preferences
- UI state (sidebars, modals, etc.)

**Location**: `/src/stores/`

**Key Features**:
- Simple, hook-based API
- No boilerplate
- Built-in TypeScript support
- Optional persistence (localStorage)
- Devtools integration ready

## Usage Patterns

### 1. Fetching Conference Data (Server State)

```tsx
import { useConferences, useConference } from './hooks';

function ConferenceList() {
  // Fetch all conferences with filters
  const { data, isLoading, error, refetch } = useConferences({
    year: 2025,
    search: 'machine learning',
    limit: 20
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {data.conferences.map(conf => (
        <div key={conf.id}>{conf.name}</div>
      ))}
    </div>
  );
}

function ConferenceDetail({ id }: { id: string }) {
  // Fetch single conference
  const { data: conference } = useConference(id);
  
  return <div>{conference?.name}</div>;
}
```

### 2. Managing Filters (Client State)

```tsx
import { useConferenceFilters } from './stores';

function FilterPanel() {
  const { 
    filters, 
    setSearchQuery, 
    setYear, 
    setSortBy,
    resetFilters 
  } = useConferenceFilters();

  return (
    <div>
      <input
        value={filters.searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search..."
      />
      
      <select 
        value={filters.sortBy}
        onChange={(e) => setSortBy(e.target.value)}
      >
        <option value="deadline">By Deadline</option>
        <option value="name">By Name</option>
      </select>

      <button onClick={resetFilters}>Reset</button>
    </div>
  );
}
```

### 3. User Preferences (Persisted Client State)

```tsx
import { useUserPreferences } from './stores';

function ThemeToggle() {
  const { preferences, setTheme } = useUserPreferences();

  return (
    <select 
      value={preferences.theme}
      onChange={(e) => setTheme(e.target.value)}
    >
      <option value="light">Light</option>
      <option value="dark">Dark</option>
      <option value="system">System</option>
    </select>
  );
}

function FavoriteButton({ conferenceId }: { conferenceId: string }) {
  const { preferences, toggleFavorite } = useUserPreferences();
  const isFavorite = preferences.favoriteConferences.includes(conferenceId);

  return (
    <button onClick={() => toggleFavorite(conferenceId)}>
      {isFavorite ? '❤️ Favorited' : '🤍 Favorite'}
    </button>
  );
}
```

### 4. UI State

```tsx
import { useUIState } from './stores';

function Sidebar() {
  const { sidebarOpen, toggleSidebar } = useUIState();

  return (
    <aside className={sidebarOpen ? 'open' : 'closed'}>
      <button onClick={toggleSidebar}>Toggle</button>
      {/* Sidebar content */}
    </aside>
  );
}

function ErrorBanner() {
  const { error, clearError } = useUIState();

  if (!error) return null;

  return (
    <div className="error-banner">
      {error}
      <button onClick={clearError}>Dismiss</button>
    </div>
  );
}
```

## Store Structure

### Conference Filters Store
**File**: `/src/stores/filters/conference-filters.ts`

**State**:
```typescript
{
  searchQuery: string;
  year?: number;
  location?: string;
  seriesIds: string[];
  showWorkshops: boolean;
  sortBy: 'deadline' | 'name' | 'date' | 'updated';
  sortOrder: 'asc' | 'desc';
}
```

**Actions**:
- `setSearchQuery(query: string)`
- `setYear(year?: number)`
- `setLocation(location?: string)`
- `toggleSeriesFilter(seriesId: string)`
- `setShowWorkshops(show: boolean)`
- `setSortBy(sortBy)`
- `setSortOrder(order)`
- `resetFilters()`

### User Preferences Store
**File**: `/src/stores/preferences/user-preferences.ts`

**State** (Persisted to localStorage):
```typescript
{
  theme: 'light' | 'dark' | 'system';
  favoriteConferences: string[];
  notificationSettings: {
    enabled: boolean;
    daysBeforeDeadline: number;
  };
  displaySettings: {
    dateFormat: 'relative' | 'absolute';
    timezone: string;
  };
}
```

**Actions**:
- `setTheme(theme)`
- `toggleFavorite(conferenceId: string)`
- `setNotificationSettings(settings)`
- `setDisplaySettings(settings)`
- `resetPreferences()`

### UI State Store
**File**: `/src/stores/ui/ui-state.ts`

**State**:
```typescript
{
  sidebarOpen: boolean;
  filterPanelOpen: boolean;
  selectedConferenceId: string | null;
  isLoading: boolean;
  error: string | null;
}
```

**Actions**:
- `toggleSidebar()` / `setSidebarOpen(open)`
- `toggleFilterPanel()` / `setFilterPanelOpen(open)`
- `setSelectedConference(id)`
- `setLoading(loading)`
- `setError(error)` / `clearError()`
- `resetUIState()`

## Query Keys

TanStack Query uses query keys for caching and invalidation. Our convention:

```typescript
conferenceKeys = {
  all: ['conferences'],
  lists: () => ['conferences', 'list'],
  list: (filters) => ['conferences', 'list', filters],
  details: () => ['conferences', 'detail'],
  detail: (id) => ['conferences', 'detail', id],
  upcoming: () => ['conferences', 'upcoming'],
  series: ['series'],
}
```

### Invalidating Cache

When data changes (e.g., after a mutation), invalidate relevant queries:

```typescript
import { useQueryClient } from '@tanstack/react-query';
import { conferenceKeys } from './hooks';

function useUpdateConference() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateConferenceApi,
    onSuccess: (data) => {
      // Invalidate all conference queries
      queryClient.invalidateQueries({ 
        queryKey: conferenceKeys.all 
      });
      
      // Or just the specific conference
      queryClient.invalidateQueries({ 
        queryKey: conferenceKeys.detail(data.id) 
      });
    },
  });
}
```

## Environment Configuration

Create a `.env` file in the `/web` directory:

```env
# API Base URL
VITE_API_BASE_URL=http://localhost:8000/api

# Optional: Enable React Query Devtools in production
VITE_ENABLE_QUERY_DEVTOOLS=false
```

## Testing

### Testing Components with TanStack Query

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen } from '@testing-library/react';

function renderWithQuery(component: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false }, // Disable retries in tests
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
}

test('displays conferences', async () => {
  renderWithQuery(<ConferenceList />);
  
  expect(await screen.findByText('Conference Name')).toBeInTheDocument();
});
```

### Testing Zustand Stores

Zustand stores are simple to test:

```tsx
import { renderHook, act } from '@testing-library/react';
import { useConferenceFilters } from './stores';

test('updates search query', () => {
  const { result } = renderHook(() => useConferenceFilters());

  act(() => {
    result.current.setSearchQuery('machine learning');
  });

  expect(result.current.filters.searchQuery).toBe('machine learning');
});
```

## Performance Tips

1. **Use selective subscriptions** in Zustand:
   ```tsx
   // Only re-render when searchQuery changes
   const searchQuery = useConferenceFilters(state => state.filters.searchQuery);
   ```

2. **Avoid over-fetching**: Use specific query keys and enable queries conditionally:
   ```tsx
   const { data } = useConference(id, {
     enabled: !!id // Only fetch when id exists
   });
   ```

3. **Debounce search inputs**:
   ```tsx
   const debouncedSearch = useDebouncedValue(searchQuery, 300);
   const { data } = useConferences({ search: debouncedSearch });
   ```

4. **Use optimistic updates** for better UX:
   ```tsx
   const mutation = useMutation({
     mutationFn: updateConference,
     onMutate: async (newData) => {
       // Cancel outgoing queries
       await queryClient.cancelQueries({ queryKey: conferenceKeys.detail(id) });
       
       // Snapshot previous value
       const previous = queryClient.getQueryData(conferenceKeys.detail(id));
       
       // Optimistically update
       queryClient.setQueryData(conferenceKeys.detail(id), newData);
       
       return { previous };
     },
     onError: (err, newData, context) => {
       // Rollback on error
       queryClient.setQueryData(conferenceKeys.detail(id), context.previous);
     },
   });
   ```

## Best Practices

1. **Keep server and client state separate** - Don't duplicate server data in Zustand
2. **Use TypeScript** - All stores and hooks are fully typed
3. **Persist only user preferences** - Not UI state or filters
4. **Use query keys consistently** - Follow the established pattern
5. **Handle loading and error states** - Always show feedback to users
6. **Leverage caching** - Don't refetch unnecessarily
7. **Use mutations for updates** - TanStack Query handles optimistic updates well

## Next Steps

- Add React Query Devtools for development: `npm install @tanstack/react-query-devtools`
- Implement real API integration once backend is ready
- Add unit tests for stores and hooks
- Consider adding middleware for logging/analytics to Zustand stores
- Set up error boundaries for better error handling

## Resources

- [TanStack Query Docs](https://tanstack.com/query/latest)
- [Zustand Docs](https://zustand-demo.pmnd.rs/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
