[CmdletBinding()]
param(
    [string]$DbName = "swiggy",
    [string]$DbUser = "postgres",
    [string]$DbPassword = "postgres",
    [switch]$EnablePostgresSetup
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

function Find-Python {
    foreach ($candidate in @("py", "python", "python3")) {
        $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($cmd) {
            return $candidate
        }
    }
    return $null
}

function Find-PostgresTools {
    $toolPaths = @(
        "$env:ProgramFiles\PostgreSQL",
        "$env:ProgramFiles(x86)\PostgreSQL",
        "$env:ProgramW6432\PostgreSQL",
        "$env:ProgramFiles\PostgreSQL\*",
        "$env:ProgramFiles(x86)\PostgreSQL\*"
    )

    foreach ($path in $toolPaths) {
        if (Test-Path $path) {
            $items = Get-ChildItem -Path $path -ErrorAction SilentlyContinue
            foreach ($item in $items) {
                $binDir = Join-Path $item.FullName "bin"
                if (Test-Path (Join-Path $binDir "psql.exe")) {
                    return $binDir
                }
            }
        }
    }

    $envPathDirs = $env:PATH -split ';'
    foreach ($dir in $envPathDirs) {
        if ($dir -and (Test-Path (Join-Path $dir "psql.exe"))) {
            return $dir
        }
    }

    return $null
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Swiggy Business & Operations Analytics - Windows Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Default mode: CSV-first portfolio workflow (no PostgreSQL required)." -ForegroundColor Green

$pythonCmd = Find-Python
if (-not $pythonCmd) {
    throw "Python 3 was not found on PATH. Install Python 3.10+ and try again."
}

$venvPath = Join-Path $repoRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    & $pythonCmd -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        throw "Virtual environment creation failed."
    }
}

$venvPython = Join-Path $venvPath "Scripts\python.exe"
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r (Join-Path $repoRoot "requirements.txt")
if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed."
}

$rawDataDir = Join-Path $repoRoot "Data\raw"
if (-not (Test-Path $rawDataDir)) {
    throw "Expected raw data folder not found: $rawDataDir"
}

Write-Host "Python environment is ready." -ForegroundColor Green

if ($EnablePostgresSetup) {
    $pgBinDir = Find-PostgresTools
    if (-not $pgBinDir) {
        Write-Host "PostgreSQL client tools were not detected on this machine." -ForegroundColor Yellow
        Write-Host "Install PostgreSQL 16 or later from https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
        Write-Host "After installation, rerun this script with -EnablePostgresSetup to create the local database." -ForegroundColor Yellow
        Write-Host "Example: .\setup_windows.ps1 -EnablePostgresSetup -DbName swiggy -DbUser postgres -DbPassword postgres" -ForegroundColor Yellow
        Write-Host "" 
        Write-Host "Project setup completed for CSV-based portfolio analysis. PostgreSQL is optional for advanced SQL demos." -ForegroundColor Green
        exit 0
    }

    $psqlExe = Join-Path $pgBinDir "psql.exe"
    $createdbExe = Join-Path $pgBinDir "createdb.exe"
    $pgIsReadyExe = Join-Path $pgBinDir "pg_isready.exe"

    Write-Host "Checking PostgreSQL server availability..." -ForegroundColor Yellow
    $env:PGPASSWORD = $DbPassword
    & $pgIsReadyExe -h localhost -p 5432 -U $DbUser
    if ($LASTEXITCODE -ne 0) {
        Write-Host "A PostgreSQL server was found, but it is not accepting connections on localhost:5432." -ForegroundColor Yellow
        Write-Host "Start the server or install PostgreSQL and then rerun this script." -ForegroundColor Yellow
        Write-Host "" 
        Write-Host "Project setup completed for Python analysis. Database creation is pending." -ForegroundColor Green
        exit 0
    }

    Write-Host "Creating or validating database '$DbName'..." -ForegroundColor Yellow
    & $createdbExe -h localhost -p 5432 -U $DbUser -e $DbName 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Database '$DbName' already exists or could not be created automatically." -ForegroundColor Yellow
    }

    $portableLoader = Join-Path $repoRoot "Database\Insert_Data_Portable.sql"
    if (-not (Test-Path $portableLoader)) {
        throw "Missing portable loader template: $portableLoader"
    }

    $loaderContent = Get-Content -Path $portableLoader -Raw
    $loaderContent = $loaderContent.Replace("__REPO_ROOT__", $repoRoot.Replace("\", "/"))
    $loaderFile = Join-Path $repoRoot "Database\Insert_Data_Local.sql"
    Set-Content -Path $loaderFile -Value $loaderContent -Encoding UTF8

    Write-Host "Running SQL schema and data load scripts..." -ForegroundColor Yellow
    & $psqlExe -h localhost -U $DbUser -d $DbName -f (Join-Path $repoRoot "Database\Create_Tables.sql")
    if ($LASTEXITCODE -ne 0) {
        throw "Schema creation failed."
    }

    & $psqlExe -h localhost -U $DbUser -d $DbName -f $loaderFile
    if ($LASTEXITCODE -ne 0) {
        throw "Data loading failed."
    }

    Write-Host "Database setup completed successfully." -ForegroundColor Green
    Write-Host "You can now open the project in Power BI and connect to the local 'swiggy' database." -ForegroundColor Green
}

Write-Host "" 
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Activate the environment: .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Run Python checks: python .\python\scripts\data_quality_checks.py" -ForegroundColor White
Write-Host "3. Run EDA summary: python .\python\scripts\eda_summary.py" -ForegroundColor White
Write-Host "4. Open Power BI and load the report under .\powerbi\Swiggy_Business_Analytics.pbix" -ForegroundColor White
Write-Host "" 
Write-Host "Setup finished." -ForegroundColor Green
