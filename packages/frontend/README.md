# ConfRadar Frontend

## Framework Selection

After evaluating the options, **React with Vite** was selected as the frontend framework for ConfRadar.

### Rationale

#### Why React + Vite?

1. **Modern Development Experience**
   - Lightning-fast Hot Module Replacement (HMR) for instant feedback during development
   - Optimized build tooling with Vite providing native ESM support
   - Significantly faster cold starts compared to webpack-based solutions

2. **TypeScript Support**
   - First-class TypeScript support out of the box
   - No additional configuration needed
   - Strong typing ensures code quality and maintainability

3. **Flexibility and Ecosystem**
   - React has the largest ecosystem of libraries and components
   - Easy to integrate with backend APIs
   - Can evolve to use Next.js or Remix for SSR if SEO becomes critical
   - Unopinionated architecture allows customization to project needs

4. **Team Familiarity and Community**
   - React is the most widely adopted frontend framework
   - Extensive documentation and community support
   - Large talent pool for future team growth

5. **MVP Focus**
   - Lightweight and fast setup aligns with MVP goals
   - Focus on data visualization and user interaction, not SEO
   - Backend-focused architecture means frontend complexity is minimal initially

#### Why Not Next.js?

While Next.js offers excellent SSR and SEO benefits, it's not necessary for the MVP:
- The PRD indicates the MVP focuses on backend data mining
- SEO is not a priority for an academic tool with known users
- Can migrate to Next.js later if SSR becomes needed
- Vite provides faster development iteration for MVP phase

#### Why Not Vue 3?

Vue is an excellent framework but:
- React has broader adoption and larger ecosystem
- More third-party integrations available
- Better alignment with potential team skills

## Project Structure

```
packages/frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── layouts/         # Layout components (navigation, etc.)
│   ├── pages/           # Route-based page components
│   ├── App.tsx          # Main application component with routing
│   ├── App.css          # Application styles
│   ├── main.tsx         # Application entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── .prettierrc          # Prettier configuration
├── eslint.config.js     # ESLint configuration
├── tsconfig.json        # TypeScript configuration
├── tsconfig.app.json    # TypeScript app-specific config
├── tsconfig.node.json   # TypeScript Node-specific config
├── vite.config.ts       # Vite configuration
└── package.json         # Dependencies and scripts
```

## Getting Started

### Prerequisites

- Node.js 20.x or higher
- npm 10.x or higher

### Installation

```bash
cd packages/frontend
npm install
```

### Development

Start the development server with hot module replacement:

```bash
npm run dev
```

The application will be available at http://localhost:5173

### Build

Build for production:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Code Quality

### Linting

The project uses ESLint with TypeScript support and React-specific rules:

```bash
# Check for linting errors
npm run lint

# Auto-fix linting errors
npm run lint:fix
```

### Formatting

Prettier is configured for consistent code formatting:

```bash
# Format all files
npm run format

# Check formatting without making changes
npm run format:check
```

### Configuration

- **ESLint**: Configured with TypeScript, React Hooks, and Prettier integration
- **Prettier**: Enforces consistent code style (single quotes, 100 char line width, etc.)
- **TypeScript**: Strict mode enabled for maximum type safety

## Routing

The application uses React Router v7 for client-side routing:

- `/` - Home page
- `/conferences` - Conference listing page
- `/about` - About page

Routes are defined in `src/App.tsx` using a layout-based structure with `<Outlet />` for nested routing.

## Technology Stack

- **React 19.1** - UI framework
- **TypeScript 5.9** - Type safety
- **Vite 7.1** - Build tool and dev server
- **React Router 7.9** - Client-side routing
- **ESLint 9.38** - Code linting
- **Prettier 3.6** - Code formatting

## Next Steps

1. **API Integration**: Connect to the backend API for fetching conference data
2. **State Management**: Add state management (Context API or Zustand) as complexity grows
3. **UI Components**: Build out the conference listing and detail views
4. **Data Fetching**: Implement API client and data fetching logic
5. **Testing**: Add Jest and React Testing Library for unit and integration tests
6. **Styling**: Consider adding a UI library (Material-UI, Chakra UI) or Tailwind CSS

## Future Considerations

- **Server-Side Rendering**: Migrate to Next.js if SEO becomes important
- **Progressive Web App**: Add PWA features for offline access
- **Mobile Support**: Ensure responsive design for mobile devices
- **Accessibility**: Implement WCAG 2.1 AA compliance
- **Analytics**: Integrate analytics for user behavior tracking

