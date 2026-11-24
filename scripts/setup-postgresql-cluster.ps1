#requires -RunAsAdministrator

$ErrorActionPreference = 'Stop'

$serverBin = 'C:\Program Files\PostgreSQL\18\bin'
$dataDirectory = 'C:\ProgramData\TechEmpire\PostgreSQL18\data'
$serviceName = 'postgresql-tech-empire-18'
$port = 5433

if (Test-Path -LiteralPath $dataDirectory) {
    throw "Refusing to initialize an existing path: $dataDirectory"
}
if (Get-Service -Name $serviceName -ErrorAction SilentlyContinue) {
    throw "Refusing to replace existing service: $serviceName"
}
if (Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue) {
    throw "Refusing to use port $port because it already has a listener."
}
foreach ($binary in @('initdb.exe', 'pg_ctl.exe', 'pg_isready.exe')) {
    if (-not (Test-Path -LiteralPath (Join-Path $serverBin $binary))) {
        throw "Required PostgreSQL 18 binary was not found: $binary"
    }
}

New-Item -ItemType Directory -Path $dataDirectory -Force | Out-Null
& icacls.exe $dataDirectory /grant 'NT AUTHORITY\NETWORK SERVICE:(OI)(CI)F' /T
if ($LASTEXITCODE -ne 0) {
    throw 'Could not grant the PostgreSQL service account access to its new data directory.'
}

& (Join-Path $serverBin 'initdb.exe') -D $dataDirectory -U postgres -A scram-sha-256 -W -E UTF8
if ($LASTEXITCODE -ne 0) {
    throw 'initdb failed. The new directory was left in place for inspection; it was not deleted.'
}

& icacls.exe $dataDirectory /setowner 'NT AUTHORITY\NETWORK SERVICE' /T /C
if ($LASTEXITCODE -ne 0) {
    throw 'Could not assign the initialized cluster to its Windows service account.'
}
& icacls.exe $dataDirectory /grant 'NT AUTHORITY\NETWORK SERVICE:(OI)(CI)F' /T /C
if ($LASTEXITCODE -ne 0) {
    throw 'Could not grant the PostgreSQL service account access to its cluster.'
}

& (Join-Path $serverBin 'pg_ctl.exe') register `
    -D $dataDirectory `
    -N $serviceName `
    -U 'NT AUTHORITY\NetworkService' `
    -S demand `
    -o "-p $port -c listen_addresses=127.0.0.1"
if ($LASTEXITCODE -ne 0) {
    throw 'PostgreSQL service registration failed. The new data directory was left in place.'
}

Start-Service -Name $serviceName
Get-Service -Name $serviceName | Select-Object Name, Status, StartType
& (Join-Path $serverBin 'pg_isready.exe') -h 127.0.0.1 -p $port
if ($LASTEXITCODE -ne 0) {
    throw 'The Tech Empire PostgreSQL service did not accept local connections.'
}
