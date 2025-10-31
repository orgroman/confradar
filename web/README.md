# ConfRadar Frontend

> Never miss a conference deadline. Track important dates, locations, and submission deadlines for academic conferences.

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Open http://localhost:3000
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier
- `npm run test` - Run tests with Vitest
- `npm run test:ui` - Run tests with UI
- `npm run typecheck` - Run TypeScript type checking

## Tech Stack

- Framework: Next.js 15 (App Router)
- Language: TypeScript
- Styling: Tailwind CSS v4
- UI Components: shadcn/ui (local primitives)
- State Management: Zustand with localStorage persistence
- Testing: Vitest + React Testing Library
- Date Handling: date-fns + date-fns-tz

## Project Structure

```
web/
├── app/                      # Next.js app directory
│   ├── conferences/          # Conference pages
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Home page
│   └── globals.css           # Global styles
├── components/               # React components
│   ├── ui/                   # UI primitives
│   ├── ConferenceCard.tsx
│   ├── FilterBar.tsx
│   ├── Header.tsx
│   └── Footer.tsx
├── lib/                      # Utilities and logic
│   ├── api/                  # API client layer
│   ├── state/                # Zustand stores
│   └── utils/                # Helper functions
├── mocks/                    # Mock data
├── tests/                    # Test files
└── public/                   # Static assets
```

## Development Notes

- Mock API: Static JSON data in `mocks/conferences.json`
- Type Safety: Full TypeScript coverage
- Code Quality: ESLint + Prettier
- CI: GitHub Actions workflow `.github/workflows/frontend.yml` (runs in `web/`)

## Environment Variables

None required for local development (mock data).

## Contributing

- Create a feature branch (`feat/...`, `fix/...`, or `chore/...`)
- Run tests: `npm run test`
- Run type check: `npm run typecheck`
- Format code: `npm run format`
- Open a PR against main (CI must pass)