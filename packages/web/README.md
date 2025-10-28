# ConfRadar Web Frontend

Modern React + TypeScript + Vite frontend for ConfRadar conference deadline tracker.

## Features

- ⚡️ **Vite** - Lightning-fast build tool with HMR
- ⚛️ **React 19** - Latest React with TypeScript support
- 📦 **Optimized Builds** - Code splitting, compression (gzip/brotli), and minification
- 🔍 **Bundle Analysis** - Built-in bundle size visualization
- 🌍 **Environment Variables** - Proper env handling for dev/prod
- 🗺️ **Source Maps** - Debug-friendly source maps
- 🎨 **Asset Optimization** - Automatic image and font optimization

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
cd packages/web
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Building for Production

Build the production-optimized bundle:

```bash
npm run build:prod
```

Build output will be in the `dist/` directory.

### Preview Production Build

Test the production build locally:

```bash
npm run preview
```

## Environment Variables

Environment variables are managed through `.env` files:

- `.env.development` - Development environment
- `.env.production` - Production environment
- `.env.example` - Example template (copy to `.env.local` for overrides)

All client-side environment variables must be prefixed with `VITE_`.

Example:
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=ConfRadar
```

## Build Configuration

### Bundle Size Target

The build is configured to keep the initial bundle size **under 500KB** (gzipped).

- Automatic code splitting for vendor libraries
- React and React-DOM in separate chunks
- Tree-shaking for unused code removal

### Compression

Both gzip and brotli compression are automatically applied to:
- Files larger than 1KB
- All JavaScript, CSS, and HTML files

### Bundle Analysis

To analyze your bundle size:

```bash
npm run analyze
```

This generates a `dist/stats.html` file showing:
- Bundle composition
- Chunk sizes (original, gzipped, and brotli)
- Module tree visualization

### Source Maps

- **Development**: Full source maps for debugging
- **Production**: Hidden source maps (not exposed to users but available for error tracking)

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build with TypeScript check |
| `npm run build:dev` | Build for development environment |
| `npm run build:prod` | Build for production environment |
| `npm run preview` | Preview production build |
| `npm run analyze` | Analyze bundle size |
| `npm run type-check` | Run TypeScript type checking |

## Build Optimizations

### Automatic Optimizations

1. **Code Splitting**: Vendor chunks separated for better caching
2. **Tree Shaking**: Unused code automatically removed
3. **Minification**: Using esbuild for fast minification
4. **Asset Inlining**: Small assets (<4KB) inlined as base64
5. **CSS Code Splitting**: CSS split by component for faster loading
6. **Compression**: Gzip and Brotli pre-compression

### Manual Chunk Configuration

Edit `vite.config.ts` to customize chunk splitting:

```typescript
manualChunks: {
  'react-vendor': ['react', 'react-dom'],
  'ui-vendor': ['@mui/material'], // Add your UI library
}
```

## Asset Organization

Built assets are organized by type:

```
dist/
├── assets/
│   ├── js/        # JavaScript bundles
│   ├── css/       # CSS files
│   ├── img/       # Images
│   └── fonts/     # Font files
└── stats.html     # Bundle analysis report
```

## Performance Tips

1. **Lazy Loading**: Use `React.lazy()` for route-based code splitting
2. **Image Optimization**: Use WebP format for images
3. **Font Loading**: Subset fonts and use `font-display: swap`
4. **API Calls**: Implement proper caching strategies

## Troubleshooting

### Build takes too long
- Check bundle size with `npm run analyze`
- Review dependencies - remove unused packages
- Consider lazy loading large components

### Bundle size too large
- Run `npm run analyze` to identify large modules
- Enable code splitting for large dependencies
- Check for duplicate dependencies

## Production Deployment

1. Build the production bundle:
   ```bash
   npm run build:prod
   ```

2. Deploy the `dist/` folder to your hosting service

3. Configure your web server to:
   - Serve pre-compressed files (`.gz`, `.br`) if supported
   - Set proper cache headers for assets
   - Redirect all routes to `index.html` for SPA routing

## Contributing

When adding new features:
1. Keep bundle size in check
2. Use environment variables for configuration
3. Run type checking before commits
4. Test production builds locally

## License

ISC
