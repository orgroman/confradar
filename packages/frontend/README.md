# ConfRadar Frontend

React + TypeScript + Vite frontend for the ConfRadar conference tracking application.

## Routing Structure

The application uses **React Router v6** for client-side routing.

### Routes

| Route | Component | Description |
|-------|-----------|-------------|
| `/` | `Home` | Conference list with filtering |
| `/conferences/:id` | `ConferenceDetail` | Individual conference details |
| `/settings` | `Settings` | User settings page |
| `/about` | `About` | About ConfRadar |
| `*` | `NotFound` | 404 page for invalid routes |

### Navigation

The `Navigation` component provides links to all main routes and is included in the `Layout` component that wraps all pages.

### URL Query Parameters

URL query parameters are used for filter state that should persist when sharing links or refreshing the page.

Example usage with the `useQueryParams` hook:

```tsx
import { useQueryParams } from '../hooks/useQueryParams';

interface FilterParams {
  search?: string;
  status?: string;
}

function MyComponent() {
  const { getParam, setParam, getAllParams } = useQueryParams<FilterParams>();
  
  const search = getParam('search');
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setParam('search', e.target.value);
  };
  
  // ...
}
```

## Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── components/     # Reusable components
│   ├── Layout.tsx      # Main layout with navigation
│   └── Navigation.tsx  # Navigation component
├── pages/          # Page components (routes)
│   ├── Home.tsx
│   ├── ConferenceDetail.tsx
│   ├── Settings.tsx
│   ├── About.tsx
│   └── NotFound.tsx
├── hooks/          # Custom React hooks
│   └── useQueryParams.ts  # Hook for URL query params
├── App.tsx         # Main app with routing setup
└── main.tsx        # Entry point
```

## Browser Navigation

- ✅ Browser back/forward buttons work correctly
- ✅ Page refresh preserves current route
- ✅ URL sharing works (including query parameters)
- ✅ Deep linking to specific pages/conferences supported

## ESLint Configuration

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

### Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

