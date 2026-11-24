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
- PostgreSQL client (`psql`): not installed/detected; it is not needed until Phase 2
- Visual Studio Code CLI: available

The project does not require PostgreSQL, Docker, Redis, or cloud services in Phase 0/1.

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
