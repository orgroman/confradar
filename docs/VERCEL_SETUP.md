# Vercel Deployment Setup - Next Steps

This document outlines the remaining steps to complete the Vercel deployment setup for the ConfRadar frontend.

## What Has Been Configured

✅ Created `.github/workflows/deploy-vercel.yml` workflow that:
- Automatically deploys preview versions on pull requests
- Automatically deploys to production on main branch merges
- Posts preview URLs as PR comments
- Uses Vercel CLI for deployment

✅ Updated documentation:
- Created `wiki/Deployment.md` with comprehensive deployment guide
- Updated `wiki/Home.md` to link to deployment documentation
- Added deployment status badges to `README.md`

✅ Verified configuration:
- Workflow YAML syntax is valid
- `.gitignore` already excludes `.vercel` directory

## Required: GitHub Secrets Configuration

The workflow requires three GitHub repository secrets that must be retrieved from Azure Key Vault and configured:

### 1. Retrieve Secrets from Azure Key Vault

The secrets are stored in Azure Key Vault (`kvconfradar`). Use Azure MCP or Azure Portal to retrieve:

- `VERCEL_TOKEN` - Vercel API authentication token
- `VERCEL_ORG_ID` - Vercel organization or team ID
- `VERCEL_PROJECT_ID` - Vercel project ID for confradar frontend

### 2. Add Secrets to GitHub Repository

Go to: https://github.com/orgroman/confradar/settings/secrets/actions

Add three new repository secrets:
1. Name: `VERCEL_TOKEN`, Value: [from Azure Key Vault]
2. Name: `VERCEL_ORG_ID`, Value: [from Azure Key Vault]
3. Name: `VERCEL_PROJECT_ID`, Value: [from Azure Key Vault]

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

### Workflow fails with "Resource not accessible by integration"
- Ensure GitHub Actions has proper permissions in repository settings
- Check: Settings > Actions > General > Workflow permissions
- Should be set to "Read and write permissions"

### Deployment fails with authentication error
- Verify `VERCEL_TOKEN` is set correctly in GitHub Secrets
- Check token hasn't expired in Vercel account settings
- Generate new token if needed: https://vercel.com/account/tokens

### Deployment fails with "Project not found"
- Verify `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID` are correct
- Get correct IDs from Vercel project settings
- Or run `vercel link` in `web/` directory and check `.vercel/project.json`

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
