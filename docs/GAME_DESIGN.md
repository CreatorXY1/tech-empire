# Tech Empire --- Game Design Document

**Document status:** Foundational source of truth\
**Version:** 1.0\
**Scope:** Core game vision and Milestone 01\
**Project type:** Local-first, single-player browser simulation

------------------------------------------------------------------------

## 1. Product Vision

**Tech Empire** is a realistic technology-industry business and
manufacturing simulation. The player starts with a small workshop and
limited capital, then develops a company into an increasingly capable
manufacturer.

The central fantasy is not simply buying factories and selling products.
It is building the industrial capabilities that make products possible:
acquiring tools, learning processes, manufacturing components, producing
specialized equipment, and eventually developing complex technologies.

The long-term game should let a player progress from basic mechanical
work to electrical equipment, electronics, computers, semiconductors,
consumer devices, and advanced industrial systems.

### 1.1 Design pillars

1.  **Manufacturing has understandable prerequisites.** Every product is
    made through a recipe or process with explicit inputs, equipment,
    facilities, skills or technologies, time, and outputs.
2.  **Capabilities are earned.** The player must acquire, research, or
    develop the capabilities needed to manufacture an item.
3.  **Buy, outsource, or manufacture.** Players can purchase items,
    contract external suppliers, or manufacture internally when capable.
    Full self-sufficiency is a strategic goal, not a starting
    requirement.
4.  **Industrial progression is grounded in reality.** Technologies and
    production methods should be based on plausible real-world
    engineering. Game abstractions are allowed, but should be clearly
    documented.
5.  **Business decisions matter.** Cash flow, costs, inventory,
    capacity, quality, and market demand should affect decisions.
6.  **The simulation is data-driven.** New materials, products,
    equipment, recipes, and technologies should primarily be added as
    content data rather than custom code.
7.  **The game remains understandable.** The UI must explain blocked
    production and show the player what is missing and how to resolve
    it.

### 1.2 Target experience

The player should feel like the founder and operator of a growing
industrial company. The interface should resemble a premium corporate
operations system: dark navy and charcoal surfaces, restrained
cyan/electric-blue accents, clear typography, subtle borders, readable
charts, and realistic industrial imagery.

The generated dashboard mockup is a visual direction reference, not a
binding pixel-perfect specification. The implementation must remain
responsive and readable at common desktop widths.

------------------------------------------------------------------------

## 2. Genre, Platform, and Scope

  -----------------------------------------------------------------------
  Attribute                           Decision
  ----------------------------------- -----------------------------------
  Genre                               Business simulation, factory
                                      management, technology progression

  Platform                            Desktop-first web browser

  Initial mode                        Single-player, local development

  Initial architecture                React/TypeScript frontend,
                                      Python/FastAPI backend, local
                                      PostgreSQL

  Multiplayer                         Out of scope

  Accounts/authentication             Out of scope for Milestone 01

  Cloud hosting                       Out of scope for local development

  Monetization                        Not defined

  Art direction                       Futuristic corporate interface with
                                      realistic industrial subject matter

  Technology progression              Realistic, capability-based
                                      progression
  -----------------------------------------------------------------------

### 2.1 Local-first does not mean throwaway

The first release runs on one computer. The architecture should still
separate frontend, backend, simulation rules, content definitions, and
persistence so cloud deployment can be added later without rewriting the
core simulation.

------------------------------------------------------------------------

## 3. Core Gameplay Loop

The long-term loop is:

1.  **Plan:** Select a product, business objective, or capability to
    develop.
2.  **Acquire:** Purchase raw materials, components, tools, equipment,
    or outsourced services.
3.  **Develop:** Research technologies, design products, and unlock
    processes.
4.  **Prepare:** Provide suitable facilities, equipment, workforce, and
    inventory.
5.  **Produce:** Run manufacturing jobs and consume inputs.
6.  **Inspect:** Check output quantity, quality, defects, and production
    costs.
7.  **Sell or use:** Sell products, fulfill orders, or consume
    components in downstream recipes.
8.  **Reinvest:** Improve facilities, equipment, skills, research, and
    supply chains.

Milestone 01 implements a small complete loop: create a company, buy a
bench shear and steel sheets, manufacture metal brackets, manage
inventory and finances, sell brackets, and save/reload the game.

------------------------------------------------------------------------

## 4. Player Start and Milestone 01 Scenario

### 4.1 New company starting state

The initial game scenario uses the following baseline values. These are
balancing defaults and may be tuned during testing, but changes must be
reflected consistently in this document and the game data.

  Starting item                             Initial value
  --------------------- ---------------------------------
  Company name                            Player supplied
  Starting cash                               \$10,000.00
  Workshop                               1 small workshop
  Workbench                                       1 owned
  Basic hand-tool set                             1 owned
  Bench shear                                   Not owned
  Steel sheets                                          0
  Metal brackets                                        0
  Employees                                             0
  Starting technology                  Basic Metalworking
  Game clock                                 Day 1, 08:00
  Save slots              One local career save initially

The workshop and basic tools are provided as starter assets. The player
must purchase the bench shear and steel sheets before starting bracket
production.

### 4.2 Milestone 01 reference economy

These values form a coherent initial balancing baseline:

  Item/action                                                      Baseline
  ---------------------------------- --------------------------------------
  Bench shear purchase price                                     \$2,500.00
  Steel sheet purchase price                             \$120.00 per sheet
  Bracket recipe input                                        1 steel sheet
  Bracket recipe output                                   10 metal brackets
  Base production duration                                  10 game minutes
  Bracket base sale price                                      \$25.00 each
  Revenue from selling 10 brackets                                 \$250.00
  Direct material cost per batch                                   \$120.00
  Bench shear ownership                                            Required
  Facility                                                   Small workshop
  Starting technology                  Basic Metalworking, already unlocked

The values intentionally make the first production loop affordable. The
bench shear is a capital investment; the steel sheet is a consumable
input. The player can manufacture multiple batches after buying more
steel sheets.

The game must distinguish **cash flow** from **profit**. Purchasing a
bench shear is an equipment/capital expenditure in the transaction
history. It reduces cash immediately but does not turn the entire
purchase price into a per-batch manufacturing cost. Milestone 01 may
display simple cash-based financial summaries; a full accounting model
is a later feature.

### 4.3 First-time player flow

1.  Show a company creation screen.
2.  Validate a non-empty company name (recommended 3--40 characters).
3.  Create a new local game save and initialize starting assets and
    cash.
4.  Open the company dashboard.
5.  Guide the player to the equipment supplier.
6.  Player purchases one bench shear. Confirm sufficient funds and
    deduct \$2,500.
7.  Player purchases at least one steel sheet. Deduct \$120 per sheet.
8.  Player opens Manufacturing and selects Metal Bracket.
9.  Show recipe, inputs, output, duration, facility, and equipment
    requirements.
10. Validate the player's state. If valid, allow production to start.
11. Advance simulation time by at least 10 game minutes.
12. Complete the order, consume one steel sheet, and add 10 metal
    brackets to inventory.
13. Player sells some or all available brackets at the baseline price.
14. Update cash, inventory, production history, and transaction history.
15. Player saves, closes/restarts the app, and reloads the same save
    with state intact.

### 4.4 Milestone 01 acceptance criteria

Milestone 01 is complete only when all of the following work end-to-end:

-   The player can create a company.
-   A persistent local save is initialized with the correct starting
    cash and assets.
-   The dashboard displays authoritative values from the backend.
-   The player can view workshop assets and inventory.
-   The player can purchase a bench shear.
-   The player can purchase steel sheets.
-   Purchases are rejected when funds are insufficient.
-   Purchases create financial transaction records.
-   The manufacturing UI displays recipe requirements and missing
    requirements.
-   The player cannot start production without the required equipment,
    facility, technology, and inputs.
-   A valid production order can be started.
-   Production consumes the correct input exactly once.
-   Completed production adds the correct output quantity.
-   The player can sell only available finished goods.
-   Selling deducts inventory and credits cash atomically.
-   Financial and production histories are visible.
-   Save/reload preserves company, cash, assets, inventory, orders, and
    histories.
-   Backend tests cover the core business rules and frontend tests cover
    important user interactions.

------------------------------------------------------------------------

## 5. Game Systems --- Long-Term Design

### 5.1 Company management

The company is the player's main entity. It owns cash, facilities,
equipment, inventory, employees, technologies, research projects, and
production orders.

Company metrics may eventually include: - Cash balance and cash flow -
Revenue, operating expenses, and profit - Company level and reputation -
Production capacity and utilization - Product quality and defect rate -
Research capability - Supplier relationships - Market share

Do not add a metric to the UI until its calculation and source data are
defined.

### 5.2 Manufacturing

Manufacturing converts inputs into outputs through a defined process. A
recipe may require: - Input materials and components - Equipment types
or specific equipment capabilities - A compatible facility - Unlocked
technologies/processes - Workforce or skill levels - Energy, utilities,
and consumables - Production time and batch size - Quality and yield
parameters

A recipe may produce multiple outputs, byproducts, or waste. Advanced
recipes may have alternative process routes.

### 5.3 Equipment

Equipment is an owned asset instance, not merely a catalog definition. A
definition describes the equipment model and capabilities. An instance
records its owner, facility, condition, maintenance state, and
operational status.

Equipment can eventually have: - Purchase price and resale value -
Supported processes - Capacity and throughput - Precision/quality
rating - Energy consumption - Reliability and wear - Maintenance
requirements - Upgrade slots or modules

### 5.4 Inventory and materials

Inventory stores quantities of materials, components, products, and
consumables. It must support: - Item identity and unit of measure -
Quantity and reserved quantity - Optional quality/lot/batch
information - Storage location - Inventory movement history

For the first milestone, use simple item quantities and a single
workshop storage location. Preserve a schema path to lots and multiple
locations later.

### 5.5 Research and technology

Research unlocks capabilities, processes, equipment designs, or product
designs. Research should have explicit prerequisites and requirements,
not arbitrary level gates alone.

Research may require: - Prior technologies - Researchers and skill
levels - A research facility - Funding - Materials or prototype
components - Time

Milestone 01 starts with Basic Metalworking already unlocked. A complete
research interface is not required for the first playable workshop.

### 5.6 Economy and market

The economy should distinguish: - Cash balance - Purchases and sales -
Equipment/capital purchases - Material costs - Operating expenses -
Revenue - Profit calculations

The initial supplier and buyer prices are deterministic. Later, the
market can introduce demand, competitor prices, contracts, reputation,
supply shortages, and price changes.

### 5.7 Employees

Employees will eventually have professions, skills, wages, availability,
experience, and assignments. Milestone 01 does not require hiring. The
founder can operate the initial workshop without an employee model.

------------------------------------------------------------------------

## 6. Technology Progression Overview

Technology progression is capability-based and inspired by real-world
industrial development. The following eras are a broad map, not rigid
calendar locks:

1.  Basic Industry and Mechanical Workshop
2.  Electrical Industry
3.  Electronics Industry
4.  Computer Industry
5.  Semiconductor Industry
6.  Consumer Technology
7.  Advanced Computing and Industrial Robotics
8.  Industrial Leadership and cutting-edge R&D

A player may research multiple branches in parallel when prerequisites
and resources permit. Do not force every technology into one linear
sequence.

See `TECHNOLOGY_TREE.md` for the detailed progression model.

------------------------------------------------------------------------

## 7. User Experience and Interface

### 7.1 Visual direction

-   Dark navy and charcoal foundations
-   Restrained cyan and electric-blue accents
-   High-contrast readable text
-   Subtle borders and restrained glow
-   Consistent spacing and typography
-   Realistic industrial imagery where it adds context
-   Responsive layouts, desktop-first
-   No cartoonish mobile-game styling or excessive neon effects

### 7.2 Main navigation --- long-term

-   Overview
-   Technology
-   Manufacturing
-   Equipment
-   Inventory
-   Research
-   Employees
-   Market
-   Finance

For Milestone 01, only the following destinations need functional
content: - Overview - Workshop/Manufacturing - Equipment & Supplies -
Inventory - Finance/Transactions

Other navigation items may be visibly marked as planned or omitted. Do
not create fake controls that appear functional but do nothing.

### 7.3 Usability requirements

-   Every blocked action must explain why it is blocked.
-   Show missing quantities and missing capabilities explicitly.
-   Confirm purchases and sales before committing when appropriate.
-   Show loading, success, empty, and error states.
-   Prevent duplicate submissions.
-   Use consistent units and currency formatting.
-   Never display mock financial values as if they were real game state.

------------------------------------------------------------------------

## 8. Simulation Rules and Integrity

1.  The backend is authoritative for cash, inventory, ownership,
    recipes, production, and sales.
2.  The frontend may optimistically display pending UI feedback but must
    reconcile with backend results.
3.  All state-changing operations must validate the current save and
    execute safely.
4.  Inventory and cash changes related to a single action must be
    atomic.
5.  Production inputs are reserved or consumed according to a documented
    lifecycle; they must never be deducted twice.
6.  A completed production order must not complete more than once.
7.  Simulation time must be explicit and testable.
8.  All important economic actions must create a transaction or event
    record.
9.  Content definitions must be versioned so save compatibility can be
    managed.
10. The game must detect invalid or cyclic manufacturing dependencies.

------------------------------------------------------------------------

## 9. Save and Load

Milestone 01 uses a local PostgreSQL database for persistent game state.
A game save represents one player's local career.

A save must preserve: - Company identity and cash - Current game time -
Starting and acquired assets - Inventory quantities - Production orders
and statuses - Completed production history - Purchase and sales
transactions - Unlocked technologies

The initial version may support one active save. The data model should
not prevent multiple save slots later.

Save operations should use database transactions. The backend should
expose explicit load and save/state endpoints even if PostgreSQL writes
are committed continuously. Do not rely on browser local storage as the
authoritative save system.

------------------------------------------------------------------------

## 10. Out of Scope Until Later Milestones

-   Online accounts and cloud saves
-   Multiplayer or shared corporations
-   Real-time PvP or leaderboards
-   Advanced logistics networks
-   Full employee simulation
-   Dynamic global market simulation
-   Competitor AI
-   Patent licensing
-   Complex accounting and taxation
-   Multiple factory locations
-   Full semiconductor fabrication simulation
-   Procedural factory floor construction
-   Mod support

These are future expansion areas, not requirements for Milestone 01.

------------------------------------------------------------------------

## 11. Definition of Done for a Feature

A feature is not complete merely because a screen exists. It is complete
when: - Its rules are documented. - Its backend behavior is implemented
and validated. - Its data is persisted where required. - Its UI reflects
backend state. - Invalid actions are handled. - Relevant automated tests
pass. - It does not break existing game saves or documented contracts.
