# ConfRadar Frontend

Modern React + TypeScript frontend for the ConfRadar conference tracking system.

## Technology Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **TanStack Query (React Query)** - Server state management
- **Zustand** - Client state management

## Getting Started

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn

### Installation

```bash
cd web
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173` (or the next available port).

### Build

Build for production:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

### Linting

```bash
npm run lint
```

## Project Structure

```
web/
├── src/
│   ├── api/              # API client and endpoints
│   │   ├── client.ts     # Base API client with fetch wrapper
│   │   └── conferences.ts # Conference-specific API calls
│   ├── components/       # React components
│   │   └── StateManagementDemo.tsx
│   ├── hooks/            # Custom React hooks
│   │   └── use-conferences.ts # TanStack Query hooks
│   ├── lib/              # Libraries and utilities
│   │   └── query/        # TanStack Query configuration
│   ├── stores/           # Zustand state stores
│   │   ├── filters/      # Filter state
│   │   ├── preferences/  # User preferences (persisted)
│   │   └── ui/           # UI state
│   ├── types/            # TypeScript type definitions
│   │   └── conference.ts # Conference-related types
│   ├── App.tsx           # Root component
│   └── main.tsx          # App entry point
├── STATE_MANAGEMENT.md   # State management documentation
└── package.json
```

## State Management

This application uses a dual-state management approach:

- **TanStack Query** for server state (API data)
- **Zustand** for client state (UI, filters, preferences)

See [STATE_MANAGEMENT.md](./STATE_MANAGEMENT.md) for detailed documentation.

### Quick Examples

**Fetching data:**
```tsx
import { useConferences } from './hooks';

function ConferenceList() {
  const { data, isLoading } = useConferences({ year: 2025 });
  // ...
}
```

**Using filters:**
```tsx
import { useConferenceFilters } from './stores';

function SearchBar() {
  const { filters, setSearchQuery } = useConferenceFilters();
  // ...
}
```

**User preferences:**
```tsx
import { useUserPreferences } from './stores';

function Settings() {
  const { preferences, setTheme } = useUserPreferences();
  // ...
}
```

## Environment Variables

Create a `.env` file in the web directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## API Integration

The frontend expects a REST API with these endpoints:

- `GET /api/conferences` - List conferences (with filters)
- `GET /api/conferences/:id` - Get conference details
- `GET /api/conferences/upcoming` - Get upcoming conferences
- `GET /api/series` - List conference series

Update `VITE_API_BASE_URL` to point to your backend.

## Development

### Hot Module Replacement (HMR)

Vite provides instant HMR. Changes to React components will update immediately without losing state.

### Type Checking

TypeScript is configured for strict type checking:

```bash
npm run build  # This runs tsc -b to type check
```

### Code Quality

ESLint is configured with React and TypeScript rules:

```bash
npm run lint
```

## Testing (TODO)

Testing infrastructure to be added:

- [ ] Vitest for unit tests
- [ ] React Testing Library for component tests
- [ ] MSW for API mocking

## Deployment

The built application is a static site that can be deployed to:

- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Any static hosting service

Build command: `npm run build`  
Output directory: `dist/`

## Contributing

When adding new features:

1. Keep server state in TanStack Query hooks
2. Keep client state in Zustand stores
3. Add types to `src/types/`
4. Document patterns in `STATE_MANAGEMENT.md`

## License

[Add license information]
