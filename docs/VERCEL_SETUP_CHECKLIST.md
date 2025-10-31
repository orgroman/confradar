# Vercel Deployment - Manual Configuration Checklist

This checklist tracks the manual configuration steps required to complete the Vercel deployment setup.

## 1. Vercel Project Setup
- [ ] Verify Vercel project exists for confradar frontend
- [ ] Confirm project is linked to GitHub repository
- [ ] Verify framework preset is set to Next.js
- [ ] Confirm root directory is set to `web/`
- [ ] Verify build settings (build command, output directory) are correct
- [ ] Ensure Node.js version is set to 20.x

## 2. Configure Azure Service Principal for GitHub Actions

The workflow uses Azure Key Vault integration with OIDC authentication.

### Setup Azure OIDC
- [ ] Create or identify Azure Service Principal for GitHub Actions
- [ ] Configure federated credentials for GitHub repository
  - Entity type: Branch
  - GitHub repository: orgroman/confradar
  - Branch: main (and other branches as needed)
- [ ] Grant Service Principal access to Key Vault (`kvconfradar`)
  - Permission: Get and List secrets
  - Access policy or RBAC role: Key Vault Secrets User

### Add Azure Secrets to GitHub
Go to: https://github.com/orgroman/confradar/settings/secrets/actions

Add three repository secrets for Azure authentication:
- [ ] `AZURE_CLIENT_ID` - Azure Service Principal Client ID
- [ ] `AZURE_TENANT_ID` - Azure Tenant ID
- [ ] `AZURE_SUBSCRIPTION_ID` - Value: `8592e500-3312-4991-9d2a-2b97e43b1810`

## 3. Verify Vercel Secrets in Azure Key Vault

Ensure these secrets exist in Azure Key Vault (`kvconfradar`) with exact names:
- [ ] `VERCEL-TOKEN` - Vercel API authentication token
- [ ] `VERCEL-ORG-ID` - Vercel organization or team ID
- [ ] `VERCEL-PROJECT-ID` - Vercel project ID for confradar frontend

**Note**: If secrets don't exist in Key Vault yet:
1. Create Vercel API token: https://vercel.com/account/tokens
2. Get Org ID from Vercel team settings or run `vercel link` in `web/` directory
3. Get Project ID from Vercel project settings or `.vercel/project.json` after linking
4. Add all three to Azure Key Vault with the exact names above

**Important**: The workflow retrieves these automatically from Key Vault. You do NOT need to add them to GitHub Secrets.

## 4. Configure Vercel Environment Variables

In Vercel project settings (https://vercel.com/[your-org]/confradar/settings/environment-variables):

### Preview Environment
- [ ] Add `NEXT_PUBLIC_API_URL` for preview/staging backend
  - Recommended value: `https://api-preview.confradar.dev` (or your staging API URL)
  - Or use localhost for testing: `http://localhost:8000`

### Production Environment
- [ ] Add `NEXT_PUBLIC_API_URL` for production backend
  - Set to production API URL when available
  - Example: `https://api.confradar.dev`

## 5. Verification & Testing

### Preview Deployment Test
- [ ] Create test branch with change to `web/` directory
- [ ] Open PR to main branch
- [ ] Verify "Deploy to Vercel" workflow runs successfully
- [ ] Check PR comment for preview deployment URL
- [ ] Visit preview URL and verify frontend loads
- [ ] Test frontend functionality on preview deployment

### Production Deployment Test
- [ ] Merge a PR to main with `web/` changes
- [ ] Verify "Deploy to Vercel" workflow runs successfully
- [ ] Check Vercel dashboard for production deployment
- [ ] Visit production URL and verify frontend loads
- [ ] Test frontend functionality on production

### Monitor Status
- [ ] Verify GitHub Actions workflow shows green status
- [ ] Check Vercel dashboard shows successful deployment
- [ ] Verify deployment status badges work in README

## 6. Optional: Configure Custom Domain

If using a custom domain:
- [ ] Add custom domain in Vercel project settings
- [ ] Configure DNS records as instructed by Vercel
- [ ] Verify SSL certificate is provisioned
- [ ] Update `NEXT_PUBLIC_API_URL` if backend URL changes
- [ ] Test custom domain loads correctly

## 7. Documentation Updates (if needed)

- [ ] Update wiki/Deployment.md with production URL
- [ ] Update README.md with live demo link (if applicable)
- [ ] Document any environment-specific configuration
- [ ] Add notes about custom domain (if configured)

## Troubleshooting Reference

If issues occur, refer to:
- `docs/VERCEL_SETUP.md` - Detailed setup guide
- `wiki/Deployment.md` - Deployment documentation
- GitHub Actions logs - Workflow execution details
- Vercel deployment logs - Build and deployment details

## Success Criteria

✅ All checklist items completed
✅ Preview deployments work on PRs
✅ Production deployments work on main branch merges
✅ Preview URLs posted as PR comments
✅ Deployment status visible in GitHub Actions
✅ Frontend loads and functions correctly

---

**Note**: This checklist can be tracked as a GitHub issue or used as a manual checklist during setup.
