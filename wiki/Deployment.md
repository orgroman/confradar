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
