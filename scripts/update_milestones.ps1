Param(
  [string]$Owner = "orgroman",
  [string]$Repo = "confradar",
  [string]$BacklogPath = "../backlog.csv"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
try {
  if (-not (Test-Path $BacklogPath)) { throw "Backlog CSV not found at $BacklogPath" }
  $rows = Import-Csv -Path $BacklogPath
  
  foreach ($row in $rows) {
    $title = $row.Title
    $milestone = $row.Milestone
    
    if (-not $milestone -or $milestone -eq "") { continue }
    
    # Find issue by title
    $searchQuery = "in:title $title"
    $json = gh issue list -R "$Owner/$Repo" -S $searchQuery --state all --json number,title | ConvertFrom-Json
    $issueNumber = $null
    foreach ($it in $json) {
      if ($it.title -eq $title) {
        $issueNumber = $it.number
        break
      }
    }
    
    if ($issueNumber) {
      Write-Host "Updating #$issueNumber '$title' → milestone '$milestone'"
      gh issue edit $issueNumber -R "$Owner/$Repo" -m "$milestone"
    } else {
      Write-Warning "Issue not found: $title"
    }
  }
}
finally {
  Pop-Location
}
