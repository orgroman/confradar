# Assign milestones and priority labels to frontend issues
param()

$ErrorActionPreference = 'Stop'

function Ensure-Milestone {
  param(
    [Parameter(Mandatory=$true)][string]$Title,
    [Parameter(Mandatory=$true)][string]$Description,
    [Parameter(Mandatory=$false)][string]$DueOn
  )
  $existingAll = gh api repos/:owner/:repo/milestones --paginate | ConvertFrom-Json
  $existing = $existingAll | Where-Object { $_.title -eq $Title }
  if (-not $existing) {
    if ($DueOn) {
      gh api repos/:owner/:repo/milestones -f title="$Title" -f state="open" -f description="$Description" -f due_on="$DueOn" | Out-Null
    } else {
      gh api repos/:owner/:repo/milestones -f title="$Title" -f state="open" -f description="$Description" | Out-Null
    }
    Write-Host "Created milestone: $Title" -ForegroundColor Green
  } else {
    Write-Host "Milestone exists: $Title" -ForegroundColor DarkGray
  }
}

function Set-IssueMeta {
  param(
    [Parameter(Mandatory=$true)][int]$Number,
    [Parameter(Mandatory=$true)][string]$PriorityLabel,
    [Parameter(Mandatory=$true)][string]$MilestoneTitle
  )
  # Add priority label if missing
  $issue = gh issue view $Number --json number,title,labels,milestone | ConvertFrom-Json
  $hasPriority = $issue.labels | ForEach-Object { $_.name } | Where-Object { $_ -like 'priority:*' }
  if (-not $hasPriority) {
    gh issue edit $Number --add-label "$PriorityLabel" | Out-Null
    Write-Host "[$Number] added label $PriorityLabel" -ForegroundColor Green
  }
  # Set milestone if missing
  $milestone = $issue.milestone.title
  if (-not $milestone) {
    gh issue edit $Number --milestone "$MilestoneTitle" | Out-Null
    Write-Host "[$Number] set milestone $MilestoneTitle" -ForegroundColor Green
  }
}

# Ensure priority labels exist (already present in repo, but idempotent)
$priorityLabels = @('priority:P0','priority:P1','priority:P2','priority:P3')
$existingLabels = gh label list --json name --jq '.[].name'
foreach ($pl in $priorityLabels) {
  if (-not ($existingLabels -match "^$pl$")) {
    switch ($pl) {
      'priority:P0' { gh label create 'priority:P0' --description 'Highest priority' --color 'b60205' }
      'priority:P1' { gh label create 'priority:P1' --description 'High priority' --color 'd93f0b' }
      'priority:P2' { gh label create 'priority:P2' --description 'Medium priority' --color 'fbca04' }
      'priority:P3' { gh label create 'priority:P3' --description 'Low priority' --color 'cccccc' }
    }
  }
}

# Create frontend milestones
Ensure-Milestone -Title 'FE-1: Frontend Setup (Dec 2025)' -Description 'Frontend project setup: framework, UI library, routing, build, CI, testing setup' -DueOn '2025-12-31T00:00:00Z'
Ensure-Milestone -Title 'FE-2: List & Search Beta (Jan 2026)' -Description 'Conference list view with search/filter integrated with API' -DueOn '2026-01-31T00:00:00Z'
Ensure-Milestone -Title 'FE-3: Detail, Export & Timezones (Feb 2026)' -Description 'Conference detail, AoE/timezones, ICS export & Google Calendar' -DueOn '2026-02-28T00:00:00Z'
Ensure-Milestone -Title 'FE-4: Testing & QA (Mar 2026)' -Description 'Accessibility, cross-browser, performance, E2E tests; release candidate' -DueOn '2026-03-31T00:00:00Z'
Ensure-Milestone -Title 'FE-5: Public Launch (Apr 2026)' -Description 'Public v1 launch and final polish' -DueOn '2026-04-15T00:00:00Z'

# Fetch frontend issues
$frontendIssues = gh issue list --label frontend --limit 200 --json number,title | ConvertFrom-Json

# Mapping rules by title
function Get-MilestoneForTitle([string]$t) {
  $lower = $t.ToLower()
  if ($lower -match 'conf\s*rada|web ui implementation') { return 'FE-5: Public Launch (Apr 2026)' }
  if ($lower -match 'infrastructure|project setup|framework|ui component|state management|routing|build tools|ci/cd|testing framework') { return 'FE-1: Frontend Setup (Dec 2025)' }
  if ($lower -match 'list page|conference card|table/card view|search bar|filter|sort|api client|list api|loading states|error handling') { return 'FE-2: List & Search Beta (Jan 2026)' }
  if ($lower -match 'detail page|important dates|change history|location details|timezone|aoe|ics|google calendar|export modal|settings|localstorage|detail api') { return 'FE-3: Detail, Export & Timezones (Feb 2026)' }
  if ($lower -match 'testing|quality|accessibility|cross-browser|performance|subscription feed') { return 'FE-4: Testing & QA (Mar 2026)' }
  return 'FE-2: List & Search Beta (Jan 2026)'
}

function Get-PriorityForTitle([string]$t) {
  $lower = $t.ToLower()
  if ($lower -match 'web ui implementation') { return 'priority:P0' }
  if ($lower -match 'infrastructure|framework|routing|api client|list api') { return 'priority:P1' }
  if ($lower -match 'list page|conference card|table/card view|search|filter|sort|loading states|error handling|detail page|important dates|timezone|aoe|ics|google calendar|detail api') { return 'priority:P1' }
  if ($lower -match 'settings|export modal|state management|build tools|ci/cd|testing framework') { return 'priority:P2' }
  if ($lower -match 'subscription feed|map integration') { return 'priority:P3' }
  return 'priority:P2'
}

foreach ($iss in $frontendIssues) {
  $ms = Get-MilestoneForTitle $iss.title
  $prio = Get-PriorityForTitle $iss.title
  Set-IssueMeta -Number $iss.number -PriorityLabel $prio -MilestoneTitle $ms
}

Write-Host "Assignment complete." -ForegroundColor Green
