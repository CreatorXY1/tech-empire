#requires -RunAsAdministrator

$ErrorActionPreference = 'Stop'

$dataDirectory = 'C:\ProgramData\TechEmpire\PostgreSQL18\data'
$serviceName = 'postgresql-tech-empire-18'
$serviceAccount = 'NT AUTHORITY\NETWORK SERVICE'
$port = 5433

if (-not (Test-Path -LiteralPath (Join-Path $dataDirectory 'PG_VERSION'))) {
    throw "Expected initialized Tech Empire cluster was not found at: $dataDirectory"
}

$service = Get-Service -Name $serviceName -ErrorAction Stop
$restartService = $service.Status -eq 'Running'
if ($restartService) {
    Stop-Service -Name $serviceName
    $service.WaitForStatus('Stopped', [TimeSpan]::FromSeconds(30))
}

try {
    & icacls.exe $dataDirectory /setowner $serviceAccount /T /C
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not assign the Tech Empire cluster files to the service account.'
    }

    & icacls.exe $dataDirectory /grant "$serviceAccount`:(OI)(CI)F" /T /C
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not grant the Tech Empire service account access to its cluster.'
    }

    $owner = (Get-Acl -LiteralPath $dataDirectory).Owner
    if ($owner -notmatch 'NETWORK SERVICE$') {
        throw "Unexpected data directory owner after correction: $owner"
    }
}
finally {
    if ($restartService) {
        Start-Service -Name $serviceName
        $service.WaitForStatus('Running', [TimeSpan]::FromSeconds(30))
    }
}

& 'C:\Program Files\PostgreSQL\18\bin\pg_isready.exe' -h 127.0.0.1 -p $port
if ($LASTEXITCODE -ne 0) {
    throw 'The Tech Empire PostgreSQL service did not accept local connections after the ownership correction.'
}
