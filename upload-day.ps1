# Helper Script to Upload Days to GitHub
# Usage: .\upload-day.ps1 -Day "day1" -Week "week1"

param(
    [Parameter(Mandatory=$true)]
    [string]$Day,
    
    [Parameter(Mandatory=$true)]
    [string]$Week,
    
    [string]$Message = ""
)

# Colors for output
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Error { Write-Host $args -ForegroundColor Red }

Write-Info "`n=========================================="
Write-Info "  Uploading $Week/$Day to GitHub"
Write-Info "==========================================`n"

# Check if folder exists
$folderPath = "$Week/$Day"
if (-not (Test-Path $folderPath)) {
    Write-Error "Error: Folder $folderPath does not exist!"
    exit 1
}

# Default commit message if not provided
if ($Message -eq "") {
    $Message = "Add $Week/$Day: Initial implementation with documentation"
}

# Show what will be added
Write-Info "Files to be added from $folderPath`:"
Get-ChildItem -Path $folderPath -Recurse -File | ForEach-Object {
    $relativePath = $_.FullName.Replace((Get-Location).Path + "\", "")
    Write-Host "  - $relativePath"
}

# Ask for confirmation
Write-Warning "`nDo you want to proceed? (Y/N)"
$confirmation = Read-Host
if ($confirmation -ne 'Y' -and $confirmation -ne 'y') {
    Write-Info "Upload cancelled."
    exit 0
}

# Git operations
Write-Info "`nStage 1: Adding files..."
git add $folderPath
if ($LASTEXITCODE -ne 0) {
    Write-Error "Error adding files!"
    exit 1
}
Write-Success "✓ Files staged"

Write-Info "`nStage 2: Committing..."
git commit -m $Message
if ($LASTEXITCODE -ne 0) {
    Write-Error "Error committing!"
    exit 1
}
Write-Success "✓ Committed"

Write-Info "`nStage 3: Pushing to GitHub (Vab-dev branch)..."
git push origin Vab-dev
if ($LASTEXITCODE -ne 0) {
    Write-Error "Error pushing to GitHub!"
    Write-Warning "Try: git pull origin Vab-dev --rebase"
    exit 1
}
Write-Success "✓ Pushed to GitHub"

Write-Success "`n=========================================="
Write-Success "  $Week/$Day uploaded successfully! 🎉"
Write-Success "==========================================`n"

Write-Info "View at: https://github.com/Vaibhu79/Learning_Ai/tree/Vab-dev/$Week/$Day"
