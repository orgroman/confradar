# Vercel Deployment Setup Guide

This document provides instructions for configuring Vercel's native GitHub integration for the ConfRadar frontend.

## Overview

ConfRadar uses **Vercel's native GitHub App integration** for automatic deployments. This approach is simpler and more maintainable than custom GitHub Actions workflows.

**Key Features**:
- Automatic preview deployments for pull requests
- Automatic production deployments on main branch
- PR comments with deployment URLs
- No workflow configuration needed
- Managed entirely through Vercel dashboard

## Setup Steps

### 1. Install Vercel GitHub App

If not already installed:

1. Visit https://vercel.com/new
2. Click "Import Git Repository"
3. Authorize Vercel to access GitHub
4. Select the `orgroman/confradar` repository
5. Complete the integration setup

### 2. Configure Project Settings

In the Vercel dashboard for your project:

**Basic Configuration**:
- **Framework Preset**: Next.js (should auto-detect)
- **Root Directory**: `web/`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `.next` (auto-detected)
- **Install Command**: `npm install` (auto-detected)
- **Node.js Version**: 20.x

**Git Configuration**:
- **Production Branch**: `main`
- **Automatic Deployments**: Enabled
- **Deploy Previews**: Enabled for all branches

### 3. Configure Environment Variables

Navigate to: Project Settings > Environment Variables

**For Preview Environment**:
- Variable: `NEXT_PUBLIC_API_URL`
- Value: `https://api-preview.confradar.dev` (or your staging API URL)
- Environment: Preview

**For Production Environment**:
- Variable: `NEXT_PUBLIC_API_URL`
- Value: `https://api.confradar.dev` (or your production API URL)
- Environment: Production

**Important**: Only variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

### 4. Verify Integration

**Check GitHub Integration**:
1. Go to GitHub repository > Settings > Integrations
2. Verify Vercel app is listed and has access
3. Check app permissions include repository access

**Test Deployment**:
1. Create a test branch with a small change in `web/`
2. Open a pull request
3. Vercel should automatically:
   - Detect the change
   - Build the project
   - Deploy to a preview URL
   - Comment on the PR with the URL

### 5. Monitor Deployments

- **Vercel Dashboard**: https://vercel.com/
  - View all deployments
  - Check build logs
  - Monitor analytics
  
- **GitHub PR Comments**:
  - Vercel posts comments with preview URLs
  - Status checks appear on PRs
  
- **Production URL**:
  - Configure custom domain in Vercel settings
  - Or use Vercel-provided URL

## Troubleshooting

### Vercel Integration Not Working

**Check Integration Status**:
```bash
# In repository Settings > Integrations
# Verify Vercel app is installed and active
```

**Common Issues**:
1. **App not installed**: Install Vercel GitHub App
2. **No repository access**: Grant access in GitHub settings
3. **Wrong repository**: Link correct repository in Vercel dashboard

### Deployments Not Triggering

**Verify Configuration**:
- Root directory is set to `web/` in Vercel project settings
- Production branch matches your main branch name
- Automatic deployments are enabled

**Check Build Logs**:
- Open Vercel dashboard
- Go to Deployments
- Click on failed deployment
- Review build logs for errors

### Build Failures

**Common Causes**:
1. **Missing dependencies**: Check `package.json` and `package-lock.json`
2. **Environment variables**: Verify `NEXT_PUBLIC_API_URL` is set
3. **Node version**: Ensure 20.x is specified
4. **Build command**: Should be `npm run build`

**Debug Steps**:
1. Test build locally: `cd web && npm install && npm run build`
2. Check Frontend CI passes: `.github/workflows/frontend.yml`
3. Review Vercel build logs for specific errors
4. Verify environment variables are set correctly

### PR Comments Not Appearing

**Check Permissions**:
- Vercel app needs permission to post comments
- Verify in GitHub > Repository Settings > Integrations > Vercel
- Grant "Read & write" access for pull requests

**Manual Check**:
- Visit Vercel dashboard
- Find the deployment for your PR
- Copy the preview URL manually

### Environment Variables Not Working

**Verification**:
1. Ensure variables are prefixed with `NEXT_PUBLIC_`
2. Check they're set for the correct environment (preview/production)
3. Redeploy after changing variables

**Test**:
```bash
# In your Next.js code
console.log(process.env.NEXT_PUBLIC_API_URL)
```

## Advanced Configuration

### Custom Domain

1. Go to Vercel project settings > Domains
2. Add your custom domain
3. Configure DNS records as instructed
4. Wait for SSL certificate provisioning (automatic)

### Multiple Environments

Vercel supports three environments:
- **Production**: Main branch
- **Preview**: Pull requests and other branches
- **Development**: Local development (not deployed)

Configure different variables for each environment as needed.

### Ignored Build Step

To prevent deployments for certain changes:

1. Go to Project Settings > Git
2. Set "Ignored Build Step" command
3. Example: `git diff HEAD^ HEAD --quiet -- ./web/`

## Comparison with Custom Workflows

**Why use Vercel's native integration**:
- ✅ Simpler setup (no workflow file needed)
- ✅ Automatic updates and maintenance
- ✅ Optimized build performance
- ✅ Better integration with Vercel features
- ✅ No secret management needed (handled by Vercel)

**When to use custom workflows**:
- ❌ Need custom build steps before deployment
- ❌ Need to integrate with other services
- ❌ Require custom authentication flows

For ConfRadar, Vercel's native integration is the recommended approach.

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel GitHub Integration](https://vercel.com/docs/deployments/git)
- [Next.js Deployment Guide](https://nextjs.org/docs/deployment)
- [Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

## Support

For deployment issues:
1. Check Vercel dashboard deployment logs
2. Review this troubleshooting guide
3. Consult [wiki/Deployment.md](../wiki/Deployment.md)
4. Contact Vercel support if needed
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
