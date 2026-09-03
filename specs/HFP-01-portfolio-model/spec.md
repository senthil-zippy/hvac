# Spec: ZIQ-101 — Manage the spatial portfolio hierarchy

**Epic:** HFP-01 - Portfolio and Asset Model
**Priority:** P0

## User Story
As a Facilities Manager, I want to create, view, update, and remove portfolios,
buildings, floors, and zones so that the platform reflects the spaces we operate.

## Scope
CRUD for the spatial hierarchy: Portfolio → Building → Floor → Zone.

## Domain Model
| Entity | Key fields |
|---|---|
| Portfolio | id, name, code |
| Building | id, portfolio_id, name, code, address |
| Floor | id, building_id, name, code |
| Zone | id, floor_id, name, code, area, occupancy |

- A Zone belongs to exactly one Floor; a Floor belongs to exactly one Building.
- `created_at` / `updated_at` are database-owned (server-generated), not client-supplied.

## Acceptance Criteria
1. CRUD endpoints exist for each hierarchy level (Portfolio, Building, Floor, Zone).
2. A Building records its address; a Zone records area and occupancy.
3. A Zone can belong to only one Floor and a Floor to only one Building (enforced by FK + non-null parent).
4. Requesting a missing resource returns `404`.
5. An invalid request body returns `422` with field-level validation errors.
6. Creation and update timestamps are set by the database, never trusted from the client.

## Out of Scope
- Deletion-safety rules for populated hierarchy nodes (covered by ZIQ-102).
- Device/controller registration (covered by ZIQ-103).
- Filtering/search across hierarchy attributes (covered by ZIQ-104).

## API Surface (draft)
```
GET    /api/portfolios            GET    /api/portfolios/{id}
POST   /api/portfolios            PUT    /api/portfolios/{id}     DELETE /api/portfolios/{id}

GET    /api/buildings             GET    /api/buildings/{id}
POST   /api/buildings             PUT    /api/buildings/{id}      DELETE /api/buildings/{id}

GET    /api/floors                GET    /api/floors/{id}
POST   /api/floors                PUT    /api/floors/{id}         DELETE /api/floors/{id}

GET    /api/zones                 GET    /api/zones/{id}
POST   /api/zones                 PUT    /api/zones/{id}          DELETE /api/zones/{id}
```

## Traceability
Source: [docs/JIRA_USER_STORIES.md](../../docs/JIRA_USER_STORIES.md) — ZIQ-101.
