Param(
  [string]$Owner = "orgroman",
  [string]$Repo = "confradar",
  [string]$ProjectTitle = "ConfRadar Roadmap",
  [string]$BacklogPath = "../backlog.csv"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Ensure-Gh() {
  if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI (gh) is not installed. Install from https://cli.github.com/ and re-run."
  }
}

function Ensure-Auth() {
  $status = gh auth status 2>$null
  if ($LASTEXITCODE -ne 0) { gh auth login }
}

function Sync-Labels() {
  Write-Host "Syncing labels via workflow dispatch (requires workflow to exist on GitHub)..."
  try {
    gh workflow run labels.yml -R "$Owner/$Repo" | Out-Null
    Write-Host "Labels workflow dispatched. If this repo hasn't pushed the workflow yet, push first and re-run."
  }
  catch {
    Write-Warning "Label sync workflow not found remotely yet. Push the repo changes to main, then re-run to sync labels."
  }
}

function Ensure-Project($owner, $title) {
  $existing = gh project list --owner $owner --format json | ConvertFrom-Json
  $projects = $existing.projects
  if ($projects) {
    foreach ($p in $projects) {
      if ($p.title -ieq $title) { return $p.number }
    }
  }
  Write-Host "Creating user project '$title' under $owner"
  $created = gh project create --owner $owner --title $title --format json | ConvertFrom-Json
  # gh returns an object with at least number and title at top-level for create
  return $created.number
}

function Ensure-Milestones($owner, $repo, $milestoneNames) {
  if (-not $milestoneNames -or $milestoneNames.Count -eq 0) { return }
  Write-Host "Ensuring milestones exist: $($milestoneNames -join ', ')"
  $existingJson = gh api repos/$owner/$repo/milestones --paginate --silent 2>$null
  $existing = @()
  if ($LASTEXITCODE -eq 0 -and $existingJson) { $existing = $existingJson | ConvertFrom-Json }
  $existingTitles = @{}
  foreach ($m in $existing) { $existingTitles[$m.title] = $true }
  foreach ($name in $milestoneNames) {
    if (-not $existingTitles.ContainsKey($name)) {
      Write-Host "Creating milestone: $name"
      # Create with open state; description optional
      gh api repos/$owner/$repo/milestones -X POST -f title="$name" | Out-Null
    }
  }
}

function Create-Issues-And-Add-To-Project($owner, $repo, $projectNumber, $csvPath) {
  if (-not (Test-Path $csvPath)) { throw "Backlog CSV not found at $csvPath" }
  $rows = Import-Csv -Path $csvPath
  foreach ($row in $rows) {
    $labels = ($row.Labels -split ';' | ForEach-Object { $_.Trim() }) -join ','
    $title = $row.Title
    $body  = $row.Body
    $milestone = $row.Milestone

    $args = @("issue","create","-R","$owner/$repo","-t",$title,"-b",$body)
    if ($labels -ne "") { $args += @("-l", $labels) }
    if ($milestone -and $milestone -ne "") { $args += @("-m", $milestone) }

    $out = gh @args --format json | ConvertFrom-Json
    $issueUrl = $out.url
    Write-Host "Created issue: $issueUrl"

    if ($projectNumber) {
      gh project item-add --owner $owner --project $projectNumber --url $issueUrl | Out-Null
      Write-Host "  ↳ Added to project #$projectNumber"
    }
  }
}

Ensure-Gh
Ensure-Auth

Push-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
try {
  # Trigger label sync (labels workflow uses .github/labels.yml)
  Sync-Labels

  # Ensure user project exists
  $projNum = Ensure-Project -owner $Owner -title $ProjectTitle
  Write-Host "Using project number: $projNum"

  # Ensure basic milestones used by backlog exist
  Ensure-Milestones -owner $Owner -repo $Repo -milestoneNames @('M1','M2','M3','M4','M5')

  # Create issues from CSV and add to project
  Create-Issues-And-Add-To-Project -owner $Owner -repo $Repo -projectNumber $projNum -csvPath $BacklogPath
}
finally {
  Pop-Location
}
