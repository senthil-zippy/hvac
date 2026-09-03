# Data Model: ZIQ-101 — Manage the spatial portfolio hierarchy

## Portfolio
| Field | Type | Constraints |
|---|---|---|
| id | uuid / serial (PK) | generated |
| name | text | required, non-empty |
| code | text | required, non-empty, **unique** (global) |
| created_at | timestamptz | DB-set, `DEFAULT now()` |
| updated_at | timestamptz | DB-set, updated on write |

## Building
| Field | Type | Constraints |
|---|---|---|
| id | uuid / serial (PK) | generated |
| portfolio_id | FK → Portfolio.id | required, not null |
| name | text | required, non-empty |
| code | text | required, non-empty, **unique** (global) |
| address | text | required, non-empty (FR-012) |
| created_at | timestamptz | DB-set |
| updated_at | timestamptz | DB-set |

## Floor
| Field | Type | Constraints |
|---|---|---|
| id | uuid / serial (PK) | generated |
| building_id | FK → Building.id | required, not null |
| name | text | required, non-empty |
| code | text | required, non-empty, **unique** (global) |
| created_at | timestamptz | DB-set |
| updated_at | timestamptz | DB-set |

## Zone
| Field | Type | Constraints |
|---|---|---|
| id | uuid / serial (PK) | generated |
| floor_id | FK → Floor.id | required, not null |
| name | text | required, non-empty |
| code | text | required, non-empty, **unique** (global) |
| area | numeric | required, **non-negative** (FR-013) |
| occupancy | integer | required, **non-negative** (FR-013) |
| created_at | timestamptz | DB-set |
| updated_at | timestamptz | DB-set |

## Relationships
- Portfolio 1—* Building (FK `buildings.portfolio_id`, `NOT NULL`, `ON DELETE RESTRICT`)
- Building 1—* Floor (FK `floors.building_id`, `NOT NULL`, `ON DELETE RESTRICT`)
- Floor 1—* Zone (FK `zones.floor_id`, `NOT NULL`, `ON DELETE RESTRICT`)

`ON DELETE RESTRICT` is used (not `CASCADE`) because deletion-safety rules for
populated nodes belong to ZIQ-102; for ZIQ-101 a simple DB-level restrict prevents
orphaning without yet implementing the friendlier validation-error response that
ZIQ-102 will add.

## Validation Rules (enforced in Service layer, backed by DB constraints)
- `name`, `code` non-empty on all four entities.
- `code` unique per entity type (DB `UNIQUE` constraint; duplicate → `422`).
- `address` non-empty on Building.
- `area` >= 0 and `occupancy` >= 0 on Zone.
- Parent id must reference an existing row, else `422` (missing parent) or `404`
  (parent id well-formed but not found — service disambiguates per FR-009/FR-010).

## State Transitions
None — these are simple CRUD entities with no lifecycle/status field in this story.
