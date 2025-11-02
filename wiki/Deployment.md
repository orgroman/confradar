# Deployment

This page documents the deployment processes for ConfRadar components.

## Frontend Deployment (Vercel)

The Next.js frontend (`web/`) is automatically deployed to Vercel via **Vercel's native GitHub integration**.

### Vercel GitHub Integration

Vercel's GitHub App provides automatic deployments without requiring custom workflows:

- **Automatic Detection**: Vercel automatically detects the Next.js project and configures build settings
- **Preview Deployments**: Automatically created for all pull requests
- **Production Deployments**: Automatically deployed when changes are pushed to the main branch
- **PR Comments**: Deployment URLs are automatically posted as comments on pull requests
- **No Workflow Required**: Deployment is handled entirely by Vercel's infrastructure

### Prerequisites

The Vercel GitHub App must be installed and the project must be linked to the repository.

**Vercel Project Configuration**:
- **Framework Preset**: Next.js (auto-detected)
- **Root Directory**: `web/`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `.next` (auto-detected)
- **Install Command**: `npm install` (auto-detected)
- **Node.js Version**: 20.x

### Environment Variables

Configure environment variables in the Vercel dashboard for your project:

**Preview Environment**:
- `NEXT_PUBLIC_API_URL` - Backend API endpoint for preview/staging
  - Example: `https://api-preview.confradar.dev`

**Production Environment**:
- `NEXT_PUBLIC_API_URL` - Backend API endpoint for production
  - Example: `https://api.confradar.dev`

**Important**: Only `NEXT_PUBLIC_*` prefixed variables are exposed to the browser. Never expose sensitive secrets in these variables.

### How It Works

1. **On Pull Request**:
   - Vercel detects new PR or changes to existing PR
   - Automatically builds the Next.js application
   - Deploys to a unique preview URL
   - Posts deployment URL as a PR comment
   - Uses preview environment variables

2. **On Merge to Main**:
   - Vercel detects push to main branch
   - Automatically builds the Next.js application with production settings
   - Deploys to production domain
   - Uses production environment variables

### Vercel Project Setup

To link or verify the Vercel project:

1. **Install Vercel GitHub App** (if not already installed):
   - Visit: https://vercel.com/new
   - Select "Import Git Repository"
   - Authorize GitHub access
   - Select the `orgroman/confradar` repository

2. **Configure Project** (CRITICAL):
   - **Root Directory**: MUST be set to `web/` in Vercel project settings
   - Go to: Vercel Dashboard > Project > Settings > General > Root Directory
   - Enter: `web/`
   - Save the setting
   - Vercel will auto-detect Next.js and configure build settings
   - Add environment variables (see above)

3. **Verify Integration**:
   - Check repository settings in GitHub
   - Ensure Vercel app is installed and has access
   - Trigger a test deployment to verify configuration
   - Create a test PR to verify preview deployment works
- **Output Directory**: `.next` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

### Environment Variables

Configure build-time environment variables in Vercel project settings:

- `NEXT_PUBLIC_API_URL` - Backend API endpoint URL
  - Preview: `https://api-preview.confradar.dev` (or similar)
  - Production: `https://api.confradar.dev` (or actual production API URL)

**Important**: Only `NEXT_PUBLIC_*` prefixed variables are exposed to the browser. Never expose sensitive secrets in these variables.

### Manual Deployment

To manually deploy from your local machine:

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Link to project (first time only):
   ```bash
   cd web/
   vercel link
   ```

4. Deploy preview:
   ```bash
   cd web/
   vercel
   ```

5. Deploy to production:
   ```bash
   cd web/
   vercel --prod
   ```

### Monitoring Deployments

- **Vercel Dashboard**: https://vercel.com/ - View all deployments, logs, and analytics
- **GitHub PR Comments**: Vercel automatically posts deployment URLs on pull requests
- **Preview URLs**: Unique per deployment (e.g., `confradar-xyz123.vercel.app`)
- **Production URL**: Configure custom domain in Vercel project settings

### Troubleshooting

**Vercel GitHub App not working**:
- Verify Vercel GitHub App is installed: Check repository Settings > Integrations
- Ensure the app has access to the repository
- Check Vercel project is linked to the correct repository
- Verify project settings in Vercel dashboard

**Preview deployments not appearing**:
- Check if Vercel detected the `web/` directory correctly
- Verify Root Directory is set to `web/` in Vercel project settings
- Ensure GitHub App has permissions to post comments
- Check Vercel deployment logs for errors

**Build fails with "No Next.js version detected"**:

This is the most common deployment error. It means Vercel can't find the Next.js installation.

**Solution**:
1. Open Vercel Dashboard
2. Go to your project > Settings > General
3. Find "Root Directory" field
4. Change it to: `web/`
5. Click "Save"
6. Redeploy or push a new commit

**Why**: The repository root doesn't contain Next.js. The Next.js app is in the `web/` subdirectory.

**Other build failures**:
- Review build logs in Vercel dashboard
- Verify environment variables are set correctly (NEXT_PUBLIC_API_URL)
- Check Node.js version is compatible (20.x recommended)
- Ensure all dependencies are in `package.json`
- Frontend CI should pass: `.github/workflows/frontend.yml`
- Verify `vercel.json` exists in `web/` directory with correct configuration
- Confirm Root Directory is set to `web/` in Vercel Dashboard settings

**Production deployment not updating**:
- Verify changes were merged to `main` branch
- Check Vercel project production branch setting
- Review production deployment logs in Vercel dashboard

**Environment variables not working**:
- Ensure variables are prefixed with `NEXT_PUBLIC_` for client-side access
- Verify variables are set for the correct environment (preview/production)
- Redeploy after changing environment variables

### Advanced Configuration

**Custom Domain**:
1. Go to Vercel project settings > Domains
2. Add your custom domain
3. Configure DNS records as instructed by Vercel
4. Wait for SSL certificate provisioning

**Git Integration Settings**:
- Configure in Vercel project settings > Git
- Set production branch (default: `main`)
- Configure automatic deployments for branches
- Set ignored build step (if needed)

### Best Practices

1. **Environment Variables**: Always use `NEXT_PUBLIC_` prefix for client-side variables
2. **Root Directory**: Ensure `web/` is set as root directory in Vercel project settings
3. **Frontend CI**: Let frontend CI pass before merging PRs
4. **Review Previews**: Test preview deployments before merging to production
5. **Monitor Deployments**: Check Vercel dashboard after merging important changes

## Backend Deployment

Backend deployment documentation to be added when backend hosting is configured.

### Docker Compose Healthchecks

All core services in `docker-compose.yml` include healthchecks for improved reliability, observability, and orchestration. Healthchecks enable Docker and orchestration tools to:
- Detect service failures automatically
- Make informed restart decisions
- Enable dependency ordering (services wait for healthy dependencies)
- Support monitoring and alerting systems

#### Service Healthcheck Overview

| Service | Healthcheck Method | Endpoint/Command | Interval | Timeout | Start Period | Retries |
|---------|-------------------|------------------|----------|---------|--------------|---------|
| **postgres** | Shell command | `pg_isready -U confradar` | 5s | 5s | default | 5 |
| **litellm** | HTTP GET | `http://localhost:4000/health` | 15s | 5s | 10s | 5 |
| **dagster-daemon** | CLI command | `uv run dagster-daemon liveness-check` | 20s | 8s | 30s | 5 |
| **dagster-webserver** | HTTP GET | `http://localhost:3000/server_info` | 10s | 5s | 20s | 5 |
| **web** (dev) | HTTP GET | `http://localhost:3100/` (200 or 304) | 15s | 10s | 60s | 5 |
| **web-prod** | HTTP GET | `http://localhost:3100/api/health` | 30s | 3s | 10s | 3 |

#### Healthcheck Parameters Explained

- **`interval`**: How often Docker runs the healthcheck (e.g., every 15 seconds)
- **`timeout`**: Maximum time allowed for the healthcheck command to complete
- **`start_period`**: Grace period during container startup; failed checks during this time don't count toward retries
- **`retries`**: Number of consecutive failures required before marking the container as unhealthy

#### Service Dependencies

Services use `depends_on` with `condition: service_healthy` to enforce startup order:

1. **postgres** starts first (no dependencies)
2. **litellm** waits for postgres to be healthy
3. **dagster-daemon** waits for postgres and liteLLM to be healthy
4. **dagster-webserver** waits for postgres, liteLLM, and dagster-daemon to be healthy
5. **web** service has no health dependencies (frontend can start independently)

This ensures that:
- Dagster services only start after the database is ready
- The webserver waits for the daemon to be operational
- Services restart in the correct order if dependencies fail

#### Monitoring Healthcheck Status

**View all service health statuses:**
```bash
docker compose ps
```

Output shows health in the `STATUS` column:
```
NAME                STATUS
confradar-postgres  Up 5 minutes (healthy)
litellm-proxy       Up 4 minutes (healthy)
dagster-daemon      Up 3 minutes (healthy)
dagster-webserver   Up 2 minutes (healthy)
confradar-web       Up 1 minute (healthy)
```

**Watch health status in real-time:**
```bash
watch -n 2 'docker compose ps'
```

**Inspect detailed health information for a specific service:**
```bash
docker inspect <container-name> --format='{{json .State.Health}}' | jq
```

Example:
```bash
docker inspect dagster-webserver --format='{{json .State.Health}}' | jq
```

**View recent healthcheck logs:**
```bash
docker inspect dagster-webserver --format='{{range .State.Health.Log}}{{.Output}}{{end}}'
```

#### Troubleshooting Failed Healthchecks

##### General Debugging Steps

1. **Check container logs:**
   ```bash
   docker compose logs <service-name>
   ```

2. **Check healthcheck status and recent results:**
   ```bash
   docker inspect <container-name> | jq '.[0].State.Health'
   ```

3. **Manually run the healthcheck command inside the container:**
   ```bash
   docker exec <container-name> <healthcheck-command>
   ```

4. **Restart the service:**
   ```bash
   docker compose restart <service-name>
   ```

5. **Rebuild and restart if configuration changed:**
   ```bash
   docker compose up -d --build <service-name>
   ```

##### Service-Specific Troubleshooting

**PostgreSQL (`postgres`)**

*Issue*: `pg_isready` fails

*Solutions*:
- Verify PostgreSQL is actually running: `docker compose logs postgres`
- Check for startup errors or crashes
- Ensure `POSTGRES_USER` matches the healthcheck username
- Check disk space: `df -h`

*Manual test*:
```bash
docker exec confradar-postgres pg_isready -U confradar
```

**LiteLLM Proxy (`litellm`)**

*Issue*: `/health` endpoint not responding

*Solutions*:
- Check LiteLLM logs: `docker compose logs litellm`
- Verify `OPENAI_API_KEY` or `CONFRADAR_SA_OPENAI` is set correctly
- Test the endpoint manually:
  ```bash
  docker exec litellm-proxy python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:4000/health').read())"
  ```
- If timeout issues, increase `timeout` in healthcheck configuration

*Manual test*:
```bash
curl http://localhost:4000/health
```

**Dagster Daemon (`dagster-daemon`)**

*Issue*: `dagster-daemon liveness-check` fails or times out

*Solutions*:
- Check daemon logs: `docker compose logs dagster-daemon`
- Verify database connection: ensure `DATABASE_URL` is correct
- Check if daemon is actually running: `docker exec dagster-daemon ps aux | grep dagster`
- If timing out during startup, increase `start_period` (currently 30s accounts for uv cold starts)
- Ensure Dagster version ≥1.12 (supports `liveness-check` command)

*Manual test*:
```bash
docker exec dagster-daemon uv run dagster-daemon liveness-check
```

Expected output: Exit code 0 when healthy.

**Dagster Webserver (`dagster-webserver`)**

*Issue*: `/server_info` endpoint not responding

*Solutions*:
- Check webserver logs: `docker compose logs dagster-webserver`
- Verify daemon is healthy first (webserver depends on it)
- Test endpoint manually:
  ```bash
  curl http://localhost:3000/server_info
  ```
- Ensure database connection is working

*Manual test*:
```bash
docker exec dagster-webserver curl -f http://localhost:3000/server_info
```

**Web Service - Dev Mode (`web`)**

*Issue*: Healthcheck times out or fails

*Solutions*:
- Check Next.js dev server logs: `docker compose logs web`
- Dev mode needs time for initial compilation; `start_period: 60s` should accommodate this
- Verify `npm install` completed successfully
- If timing out during compilation, increase `timeout` (currently 10s) or `start_period`
- Check Node.js errors or missing dependencies

*Common causes*:
- Initial Next.js compilation takes longer than expected
- npm install is slow or failing
- Missing or broken dependencies

*Manual test*:
```bash
docker exec confradar-web node -e "require('http').get('http://localhost:3100/', (r) => console.log(r.statusCode))"
```

Or access directly:
```bash
curl -I http://localhost:3100/
```

**Web Service - Production Mode (`web-prod`)**

*Issue*: `/api/health` endpoint fails

*Solutions*:
- Verify production build completed: `docker compose logs web-prod`
- Ensure `/api/health` route exists in production build
- Check for build or runtime errors
- Production healthcheck expects 200 OK; verify endpoint implementation

*Manual test*:
```bash
curl http://localhost:3101/api/health
```

#### Common Healthcheck Patterns

**HTTP-based healthcheck (simple):**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 3s
  retries: 3
```

**HTTP-based healthcheck (Python urllib, no curl required):**
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request,sys; r=urllib.request.urlopen('http://localhost:4000/health', timeout=3); sys.exit(0) if r.status==200 else sys.exit(1)"]
  interval: 15s
  timeout: 5s
  retries: 5
```

**HTTP-based healthcheck (Node.js, no curl required):**
```yaml
healthcheck:
  test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"]
  interval: 10s
  timeout: 5s
  retries: 5
```

**CLI-based healthcheck:**
```yaml
healthcheck:
  test: ["CMD", "uv", "run", "dagster-daemon", "liveness-check"]
  interval: 20s
  timeout: 8s
  start_period: 30s
  retries: 5
```

**Shell command healthcheck:**
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 5s
  timeout: 5s
  retries: 5
```

#### Adding Healthchecks to New Services

When adding a new service to `docker-compose.yml`, follow these guidelines:

1. **Choose the appropriate healthcheck method:**
   - HTTP-based for web services or APIs with health endpoints
   - CLI-based for services with built-in health commands
   - Shell-based for simple checks (process existence, file availability)

2. **Set appropriate timing parameters:**
   - `interval`: Balance between responsiveness and overhead (10-30s is typical)
   - `timeout`: Allow enough time for the service to respond (3-10s)
   - `start_period`: Account for initialization time (10-60s depending on service)
   - `retries`: Enough to avoid false positives (3-5 is typical)

3. **Test the healthcheck:**
   ```bash
   # Start the service
   docker compose up -d <service-name>
   
   # Monitor health status
   watch -n 2 'docker compose ps <service-name>'
   
   # Check detailed health info
   docker inspect <container-name> --format='{{json .State.Health}}' | jq
   ```

4. **Add service dependencies if needed:**
   ```yaml
   depends_on:
     database:
       condition: service_healthy
     cache:
       condition: service_healthy
   ```

5. **Document the healthcheck in this wiki.**

#### Best Practices

1. **Always provide a healthcheck for production services** - Enables automated failure detection and recovery.

2. **Use lightweight healthcheck commands** - Avoid expensive operations; healthchecks run frequently and should complete quickly.

3. **Set realistic timing parameters:**
   - Fast services (APIs): `interval: 10s, timeout: 3s, start_period: 10s`
   - Slow services (databases, heavy apps): `interval: 30s, timeout: 10s, start_period: 60s`

4. **Test healthchecks during development:**
   - Verify they pass when the service is healthy
   - Verify they fail when the service is unhealthy
   - Check they don't cause false positives during normal operation

5. **Use `start_period` generously** - It's better to wait a bit longer during startup than to have false failures.

6. **Avoid dependencies on external services in healthchecks** - Healthchecks should test the service itself, not external dependencies (use separate monitoring for that).

7. **Monitor healthcheck overhead** - Frequent checks can add load; balance responsiveness with resource usage.

8. **Document expected behavior** - Note any peculiarities or special considerations in comments or documentation.

#### CI/CD Integration

Healthchecks are valuable in CI/CD pipelines to validate services before running tests:

```yaml
# Example: GitHub Actions waiting for services to be healthy
- name: Wait for services
  run: |
    timeout 120 bash -c 'until docker compose ps | grep -q "healthy"; do sleep 2; done'
```

Or use Docker Compose's built-in wait functionality:
```yaml
# In docker-compose.yml
services:
  test-runner:
    depends_on:
      web:
        condition: service_healthy
      api:
        condition: service_healthy
```

#### Monitoring in Production

For production deployments, integrate healthchecks with monitoring tools:

- **Prometheus**: Export healthcheck metrics
- **Datadog/New Relic**: Use container monitoring integrations
- **AWS ECS/ELB**: Configure health checks matching Docker healthcheck logic
- **Kubernetes**: Use readiness and liveness probes based on the same health endpoints

Ensure production health endpoints are:
- Authenticated if the service requires auth
- Lightweight and fast (< 100ms response time)
- Do not trigger side effects (read-only)

#### Related Documentation

- [Development Guide](Development-Guide) - Local development and Docker Compose setup
- [Architecture](Architecture) - System architecture and service interaction
- [docker-compose.yml](../docker-compose.yml) - Service definitions and healthcheck configurations

## Secrets Management

ConfRadar uses **Azure Key Vault** for centralized secrets management in both local development and CI/CD pipelines.

### Azure Key Vault Setup

**Key Vault Name**: `kvconfradar`  
**Azure Subscription ID**: `8592e500-3312-4991-9d2a-2b97e43b1810`

All sensitive credentials (API keys, connection strings, service account tokens) are stored in Azure Key Vault and retrieved at runtime or during CI/CD execution.

### GitHub Actions Integration

GitHub Actions can securely access Azure Key Vault secrets using **federated identity (OIDC)** without storing long-lived secrets.

**Official Documentation**: [Use GitHub Actions to connect to Azure Key Vault](https://learn.microsoft.com/en-us/azure/developer/github/github-actions-key-vault)

#### How It Works

1. **Federated Identity**: GitHub's OIDC provider issues tokens that Azure trusts, eliminating the need for secrets or passwords.
2. **Azure Login**: GitHub Actions workflows authenticate to Azure using `azure/login@v1` with federated credentials.
3. **Retrieve Secrets**: Use `azure/get-keyvault-secrets@v1` or Azure CLI to fetch secrets from Key Vault.
4. **Inject into Workflow**: Retrieved secrets are available as environment variables for subsequent steps.

#### Required GitHub Secrets

The following **GitHub repository secrets** must be configured for Azure Key Vault integration:

- `AZURE_CLIENT_ID` - Service principal / managed identity client ID
- `AZURE_TENANT_ID` - Azure Active Directory tenant ID  
- `AZURE_SUBSCRIPTION_ID` - Azure subscription ID (already documented: `8592e500-3312-4991-9d2a-2b97e43b1810`)

**Note**: These secrets are already configured in the `orgroman/confradar` repository.

#### Example Workflow

```yaml
name: Deploy with Secrets from Azure Key Vault

on:
  push:
    branches: [main]

permissions:
  id-token: write  # Required for OIDC token
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC)
        uses: azure/login@v1
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Get secrets from Key Vault
        uses: azure/get-keyvault-secrets@v1
        with:
          keyvault: "kvconfradar"
          secrets: 'OPENAI-API-KEY, VERCEL-TOKEN'
        id: keyvault

      - name: Use secrets in deployment
        env:
          OPENAI_API_KEY: ${{ steps.keyvault.outputs.OPENAI-API-KEY }}
          VERCEL_TOKEN: ${{ steps.keyvault.outputs.VERCEL-TOKEN }}
        run: |
          echo "Deploying with secrets from Key Vault..."
          # Your deployment commands here
```

### Best Practices

1. **Single Source of Truth**: Store all secrets in Azure Key Vault; avoid duplicating in GitHub Secrets unless required for OIDC authentication.
2. **Use Federated Identity**: Prefer OIDC-based authentication over service principal secrets for GitHub Actions.
3. **Principle of Least Privilege**: Grant Key Vault access policies only to identities that need them (GitHub Actions service principal, developers).
4. **Audit Access**: Enable Azure Key Vault logging and monitor secret access patterns.
5. **Rotate Secrets Regularly**: Update secrets in Key Vault; workflows will automatically use the latest values.
6. **Never Commit Secrets**: Secrets must never be committed to the repository, even in examples or documentation.

### Local Development

For local development, authenticate to Azure and retrieve secrets manually or via Azure CLI:

```powershell
# Login to Azure
az login

# Retrieve a secret
az keyvault secret show --vault-name kvconfradar --name OPENAI-API-KEY --query value -o tsv

# Set as environment variable
$env:OPENAI_API_KEY = $(az keyvault secret show --vault-name kvconfradar --name OPENAI-API-KEY --query value -o tsv)
```

Alternatively, use **Azure MCP** to access Key Vault secrets interactively during development sessions.

### Related Documentation

- [Development Guide](Development-Guide) - Local development setup and secret management
- [Microsoft Learn: GitHub Actions + Azure Key Vault](https://learn.microsoft.com/en-us/azure/developer/github/github-actions-key-vault)
- [Azure Key Vault Documentation](https://learn.microsoft.com/en-us/azure/key-vault/)

## Related

- [Architecture](Architecture) - System architecture overview
- [Development Guide](Development-Guide) - Local development setup
- [Frontend CI](.github/workflows/frontend.yml) - Frontend testing and building
- [Vercel Documentation](https://vercel.com/docs) - Official Vercel documentation
