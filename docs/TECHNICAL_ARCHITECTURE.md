# Tech Empire --- Technical Architecture

**Document status:** Foundational source of truth\
**Version:** 1.0\
**Architecture style:** Local-first modular monolith\
**Related documents:** `GAME_DESIGN.md`, `TECHNOLOGY_TREE.md`,
`MANUFACTURING_SYSTEM.md`

------------------------------------------------------------------------

## 1. Architecture Goals

The architecture must: - Support a single-player local browser game
first. - Keep game rules authoritative on the backend. - Separate UI,
API, simulation logic, persistence, and game content. - Support
data-driven products, recipes, equipment, materials, and technologies. -
Make manufacturing and economy behavior testable without a browser. -
Preserve a practical path to cloud hosting and multiple player accounts
later. - Avoid premature infrastructure such as Redis, microservices,
WebSockets, and Docker.

Use a **modular monolith**: one backend application with clearly
separated modules. Do not split the game into microservices during the
initial development.

## 2. Agreed Technology Stack

  -----------------------------------------------------------------------
  Layer                   Technology              Role
  ----------------------- ----------------------- -----------------------
  Frontend framework      React                   UI composition and
                                                  interaction

  Frontend language       TypeScript              Type safety

  Build/dev server        Vite                    Local frontend
                                                  development

  Styling                 Tailwind CSS            Responsive design
                                                  system

  Icons                   Lucide React            Consistent interface
                                                  icons

  Charts                  Recharts                Financial and
                                                  production charts

  Dependency              React Flow              Technology and recipe
  visualization                                   graphs

  API client state        TanStack Query          Fetching, caching,
                                                  mutations

  Backend language        Python                  Game logic and
                                                  simulation

  API framework           FastAPI                 REST API and request
                                                  validation

  Validation              Pydantic                API schemas and data
                                                  validation

  ORM                     SQLAlchemy              Relational persistence

  Migrations              Alembic                 Versioned database
                                                  schema

  Database                PostgreSQL              Persistent game state

  Backend tests           Pytest                  Simulation and API
                                                  tests

  Frontend tests          Vitest + React Testing  UI and interaction
                          Library                 tests

  Version control         Git                     Source history
  -----------------------------------------------------------------------

Use compatible stable releases when the project is initialized. Pin
dependencies and record the chosen versions in package and
requirements/lock files. Do not silently upgrade major versions during
feature work.

## 3. Local Development Topology

Default local endpoints:

  Service      Address
  ------------ ------------------------------
  Frontend     `http://localhost:5173`
  Backend      `http://localhost:8000`
  API docs     `http://localhost:8000/docs`
  PostgreSQL   `localhost:5432`

PostgreSQL is a local database service, not a browser-facing service.
Only the backend connects to it.

The browser communicates with FastAPI over HTTP. Configure explicit CORS
for the local Vite origin during development. Never expose database
credentials to the frontend.

## 4. High-Level Architecture

``` text
Browser
  React + TypeScript + Tailwind
          |
          | HTTP REST API
          v
FastAPI Application
  API Routes
      |
      v
  Application Services
      |
      +---- Simulation Engine
      |       +---- Manufacturing
      |       +---- Inventory
      |       +---- Economy
      |       +---- Technology
      |       +---- Time/Progress
      |
      +---- Repositories
              |
              v
         SQLAlchemy
              |
              v
         PostgreSQL
```

Game content is loaded from version-controlled definitions in
`game-data/` and validated before use. The database stores
player-specific state and may also store a content version or snapshot
reference.

## 5. Repository Structure

Recommended monorepo:

``` text
tech-empire/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   ├── dashboard/
│   │   │   ├── manufacturing/
│   │   │   ├── inventory/
│   │   │   └── shared/
│   │   ├── pages/
│   │   ├── features/
│   │   │   ├── company/
│   │   │   ├── workshop/
│   │   │   ├── manufacturing/
│   │   │   ├── equipment/
│   │   │   ├── inventory/
│   │   │   └── finance/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── stores/
│   │   ├── types/
│   │   └── styles/
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── errors.py
│   │   ├── database/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── simulation/
│   │   │   ├── engine.py
│   │   │   ├── manufacturing.py
│   │   │   ├── dependency_resolver.py
│   │   │   ├── inventory.py
│   │   │   ├── economy.py
│   │   │   ├── technology.py
│   │   │   └── clock.py
│   │   └── main.py
│   ├── migrations/
│   ├── tests/
│   ├── requirements.txt
│   └── alembic.ini
│
├── game-data/
│   ├── manifest.json
│   ├── materials/
│   ├── components/
│   ├── products/
│   ├── equipment/
│   ├── facilities/
│   ├── technologies/
│   └── recipes/
│
├── docs/
│   ├── GAME_DESIGN.md
│   ├── TECHNOLOGY_TREE.md
│   ├── MANUFACTURING_SYSTEM.md
│   └── TECHNICAL_ARCHITECTURE.md
│
├── .env.example
├── .gitignore
└── README.md
```

The structure is a target organization, not a requirement to create
every empty directory on day one. Add modules when their
responsibilities are implemented.

## 6. Backend Layer Responsibilities

### 6.1 API routes

Routes should: - Parse HTTP requests. - Validate input schemas. - Call
application services. - Return response schemas. - Map known domain
errors to appropriate HTTP responses.

Routes must not contain manufacturing formulas or directly manipulate
complex inventory state.

### 6.2 Application services

Services coordinate use cases such as: - Create company - Load game -
Purchase equipment - Purchase materials - Start production - Advance
simulation - Sell finished products - Retrieve dashboard summary

Services enforce transaction boundaries and coordinate repositories and
simulation modules.

### 6.3 Simulation modules

Simulation modules contain deterministic game rules: - Manufacturing
validation and completion - Recursive dependency resolution - Inventory
reservation and movement - Cash and transaction calculations -
Technology prerequisite evaluation - Game-time advancement

They should be testable without HTTP or React.

### 6.4 Repositories

Repositories encapsulate SQLAlchemy queries and persistence operations.
Avoid scattering raw database queries throughout routes and simulation
code.

### 6.5 Pydantic schemas

Schemas define request and response contracts. They are separate from
SQLAlchemy database models. Do not expose ORM models directly as API
responses.

## 7. Frontend Architecture

### 7.1 Main layout

The long-term shell contains: - Sidebar navigation - Top bar with
company name, game date, speed controls, and cash balance - Main content
region - Optional contextual panels

### 7.2 Milestone 01 pages

Functional pages: 1. Company creation 2. Overview dashboard 3. Workshop
/ Manufacturing 4. Equipment & Supplies 5. Inventory 6. Finance /
Transactions

The Technology, Research, Employees, and Market destinations can be
deferred or shown as clearly unavailable planned features. Do not
present nonfunctional controls as implemented.

### 7.3 Component principles

-   Build reusable, typed components.
-   Keep page composition separate from data-fetching logic.
-   Keep API calls in service modules.
-   Use TanStack Query for backend state and cache invalidation.
-   Keep temporary UI state local where practical.
-   Do not duplicate authoritative cash or inventory in an independent
    frontend game simulation.
-   Use responsive CSS even though the design is desktop-first.
-   Provide loading, empty, error, and success states.

### 7.4 Visual design tokens

Establish shared tokens for: - Background and elevated surfaces -
Primary and secondary text - Cyan/blue accent - Success, warning, and
error states - Border colors - Spacing and radii - Typography scale -
Chart series and grid lines

The dashboard reference uses a dark navy industrial-corporate aesthetic.
Reuse design tokens across all pages rather than styling each screen
independently.

## 8. Database Design

Use PostgreSQL with SQLAlchemy and Alembic.

### 8.1 Initial entities

The first database schema should include the minimum entities needed for
a playable save:

  -----------------------------------------------------------------------
  Entity/table                        Purpose
  ----------------------------------- -----------------------------------
  `companies`                         Company name, cash balance,
                                      creation metadata

  `game_saves`                        Local career save, game clock,
                                      content version

  `facilities`                        Owned workshop/factory instances

  `equipment_instances`               Owned machine/tool instances

  `inventory_balances`                Quantity and reserved quantity by
                                      save/location/item

  `production_orders`                 Recipe, batch count, status,
                                      start/due/completion time

  `inventory_movements`               Auditable quantity changes

  `financial_transactions`            Purchases, sales, and other cash
                                      movements
  -----------------------------------------------------------------------

Additional tables can be added as features require them: - Research
projects and technology unlocks - Employees and assignments - Suppliers
and market offers - Sales orders - Equipment maintenance - Inventory
lots and quality records

### 8.2 Data definition vs player state

Global game definitions live in `game-data/` initially: - Item
definitions - Equipment definitions - Facility definitions - Recipe
definitions - Technology definitions

Player-specific state lives in PostgreSQL: - Owned equipment - Facility
instances - Inventory balances - Company cash - Active production
orders - Unlocked technology IDs - Transactions and movement history

Do not duplicate all catalog definitions into each player save. Store
stable IDs and a content version. Consider snapshots or migration logic
if future content updates change old definitions.

### 8.3 Money and quantities

-   Store money using fixed-precision decimal types, not floating-point
    values.
-   Use consistent currency representation (USD for the initial sample
    scenario).
-   Store item quantities using integer units for Milestone 01.
-   Future recipes may require fractional units; choose a deliberate
    decimal precision when that feature is designed.
-   Validate nonnegative balances and quantities at the service and
    database levels where appropriate.

### 8.4 Transaction boundaries

The following operations must be atomic: - Purchase equipment: verify
cash, deduct cash, create equipment instance, create financial
transaction. - Purchase materials: verify cash, deduct cash, add
inventory, create inventory movement, create financial transaction. -
Start production: validate requirements, reserve inputs, create
production order. - Complete production: consume reservations, add
outputs, update order, record movements. - Sell products: verify
available stock, deduct inventory, credit cash, create movement and
financial transaction.

Use database transactions and appropriate row locking or conditional
updates to avoid race conditions, even in local single-player
development.

## 9. Save System

A local save is represented by a database record linked to the company's
game state.

Milestone 01 supports one active career save, but the schema should
allow multiple saves later.

Save/load requirements: - New game creates company, save, starter
facility, workbench, hand tools, starting balance, and starting
technology. - Loading returns the saved state from the backend. -
State-changing operations persist through PostgreSQL. - Save data
includes a content version. - The frontend must not be the authoritative
save store. - A browser refresh or application restart must not erase
progress.

A future export/import feature may serialize a validated save package,
but it is not required now.

## 10. Game Content Data

Content is data-driven and version-controlled.

Recommended content categories: - Materials - Components - Products -
Equipment - Facilities - Technologies - Recipes

Each definition must have a stable ID and schema version. Build a
content loader/validator that checks references and invalid values at
application startup or during tests.

Avoid embedding catalog data in React components or route handlers.

## 11. API Contract --- Milestone 01

Use versioned API paths, for example `/api/v1`.

Suggested endpoints:

  Method   Endpoint                        Purpose
  -------- ------------------------------- -----------------------------------
  `POST`   `/api/v1/games`                 Create a new local game/company
  `GET`    `/api/v1/games/current`         Load current game state
  `GET`    `/api/v1/dashboard`             Retrieve dashboard summary
  `GET`    `/api/v1/inventory`             Retrieve inventory
  `GET`    `/api/v1/equipment/catalog`     List purchasable equipment
  `POST`   `/api/v1/equipment/purchases`   Purchase equipment
  `GET`    `/api/v1/materials/catalog`     List purchasable materials
  `POST`   `/api/v1/material-purchases`    Purchase materials
  `GET`    `/api/v1/recipes`               List available recipe definitions
  `POST`   `/api/v1/production-orders`     Validate and start production
  `POST`   `/api/v1/simulation/advance`    Advance game time explicitly
  `GET`    `/api/v1/production-orders`     List production orders
  `POST`   `/api/v1/sales`                 Sell available finished goods
  `GET`    `/api/v1/transactions`          Retrieve financial history

Exact request/response schemas should be defined during implementation
and reflected in generated OpenAPI documentation. Do not allow the
frontend to submit authoritative cash balances, inventory balances, or
arbitrary production outputs.

### 11.1 API error shape

Use a consistent structured error response with: - Stable error code -
Human-readable message - Optional field or requirement details -
Optional correlation/request identifier

Manufacturing validation should return machine-readable requirement
failures so the frontend can display them clearly.

## 12. Simulation Clock

Milestone 01 uses explicit backend simulation advancement: - Game time
is persisted in the save. - An advance command requests a number of game
minutes. - The backend advances time and processes due production
orders. - Repeated advancement must not complete an order twice. - Tests
can advance exact durations deterministically.

A later feature may add pause/1x/2x/5x/10x controls. Real-time
scheduling and offline progression are deferred. The backend remains
authoritative when those features are introduced.

## 13. Security and Local Configuration

Even for local development: - Keep database credentials in environment
variables. - Commit `.env.example`, never the real `.env`. - Do not
expose database connection strings to the frontend. - Restrict CORS to
the local frontend origin. - Validate all API inputs. - Never trust
client-submitted prices, cash, inventory, or production outcomes. - Use
parameterized ORM queries. - Avoid binding PostgreSQL to public network
interfaces. - Do not add authentication until required, but do not
design APIs that assume the browser is trusted.

## 14. Testing Strategy

### Backend

-   Unit tests for recipe validation and calculations
-   Unit tests for inventory and economy rules
-   Dependency graph cycle detection tests
-   API tests for purchase, production, sale, and save/load
-   Transaction rollback tests
-   Idempotency tests for production completion
-   Content catalog validation tests

### Frontend

-   Component tests for dashboard and inventory display
-   Interaction tests for purchase and production forms
-   Error-state tests for insufficient funds and missing requirements
-   API integration tests using mocked HTTP responses where appropriate
-   Responsive layout checks

### End-to-end

A future E2E test should execute the full Milestone 01 loop from company
creation to selling brackets and reloading the save.

## 15. Development Workflow

Recommended implementation sequence:

1.  Initialize Git repository and documentation.
2.  Create frontend and backend project skeletons.
3.  Install and configure local PostgreSQL.
4.  Configure SQLAlchemy and Alembic.
5.  Create initial database migration.
6.  Implement game content definitions and validation.
7.  Implement company creation and save loading.
8.  Implement inventory and financial services.
9.  Implement equipment/material purchases.
10. Implement manufacturing validation and production orders.
11. Implement simulation advancement and completion.
12. Implement sales.
13. Build and integrate Milestone 01 UI.
14. Add tests and verify save/reload.
15. Review architecture before adding research and employee systems.

## 16. Future Online Migration

The local-first design should support a later hosted version: - Deploy
the FastAPI application to a cloud host. - Provision managed
PostgreSQL. - Add user authentication and authorization. - Associate
each save/company with an authenticated user. - Add rate limits,
backups, monitoring, and secure secrets management. - Keep the
simulation engine and content definitions unchanged where possible.

Do not build cloud-specific assumptions into the simulation engine.

## 17. Architecture Decision Records

### ADR-001: Modular monolith

**Decision:** One FastAPI backend with modular boundaries.\
**Reason:** Easier local development, testing, and deployment than
microservices.

### ADR-002: Backend-authoritative simulation

**Decision:** Backend calculates all consequential game outcomes.\
**Reason:** Prevents client manipulation and centralizes rules.

### ADR-003: PostgreSQL for persistence

**Decision:** Use local PostgreSQL from the beginning.\
**Reason:** Relational data, transactions, constraints, and a direct
migration path to managed PostgreSQL.

### ADR-004: Version-controlled game content

**Decision:** Store initial catalog definitions as structured files in
`game-data/`.\
**Reason:** Content can be reviewed, tested, versioned, and extended
without coupling it to UI code.

### ADR-005: Explicit simulation advancement for MVP

**Decision:** Advance game time through backend commands.\
**Reason:** Deterministic tests and simpler initial implementation.

### ADR-006: No premature infrastructure

**Decision:** Exclude Docker, Redis, WebSockets, multiplayer, and cloud
deployment from the first milestone.\
**Reason:** They do not solve a current MVP requirement.
