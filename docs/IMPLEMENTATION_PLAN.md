# Tech Empire — Implementation Plan

**Document status:** Foundational implementation roadmap  
**Version:** 1.0  
**Scope:** Local-first project initialization through Milestone 01 playable workshop  
**Authority:** This plan operationalizes the four foundational documents. If a conflict is found, stop and reconcile the source-of-truth documents before coding.

---

## 1. Purpose

This document converts the Tech Empire design and architecture into small, testable implementation tasks for human developers and AI coding agents.

It defines:
- The order in which the project should be built.
- The expected deliverables for each phase.
- Frontend, backend, database, and testing responsibilities.
- Acceptance criteria and completion gates.
- Rules for keeping implementation aligned with the game design.

**This is a plan, not application code.** No project scaffold, database schema, migrations, or gameplay implementation is created by this document.

## 2. Governing Documents

The following files are the project's foundational source of truth:

1. `GAME_DESIGN.md` — product vision, gameplay loop, MVP scope, economy, UI direction, and acceptance criteria.
2. `TECHNOLOGY_TREE.md` — technology definitions, prerequisites, disciplines, and progression.
3. `MANUFACTURING_SYSTEM.md` — recipes, equipment capabilities, production lifecycle, recursive dependencies, inventory, and sales.
4. `TECHNICAL_ARCHITECTURE.md` — stack, project structure, database, API boundaries, persistence, and testing.

Keep these files in the repository under `docs/`. This plan should also live in `docs/IMPLEMENTATION_PLAN.md`.

## 3. Milestone 01 Definition

**Milestone name:** Playable Workshop Simulation

**Player outcome:** The player creates a company, buys a bench shear and steel sheets, manufactures metal brackets, manages inventory and finances, sells the brackets, and can close/restart the application without losing progress.

### 3.1 Fixed baseline values

| Item or action | Baseline |
|---|---:|
| Starting cash | $10,000.00 |
| Starting facility | 1 small workshop |
| Starting tools | 1 workbench and 1 basic hand-tool set |
| Starting technology | Basic Workshop Practice and Basic Metalworking unlocked |
| Bench shear purchase price | $2,500.00 |
| Steel sheet purchase price | $120.00 per sheet |
| Recipe input | 1 steel sheet |
| Recipe output | 10 metal brackets |
| Production duration | 10 game minutes per batch |
| Bracket sale price | $25.00 each |
| Revenue for selling 10 brackets | $250.00 |

Use USD for the initial sample economy, as defined in the game design. Do not independently change these values in UI mock data, tests, or seed content.

### 3.2 Required player journey

1. Create a company with a validated name.
2. Initialize a new game save and starter assets.
3. View company overview and cash balance.
4. Purchase one bench shear.
5. Purchase one or more steel sheets.
6. Inspect the metal bracket recipe and its requirements.
7. Start a production batch when all requirements are satisfied.
8. Advance game time by 10 minutes.
9. Complete production: consume one steel sheet and add ten brackets.
10. Sell an available quantity of brackets.
11. Review inventory, production history, and financial transactions.
12. Restart/reload and verify that the state persists.

## 4. Development Principles

1. **One vertical slice at a time.** Prefer a small complete capability over many unfinished screens.
2. **Backend owns game outcomes.** React never calculates authoritative cash, stock, production output, or sale results.
3. **Keep the backend a modular monolith.** Do not introduce microservices.
4. **Use structured content data.** Recipes and catalog definitions must not be hardcoded into React pages or API route handlers.
5. **Database changes use migrations.** Never rely on manually editing the database as the only record of a schema change.
6. **Test rules before UI integration.** Manufacturing and economy rules must be testable without a browser.
7. **Do not fake functionality.** A visible button must either work or be clearly marked unavailable.
8. **Avoid premature infrastructure.** No Redis, WebSockets, Docker requirement, cloud deployment, authentication, multiplayer, or background worker is needed for this milestone.
9. **Keep documentation synchronized.** If a design decision changes, update the governing document and this plan before implementation diverges.
10. **No broad rewrites without evidence.** Inspect the current implementation and report impact before changing architecture.

---

# 5. Phase 0 — Repository and Development Environment

**Goal:** Establish a clean local project workspace and verify that the selected tools run.

### Task 0.1 — Create the repository structure

Create the monorepo structure described in `TECHNICAL_ARCHITECTURE.md`, including:
- `frontend/`
- `backend/`
- `game-data/`
- `docs/`

Place the five Markdown documents in `docs/`.

**Acceptance criteria**
- The four foundational documents and this plan are present under `docs/`.
- Frontend and backend are separate projects in one repository.
- `.gitignore` excludes virtual environments, dependency folders, build outputs, caches, local `.env`, and generated secrets.
- `.env.example` contains placeholder configuration only.
- README explains the local project layout and planned commands.

### Task 0.2 — Verify local prerequisites

Verify compatible installed versions of:
- Git
- Node.js LTS and npm
- Python 3
- PostgreSQL
- A code editor

Record exact selected versions in the README or a development setup note.

**Acceptance criteria**
- Version commands run successfully.
- No real credentials are committed.
- Setup instructions are reproducible on the development machine.

### Task 0.3 — Establish Git baseline

Initialize Git if needed and create a baseline commit containing documentation and safe project configuration.

**Acceptance criteria**
- `git status` is understood and clean after the baseline commit.
- No `.env`, database dump, virtual environment, or dependency directory is tracked.

**Exit gate:** A clean repository exists and local development prerequisites are verified.

---

# 6. Phase 1 — Frontend and Backend Skeletons

**Goal:** Start React and FastAPI independently and verify communication.

## 6.1 Frontend setup

Use:
- React
- TypeScript
- Vite
- Tailwind CSS
- Lucide React

Add only the dependencies needed for the initial shell. TanStack Query and charting libraries can be added when their first use case is implemented.

**Deliverables**
- Vite development server.
- TypeScript configuration.
- Tailwind configuration and global design tokens.
- Basic application shell.
- A temporary API connectivity indicator or health-check view.

**Acceptance criteria**
- Frontend starts using the documented command.
- TypeScript type checking passes.
- Tailwind styles render.
- No gameplay logic or authoritative game state is implemented in the frontend.

## 6.2 Backend setup

Use:
- Python
- FastAPI
- Pydantic
- Pytest

Install SQLAlchemy and Alembic in Phase 2 when PostgreSQL persistence is configured. Phase 1 does not create database models or migrations.

**Deliverables**
- FastAPI application entry point.
- Configuration module reading environment variables.
- `GET /api/v1/health` endpoint.
- Versioned `/api/v1` route organization.
- Pytest configuration and one health endpoint test.

**Acceptance criteria**
- Backend starts using the documented command.
- `/api/v1/health` returns a simple healthy response.
- `/docs` loads the generated OpenAPI documentation.
- Tests pass.
- No gameplay logic is added yet.

## 6.3 Frontend-backend connectivity

Configure local CORS for the Vite origin and make a frontend request to the backend health endpoint.

**Acceptance criteria**
- Browser can call the backend health endpoint.
- CORS is restricted to the configured local frontend origin.
- API base URL is read from frontend environment configuration.
- No database credentials are exposed to frontend variables.

**Exit gate:** React and FastAPI run independently and communicate over HTTP.

---

# 7. Phase 2 — PostgreSQL and Persistence Foundation

**Goal:** Connect FastAPI to local PostgreSQL and establish migration-controlled schema management.

### Task 2.1 — Configure PostgreSQL

Create a local database and a least-privilege development database user.

Use environment variables for:
- Database host
- Port
- Database name
- Username
- Password
- SQLAlchemy connection URL assembled by backend configuration

Do not expose PostgreSQL directly to the browser. Only the backend connects to it.

### Task 2.2 — Configure SQLAlchemy

Implement:
- SQLAlchemy engine
- Session factory
- Declarative base
- Request-scoped database session dependency
- Connection lifecycle handling

### Task 2.3 — Configure Alembic

Configure Alembic to read the application's SQLAlchemy metadata.

**Acceptance criteria**
- Backend can connect to PostgreSQL.
- A database connectivity test passes.
- Alembic can generate and apply a test migration.
- A fresh local database can be brought to the latest schema using documented commands.
- Migration status is reproducible.
- No production or cloud database configuration is required.

### Task 2.4 — Initial schema planning

Before creating tables, review the required Milestone 01 entities:

- `companies`
- `game_saves`
- `facilities`
- `equipment_instances`
- `inventory_balances`
- `production_orders`
- `inventory_movements`
- `financial_transactions`

Define primary keys, foreign keys, unique constraints, timestamps, money precision, and quantity rules.

**Important:** Do not create all future-game tables prematurely. Add only fields needed by Milestone 01, while preserving stable IDs and sensible extension points.

**Exit gate:** A fresh PostgreSQL database can be migrated and queried through the backend.

---

# 8. Phase 3 — Game Content Catalog

**Goal:** Define the initial items, equipment, facility, technology, and recipe as version-controlled content.

### Task 3.1 — Define content schemas

Create validated schemas for:
- Item/material definitions
- Equipment definitions
- Facility definitions
- Technology definitions
- Recipe definitions
- Content manifest/version

Use stable string IDs.

### Task 3.2 — Add initial content

Minimum catalog entries:

| Type | ID | Name |
|---|---|---|
| Material | `steel_sheet` | Steel Sheet |
| Product | `metal_bracket` | Metal Bracket |
| Equipment | `bench_shear` | Bench Shear |
| Facility | `small_workshop` | Small Workshop |
| Technology | `basic_workshop_practice` | Basic Workshop Practice |
| Technology | `basic_metalworking` | Basic Metalworking |
| Recipe | `metal_bracket_basic` | Metal Bracket |

Add starter workbench and basic hand-tool definitions if represented as equipment catalog entries.

### Task 3.3 — Validate catalog references

Validate:
- Unique IDs
- Positive quantities and durations
- Existing item references in recipe inputs and outputs
- Existing capability references
- Existing technology references
- Valid content version
- No recursive recipe cycles in the available make paths

**Acceptance criteria**
- Catalog loads from `game-data/`.
- Invalid content fails with actionable errors.
- Tests cover valid content and at least one invalid reference and one cycle.
- Frontend does not contain a second hardcoded copy of the catalog.

**Exit gate:** The backend can load and validate the initial game content.

---

# 9. Phase 4 — New Game, Company, and Save Loading

**Goal:** Create and reload a player's local career.

### Task 4.1 — Company creation contract

Implement `POST /api/v1/games`.

Validate:
- Company name is present.
- Name length follows the game design rule.
- Unsupported or malformed input is rejected.

The backend initializes:
- Company
- Game save
- Starting cash of $10,000
- One small workshop
- One workbench
- One basic hand-tool set
- Basic Workshop Practice unlock
- Basic Metalworking unlock
- Initial game time Day 1, 08:00

All creation steps must be one database transaction.

### Task 4.2 — Load current game

Implement `GET /api/v1/games/current`.

Return the authoritative current save summary, including:
- Company identity
- Cash
- Game time
- Facility summary
- Owned equipment summary
- Unlocked technology IDs
- Content version

### Task 4.3 — Frontend company creation

Build the company creation screen and first-load flow.

**Acceptance criteria**
- A valid company creates exactly one initial save.
- Invalid names are rejected with clear feedback.
- Refreshing the browser can reload the existing game.
- Duplicate submissions do not create duplicate companies.
- Database rollback leaves no partial company if initialization fails.
- A fresh game has the exact starting state defined in `GAME_DESIGN.md`.

**Exit gate:** A player can create a career and reload it after a browser refresh.

---

# 10. Phase 5 — Inventory and Financial Ledger

**Goal:** Establish reliable stock and cash accounting before purchases or manufacturing.

### Task 5.1 — Inventory service

Implement operations to:
- Read item balances.
- Calculate available quantity as on-hand minus reserved.
- Add inventory movement records.
- Reserve and release quantities.
- Consume reserved quantities.
- Reject negative stock and invalid quantities.

### Task 5.2 — Economy service

Implement:
- Cash balance reads.
- Purchase debit.
- Sales credit.
- Financial transaction history.
- Decimal-safe money arithmetic.

Do not accept a new cash balance from the frontend. The backend calculates all balance changes.

### Task 5.3 — Transaction integrity

Add database-level and service-level protections appropriate to the operations.

**Acceptance criteria**
- Inventory movements explain every stock change.
- Financial transactions explain every cash change.
- Money is stored using fixed-precision decimal types.
- Invalid quantities and insufficient cash are rejected.
- Failed operations roll back all related changes.
- Tests verify that no negative cash or available inventory is produced.

**Exit gate:** Inventory and cash can be queried and changed only through tested backend services.

---

# 11. Phase 6 — Equipment and Material Purchasing

**Goal:** Allow the player to acquire the bench shear and steel sheets.

### Task 6.1 — Catalog read endpoints

Implement read-only endpoints for available equipment and materials.

### Task 6.2 — Equipment purchase

Implement `POST /api/v1/equipment/purchases`.

The backend must:
1. Validate the equipment ID and quantity.
2. Resolve the catalog price on the server.
3. Verify sufficient company cash.
4. Deduct cash.
5. Create the owned equipment instance.
6. Record a financial transaction.
7. Commit atomically.

### Task 6.3 — Material purchase

Implement `POST /api/v1/material-purchases`.

The backend must:
1. Validate material ID and quantity.
2. Resolve the unit price on the server.
3. Calculate total cost.
4. Verify sufficient cash.
5. Deduct cash.
6. Add inventory.
7. Record inventory movement.
8. Record financial transaction.
9. Commit atomically.

### Task 6.4 — Frontend supplier screens

Build equipment and supplies views with:
- Item name and description
- Price
- Relevant capabilities or unit
- Quantity selector for materials
- Purchase confirmation
- Current cash display
- Insufficient-funds feedback

**Acceptance criteria**
- Player can buy one bench shear for $2,500.
- Player can buy steel sheets for $120 each.
- Client-submitted prices are ignored or rejected.
- Insufficient funds prevent all partial changes.
- Purchases appear in transaction history.
- Purchased equipment and materials appear in the correct views after reload.

**Exit gate:** The player can acquire all inputs needed for the first recipe.

---

# 12. Phase 7 — Manufacturing Validation and Production

**Goal:** Execute the first real production order using backend rules.

### Task 7.1 — Requirement validator

Implement validation for:
- Recipe availability
- Required technology
- Facility capability
- Equipment capability and availability
- Available input inventory
- Production capacity

Return structured requirement failures with stable error codes and useful details.

### Task 7.2 — Start production

Implement `POST /api/v1/production-orders`.

The backend must:
1. Resolve the recipe from trusted content.
2. Validate requested batch count.
3. Validate all requirements.
4. Calculate required inputs and duration.
5. Reserve required inputs atomically.
6. Create the production order.
7. Return the order and its current status.

For Milestone 01, one batch consumes/reserves one steel sheet and produces ten brackets after completion.

### Task 7.3 — Simulation advancement

Implement `POST /api/v1/simulation/advance`.

- Accept an explicit positive number of game minutes.
- Advance the persisted game clock.
- Find due production orders.
- Complete each due order exactly once.
- Process completion in a safe transaction.
- Return updated time and completed order summaries.

A 9-minute advance must not complete a 10-minute batch. Advancing to 10 minutes must complete it.

### Task 7.4 — Production completion

On completion:
- Consume the reserved steel sheet.
- Add ten metal brackets.
- Update production order status and completion time.
- Record inventory movements.
- Record production history.
- Prevent duplicate output on repeated processing.

### Task 7.5 — Frontend manufacturing view

Display:
- Recipe name and description
- Input and output quantities
- Duration
- Required technology
- Facility and equipment requirements
- Current available inputs
- Missing requirements
- Start-production action
- Active/completed orders
- Game-time advancement controls for the MVP

**Acceptance criteria**
- Production cannot start without the bench shear.
- Production cannot start without one available steel sheet.
- Production cannot start without the required facility and technology.
- Valid production reserves one sheet.
- Completion after 10 game minutes consumes one sheet and adds ten brackets.
- Repeated completion processing cannot duplicate output.
- State remains correct after reload.

**Exit gate:** The player can manufacture metal brackets through a validated production order.

---

# 13. Phase 8 — Sales and Financial History

**Goal:** Complete the business loop by selling manufactured products.

### Task 8.1 — Sales endpoint

Implement `POST /api/v1/sales`.

The backend must:
1. Validate item and positive quantity.
2. Resolve the sale price from trusted market/content data.
3. Verify available unreserved inventory.
4. Deduct inventory.
5. Credit company cash.
6. Record inventory movement.
7. Record financial transaction.
8. Commit atomically.

### Task 8.2 — Financial history endpoint

Implement `GET /api/v1/transactions`.

Return transaction type, amount, item/description where relevant, and timestamp.

### Task 8.3 — Frontend sales and finance views

Display:
- Sellable inventory
- Sale quantity
- Unit price
- Expected gross revenue
- Confirmation
- Updated cash
- Transaction history

Label gross revenue accurately. Do not call it net profit while operating costs and full accounting are not modeled.

**Acceptance criteria**
- Player can sell ten brackets for $250.
- Selling more than available stock is rejected.
- Cash and stock change atomically.
- Sale appears in financial and inventory histories.
- Reload preserves the sale result.

**Exit gate:** The player can complete the buy → make → sell loop.

---

# 14. Phase 9 — Dashboard and UI Integration

**Goal:** Present authoritative game state through the agreed futuristic industrial interface.

### Required dashboard content

- Company name
- Game date/time
- Cash balance
- Revenue and expense summaries based only on recorded transactions
- Production status
- Workshop equipment
- Inventory summary
- Recent transactions
- Company progression summary only where backed by defined data

### UI implementation rules

- Follow the dark navy/charcoal visual direction with restrained cyan/electric-blue accents.
- Use consistent spacing, typography, border, and surface tokens.
- Use reusable cards, tables, status labels, and dialogs.
- Use responsive layouts.
- Provide loading, empty, success, and error states.
- Use Lucide icons consistently.
- Do not use fabricated dashboard values once API integration is active.
- Do not create nonfunctional links for future systems.

**Acceptance criteria**
- Dashboard values match backend responses.
- Purchase, production, and sale actions refresh affected views.
- No stale cash or inventory remains after a successful mutation.
- Errors are understandable and do not silently disappear.
- Layout remains usable at supported desktop and tablet widths.

**Exit gate:** The core game loop is usable through the integrated frontend.

---

# 15. Phase 10 — Persistence, Regression, and Milestone Verification

**Goal:** Verify the complete Milestone 01 experience and protect it against regressions.

### 15.1 Backend test coverage

Required cases:
- Company creation and starting state
- Invalid company name
- Duplicate submission protection
- Purchase success and insufficient funds
- Material quantity and price calculations
- Inventory reservation
- Missing equipment/technology/facility/input
- Production completion at the correct game time
- Idempotent production completion
- Sale success and insufficient stock
- Atomic rollback
- Save reload

### 15.2 Frontend test coverage

Required cases:
- Company creation form validation
- Dashboard loading and error states
- Purchase confirmation and failure feedback
- Manufacturing requirements display
- Start production disabled when blocked
- Sale quantity validation
- Updated balances after successful operations

### 15.3 Manual end-to-end acceptance run

Execute this exact scenario on a fresh local database:

1. Start frontend and backend.
2. Create a company.
3. Verify $10,000 starting cash and starter assets.
4. Purchase one bench shear. Verify cash becomes $7,500.
5. Purchase one steel sheet. Verify cash becomes $7,380.
6. Start one metal bracket batch.
7. Verify one sheet is reserved and cannot be used by a second order.
8. Advance 9 minutes. Verify the order is still running.
9. Advance 1 more minute. Verify completion.
10. Verify one sheet has been consumed and ten brackets are in inventory.
11. Sell ten brackets.
12. Verify $250 gross sale revenue and cash becomes $7,630.
13. Verify bracket inventory returns to zero.
14. Restart the frontend/backend processes.
15. Load the current game.
16. Verify company, cash, game time, equipment, inventory, production history, and transactions persist.

This scenario assumes no other purchases or transactions and uses the fixed baseline prices.

### 15.4 Definition of Milestone 01 complete

Milestone 01 is complete only when:
- Every acceptance criterion in `GAME_DESIGN.md` is met.
- The manual end-to-end scenario passes.
- Backend and frontend tests pass.
- A fresh database can be initialized using migrations.
- No critical data-integrity bugs remain.
- Documentation and setup instructions match the working implementation.
- No required feature is represented by mock-only behavior.

---

# 16. Explicitly Deferred Work

Do not implement these as part of Milestone 01 unless a documented blocker makes one essential:

- User registration/authentication
- Cloud hosting or cloud database
- Multiplayer
- Multiple companies per user
- Multiple save-slot UI
- Redis
- WebSockets
- Docker as a requirement
- Background workers
- Real-time/offline simulation progression
- Employee hiring and skill simulation
- Full research project UI
- Dynamic market and competitor simulation
- Taxes and full double-entry accounting
- Multiple factories and logistics networks
- Equipment maintenance and degradation
- Advanced quality, scrap, and yield simulation
- Full recursive dependency planning UI
- Semiconductor fabrication gameplay

The data model and module boundaries should leave room for these systems, but do not build speculative abstractions without an immediate use case.

---

# 17. AI Coding Agent Operating Instructions

Any AI coding agent working on Tech Empire must follow these rules:

1. Read all five documents in `docs/` before proposing or changing implementation.
2. Identify the current phase and task before editing.
3. Inspect the existing repository before assuming files, frameworks, or code structure.
4. State the planned changes and affected files before a substantial implementation.
5. Implement only the requested task and its necessary dependencies.
6. Do not silently change game balance, recipe values, technology prerequisites, API contracts, or architecture.
7. Do not add libraries or infrastructure without explaining why they are needed.
8. Keep game rules in backend simulation/services, not React components.
9. Use Alembic migrations for schema changes.
10. Add or update tests with every meaningful behavior change.
11. Run relevant tests and report exact results.
12. Do not claim a feature works if it is only mocked or visually represented.
13. If a source document is ambiguous or contradictory, stop and report the conflict instead of inventing a rule.
14. At task completion, report:
    - What changed
    - Files created/modified
    - Tests run and results
    - Manual verification still needed
    - Known limitations
    - Recommended next task

### Required task report format

```text
Task:
Status: Complete / Partial / Blocked

Implemented:
- ...

Files changed:
- ...

Validation:
- Command:
- Result:

Manual verification:
- ...

Known limitations:
- ...

Next task:
- ...
```

---

# 18. Recommended First Coding Session

The first coding session should complete only **Phase 0 and Phase 1**:

1. Inspect the development machine and repository location.
2. Create or verify the monorepo structure.
3. Place the five documents under `docs/`.
4. Initialize Git and `.gitignore`.
5. Scaffold the React + TypeScript + Vite frontend.
6. Scaffold the FastAPI backend.
7. Add frontend and backend health checks.
8. Configure local CORS.
9. Verify the frontend can call the backend.
10. Run tests and document exact setup commands.

**Do not implement PostgreSQL models, purchases, inventory, or manufacturing in the first coding session.** Those belong to later phases and should begin only after the application skeleton is verified.

## 19. Current Project Status

Current verified project status after Phase 0 and Phase 1 foundation work:

| Area | Status |
|---|---|
| Game design documentation | Defined |
| Technology tree documentation | Defined |
| Manufacturing specification | Defined |
| Technical architecture | Defined |
| Implementation plan | Defined |
| Repository scaffold | Present; Git initialized; ignore rules and setup documentation added |
| Frontend application | React, TypeScript, Vite, and Tailwind shell implemented; tests, lint, typecheck, and build passed |
| Backend application | FastAPI health API and local CORS implemented; backend checks passed |
| PostgreSQL integration | Not started |
| Milestone 01 gameplay | Not started |

PostgreSQL client was not detected during Phase 0 verification and is not required until Phase 2. Do not assume a task is complete merely because files were generated; verify the files, run the relevant commands, and test the behavior.
