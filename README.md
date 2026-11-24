# Tech Empire

Tech Empire is a local-first, single-player technology manufacturing and business simulation. The long-term game focuses on developing industrial capabilities, acquiring equipment and materials, manufacturing products, and growing a company.

Phase 0 (repository and development environment), Phase 1 (frontend and backend skeletons), and Phase 2 (PostgreSQL persistence foundation) are implemented and locally verified. The Phase 2 schema contains only the minimum documented Milestone 01 tables. Gameplay workflows and simulation logic remain deferred to later phases.

## Project structure

```text
backend/       FastAPI application and backend checks
docs/          Foundational game and implementation documents
frontend/      React, TypeScript, Vite, and Tailwind application
game-data/     Version-controlled game definitions (added in later phases)
```

## Prerequisites

Verified development machine versions:

- Node.js 24.11.1 and npm 11.8.0
- Python 3.12.10
- Git 2.51.0.windows.2
- PostgreSQL 14 and 18 installation folders are present. The PostgreSQL 18 client reports version 18.3 at `C:\Program Files\PostgreSQL\18\bin\psql.exe`; add its `bin` directory to `PATH` only if you want to run `psql` without the full path.
- PostgreSQL 18 Windows service (`postgresql-x64-18`): installed and Running with Manual startup. It uses the existing initialized cluster on port 5432. Tech Empire's separate service (`postgresql-tech-empire-18`) is Running with Manual startup on loopback port 5433; its data-directory owner must be corrected to `NetworkService` before app databases are created. No PostgreSQL 14 Windows service was detected.
- Visual Studio Code CLI: available

PostgreSQL 18 has an initialized local data directory. Do not reinitialize or replace it. Tech Empire's separate cluster uses a new data directory, service, and loopback-only port. Docker, Redis, and cloud services are not required for local development.

## Run locally

Open two terminals from the repository root.

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --env-file .env
```

The API health response is at <http://127.0.0.1:8000/api/v1/health>; the read-only database check is at <http://127.0.0.1:8000/api/v1/health/database>; interactive API docs are at <http://127.0.0.1:8000/docs>.

Run backend checks from `backend/`:

```powershell
python -m pytest
```

### Frontend

```powershell
cd frontend
npm ci
if (-not (Test-Path .env.local)) { Copy-Item .env.example .env.local }
npm run dev
```

Open <http://127.0.0.1:5173>. The shell calls `/api/v1/health` using the required `VITE_API_BASE_URL` and shows Checking connection, Connected, or Disconnected. The check times out after five seconds and refreshes every 30 seconds. Set `VITE_API_BASE_URL` in `frontend/.env.local` to change the backend address; restart Vite after changing it.

Frontend checks/build:

```powershell
npm run typecheck
npm test
npm run lint
npm run build
```

The Vite origin and backend CORS origin must match. The backend reads `FRONTEND_ORIGIN` from `backend/.env`; its default is `http://127.0.0.1:5173`. Do not put backend secrets in variables prefixed with `VITE_`.

### PostgreSQL and Alembic

The backend alone connects to PostgreSQL. Copy `backend/.env.example` to
`backend/.env` (preserve existing local settings) and set
`DATABASE_PASSWORD` to the generated password for the dedicated application
role. Defaults target `127.0.0.1:5433`, database `tech_empire_dev`, and role
`tech_empire_app`. Override `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`,
or `DATABASE_USER` if your local PostgreSQL setup differs. Never put these
values in frontend variables.

To create an isolated PostgreSQL 18 cluster, run the following in an elevated
PowerShell session. The setup script refuses to initialize the target data
directory if it already exists. `initdb -W`
prompts you privately to set a new PostgreSQL administrator password. The
existing `C:\Program Files\PostgreSQL\18\data` directory is not used.

```powershell
Set-Location 'D:\Tech Empire\tech-empire'
.\scripts\setup-postgresql-cluster.ps1
```

If this cluster was initialized as a different Windows user than the service
account, run `scripts/repair-postgresql-cluster-owner.ps1` from an elevated
PowerShell session before creating app databases. It stops and restarts only
the Tech Empire service and changes ownership/permissions of the new cluster
directory without reinitializing or deleting its data.

In pgAdmin, right-click **Servers** → **Register** → **Server**. On **General**,
set the name to `Tech Empire PostgreSQL 18`. On **Connection**, enter host
`127.0.0.1`, port `5433`, maintenance database `postgres`, and username
`postgres`. Save, then enter the administrator password you set during
`initdb` when pgAdmin prompts. Keep that password out of the application
`.env`.

Using a PostgreSQL administrator account in pgAdmin Query Tool, create a
separate local app role and databases. Use the `DATABASE_PASSWORD` value
already stored in ignored `backend/.env` for the app role; it is separate from
the PostgreSQL administrator password. While connected to the
`Tech Empire PostgreSQL 18` server's `postgres` database, run these as separate statements
(PostgreSQL does not allow `CREATE DATABASE` inside a transaction):

```sql
CREATE ROLE tech_empire_app LOGIN PASSWORD 'replace-with-a-generated-password';
CREATE DATABASE tech_empire_dev;
CREATE DATABASE tech_empire_test;
```

Connect to each new database as the administrator and run the following to
give the app role DDL rights only inside its own schema (the role cannot create
roles or databases):

```sql
REVOKE ALL ON DATABASE tech_empire_dev FROM PUBLIC;
GRANT CONNECT ON DATABASE tech_empire_dev TO tech_empire_app;
CREATE SCHEMA tech_empire_app AUTHORIZATION tech_empire_app;
ALTER ROLE tech_empire_app IN DATABASE tech_empire_dev
    SET search_path = tech_empire_app;
```

For `tech_empire_test`, use the same statements with that database name in the
`REVOKE`, `GRANT`, and `ALTER ROLE` statements. Set
`DATABASE_TEST_NAME=tech_empire_test` in `backend/.env` to enable the optional
PostgreSQL integration test. It refuses to use the development database.

From `backend/`, with its virtual environment active and `.env` configured:

```powershell
python -m alembic current
python -m alembic upgrade head
python -m alembic revision --autogenerate -m "describe schema change"
python -m alembic history
```

Review every generated revision before applying it. The Phase 2 migration
chain creates only the eight Milestone 01 persistence entities defined in
[`docs/DATABASE_SCHEMA_PLAN.md`](docs/DATABASE_SCHEMA_PLAN.md).

## Development scope

The five source-of-truth documents are in `docs/`. PostgreSQL connectivity,
SQLAlchemy session infrastructure, Alembic migration control, and the eight
documented Milestone 01 persistence tables are implemented. Authentication,
save lifecycle operations, company creation, inventory operations, purchases,
manufacturing behavior, research, staffing, market behavior, and simulation
rules belong to later phases.
