# Production Deployment Guide

This document explains how to build and run the Next.js frontend in production mode.

## Quick Start

### Build and Run Production Image

```bash
# Build and start the production service
docker-compose --profile production up --build web-prod

# Or run in detached mode
docker-compose --profile production up -d --build web-prod
```

The production service will be available at http://localhost:3101

### Stop Production Service

```bash
docker-compose --profile production down
```

## Production Features

### Dockerfile.prod

The production Dockerfile (`web/Dockerfile.prod`) implements:

- ✅ **Multi-stage build** - Separate stages for deps, build, and runtime
- ✅ **Standalone output** - Next.js generates optimized standalone bundle
- ✅ **Minimal runtime image** - Only production dependencies included
- ✅ **Non-root user** - Runs as unprivileged `nextjs` user (UID 1001)
- ✅ **Health check** - Built-in healthcheck endpoint at `/api/health`
- ✅ **Security** - No dev dependencies, minimal attack surface

### Docker Compose Profile

The `web-prod` service:

- Uses production Dockerfile (`Dockerfile.prod`)
- Exposes on port **3101** (to avoid conflict with dev on 3100)
- Has health check configured
- Only starts when `production` profile is active

## Configuration

### Environment Variables

Set these in `docker-compose.yml` under `web-prod.environment`:

```yaml
NODE_ENV: production
NEXT_TELEMETRY_DISABLED: "1"
# NEXT_PUBLIC_API_URL: http://api.confradar.com  # If using external API
```

### Build Arguments

The Dockerfile accepts build arguments:

```bash
docker build \
  --build-arg NODE_ENV=production \
  -f Dockerfile.prod \
  -t confradar-web:latest \
  .
```

## Health Check

The production image includes a health check endpoint:

```bash
# Check health status
curl http://localhost:3101/api/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-11-01T20:00:00.000Z",
  "service": "confradar-web"
}
```

## Troubleshooting

### Container won't start

Check logs:
```bash
docker logs confradar-web-prod
```

### Build failures

Ensure you have a `package-lock.json`:
```bash
cd web
npm install  # This will create package-lock.json
```

### Health check failing

Verify the `/api/health` endpoint exists and returns 200:
```bash
docker exec confradar-web-prod wget -O- http://localhost:3100/api/health
```

## Size Optimization

Current image sizes:
- Dev image (`Dockerfile`): ~500MB (includes dev dependencies)
- Prod image (`Dockerfile.prod`): ~200MB (standalone output only)

## Production Checklist

Before deploying to production:

- [ ] Set `NODE_ENV=production` environment variable
- [ ] Configure `NEXT_PUBLIC_API_URL` if using external API
- [ ] Verify health check returns 200
- [ ] Test image builds successfully
- [ ] Verify no dev dependencies in final image
- [ ] Check container starts without errors
- [ ] Confirm frontend loads in browser

## Related Documentation

- [Next.js Standalone Output](https://nextjs.org/docs/app/api-reference/next-config-js/output)
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Compose Profiles](https://docs.docker.com/compose/profiles/)
