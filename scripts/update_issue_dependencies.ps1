# Update GitHub Issues with Dependencies and Relations
# Run this script to add dependency tracking to issues

Write-Host "🔗 Updating Issue Dependencies and Relations..." -ForegroundColor Cyan

# Foundation Layer - Schema & KB
Write-Host "`n📊 Foundation Layer..." -ForegroundColor Yellow
gh issue comment 3 --body "**Dependencies**: None (foundation)`n**Blocks**: #7, #8, #20, #22, #36`n`n🔴 **CRITICAL PATH** - Must complete before any KB work"
gh issue comment 7 --body "**Depends on**: #3 (schema definition)`n**Blocks**: #8, #20, #22, #36, #12, #13, #15, #29, #37`n`n🔴 **CRITICAL PATH** - Core storage layer"
gh issue comment 22 --body "**Depends on**: #3, #7`n**Blocks**: Production deployments"

# Retrieval and Extraction
Write-Host "`n🔍 Retrieval and Extraction..." -ForegroundColor Yellow
gh issue comment 1 --body "**Dependencies**: None (can start now)`n**Blocks**: #2, #4, #38`n`n✅ First data source to implement"
gh issue comment 2 --body "**Depends on**: #1 (validate approach first)`n**Enhances**: Discovery beyond seeds"
gh issue comment 4 --body "**Depends on**: #1 (needs data to parse)`n**Blocks**: #5, #6, #8, #20`n`n🔴 **CRITICAL PATH** - Core extraction logic"
gh issue comment 5 --body "**Depends on**: #4 (rule-first must exist), #53 ✅ (LLM API)`n**Enhances**: #4 for complex cases"
gh issue comment 6 --body "**Depends on**: #4 (part of date extraction)`n`n⚠️ Critical for deadline accuracy"

# Intelligence - Change Detection & Clustering
Write-Host "`n🧠 Intelligence Layer..." -ForegroundColor Yellow
gh issue comment 8 --body "**Depends on**: #7 (KB for history), #4 (extraction)`n**Blocks**: #19, #31, #12`n`n🔴 **CRITICAL PATH** - Enables monitoring and serving"
gh issue comment 20 --body "**Depends on**: #7 (KB), #4 (extraction)`n**Blocks**: Production readiness"
gh issue comment 9 --body "**Depends on**: #7 (KB)`n**Blocks**: #10, #11, #36`n**Works with**: #38"
gh issue comment 10 --body "**Depends on**: #9 (normalization first)`n**Blocks**: #11, #36, #38"
gh issue comment 11 --body "**Depends on**: #10 (clustering)`n**Enhances**: Deduplication"
gh issue comment 36 --body "**Depends on**: #9, #10, #11`n**Enhances**: Advanced deduplication"
gh issue comment 38 --body "**Depends on**: #1, #2, #9, #10`n**Integrates**: Multiple data sources"

# Orchestration and Monitoring
Write-Host "`n⚙️ Orchestration and Monitoring..." -ForegroundColor Yellow
gh issue comment 19 --body "**Depends on**: #18 ✅ (orchestration), #8 (change detection), #24 (logging)`n**Blocks**: Production operations`n`n🔴 **CRITICAL PATH** - Required for production"
gh issue comment 21 --body "**Depends on**: #18 ✅ (orchestration)`n**Blocks**: Reliable operations"

# Serving Layer
Write-Host "`n📤 Serving Layer..." -ForegroundColor Yellow
gh issue comment 12 --body "**Depends on**: #7 (KB), #8 (change detection)`n**Blocks**: #31`n`n🎯 Primary user-facing interface"
gh issue comment 13 --body "**Depends on**: #7 (KB), #8 (change detection)`n**Alternative to**: #12"
gh issue comment 15 --body "**Depends on**: #7 (KB)"
gh issue comment 29 --body "**Depends on**: #7 (KB)`n**Blocks**: #30`n**Alternative to**: #12"
gh issue comment 30 --body "**Depends on**: #29 (API must exist)`n**Required for**: Production API"
gh issue comment 31 --body "**Depends on**: #8 (change detection), #12 or #29 (data access)`n**Enhances**: User experience"

# Testing
Write-Host "`n🧪 Testing Infrastructure..." -ForegroundColor Yellow
gh issue comment 32 --body "**Dependencies**: None (can start now)`n**Blocks**: #33, #14, #34`n`n🔴 Foundation for quality assurance"
gh issue comment 33 --body "**Depends on**: #32 (unit tests first), #18 ✅ (orchestration)`n**Blocks**: Production deployment"
gh issue comment 14 --body "**Depends on**: #32, #33`n**Validates**: Extraction quality (#4, #5)"
gh issue comment 34 --body "**Depends on**: #32, #33`n**Required for**: Production launch"

# Code Quality
Write-Host "`n✨ Code Quality..." -ForegroundColor Yellow
gh issue comment 41 --body "**Dependencies**: None (can start now)`n**Blocks**: #42, #43, #16`n`n🔴 Foundation for code quality"
gh issue comment 42 --body "**Depends on**: #41 (formatting first)`n**Works with**: #43"
gh issue comment 43 --body "**Depends on**: #41, #42`n**Enforces**: Code quality standards"

# Infrastructure
Write-Host "`n🏗️ Infrastructure..." -ForegroundColor Yellow
gh issue comment 23 --body "**Dependencies**: None (can start now)`n**Blocks**: #27, #28`n`n🔴 **CRITICAL PATH** - Required for production"
gh issue comment 24 --body "**Dependencies**: None (can start now)`n**Blocks**: #19, #25, #26`n`n🔴 **CRITICAL PATH** - Foundation for observability"
gh issue comment 25 --body "**Depends on**: #24 (logging)`n**Works with**: #19"
gh issue comment 26 --body "**Depends on**: #24 (logging)`n**Enhances**: Production error tracking"
gh issue comment 27 --body "**Depends on**: #23 (secrets)`n**Blocks**: #28`n`n⚠️ Partially complete (Dagster containerized)"
gh issue comment 28 --body "**Depends on**: #23, #27`n**Blocks**: Production launch"
gh issue comment 40 --body "**Status**: ✅ Using uv (from #39)`n**May need**: Refinement based on team feedback"

# Documentation
Write-Host "`n📚 Documentation..." -ForegroundColor Yellow
gh issue comment 16 --body "**Depends on**: #41, #43`n**Status**: Ongoing - can document as we implement"
gh issue comment 17 --body "**Status**: ✅ Wiki exists and is maintained`n**Action**: Keep updated with architectural decisions"

# Future Enhancements
Write-Host "`n🚀 Future Enhancements..." -ForegroundColor Yellow
gh issue comment 37 --body "**Depends on**: #7 (KB)`n**Priority**: P3 - Nice-to-have enhancement"
gh issue comment 35 --body "**Depends on**: #7 (KB), #20 (quality validation)`n**Priority**: P3 - Quality control tool"

Write-Host "`n✅ Issue dependencies updated!" -ForegroundColor Green
Write-Host "`nNext: Review .github/ISSUE_DEPENDENCIES.md for the full dependency graph" -ForegroundColor Cyan
