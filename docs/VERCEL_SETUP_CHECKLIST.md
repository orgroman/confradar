# Vercel Native Integration - Setup Checklist

This checklist guides you through configuring Vercel's native GitHub integration for automated deployments.

## 1. Vercel GitHub App Installation

- [ ] Visit https://vercel.com/new
- [ ] Click "Import Git Repository"
- [ ] Authorize Vercel to access GitHub account
- [ ] Select `orgroman/confradar` repository
- [ ] Complete Vercel GitHub App installation

## 2. Vercel Project Configuration

### Basic Settings - CRITICAL: Root Directory
- [ ] Verify Vercel project exists for confradar frontend
- [ ] Go to Vercel Dashboard > Project > Settings > General
- [ ] **CRITICAL**: Find "Root Directory" setting and set to `web/`
  - This is THE most common issue - if not set, deployments will fail
  - The error will be: "No Next.js version detected"
  - Must be exactly: `web/` (with trailing slash)
- [ ] Click "Save" after setting root directory
- [ ] Confirm framework preset is set to **Next.js** (should auto-detect after root dir is set)
- [ ] Verify build command: `npm run build` (auto-detected)
- [ ] Verify output directory: `.next` (auto-detected)
- [ ] Verify install command: `npm install` (auto-detected)
- [ ] Set Node.js version to **20.x**

### Git Integration Settings
- [ ] Set production branch to `main`
- [ ] Enable automatic deployments
- [ ] Enable deploy previews for all branches/PRs
- [ ] Verify repository is correctly linked

## 3. Environment Variables Configuration

In Vercel project settings > Environment Variables:

### Preview Environment
- [ ] Add `NEXT_PUBLIC_API_URL` for preview/staging backend
  - Suggested value: `https://api-preview.confradar.dev`
  - Or for testing: `http://localhost:8000`
  - Select environment: **Preview**

### Production Environment
- [ ] Add `NEXT_PUBLIC_API_URL` for production backend
  - Set to production API URL when available
  - Example: `https://api.confradar.dev`
  - Select environment: **Production**

**Note**: Only `NEXT_PUBLIC_*` variables are exposed to browser. Keep secrets server-side.

## 4. GitHub Integration Verification

- [ ] Check GitHub repository > Settings > Integrations
- [ ] Verify Vercel app is installed and active
- [ ] Ensure Vercel has permission to access repository
- [ ] Verify Vercel can post comments on PRs (Read & write access)

## 5. Test Deployments

### Preview Deployment Test
- [ ] Create test branch: `git checkout -b test-vercel-deployment`
- [ ] Make small change in `web/` directory
- [ ] Commit and push: `git push origin test-vercel-deployment`
- [ ] Open pull request to `main`
- [ ] Verify Vercel check appears on PR
- [ ] Wait for deployment to complete
- [ ] Check for Vercel comment with preview URL on PR
- [ ] Visit preview URL and verify frontend loads correctly
- [ ] Test functionality on preview deployment

### Production Deployment Test
- [ ] Merge a PR to main branch (or push directly if needed)
- [ ] Check Vercel dashboard for deployment
- [ ] Verify production deployment succeeds
- [ ] Visit production URL and verify frontend loads
- [ ] Test frontend functionality on production

## 6. Monitor and Verify

- [ ] Check Vercel dashboard shows deployments: https://vercel.com/
- [ ] Verify PR comments appear with deployment URLs
- [ ] Check deployment status and logs
- [ ] Confirm frontend CI passes: `.github/workflows/frontend.yml`
- [ ] Verify no deployment workflow conflicts

## 7. Optional: Custom Domain Setup

If using a custom domain:
- [ ] Go to Vercel project settings > Domains
- [ ] Add custom domain
- [ ] Configure DNS records as instructed by Vercel
- [ ] Wait for SSL certificate provisioning
- [ ] Verify custom domain works
- [ ] Update documentation with custom domain URL

## Troubleshooting Checklist

If deployments aren't working:

### Error: "No Next.js version detected"

This is the #1 deployment error. Fix it immediately:

- [ ] Open Vercel Dashboard > Project > Settings > General
- [ ] Find "Root Directory" field
- [ ] Verify it's set to `web/` (not empty, not `.`)
- [ ] Click "Save" if you changed it
- [ ] Push a new commit or click "Redeploy" in Vercel dashboard
- [ ] Check build logs to confirm error is resolved

### Check Vercel Integration
- [ ] Vercel GitHub App is installed
- [ ] App has access to repository
- [ ] Project is linked to correct repository
- [ ] Root directory is set to `web/` (see above)

### Check Build Configuration
- [ ] Frontend builds locally: `cd web && npm install && npm run build`
- [ ] Frontend CI passes on GitHub
- [ ] Environment variables are set in Vercel
- [ ] Node.js version is compatible (20.x)

### Check Permissions
- [ ] Vercel can post PR comments
- [ ] Automatic deployments are enabled
- [ ] No conflicting GitHub Actions workflows

### Review Logs
- [ ] Check Vercel dashboard deployment logs
- [ ] Review build errors in Vercel console
- [ ] Check GitHub Actions if any workflows are running
- [ ] Verify no errors in PR checks

## Documentation Updates

After successful setup:
- [ ] Update `wiki/Deployment.md` with any project-specific notes
- [ ] Document production URL in README if applicable
- [ ] Note any custom configuration in team wiki
- [ ] Update this checklist with lessons learned

## Success Criteria

✅ Preview deployments work automatically on PRs
✅ Preview URLs posted as PR comments
✅ Production deployments work on main branch merges
✅ Vercel integration is stable and reliable
✅ Team understands how to monitor and troubleshoot deployments

---

**Note**: This approach uses Vercel's native GitHub integration, which is simpler and more reliable than custom GitHub Actions workflows. No manual secret management or workflow configuration is needed.

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
