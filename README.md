# Tech Empire

Tech Empire is a local-first, single-player technology manufacturing and business simulation. The long-term game focuses on developing industrial capabilities, acquiring equipment and materials, manufacturing products, and growing a company.

This repository currently contains the Phase 0 and Phase 1 development foundation: the project documentation, a React/TypeScript/Vite frontend shell, and a FastAPI backend health endpoint. Gameplay, persistence, and database integration have not been implemented.

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
- PostgreSQL 18 Windows service (`postgresql-x64-18`): installed, stopped, and disabled. No PostgreSQL 14 Windows service was detected. The default PostgreSQL port (5432) had no listener during this check.
- Visual Studio Code CLI: available

The database server does not need to be running for Phase 0/1. PostgreSQL service setup and database connectivity are part of Phase 2. Docker, Redis, and cloud services are not required for local development.

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

The API health response is at <http://127.0.0.1:8000/api/v1/health>; interactive API docs are at <http://127.0.0.1:8000/docs>.

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

## Development scope

The five source-of-truth documents are in `docs/`. Current work is limited to repository setup and application skeletons. PostgreSQL models and migrations, authentication, saves, company creation, inventory, purchases, manufacturing, research, staffing, market behavior, and simulation rules belong to later phases.
