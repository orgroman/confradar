# Script to organize GitHub issues into epics using sub-issue relationships
# Requires: gh CLI authenticated and gh-sub-issue extension installed
# Install: gh extension install yahsan2/gh-sub-issue

param(
    [switch]$DryRun = $false
)

$owner = "orgroman"
$repo = "confradar"

Write-Host "=== GitHub Issue Epic Organization ===" -ForegroundColor Cyan
Write-Host "Repository: $owner/$repo" -ForegroundColor Yellow
if ($DryRun) {
    Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Magenta
}
Write-Host ""

# Function to link sub-issue to parent epic using gh sub-issue extension
function Add-SubIssue {
    param(
        [int]$epicNumber,
        [int]$subIssueNumber
    )
    
    Write-Host "  Linking #$subIssueNumber → Epic #$epicNumber..." -NoNewline
    
    if ($DryRun) {
        Write-Host " [DRY RUN]" -ForegroundColor Magenta
        return $true
    }
    
    try {
        # Using gh sub-issue add command
        $result = gh sub-issue add $epicNumber $subIssueNumber --repo "$owner/$repo" 2>&1
        
        # Check if the command succeeded
        if ($LASTEXITCODE -eq 0) {
            Write-Host " OK" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host " Failed ($result)" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host " Failed ($_)" -ForegroundColor Red
        return $false
    }
}

# Track statistics
$stats = @{
    Total = 0
    Success = 0
    Failed = 0
}

# Epic #171: Infrastructure & DevOps (remaining issues)
Write-Host "Epic #171: Infrastructure & DevOps" -ForegroundColor Cyan
$epic171_remaining = @(40, 41, 42, 43, 44, 45, 134, 135, 136, 147, 157)
foreach ($issue in $epic171_remaining) {
    $stats.Total++
    if (Add-SubIssue -epicNumber 171 -subIssueNumber $issue) {
        $stats.Success++
    }
    else {
        $stats.Failed++
    }
    Start-Sleep -Milliseconds 300
}

# Epic #172: Data Pipeline
Write-Host "`nEpic #172: Data Pipeline" -ForegroundColor Cyan
$epic172_issues = @(
    1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 17, 18, 20, 22,
    35, 36, 37, 38, 39, 45, 46, 47, 48, 49, 50,
    51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
    61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
    71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
    81, 82, 83, 84, 85
)
foreach ($issue in $epic172_issues) {
    $stats.Total++
    if (Add-SubIssue -epicNumber 172 -subIssueNumber $issue) {
        $stats.Success++
    }
    else {
        $stats.Failed++
    }
    Start-Sleep -Milliseconds 300
}

# Epic #173: Serving & Output
Write-Host "`nEpic #173: Serving & Output" -ForegroundColor Cyan
$epic173_issues = @(12, 13, 15, 29, 30, 31)
foreach ($issue in $epic173_issues) {
    $stats.Total++
    if (Add-SubIssue -epicNumber 173 -subIssueNumber $issue) {
        $stats.Success++
    }
    else {
        $stats.Failed++
    }
    Start-Sleep -Milliseconds 300
}

# Epic #86: Frontend Application sub-epics
Write-Host "`nEpic #86: Frontend Application" -ForegroundColor Cyan
$epic86_subepics = @(88, 89, 90, 91, 92, 93, 94, 95, 96)
foreach ($issue in $epic86_subepics) {
    $stats.Total++
    if (Add-SubIssue -epicNumber 86 -subIssueNumber $issue) {
        $stats.Success++
    }
    else {
        $stats.Failed++
    }
    Start-Sleep -Milliseconds 300
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "Total issues processed: $($stats.Total)" -ForegroundColor White
Write-Host "Successfully linked:    $($stats.Success)" -ForegroundColor Green
Write-Host "Failed:                 $($stats.Failed)" -ForegroundColor Red

if ($DryRun) {
    Write-Host "`nThis was a DRY RUN. Run without -DryRun to apply changes." -ForegroundColor Magenta
}

Write-Host "`nDone!" -ForegroundColor Green
