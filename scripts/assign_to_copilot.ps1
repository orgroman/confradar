# Assign issues to GitHub Copilot coding agent via API

# The Copilot agent ID we found earlier
$CopilotAgentId = "BOT_kgDOC9w8XQ"

# Issues to delegate
$IssueNumbers = @(97, 98, 99, 100, 101)

Write-Host "Assigning issues to GitHub Copilot coding agent..." -ForegroundColor Cyan

foreach ($IssueNum in $IssueNumbers) {
    Write-Host ""
    Write-Host "Processing issue #$IssueNum..." -ForegroundColor Yellow
    
    # First, get the issue's node ID
    $issueData = gh issue view $IssueNum --json id,title | ConvertFrom-Json
    $issueNodeId = $issueData.id
    $issueTitle = $issueData.title
    
    Write-Host "  Title: $issueTitle" -ForegroundColor Gray
    Write-Host "  Node ID: $issueNodeId" -ForegroundColor Gray
    
    # Create a temporary GraphQL file using replaceActorsForAssignable mutation with actorIds
    $mutationFile = "scripts\temp_mutation.graphql"
    $mutationContent = "mutation { replaceActorsForAssignable(input: {assignableId: `"$issueNodeId`", actorIds: [`"$CopilotAgentId`"]}) { assignable { ... on Issue { id number title assignees(first: 10) { nodes { login } } } } } }"
    Set-Content -Path $mutationFile -Value $mutationContent
    
    # Execute the mutation
    try {
        $result = gh api graphql -F query=@$mutationFile | ConvertFrom-Json
        
        if ($result.data.replaceActorsForAssignable.assignable) {
            $assignees = $result.data.replaceActorsForAssignable.assignable.assignees.nodes | ForEach-Object { $_.login }
            Write-Host "  Success - Successfully assigned to: $($assignees -join ', ')" -ForegroundColor Green
        } else {
            Write-Host "  Failed - (no data returned)" -ForegroundColor Red
            if ($result.errors) {
                Write-Host "    Errors: $($result.errors | ConvertTo-Json -Compress)" -ForegroundColor Red
            }
        }
    } catch {
        Write-Host "  Error: $_" -ForegroundColor Red
    }
    
    Start-Sleep -Milliseconds 500
}

# Clean up temp file
if (Test-Path "scripts\temp_mutation.graphql") {
    Remove-Item "scripts\temp_mutation.graphql"
}

Write-Host ""
Write-Host "Done! Check the issues to verify Copilot assignment." -ForegroundColor Cyan
