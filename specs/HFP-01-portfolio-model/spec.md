# Feature Specification: Manage the spatial portfolio hierarchy

**Feature Branch**: `HFP-01-portfolio-model`

**Created**: 2026-09-03

**Status**: Draft

**Input**: User description: "Manage the spatial portfolio hierarchy (ZIQ-101, Epic HFP-01: Portfolio and Asset Model, Priority P0). As a Facilities Manager, I want to create, view, update, and remove portfolios, buildings, floors, and zones so that the platform reflects the spaces we operate. Acceptance criteria: CRUD endpoints and UI workflows exist for each hierarchy level (Portfolio, Building, Floor, Zone); a building records its address; a zone records area and occupancy; a zone can belong to only one floor and a floor to only one building; missing resources return 404; invalid bodies return 422; creation and updates record database-owned timestamps."

**Traceability**: [docs/JIRA_USER_STORIES.md](../../docs/JIRA_USER_STORIES.md) — ZIQ-101, Epic HFP-01, Priority P0.

## Clarifications

### Session 2026-09-03

- Q: Should Portfolio/Building/Floor/Zone `code` values be unique, and at what scope? → A: Globally unique across the whole entity type (e.g., no two buildings in the system share a code, regardless of portfolio).
- Q: Should the list endpoints (portfolios/buildings/floors/zones) support pagination? → A: Yes, paginated with limit/offset (or cursor) parameters; unbounded full-list responses are not acceptable.
- Q: How should concurrent updates to the same record be handled? → A: Last write wins; no optimistic-concurrency/version check is required for this story.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Record the operated space hierarchy (Priority: P1)

As a Facilities Manager, I want to create and view portfolios, buildings, floors, and zones so that the platform has an accurate record of every space we operate before any other fleet data (devices, telemetry, alarms) can be attached to it.

**Why this priority**: Nothing else in the platform can exist without a space to attach to. This is the minimum viable slice: without it, no device, telemetry, or alarm feature can be exercised.

**Independent Test**: Can be fully tested by creating a portfolio, a building under it (with address), a floor under that building, and a zone under that floor (with area and occupancy), then retrieving each record individually and as a list — delivering a usable, navigable space hierarchy on its own.

**Acceptance Scenarios**:

1. **Given** no existing portfolios, **When** a Facilities Manager creates a portfolio with a name and code, **Then** the portfolio is created and appears when listed and retrieved by id.
2. **Given** an existing portfolio, **When** a Facilities Manager creates a building under it with a name, code, and address, **Then** the building is created, linked to that portfolio, and its address is retrievable.
3. **Given** an existing building, **When** a Facilities Manager creates a floor under it, **Then** the floor is created and linked to exactly that building.
4. **Given** an existing floor, **When** a Facilities Manager creates a zone under it with area and occupancy, **Then** the zone is created, linked to exactly that floor, and its area and occupancy are retrievable.
5. **Given** a hierarchy of portfolios, buildings, floors, and zones, **When** a Facilities Manager requests a listing at any level, **Then** all records at that level are returned.

---

### User Story 2 - Keep space records current (Priority: P2)

As a Facilities Manager, I want to update portfolio, building, floor, and zone records so that the platform stays accurate as addresses change, spaces are renamed, or measured area and occupancy are corrected.

**Why this priority**: Space data changes over time (renovations, re-measurements, renaming). Accurate records depend on being able to correct them, but this is only valuable once records exist (User Story 1).

**Independent Test**: Can be fully tested by updating an existing building's address and an existing zone's area/occupancy, then confirming the retrieved record reflects the new values and an updated timestamp.

**Acceptance Scenarios**:

1. **Given** an existing building, **When** a Facilities Manager updates its address, **Then** the retrieved building reflects the new address and an updated timestamp newer than its creation timestamp.
2. **Given** an existing zone, **When** a Facilities Manager updates its area and occupancy, **Then** the retrieved zone reflects the new values.
3. **Given** an update request with an invalid value (e.g., negative occupancy), **When** it is submitted, **Then** the update is rejected and the stored record is unchanged.

---

### User Story 3 - Remove space records no longer in operation (Priority: P3)

As a Facilities Manager, I want to remove portfolio, building, floor, and zone records so that the platform doesn't retain spaces we no longer operate.

**Why this priority**: Least frequent operation and lowest immediate value; removal safety rules for populated hierarchy nodes are handled by a separate story (ZIQ-102), so this story only needs to cover straightforward removal of empty/leaf records.

**Independent Test**: Can be fully tested by creating a zone with no dependents and removing it, then confirming it no longer appears in listings or direct retrieval.

**Acceptance Scenarios**:

1. **Given** an existing zone, **When** a Facilities Manager removes it, **Then** it no longer appears in listings and requesting it by id returns not-found.
2. **Given** an existing portfolio, building, or floor with no children, **When** a Facilities Manager removes it, **Then** it is removed and no longer retrievable.

---

### Edge Cases

- Requesting a portfolio, building, floor, or zone by an id that doesn't exist returns a not-found response.
- Submitting a create or update request with a missing required field, wrong data type, or invalid value (e.g., negative area, negative occupancy, blank name) returns a validation error identifying the offending field(s).
- Submitting a create request for a building, floor, or zone without specifying its required parent (portfolio, building, or floor respectively) returns a validation error.
- Submitting a client-supplied value for creation or update timestamps has no effect; the system always uses its own clock.
- Attempting to re-parent a zone to a floor belonging to a different building than its current floor is treated as a normal update to the zone's floor reference (the floor/building relationship itself is fixed at the floor level).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow creation of a Portfolio with a name and code.
- **FR-002**: System MUST allow creation of a Building under a Portfolio with a name, code, and address.
- **FR-003**: System MUST allow creation of a Floor under a Building with a name and code.
- **FR-004**: System MUST allow creation of a Zone under a Floor with a name, code, area, and occupancy.
- **FR-005**: System MUST allow viewing a single record and listing all records at each hierarchy level (Portfolio, Building, Floor, Zone), with list results paginated (limit/offset or cursor) rather than returned as one unbounded set.
- **FR-006**: System MUST allow updating the editable fields of a Portfolio, Building, Floor, or Zone.
- **FR-007**: System MUST allow removing a Portfolio, Building, Floor, or Zone record.
- **FR-008**: System MUST enforce that every Zone belongs to exactly one Floor, and every Floor belongs to exactly one Building, at all times.
- **FR-009**: System MUST return a not-found response when a request targets a Portfolio, Building, Floor, or Zone id that does not exist.
- **FR-010**: System MUST return a validation error response with field-level detail when a create or update request body is invalid (missing required field, wrong type, or out-of-range value).
- **FR-011**: System MUST set creation and update timestamps itself and MUST ignore any timestamp values supplied by the client.
- **FR-012**: System MUST require and store a non-empty address on every Building.
- **FR-013**: System MUST require and store a non-negative area and a non-negative occupancy on every Zone.
- **FR-014**: System MUST provide a UI workflow for a Facilities Manager to perform create, view, update, and remove actions at each hierarchy level.
- **FR-015**: System MUST enforce that each entity's `code` is unique across all records of that entity type (e.g., no two Buildings anywhere share a code), rejecting a duplicate with a validation error.
- **FR-016**: System MUST apply last-write-wins semantics on concurrent updates to the same record; no version/ETag conflict check is required.

### Key Entities

- **Portfolio**: Top of the hierarchy; represents a collection of buildings under common management. Identified by name and code.
- **Building**: Belongs to exactly one Portfolio; represents a physical building. Has a name, code, and address.
- **Floor**: Belongs to exactly one Building; represents a floor within that building. Has a name and code.
- **Zone**: Belongs to exactly one Floor; represents an operational space within that floor. Has a name, code, area, and occupancy.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A Facilities Manager can create a full portfolio-to-zone chain (one portfolio, one building, one floor, one zone) and retrieve every record individually within a single working session, with no manual data-consistency fixes required afterward.
- **SC-002**: 100% of requests referencing a nonexistent Portfolio, Building, Floor, or Zone id receive a not-found response.
- **SC-003**: 100% of create/update requests with invalid or missing required data receive a validation error identifying the specific field(s) at fault.
- **SC-004**: 100% of stored creation and update timestamps match the system's own clock at the time of the write, regardless of any timestamp value submitted by the client.
- **SC-005**: 0% of Zones or Floors can exist without a valid parent Floor or Building respectively, verified across all records at any point in time.

## Assumptions

- The existing platform authentication/authorization model determines who may act as a "Facilities Manager"; this feature does not introduce new auth mechanisms.
- Name and code fields are free-text but required (non-empty) at every hierarchy level; `code` is additionally unique per entity type across the entire system (see Clarifications).
- Removal in this story covers only straightforward deletion of records; refusing deletion of a hierarchy node that still has children is explicitly out of scope here and is covered by ZIQ-102.
- Concurrent writes to the same record use last-write-wins; no optimistic concurrency control is introduced by this story.
- List endpoints return paginated results; the pagination style (limit/offset vs. cursor) is finalized during planning.
- "UI workflows" refers to the platform's existing web administration surface; no new client application is introduced by this feature.
