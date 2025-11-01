# Frontend Image Registry

This document describes the container image registry workflow for the ConfRadar frontend application.

## Overview

The frontend Docker image is automatically built and published to GitHub Container Registry (GHCR) on every push to the `main` branch that affects the `web/` directory.

## Registry Location

Images are published to:
```
ghcr.io/orgroman/confradar/web
```

## Available Tags

The workflow automatically generates multiple tags for each build:

- **`latest`**: Latest build from main branch
- **`sha-<short>`**: Git commit SHA (short format, 7 characters)
- **`main`**: Main branch (same as latest)

### Examples

```bash
# Pull latest image
docker pull ghcr.io/orgroman/confradar/web:latest

# Pull specific commit
docker pull ghcr.io/orgroman/confradar/web:sha-136663f
```

## Authentication

### Public Access

Images are publicly readable. No authentication is required to pull:

```bash
docker pull ghcr.io/orgroman/confradar/web:latest
```

### For Private Repositories

If the repository is private, authenticate with a GitHub Personal Access Token:

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker pull ghcr.io/orgroman/confradar/web:latest
```

## Using the Published Image

### With Docker

```bash
# Run the frontend container
docker run -d \
  --name confradar-web \
  -p 3100:3100 \
  -e NODE_ENV=production \
  ghcr.io/orgroman/confradar/web:latest
```

### With Docker Compose

Update your `docker-compose.yml`:

```yaml
services:
  web-prod:
    image: ghcr.io/orgroman/confradar/web:latest
    ports:
      - "3101:3100"
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3100/api/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) })"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Then run:

```bash
docker-compose pull web-prod
docker-compose up -d web-prod
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: confradar-web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: confradar-web
  template:
    metadata:
      labels:
        app: confradar-web
    spec:
      containers:
      - name: web
        image: ghcr.io/orgroman/confradar/web:latest
        ports:
        - containerPort: 3100
        env:
        - name: NODE_ENV
          value: "production"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 3100
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 3100
          initialDelaySeconds: 10
          periodSeconds: 5
```

## Build Process

### Workflow Trigger

The workflow runs on:
1. Push to `main` branch with changes in `web/` or `.github/workflows/publish-frontend.yml`
2. Manual workflow dispatch

### Build Stages

The workflow performs:
1. **Checkout** - Clone repository code
2. **Setup Buildx** - Enable Docker BuildKit with advanced features
3. **Login** - Authenticate to GHCR using `GITHUB_TOKEN`
4. **Metadata** - Generate image tags and labels
5. **Build & Push** - Build image with layer caching and push to registry

### Build Caching

GitHub Actions cache is used to speed up builds:
- **Cache source**: Previous build layers from GitHub Actions cache
- **Cache target**: New layers stored in GitHub Actions cache
- **Mode**: `max` (caches all layers, not just final image)

Typical build times:
- **Cold cache** (first build): ~5-10 minutes
- **Warm cache** (incremental): ~1-3 minutes

## Image Details

### Base Image
- **Base**: `node:20-alpine`
- **Size**: ~200MB (production standalone build)
- **Security**: Runs as non-root user (`nextjs:nodejs` UID 1001)

### Contents
- Next.js standalone build (`.next/standalone/`)
- Static assets (`.next/static/`, `public/`)
- Node.js runtime (Node 20 LTS)

### Health Check
Built-in health check at `/api/health`:
```bash
curl http://localhost:3100/api/health
# Returns: {"status":"healthy","timestamp":"2025-11-01T...","service":"confradar-web"}
```

## Debugging

### View Workflow Runs

1. Go to [Actions tab](https://github.com/orgroman/confradar/actions)
2. Select "Publish Frontend Image" workflow
3. View logs for each step

### Check Image Details

```bash
# Inspect image
docker inspect ghcr.io/orgroman/confradar/web:latest

# View image history
docker history ghcr.io/orgroman/confradar/web:latest

# Check image size
docker images ghcr.io/orgroman/confradar/web
```

### Test Image Locally

```bash
# Pull and run
docker pull ghcr.io/orgroman/confradar/web:latest
docker run -d -p 3100:3100 --name test-web ghcr.io/orgroman/confradar/web:latest

# Check logs
docker logs test-web

# Test health endpoint
curl http://localhost:3100/api/health

# Cleanup
docker stop test-web && docker rm test-web
```

## Troubleshooting

### Build Failures

**Symptom**: Workflow fails during build
- Check workflow logs in Actions tab
- Verify `web/Dockerfile.prod` is valid
- Ensure `web/next.config.mjs` has `output: 'standalone'`

### Authentication Issues

**Symptom**: Cannot pull image
- Verify repository visibility (public vs private)
- For private repos, ensure PAT has `read:packages` scope
- Check GHCR package permissions in repository settings

### Image Won't Start

**Symptom**: Container exits immediately
- Check logs: `docker logs <container-name>`
- Verify environment variables are set correctly
- Ensure port 3100 is not already in use

### Health Check Fails

**Symptom**: Container unhealthy
- Check if app is listening on port 3100
- Verify `/api/health` endpoint exists
- Review application logs for errors

## Maintenance

### Cleaning Up Old Images

GitHub Actions cache and old images can accumulate. To manage:

1. **Via GitHub UI**:
   - Go to repository Settings → Packages
   - Select `confradar/web` package
   - Delete old versions

2. **Via CLI** (requires `gh` CLI):
```bash
# List package versions
gh api /users/orgroman/packages/container/confradar%2Fweb/versions

# Delete specific version
gh api -X DELETE /users/orgroman/packages/container/confradar%2Fweb/versions/<VERSION_ID>
```

### Cache Management

GitHub Actions cache has a 10GB limit per repository. Old cache entries are automatically evicted. To manually clear:

1. Go to repository Settings → Actions → Caches
2. Delete old cache entries

## Security Considerations

1. **Image Scanning**: Consider adding vulnerability scanning (e.g., Trivy, Snyk)
2. **Secret Management**: Never include secrets in image or environment variables
3. **OIDC Authentication**: For production deployments, use OIDC instead of PATs
4. **Non-root User**: Image runs as UID 1001, not root
5. **Minimal Base**: Alpine Linux reduces attack surface

## Future Enhancements

- [ ] Add image vulnerability scanning in workflow
- [ ] Implement multi-platform builds (arm64 support)
- [ ] Add semantic versioning tags on releases
- [ ] Set up image signing with Cosign
- [ ] Configure automatic image cleanup policy

## Related Documentation

- [Production Frontend Setup](./PRODUCTION_FRONTEND.md)
- [Dockerfile.prod](../web/Dockerfile.prod)
- [GitHub Actions Workflow](../.github/workflows/publish-frontend.yml)
- [GHCR Documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
