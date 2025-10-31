# Deployment

This page documents the deployment processes for ConfRadar components.

## Frontend Deployment (Vercel)

The Next.js frontend (`web/`) is automatically deployed to Vercel via GitHub Actions.

### Deployment Workflow

The deployment process is handled by the `.github/workflows/deploy-vercel.yml` workflow:

- **Preview Deployments**: Triggered on pull requests to `main` when `web/**` files change
- **Production Deployments**: Triggered on push to `main` branch when `web/**` files change

### Prerequisites

The following secrets must be configured in GitHub repository secrets:

- `VERCEL_TOKEN` - Vercel API token for authentication
- `VERCEL_ORG_ID` - Vercel organization/team ID
- `VERCEL_PROJECT_ID` - Vercel project ID for the confradar frontend

These secrets are stored in Azure Key Vault (`kvconfradar`) and can be synced to GitHub Secrets.

### How It Works

1. **On Pull Request**:
   - Workflow triggers when PR is opened/updated with `web/**` changes
   - Installs Vercel CLI
   - Pulls Vercel environment info for preview environment
   - Builds the Next.js application
   - Deploys to a unique preview URL
   - Posts deployment URL as a PR comment

2. **On Merge to Main**:
   - Workflow triggers when changes are pushed to `main`
   - Installs Vercel CLI
   - Pulls Vercel environment info for production environment
   - Builds the Next.js application with production settings
   - Deploys to production domain
   - Outputs deployment URL in workflow summary

### Vercel Project Configuration

The Vercel project should be configured with:

- **Framework Preset**: Next.js
- **Root Directory**: `web/`
- **Build Command**: `npm run build` (auto-detected)
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

- View deployment logs in Vercel dashboard: https://vercel.com/
- View GitHub Actions workflow runs: https://github.com/orgroman/confradar/actions/workflows/deploy-vercel.yml
- Preview URLs are unique per deployment and posted on PRs
- Production URL: [To be configured in Vercel project settings]

### Troubleshooting

**Deployment fails with authentication error**:
- Verify `VERCEL_TOKEN` secret is set correctly in GitHub repository secrets
- Check token hasn't expired in Vercel settings

**Deployment fails with project not found**:
- Verify `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID` are correct
- Check project exists in Vercel dashboard

**Build fails**:
- Check frontend CI workflow passes first (`.github/workflows/frontend.yml`)
- Review build logs in Vercel dashboard
- Verify environment variables are set correctly

**Preview deployment succeeds but production fails**:
- Check production environment variables in Vercel
- Verify no preview-specific configuration is breaking production

### Best Practices

1. **Always test locally first**: Run `npm run build` in `web/` before pushing
2. **Run Frontend CI**: Ensure linting, tests, and builds pass before deployment
3. **Review preview deployments**: Test preview URLs before merging PRs
4. **Monitor production**: Check production deployment after merging
5. **Use environment-specific URLs**: Ensure preview and production use different backend API URLs

## Backend Deployment

Backend deployment documentation to be added when backend hosting is configured.

## Related

- [Architecture](Architecture) - System architecture overview
- [Development Guide](Development-Guide) - Local development setup
- [Frontend CI](.github/workflows/frontend.yml) - Frontend testing and building
- [Vercel Deployment Workflow](.github/workflows/deploy-vercel.yml) - Deployment automation
