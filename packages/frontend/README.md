# ConfRadar Frontend

Modern React frontend for ConfRadar built with Vite, TypeScript, Tailwind CSS, and shadcn/ui components.

## Tech Stack

- **React 19.1** - UI framework
- **TypeScript** - Type safety
- **Vite 7.1** - Build tool and dev server
- **Tailwind CSS 3.4** - Utility-first CSS framework
- **shadcn/ui** - High-quality, accessible UI components
- **Lucide React** - Icon library

## Getting Started

### Prerequisites

- Node.js 18+ or later
- npm (comes with Node.js)

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

The app will be available at `http://localhost:5173/`

### Building for Production

```bash
npm run build
```

The production-ready files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Styling System

### Tailwind CSS Configuration

The project uses Tailwind CSS with a custom configuration that includes:

#### Design Tokens

**Colors:**
- Primary colors: Blue scale (50-950) for main brand colors
- Secondary colors: Slate scale (50-950) for neutral tones
- Semantic colors via CSS variables:
  - `background` / `foreground`
  - `primary` / `primary-foreground`
  - `secondary` / `secondary-foreground`
  - `muted` / `muted-foreground`
  - `accent` / `accent-foreground`
  - `destructive` / `destructive-foreground`
  - `border`, `input`, `ring`
  - `card` / `card-foreground`
  - `popover` / `popover-foreground`

**Typography:**
- Font Family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif
- Monospace: Fira Code

**Spacing:**
- Standard Tailwind spacing scale plus custom:
  - `128` (32rem)
  - `144` (36rem)

**Border Radius:**
- Configured via CSS variable `--radius` (0.5rem default)
- Utility classes: `rounded-lg`, `rounded-md`, `rounded-sm`

#### Responsive Breakpoints

```
xs:  475px   - Extra small devices
sm:  640px   - Small devices (phones)
md:  768px   - Medium devices (tablets)
lg:  1024px  - Large devices (laptops)
xl:  1280px  - Extra large devices (desktops)
2xl: 1536px  - Extra extra large devices
```

Usage example:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  {/* Responsive grid */}
</div>
```

### Theme System

The app includes a complete theme system with light and dark modes.

#### Theme Provider

Wrap your app with the `ThemeProvider` component:

```tsx
import { ThemeProvider } from '@/components/theme-provider'

<ThemeProvider defaultTheme="light" storageKey="confradar-ui-theme">
  <App />
</ThemeProvider>
```

#### Using Theme Hook

```tsx
import { useTheme } from '@/components/theme-provider'

function MyComponent() {
  const { theme, setTheme } = useTheme()
  
  return (
    <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
      Toggle theme
    </button>
  )
}
```

### UI Components

The project uses shadcn/ui components which are:
- **Accessible** - Built with ARIA attributes and keyboard navigation
- **Customizable** - Fully styled with Tailwind CSS
- **Type-safe** - Written in TypeScript
- **Composable** - Small, reusable building blocks

#### Available Components

##### Button

```tsx
import { Button } from '@/components/ui/button'

// Variants
<Button variant="default">Default</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
<Button variant="destructive">Destructive</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Icon /></Button>
```

##### Card

```tsx
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Content goes here</p>
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

#### Adding More Components

To add more shadcn/ui components:

1. Browse available components at [ui.shadcn.com](https://ui.shadcn.com)
2. Copy the component code from the documentation
3. Create a new file in `src/components/ui/`
4. Update imports to use `@/` path alias

### Utility Functions

#### cn() - Class Name Utility

Combines `clsx` and `tailwind-merge` for intelligent class merging:

```tsx
import { cn } from '@/lib/utils'

<div className={cn(
  "base-classes",
  condition && "conditional-classes",
  className // External className prop
)} />
```

## Project Structure

```
src/
├── components/
│   ├── ui/                    # shadcn/ui components
│   │   ├── button.tsx
│   │   └── card.tsx
│   └── theme-provider.tsx     # Theme management
├── lib/
│   └── utils.ts               # Utility functions
├── App.tsx                    # Main app component
├── main.tsx                   # App entry point
└── index.css                  # Global styles + Tailwind
```

## Path Aliases

The project uses `@/` as an alias for the `src/` directory:

```tsx
// Instead of
import { Button } from '../../components/ui/button'

// You can write
import { Button } from '@/components/ui/button'
```

## Linting

```bash
npm run lint
```

## Configuration Files

- `tailwind.config.js` - Tailwind CSS configuration
- `postcss.config.js` - PostCSS configuration
- `vite.config.ts` - Vite build configuration
- `tsconfig.json` - TypeScript configuration
- `tsconfig.app.json` - App-specific TypeScript config

## Best Practices

1. **Use Semantic HTML** - Use appropriate HTML elements for better accessibility
2. **Leverage Tailwind Utilities** - Prefer Tailwind classes over custom CSS
3. **Component Composition** - Build complex UIs from small, reusable components
4. **Type Safety** - Always define proper TypeScript types for props
5. **Responsive Design** - Design mobile-first, enhance for larger screens
6. **Dark Mode Support** - Use CSS variables for colors to support theme switching
7. **Accessibility** - Ensure all interactive elements are keyboard accessible

## License

See main repository LICENSE file.
