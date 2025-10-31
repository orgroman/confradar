# Vercel Deployment Setup - Next Steps

This document outlines the remaining steps to complete the Vercel deployment setup for the ConfRadar frontend.

## What Has Been Configured

✅ Created `.github/workflows/deploy-vercel.yml` workflow that:
- Automatically retrieves Vercel secrets from Azure Key Vault
- Automatically deploys preview versions on pull requests
- Automatically deploys to production on main branch merges
- Posts preview URLs as PR comments
- Uses Vercel CLI for deployment
- Authenticates with Azure using OpenID Connect (OIDC)

✅ Updated documentation:
- Created `wiki/Deployment.md` with comprehensive deployment guide
- Updated `wiki/Home.md` to link to deployment documentation
- Added deployment status badges to `README.md`

✅ Verified configuration:
- Workflow YAML syntax is valid
- `.gitignore` already excludes `.vercel` directory

## Required: GitHub Secrets Configuration

The workflow uses **Azure Key Vault integration** to automatically retrieve Vercel secrets. This requires configuring Azure authentication in GitHub.

### 1. Configure Azure Service Principal for GitHub Actions

The workflow uses OpenID Connect (OIDC) to authenticate with Azure without storing credentials.

**Required GitHub Secrets**:
Go to: https://github.com/orgroman/confradar/settings/secrets/actions

Add three repository secrets for Azure authentication:
1. Name: `AZURE_CLIENT_ID`, Value: [Azure Service Principal Client ID]
2. Name: `AZURE_TENANT_ID`, Value: [Azure Tenant ID]
3. Name: `AZURE_SUBSCRIPTION_ID`, Value: `8592e500-3312-4991-9d2a-2b97e43b1810`

**Setting up Azure OIDC for GitHub Actions**:

Follow the official guide: https://learn.microsoft.com/en-us/azure/developer/github/github-actions-key-vault

Key steps:
1. Create or use existing Azure Service Principal
2. Configure federated credentials for GitHub Actions
3. Grant Service Principal access to Key Vault (`kvconfradar`)
4. Add the Service Principal credentials to GitHub Secrets

### 2. Verify Vercel Secrets in Azure Key Vault

Ensure the following secrets exist in Azure Key Vault (`kvconfradar`) with these exact names:

- `VERCEL-TOKEN` - Vercel API authentication token
- `VERCEL-ORG-ID` - Vercel organization or team ID  
- `VERCEL-PROJECT-ID` - Vercel project ID for confradar frontend

**Note**: The workflow retrieves these secrets automatically from Key Vault. You do NOT need to add them manually to GitHub Secrets.

## Vercel Project Configuration

Ensure the Vercel project is configured with:

### Basic Settings
- **Framework Preset**: Next.js (should auto-detect)
- **Root Directory**: `web/`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `.next` (auto-detected)
- **Install Command**: `npm install` (auto-detected)
- **Node.js Version**: 20.x

### Environment Variables

Configure in Vercel project settings (https://vercel.com/[your-org]/[project]/settings/environment-variables):

#### Preview Environment
- `NEXT_PUBLIC_API_URL`: URL for preview/staging backend API
  - Example: `https://api-preview.confradar.dev`

#### Production Environment
- `NEXT_PUBLIC_API_URL`: URL for production backend API
  - Example: `https://api.confradar.dev`

**Note**: Only environment variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. Do not expose sensitive secrets.

## Verification Steps

Once secrets are configured:

1. **Test Preview Deployment**:
   - Create a test PR with a change to any file in `web/`
   - Verify workflow runs successfully in Actions tab
   - Check that preview URL is posted as a PR comment
   - Visit preview URL to verify deployment

2. **Test Production Deployment**:
   - Merge a PR to main branch with changes to `web/`
   - Verify workflow runs successfully in Actions tab
   - Check deployment in Vercel dashboard
   - Visit production URL to verify deployment

3. **Monitor Status**:
   - Check GitHub Actions: https://github.com/orgroman/confradar/actions/workflows/deploy-vercel.yml
   - Check Vercel dashboard: https://vercel.com/

## Workflow Details

### Preview Deployments (Pull Requests)
- Triggers on: PR opened/synchronized to `main` with `web/**` changes
- Deploys to: Unique preview URL (e.g., `confradar-xyz123.vercel.app`)
- Notification: PR comment with deployment URL
- Environment: Preview

### Production Deployments (Main Branch)
- Triggers on: Push to `main` branch with `web/**` changes
- Deploys to: Production domain (configured in Vercel)
- Notification: GitHub Actions summary
- Environment: Production

## Troubleshooting

### Azure authentication fails
- Verify Azure Service Principal is configured correctly
- Check `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_SUBSCRIPTION_ID` in GitHub Secrets
- Ensure federated credentials are configured for GitHub Actions OIDC
- Verify Service Principal has `Get` and `List` permissions on Key Vault secrets
- Check Azure Portal > Key Vault > Access policies

### Workflow fails with "Resource not accessible by integration"
- Ensure GitHub Actions has proper permissions in repository settings
- Check: Settings > Actions > General > Workflow permissions
- Should be set to "Read and write permissions"

### Cannot retrieve secrets from Key Vault
- Verify secrets exist in Key Vault with exact names: `VERCEL-TOKEN`, `VERCEL-ORG-ID`, `VERCEL-PROJECT-ID`
- Check Service Principal has access to Key Vault
- Review workflow logs for specific error messages
- Verify Key Vault name is correct: `kvconfradar`

### Deployment fails with authentication error
- Check that `VERCEL-TOKEN` in Key Vault is valid
- Verify token hasn't expired in Vercel account settings
- Generate new token if needed: https://vercel.com/account/tokens
- Update token in Azure Key Vault

### Deployment fails with "Project not found"
- Verify `VERCEL-ORG-ID` and `VERCEL-PROJECT-ID` in Key Vault are correct
- Get correct IDs from Vercel project settings
- Or run `vercel link` in `web/` directory and check `.vercel/project.json`
- Update values in Azure Key Vault if needed

### Build succeeds but deployment fails
- Check Vercel project settings (root directory, build command)
- Review environment variables in Vercel dashboard
- Check Vercel deployment logs for errors

## Additional Resources

- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Vercel GitHub Actions](https://vercel.com/docs/deployments/git/vercel-for-github)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Wiki: Deployment Guide](https://github.com/orgroman/confradar/wiki/Deployment)

## Support

For issues:
1. Check GitHub Actions workflow logs
2. Check Vercel deployment logs in dashboard
3. Review this document and wiki documentation
4. Create issue in repository with logs and error messages
