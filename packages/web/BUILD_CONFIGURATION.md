# Build Configuration & Optimization

## Overview

This document details the build configuration, optimization strategies, and deployment guidelines for the ConfRadar web frontend.

## Build Tool: Vite

We use **Vite 7** as our build tool for the following reasons:

- ⚡️ Lightning-fast HMR (Hot Module Replacement) during development
- 📦 Optimized production builds with Rollup
- 🔌 Rich plugin ecosystem
- 🎯 Native ES modules support
- 🚀 Fast cold start times

## Build Configuration

### File Structure

```
packages/web/
├── vite.config.ts          # Main Vite configuration
├── tsconfig.json           # TypeScript configuration
├── tsconfig.node.json      # Node-specific TS config
├── .env.example            # Environment variables template
├── .env.development        # Development environment
├── .env.production         # Production environment
└── src/
    ├── vite-env.d.ts       # Vite type definitions
    └── ...
```

### Environment Variables

#### Naming Convention
- All client-side variables must be prefixed with `VITE_`
- Example: `VITE_API_URL`, `VITE_APP_TITLE`

#### Available Environments
1. **Development** (`.env.development`)
   - Used when running `npm run dev` or `npm run build:dev`
   - Enables debugging features
   - Points to local API

2. **Production** (`.env.production`)
   - Used when running `npm run build:prod`
   - Disables debugging
   - Points to production API

#### Adding New Variables

1. Define in `.env.example`:
```bash
VITE_NEW_FEATURE=value
```

2. Add type definition in `src/vite-env.d.ts`:
```typescript
interface ImportMetaEnv {
  readonly VITE_NEW_FEATURE: string;
}
```

3. Use in code:
```typescript
const feature = import.meta.env.VITE_NEW_FEATURE;
```

## Optimization Features

### 1. Code Splitting

**Automatic code splitting** divides the bundle into smaller chunks for better caching and faster loading.

#### Vendor Chunks
React and React-DOM are separated into a dedicated vendor chunk:

```typescript
manualChunks: {
  'react-vendor': ['react', 'react-dom'],
}
```

**Benefits:**
- Vendor code changes less frequently → better browser caching
- Main app code can be updated without re-downloading React
- Parallel loading of chunks

#### Adding More Chunks

Edit `vite.config.ts`:

```typescript
manualChunks: {
  'react-vendor': ['react', 'react-dom'],
  'ui-vendor': ['@mui/material', '@emotion/react'],
  'utils': ['lodash', 'date-fns'],
}
```

### 2. Compression

Both **gzip** and **brotli** compression are automatically applied during build.

#### Configuration
- Files > 1KB are compressed
- Both `.gz` and `.br` files are generated
- Original files are preserved

#### Compression Comparison

| File Type | Original | Gzipped | Brotli | Ratio (Brotli) |
|-----------|----------|---------|--------|----------------|
| JS Bundle | 183 KB   | 58 KB   | 49 KB  | 73% reduction  |
| React Vendor | 12 KB | 4 KB | 4 KB | 67% reduction |
| CSS | 1 KB | 0.6 KB | 0.4 KB | 60% reduction |

#### Server Configuration

**Nginx:**
```nginx
# Enable gzip
gzip on;
gzip_vary on;
gzip_types text/plain text/css application/json application/javascript text/xml;

# Serve pre-compressed files
gzip_static on;
brotli_static on;
```

**Apache:**
```apache
# Enable compression
AddOutputFilterByType DEFLATE text/html text/css application/javascript

# Serve pre-compressed files
RewriteRule ^(.*)\.js$ $1.js.gz [QSA]
RewriteRule ^(.*)\.css$ $1.css.gz [QSA]
```

### 3. Bundle Analysis

Run bundle analysis to visualize your bundle composition:

```bash
npm run analyze
```

This generates `dist/stats.html` with:
- Interactive treemap of your bundle
- Size breakdown by module
- Gzipped and Brotli sizes
- Chunk composition

**Use Cases:**
- Identify large dependencies
- Find duplicate packages
- Optimize bundle size
- Track size changes over time

### 4. Asset Optimization

#### Images
- Assets < 4KB are inlined as base64
- Larger assets get content-based hash names
- Organized in `dist/assets/img/`

**Recommendations:**
- Use WebP format for better compression
- Implement lazy loading for images
- Use `<picture>` for responsive images

#### Fonts
- Font files are extracted to `dist/assets/fonts/`
- Use font subsetting to reduce file size
- Implement `font-display: swap` for better performance

```css
@font-face {
  font-family: 'MyFont';
  src: url('./fonts/myfont.woff2') format('woff2');
  font-display: swap; /* Prevent FOIT (Flash of Invisible Text) */
}
```

### 5. Source Maps

Source maps help debug production code.

#### Configuration
- **Development**: Full source maps (`sourcemap: true`)
- **Production**: Hidden source maps (`sourcemap: 'hidden'`)

**Hidden source maps:**
- Not referenced in JS files (users don't see them)
- Can be uploaded to error tracking services
- Enable debugging without exposing source code

#### Using with Error Tracking

Upload source maps to Sentry/Rollbar:
```bash
# Example with Sentry
sentry-cli releases files VERSION upload-sourcemaps dist/
```

### 6. Minification

**esbuild** is used for fast JavaScript/CSS minification.

**Features:**
- 10-100x faster than Terser
- Removes dead code
- Shortens variable names
- Removes whitespace and comments

## Build Scripts

| Script | Command | Description | Source Maps | Minification |
|--------|---------|-------------|-------------|--------------|
| `dev` | `vite` | Development server | Full | No |
| `build` | `tsc && vite build` | Default build | Hidden | Yes |
| `build:dev` | `vite build --mode development` | Dev build | Full | Yes |
| `build:prod` | `vite build --mode production` | Prod build | Hidden | Yes |
| `preview` | `vite preview` | Preview prod build | - | - |
| `analyze` | Build + open stats | Bundle analysis | Hidden | Yes |

## Performance Benchmarks

### Build Performance

| Operation | Time | Description |
|-----------|------|-------------|
| Cold start (dev) | ~500ms | First dev server start |
| HMR update | <100ms | File change → browser update |
| Type check | ~2s | Full TypeScript check |
| Production build | ~2s | Full optimized build |

### Bundle Size

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Initial JS (gzipped) | <500 KB | ~61 KB | ✅ |
| Total JS (raw) | - | ~195 KB | ✅ |
| CSS (gzipped) | - | ~0.6 KB | ✅ |

## Production Deployment

### Build Steps

1. **Install dependencies:**
```bash
npm ci --production=false
```

2. **Run type checking:**
```bash
npm run type-check
```

3. **Build for production:**
```bash
npm run build:prod
```

4. **Deploy the `dist/` folder**

### Hosting Recommendations

#### Static Hosting (Vercel, Netlify, Cloudflare Pages)

**Vercel:**
```json
{
  "buildCommand": "npm run build:prod",
  "outputDirectory": "dist"
}
```

**Netlify:**
```toml
[build]
  command = "npm run build:prod"
  publish = "dist"
```

#### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build:prod

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

### Caching Strategy

Configure cache headers:

```nginx
location /assets/ {
  # Immutable assets (with hash in filename)
  expires 1y;
  add_header Cache-Control "public, immutable";
}

location / {
  # HTML files (no cache)
  expires -1;
  add_header Cache-Control "no-cache, no-store, must-revalidate";
}
```

## Monitoring & Optimization

### Key Metrics to Track

1. **Bundle Size**
   - Monitor with `npm run analyze`
   - Set up CI checks for size increases
   - Target: Keep initial bundle < 500 KB

2. **Build Time**
   - Track in CI/CD pipeline
   - Investigate if build time > 5 minutes

3. **Lighthouse Scores**
   - Performance: > 90
   - Best Practices: > 90
   - SEO: > 90

### Optimization Checklist

- [ ] Run bundle analysis regularly
- [ ] Implement lazy loading for routes
- [ ] Optimize images (WebP, lazy loading)
- [ ] Use font subsetting
- [ ] Enable compression on server
- [ ] Configure proper cache headers
- [ ] Monitor bundle size in CI
- [ ] Set up error tracking with source maps
- [ ] Implement service worker for PWA (optional)
- [ ] Audit with Lighthouse

## Troubleshooting

### Build Fails with Memory Error

Increase Node.js memory:
```bash
NODE_OPTIONS=--max-old-space-size=4096 npm run build
```

### Bundle Size Too Large

1. Run `npm run analyze`
2. Identify large modules
3. Consider:
   - Lazy loading
   - Alternative smaller libraries
   - Tree-shaking configuration
   - Remove unused dependencies

### Slow Development Server

1. Reduce number of dependencies
2. Use `optimizeDeps.include` in vite.config.ts
3. Increase Node.js memory
4. Check for circular dependencies

### Environment Variables Not Working

1. Verify prefix: Must start with `VITE_`
2. Restart dev server after changing .env files
3. Check type definitions in vite-env.d.ts

## Future Enhancements

- [ ] Add Service Worker for offline support
- [ ] Implement PWA features
- [ ] Add performance budgets in CI
- [ ] Set up automated Lighthouse checks
- [ ] Implement critical CSS extraction
- [ ] Add image optimization pipeline
- [ ] Configure CDN for assets
- [ ] Set up A/B testing infrastructure

## References

- [Vite Documentation](https://vitejs.dev/)
- [Rollup Options](https://rollupjs.org/configuration-options/)
- [Web Vitals](https://web.dev/vitals/)
- [Bundle Size Guidelines](https://web.dev/performance-budgets/)
