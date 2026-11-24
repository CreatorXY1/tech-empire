# Tech Empire --- Technology Tree and Progression

**Document status:** Foundational source of truth\
**Version:** 1.0\
**Related documents:** `GAME_DESIGN.md`, `MANUFACTURING_SYSTEM.md`

------------------------------------------------------------------------

## 1. Purpose

This document defines how technological capabilities are organized,
researched, and unlocked in Tech Empire.

Technology progression is realistic and capability-based. It should
reflect plausible relationships between engineering disciplines,
materials, processes, equipment, and products.

The tree is not a simple list of levels. It is a directed dependency
graph. Technologies may have multiple prerequisites, and multiple
branches may progress in parallel.

## 2. Core Rules

1.  A technology definition is global game content; a company's unlock
    is player state.
2.  A technology can unlock one or more capabilities, recipes, equipment
    designs, product designs, or further technologies.
3.  A technology may require several prerequisite technologies.
4.  Research can require money, time, personnel, facilities, and
    experimental materials.
5.  The player may acquire a product or machine from a supplier without
    researching how to manufacture it, unless the item is restricted by
    a separate game rule.
6.  Owning equipment does not automatically grant the knowledge to use
    every process it could theoretically support.
7.  A technology should represent a meaningful capability, not a tiny
    arbitrary stat increase.
8.  Technologies must not have circular prerequisites.
9.  Era labels are organizational groupings, not mandatory chronological
    locks.
10. The game may simplify real-world complexity, but simplifications
    must be documented.

## 3. Technology Definition

Each technology should have, at minimum:

  -----------------------------------------------------------------------
  Field                               Meaning
  ----------------------------------- -----------------------------------
  `id`                                Stable unique identifier

  `name`                              Player-facing name

  `description`                       Explanation of the capability

  `discipline`                        Engineering or science branch

  `era`                               Broad progression era

  `prerequisites`                     Required technology IDs

  `research_cost`                     Funding requirement

  `research_duration`                 Base game-time duration

  `facility_requirements`             Required research facility
                                      capabilities

  `staff_requirements`                Optional role/skill requirements

  `material_requirements`             Optional experimental inputs

  `unlocks`                           Capability, recipe, equipment,
                                      product, or technology IDs

  `status`                            Content lifecycle state, such as
                                      planned or available
  -----------------------------------------------------------------------

Use stable IDs such as `basic_metalworking`, `electrical_motors`, and
`printed_circuit_boards`. Display names may change without changing IDs.

## 4. Technology Disciplines

### 4.1 Mechanical Engineering

Covers: - Hand tools and workshop practice - Measurement and
tolerances - Metal cutting, drilling, forming, and joining - Machine
elements, bearings, gears, and shafts - Machine tools - CNC systems and
precision manufacturing - Robotics and mechatronics

### 4.2 Materials Science and Metallurgy

Covers: - Ferrous and non-ferrous metals - Alloys and heat treatment -
Polymers and composites - Ceramics and glass - Semiconductor-grade
materials - Surface treatments and coatings - Advanced materials
research

### 4.3 Electrical Engineering

Covers: - Electrical safety and fundamentals - DC/AC power - Motors and
generators - Transformers and power distribution - Power electronics -
Sensors and control systems - Industrial power and automation

### 4.4 Electronics Engineering

Covers: - Passive components - Diodes and transistors - Analog and
digital circuits - Printed circuit boards - Surface-mount assembly -
Integrated circuits - Electronic testing and reliability

### 4.5 Computer Engineering and Computer Science

Covers: - Digital logic - Computer architecture - Microprocessors -
Memory and storage systems - Firmware and embedded systems - Operating
systems and software - Networking and server systems

### 4.6 Semiconductor Engineering

Covers: - Semiconductor materials and device physics - Wafer
preparation - Oxidation and deposition - Photolithography - Etching and
doping - Thin-film processing - Process integration - Chip testing,
dicing, and packaging - Advanced packaging and process research

### 4.7 Manufacturing Engineering

Covers: - Production planning - Process capability and quality control -
Industrial automation - Lean manufacturing - Robotics - Factory control
systems - Advanced production optimization

### 4.8 Chemical and Process Engineering

Covers: - Chemical handling and process safety - Purification and
separation - Industrial gases and chemicals - Process control -
Specialty chemical production - Cleanroom utilities and waste treatment

### 4.9 Energy and Environmental Systems

Covers: - Power generation - Batteries and energy storage - Power
conversion - Cooling and thermal management - Energy efficiency - Water
treatment and industrial utilities

## 5. Broad Progression Eras

Eras organize the technology catalog. They do not automatically unlock
all technologies in an era.

### Era 1 --- Basic Industry and Mechanical Workshop

Foundational capabilities: - Basic Workshop Practice - Basic
Metalworking - Measurement and Dimensional Inspection - Drilling and
Cutting - Joining and Fastening - Basic Materials Handling

Example outputs: - Fasteners - Brackets - Simple tools - Metal frames -
Basic mechanical assemblies

**Milestone 01 starting condition:** `basic_metalworking` is already
unlocked.

### Era 2 --- Electrical Industry

Potential capabilities: - Electrical Fundamentals - Electrical Safety
and Wiring - Electromagnetism - Electric Motor Fundamentals - Generator
and Transformer Fundamentals - Basic Electrical Testing - Industrial
Motor Control

Example outputs: - Wiring assemblies - Simple motors - Power supplies -
Transformers - Electrical control panels

### Era 3 --- Electronics Industry

Potential capabilities: - Passive Electronic Components - Semiconductor
Device Fundamentals - Diodes and Transistors - Analog Electronics -
Digital Logic - PCB Design - PCB Fabrication - PCB Assembly and
Soldering - Electronic Testing

Example outputs: - Circuit boards - Electronic controllers - Radios -
Sensors - Power-control modules

### Era 4 --- Computer Industry

Potential capabilities: - Boolean Logic and Digital Systems - Computer
Architecture - Microprocessor Fundamentals - Memory Architecture -
Storage Technologies - Embedded Systems - Firmware Development -
Computer System Integration

Example outputs: - Microcontroller boards - Computer systems - Servers -
Memory modules - Storage devices

### Era 5 --- Semiconductor Industry

Potential capabilities: - Semiconductor Materials - Wafer Preparation -
Cleanroom Operations - Thin-Film Deposition - Photolithography -
Etching - Doping and Ion Implantation - Process Integration - Wafer
Inspection and Metrology - Dicing and Packaging - Semiconductor Test

Example outputs: - Integrated circuits - Memory chips -
Microprocessors - Graphics processors - Specialized controllers

Semiconductor fabrication is a major industrial undertaking. It requires
a network of specialized equipment, materials, utilities, process
control, metrology, and trained personnel. It must not be represented as
one generic "chip machine."

### Era 6 --- Consumer Technology

Potential capabilities: - Mobile System Integration - Display
Technologies - Battery Pack Engineering - Camera Module Integration -
Wireless Communication - Thermal and Power Management - Device
Reliability Testing - Consumer Product Design

Example outputs: - Smartphones - Tablets - Laptops - Wearables - Smart
home devices

### Era 7 --- Advanced Computing and Industrial Robotics

Potential capabilities: - High-Performance Computing - AI Accelerator
Architecture - Advanced Semiconductor Packaging - Industrial Robotics -
Machine Vision - Autonomous Control - High-Density Energy Storage -
Advanced Thermal Management

Example outputs: - AI servers - Industrial robots - High-performance
compute systems - Advanced automation platforms

### Era 8 --- Industrial Leadership and Advanced R&D

Potential capabilities: - Cutting-edge process development - Advanced
packaging research - Novel materials research - High-precision
manufacturing systems - Advanced industrial automation - Specialized
next-generation computing

This era represents difficult, expensive research and industrial
leadership. It should remain grounded in plausible engineering rather
than becoming magical or purely science-fictional.

## 6. Example Dependency Graphs

The following are conceptual relationships. Exact prerequisites should
be finalized as game content is balanced.

### 6.1 Metal bracket

`Basic Workshop Practice`\
→ `Basic Metalworking`\
→ `Metal Cutting and Forming`\
→ `Metal Bracket Recipe`

The bracket recipe also requires a suitable workshop, a bench shear, and
steel sheet inventory. Technology alone is insufficient.

### 6.2 Electric motor

`Electrical Fundamentals` + `Mechanical Workshop Practice`\
→ `Electromagnetism`\
→ `Electric Motor Fundamentals`\
→ `Motor Winding and Assembly`\
→ `Electric Motor Recipe`

Possible inputs include copper wire, steel laminations, shaft, bearings,
insulation, and housing. Production requires winding and assembly
equipment appropriate to the recipe.

### 6.3 Printed circuit board

`Electronics Fundamentals`\
→ `PCB Design`\
→ `PCB Fabrication`\
→ `PCB Assembly`

PCB design, bare-board fabrication, and component assembly are separate
capabilities and should not be collapsed into one process when the
simulation becomes more detailed.

### 6.4 CPU

`Semiconductor Device Fundamentals`\
→ `Semiconductor Materials`\
→ `Wafer Preparation`\
→ `Photolithography`, `Deposition`, `Etching`, and `Doping`\
→ `Process Integration`\
→ `Integrated Circuit Design and Fabrication`\
→ `Wafer Test`\
→ `Dicing and Packaging`\
→ `Microprocessor Product`

A CPU also requires architecture/design capability and a validated chip
design. Having a fabrication facility alone does not create a working
processor.

### 6.5 Smartphone

`Computer Engineering` + `Consumer Product Design` + relevant component
capabilities\
→ `Mobile System Integration`\
→ `Smartphone Assembly`

A smartphone recipe can require CPU, memory, storage, display, battery
pack, camera module, motherboard/PCB assembly, enclosure, and final
test. The player may purchase some components while manufacturing
others.

## 7. Research Projects

Research projects are active company activities that attempt to unlock a
technology or improve an existing capability.

A research project should record: - Technology being researched -
Status: locked, available, active, completed, or cancelled - Progress
and required effort - Start and completion time - Funding
committed/spent - Assigned staff and facility - Consumed experimental
materials - Completion result

Research must validate prerequisites before it starts. Progress should
be computed by the backend simulation, not by a frontend-only timer.

## 8. Technology Unlock Types

A completed technology may unlock one or more of:

1.  **Process capability:** A company can execute a manufacturing
    process.
2.  **Recipe:** A company can manufacture a specific item.
3.  **Equipment design:** A company can design/manufacture a machine.
4.  **Product design:** A company can design a product for
    manufacturing.
5.  **Facility capability:** A facility can support a new class of
    process.
6.  **Efficiency improvement:** A documented modifier to time, yield,
    quality, or resource use.
7.  **Further research:** New technology projects become available.

Unlocks should be explicit and machine-readable.

## 9. Equipment and Technology Are Separate

Technology and equipment are distinct requirements.

Example: - A company may research CNC machining but not own a CNC
machine. - A company may purchase a CNC machine but not have the
advanced design knowledge required for a particular precision process. -
A company may outsource a machined component without owning a machine or
researching the process.

The requirement validator must check each requirement category
separately.

## 10. Research Balance Principles

-   Early technologies should be inexpensive and quick enough to support
    learning.
-   Advanced technologies should require meaningful investment and
    prerequisites.
-   Research cost should scale with industrial complexity, not arbitrary
    era labels alone.
-   Multiple branches should offer strategic options.
-   Research should unlock useful capabilities, not only numerical
    bonuses.
-   Avoid hard dead ends: where reasonable, the player should have
    purchase or outsourcing alternatives.
-   A player should always be able to identify the next actionable
    prerequisite.

## 11. Milestone 01 Technology Scope

Only the following technology content is required for the first playable
workshop:

  -----------------------------------------------------------------------
  Technology              Initial state           Purpose
  ----------------------- ----------------------- -----------------------
  Basic Workshop Practice Unlocked                Enables basic workshop
                                                  operations

  Basic Metalworking      Unlocked                Enables metal bracket
                                                  recipe

  Metal Cutting and       May be represented as   Avoids unnecessary
  Forming                 included in Basic       early research gate
                          Metalworking for MVP    
  -----------------------------------------------------------------------

No research timer, research staff, or research laboratory is required
for Milestone 01. The technology model should nevertheless be designed
so these can be added later.

## 12. Validation Requirements

-   Every prerequisite ID must refer to an existing technology.
-   Technology prerequisite graph must be acyclic.
-   Every unlock ID must refer to a known capability or content
    definition.
-   Research cannot start when prerequisites are unmet.
-   A completed technology cannot be researched again unless a future
    repeatable research mechanic explicitly allows it.
-   Save data should store unlocked technology IDs, not duplicate the
    full technology definition.
-   Definition version changes must not silently invalidate existing
    saves.
