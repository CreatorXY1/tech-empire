# Tech Empire --- Manufacturing System Specification

**Document status:** Foundational source of truth\
**Version:** 1.0\
**Related documents:** `GAME_DESIGN.md`, `TECHNOLOGY_TREE.md`,
`TECHNICAL_ARCHITECTURE.md`

------------------------------------------------------------------------

## 1. Purpose

The manufacturing system is the core gameplay system of Tech Empire. It
defines how products are made, what capabilities are required, how
dependencies are resolved, how production consumes resources, and how
outputs enter inventory.

The system must support the long-term goal of recursive manufacturing
dependencies: a product may require components; components may require
materials and equipment; equipment may itself require manufactured parts
and specialized processes.

Milestone 01 implements a deliberately small subset: purchase a bench
shear and steel sheets, manufacture metal brackets, and sell the
finished goods.

## 2. Core Concepts

### 2.1 Catalog definition vs owned instance

A catalog definition describes what an item or machine is. An owned
instance or inventory record describes what the company possesses.

Examples: - `bench_shear` is an equipment definition. - A specific bench
shear owned by a company is an equipment instance. - `steel_sheet` is a
material definition. - 12 steel sheets in a company's workshop inventory
are an inventory balance.

Do not store mutable player ownership directly in global content
definitions.

### 2.2 Item categories

The content model should support at least:

-   Raw materials
-   Processed materials
-   Components
-   Subassemblies
-   Finished products
-   Consumables
-   Equipment
-   Tools
-   Byproducts
-   Waste

For Milestone 01, only steel sheet and metal bracket item definitions
are required as inventory items. The bench shear is an equipment
definition and owned equipment instance.

### 2.3 Recipe

A recipe defines a manufacturing process that transforms input
quantities into output quantities under specified conditions.

A recipe may contain: - Stable ID and version - Name and description -
Input items and quantities - Output items and quantities - Byproducts
and waste - Required equipment capabilities or equipment types -
Required facility capabilities - Required technology/process
capabilities - Workforce and skill requirements - Energy/utilities
requirements - Base duration - Batch size - Quality/yield parameters -
Cost and safety metadata where applicable

### 2.4 Process and equipment capability

A recipe should usually require capabilities, not one exact brand/model
of machine.

Example: a recipe may require `sheet_metal_shearing`. A bench shear
definition provides that capability. A more advanced machine could also
provide it with better throughput or quality.

This keeps recipes flexible and allows equipment upgrades without
duplicating recipes.

For Milestone 01, the metal bracket recipe requires an equipment
capability provided by the bench shear.

### 2.5 Facility

A facility has capabilities, capacity, and possibly environmental
requirements. A small workshop provides the `basic_metalworking`
facility capability.

Future facility types may include: - Mechanical workshop - Electrical
workshop - Electronics lab - PCB production facility - Machine shop -
Chemical processing plant - Semiconductor cleanroom - Assembly factory -
Testing laboratory

## 3. Milestone 01 Manufacturing Content

### 3.1 Starting assets

  -------------------------------------------------------------------------
  Asset                                     Quantity Notes
  --------------------- ---------------------------- ----------------------
  Small workshop                                   1 Provides
                                                     `basic_metalworking`
                                                     facility capability

  Workbench                                        1 Starter asset

  Basic hand-tool set                              1 Starter asset

  Bench shear                                      0 Must be purchased

  Steel sheet                                      0 Must be purchased

  Metal bracket                                    0 Produced by player
  -------------------------------------------------------------------------

### 3.2 Bench shear definition

  Field                  Baseline
  ---------------------- -------------------------------
  ID                     `bench_shear`
  Name                   Bench Shear
  Category               Sheet-metal equipment
  Purchase price         \$2,500.00
  Provides capability    `sheet_metal_shearing`
  Facility requirement   `basic_metalworking`
  Ownership              Required for bracket recipe
  Maintenance            Not simulated in Milestone 01

The supplier sells one bench shear at the baseline price. Purchasing
creates an owned equipment instance and a financial transaction.

### 3.3 Steel sheet definition

  Field                Baseline
  -------------------- --------------------
  ID                   `steel_sheet`
  Name                 Steel Sheet
  Category             Raw/stock material
  Unit                 sheet
  Purchase price       \$120.00 per sheet
  Inventory behavior   Consumable input

For Milestone 01, one sheet is treated as one standardized game unit.
Real sheet dimensions and cutting optimization are future details.

### 3.4 Metal bracket recipe

  Field                           Baseline
  ------------------------------- -----------------------------------
  ID                              `metal_bracket_basic`
  Name                            Metal Bracket
  Input                           1 steel sheet
  Output                          10 metal brackets
  Base duration                   10 game minutes per batch
  Required facility capability    `basic_metalworking`
  Required equipment capability   `sheet_metal_shearing`
  Required technology             `basic_metalworking`
  Base sale price                 \$25.00 per bracket
  Employees                       Not required in Milestone 01
  Quality/yield                   Fixed full yield for Milestone 01

The recipe is an abstraction for the first playable loop. Later versions
may add cutting layouts, forming steps, deburring, inspection, scrap,
quality grades, and alternative processes.

### 3.5 Baseline economics

A single batch consumes one steel sheet worth \$120 and produces ten
brackets. Selling all ten at \$25 each produces \$250 gross revenue.

This does not mean the net profit is automatically \$130: equipment
capital expenditure, operating costs, labor, utilities, taxes, and other
expenses are not fully modeled in Milestone 01. The UI must label gross
revenue and cash balance accurately rather than presenting an incomplete
figure as fully calculated net profit.

## 4. Manufacturing Lifecycle

A production order should have an explicit lifecycle:

1.  **Draft:** Player is configuring the order.
2.  **Validated:** Requirements are satisfied.
3.  **Queued:** Order is accepted but not yet running, if queueing is
    implemented.
4.  **Running:** Production time is advancing.
5.  **Completed:** Inputs have been consumed and outputs committed.
6.  **Cancelled:** Order was cancelled before completion, subject to the
    documented cancellation policy.
7.  **Failed:** An unrecoverable production error occurred; state must
    remain auditable.

For the first milestone, queued state may be skipped and an order may
move directly from validated to running.

### 4.1 Starting production

The backend must validate all requirements using current authoritative
state:

-   Recipe exists and is available.
-   Company has unlocked required technologies.
-   Facility has required capabilities.
-   Required equipment is owned, operational, and available.
-   Inventory has sufficient unreserved inputs.
-   Production capacity is available.
-   Any future employee, utility, and safety requirements are satisfied.

If validation fails, return structured reasons. Example reason codes: -
`MISSING_TECHNOLOGY` - `MISSING_FACILITY_CAPABILITY` -
`MISSING_EQUIPMENT_CAPABILITY` - `EQUIPMENT_UNAVAILABLE` -
`INSUFFICIENT_INPUT` - `INSUFFICIENT_CAPACITY` - `RECIPE_NOT_AVAILABLE`

The UI must show human-readable explanations and missing quantities.

### 4.2 Input reservation and consumption

The system must prevent the same inventory from being committed to
multiple orders.

Recommended lifecycle: - When an order starts, atomically reserve its
required inputs. - When the order completes, convert reservations into
consumed quantities and add outputs. - If an order is cancelled before
production starts, release reservations. - If cancellation during
production is later supported, define whether inputs are partially
consumed, fully lost, or partially returned. Do not invent behavior per
screen.

For Milestone 01, production can reserve one steel sheet at start and
consume it at completion. If the process is cancelled before completion,
release the reserved sheet. This is a simplified rule and should be
tested.

### 4.3 Production completion

Completion must be idempotent: repeated requests or repeated simulation
ticks must never grant output twice.

On completion, one database transaction must: 1. Confirm order is
running and due. 2. Confirm the expected reservation exists. 3. Consume
reserved inputs. 4. Add recipe outputs to inventory. 5. Update order
status and completion time. 6. Record inventory movements. 7. Record a
production event/history entry.

If any step fails, the transaction must roll back.

## 5. Simulation Time

The backend owns simulation time. The browser does not decide when an
order completes.

For the initial architecture: - Game time is stored in the save state. -
Simulation commands advance game time by an explicit number of game
minutes. - Production completion is evaluated against game time. - The
frontend can offer pause and speed controls later, but those controls
send commands or settings to the backend. - A background loop is not
required for Milestone 01.

This explicit-advance approach makes tests deterministic. Later, a
controlled simulation scheduler can translate real elapsed time and
speed settings into simulation advancement.

## 6. Recursive Dependency Resolution

### 6.1 Objective

Given a target product and quantity, the resolver should inspect its
recipe and recursively inspect the recipes of any internally
manufacturable inputs.

It should produce: - A dependency graph - Total material requirements -
Required equipment capabilities - Required facility capabilities -
Required technologies - Available inventory contributions - Missing
quantities/capabilities - Possible acquisition alternatives (purchase,
outsource, manufacture)

### 6.2 Make, buy, or outsource

Every required item may have one or more acquisition strategies:

-   **Buy:** Purchase from an available supplier.
-   **Outsource:** Contract an external manufacturer to provide it.
-   **Make:** Manufacture internally if the company has the recipe and
    capabilities.

The resolver must not assume that every input must be manufactured
internally. The player may buy a CPU or outsource PCB assembly even if
they cannot manufacture those items.

### 6.3 Recursive traversal rules

1.  Start with the target item and requested quantity.
2.  Check available inventory and any reserved quantities.
3.  Determine the remaining quantity.
4.  Consider valid acquisition strategies.
5.  If `make` is selected, find an available recipe.
6.  Multiply recipe input quantities by required batch count.
7.  Recursively resolve each input.
8.  Collect equipment, facility, and technology requirements.
9.  Track dependencies and detect cycles.
10. Return a graph and a human-readable explanation.

### 6.4 Batch rounding

If a recipe outputs a fixed batch quantity, calculate the number of
batches using ceiling division.

Example: a recipe produces 10 brackets per batch. A request for 11
brackets requires 2 batches, unless the recipe supports variable batch
sizes.

The resolver must distinguish: - Requested output quantity - Planned
batch count - Actual output quantity - Excess output added to inventory

### 6.5 Cycle detection

Manufacturing recipe graphs must be acyclic for a selected internal make
path.

If recipe A requires B and recipe B requires A, the resolver must report
a circular dependency and refuse to produce an infinite plan. The error
should identify the cycle path.

A catalog validation tool should detect cycles before game content is
loaded.

### 6.6 Alternative recipes

The long-term system should allow multiple recipes for the same output.
Each recipe may differ in: - Inputs - Equipment - Facility -
Technology - Duration - Yield - Quality - Energy - Cost

The player or planner can select an available recipe. Do not assume one
item always has exactly one manufacturing method.

## 7. Equipment Manufacturing

Equipment is also a product and may eventually have a manufacturing
recipe.

Example conceptual dependency:

`CNC Machine` - Steel frame - Linear guides - Servo motors - Spindle -
Control electronics - Precision sensors - Fasteners and cables

Those components may themselves require: - Metal cutting and machining -
Motor winding - PCB fabrication and assembly - Precision measurement -
Materials processing

However, some equipment dependencies may be purchased from suppliers.
The game must not create an impossible infinite loop in which every
machine requires a machine that requires itself.

### 7.1 Foundational bootstrap rule

The game world provides an initial external industrial economy. The
player can purchase basic tools and machinery from suppliers even before
they can manufacture them.

The player is not required to manufacture every tool from raw ore.
Self-sufficiency is an optional long-term strategic achievement.

## 8. Inventory Integration

Inventory changes must be recorded as movements, not only as a silently
overwritten quantity.

Movement types should eventually include: - Purchase received -
Production input reserved - Production input consumed - Production
output received - Sale dispatched - Reservation released - Adjustment -
Waste/byproduct generated

For Milestone 01, maintain item quantity and an inventory movement
history. A single workshop location is sufficient.

## 9. Sales Integration

A sale must validate that the company has enough unreserved finished
goods.

For the first milestone: - Base sale price: \$25 per metal bracket. -
Player may sell a chosen positive quantity up to available quantity. -
Selling deducts inventory and credits company cash in one database
transaction. - A sale transaction records item, quantity, unit price,
gross revenue, and timestamp. - Do not allow negative quantities, zero
quantities, or sale quantities greater than available inventory.

Future market mechanics may change sale prices based on demand, quality,
contracts, reputation, and competition.

## 10. Data Validation and Content Integrity

Before loading game content: - Every recipe input/output item ID must
exist. - Every equipment capability referenced by a recipe must be
defined. - Every facility capability must be defined. - Every technology
requirement must exist. - Quantities and durations must be positive. -
Recipes must have at least one output. - Recipe IDs and item IDs must be
unique. - Recursive make paths must be cycle-checked. - Content versions
must be tracked.

## 11. Milestone 01 Test Scenarios

1.  Player without bench shear cannot start metal bracket production.
2.  Player without steel sheet cannot start production.
3.  Player with bench shear, workshop, technology, and one steel sheet
    can start one batch.
4.  Starting a batch reserves one steel sheet.
5.  A second batch cannot reserve the same sheet.
6.  Advancing 9 game minutes does not complete a 10-minute order.
7.  Advancing to 10 game minutes completes the order once.
8.  Completion consumes one sheet and adds ten brackets.
9.  Reprocessing the same completion event does not add another ten
    brackets.
10. Player can sell ten brackets and receive \$250.
11. Selling more than available inventory is rejected.
12. Cash and inventory remain unchanged if a purchase or sale
    transaction fails.
13. Reloading the save preserves all resulting state.
14. A deliberately cyclic recipe graph is rejected by content
    validation.
