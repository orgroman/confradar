# Frontend Build Setup

The ConfRadar web frontend is located in `packages/web/` and uses Vite as the build tool.

## Quick Start

```bash
cd packages/web
npm install
npm run dev
```

## Build Commands

- `npm run dev` - Start development server
- `npm run build:prod` - Build for production
- `npm run preview` - Preview production build
- `npm run analyze` - Analyze bundle size

## Documentation

See `packages/web/BUILD_CONFIGURATION.md` for detailed build configuration documentation.

## Key Features

✅ Vite for lightning-fast builds
✅ Production bundle optimization (<500KB gzipped)
✅ Environment variable handling
✅ Code splitting with vendor chunks
✅ Gzip and Brotli compression
✅ Bundle size analysis
✅ Source maps for debugging
✅ Asset optimization (images, fonts)

## Production Build Verification

Current production build metrics:
- Total JS (gzipped): ~61 KB
- Total JS (raw): ~195 KB
- Build time: ~2 seconds

All acceptance criteria met ✅
