# Implementation Plan: Manage the spatial portfolio hierarchy

**Branch**: `HFP-01-portfolio-model` | **Date**: 2026-09-03 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/HFP-01-portfolio-model/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

CRUD for the spatial hierarchy (Portfolio → Building → Floor → Zone) as a Python
FastAPI backend behind a documented REST contract, backed by PostgreSQL. Layering
follows the constitution: Router → Service → Repository, with the repository as the
only place SQL lives. Schema is authored once in `database/schema.sql`.
Globally-unique `code` per entity type, paginated list endpoints, and last-write-wins
concurrency per the ZIQ-101 clarifications.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: FastAPI, Pydantic v2, psycopg (or SQLAlchemy Core, no ORM
auto-migrations per constitution), uvicorn, pytest, httpx (test client)

**Storage**: PostgreSQL (containerized), schema in `database/schema.sql`

**Testing**: pytest (unit for services, integration for routers against a real test
database)

**Target Platform**: Linux container / local dev on Windows via Docker Postgres

**Project Type**: web-service (backend only for this slice; frontend deferred)

**Performance Goals**: not specified for this story; standard CRUD latency
(sub-200ms p95 for single-record reads) is a reasonable local target, not a hard gate

**Constraints**: no ORM auto-migrations (`create_all()` / `ddl-auto` forbidden by
constitution); `created_at`/`updated_at` are database-set only; `code` unique per
entity type; list endpoints paginated; last-write-wins on concurrent updates

**Scale/Scope**: capstone scale (single portfolio, dozens of buildings/zones) — no
special sharding/partitioning needed

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Layered Architecture, No Skipping** — PASS. Plan uses Router → Service →
  Repository; no SQL outside repositories; no business rules in routers.
- **II. Schema Owned Once** — PASS. `portfolios`/`buildings`/`floors`/`zones` tables
  added to `database/schema.sql`; no ORM auto-migration tooling used.
  `created_at`/`updated_at` are `DEFAULT now()`, never client-supplied.
- **III. Spec-First, Test-First** — PASS. This plan follows `spec.md`; `tasks.md`
  (next step) will require a test per endpoint before implementation is done.
- **IV. Contract-Driven Interfaces & Cross-Backend Parity** — PASS for this slice.
  Error contract fixed to `404`/`422` per constitution; only one backend
  (Python) is being built for this story, so cross-backend parity is N/A until/unless
  other backends are added later.
- **V. Determinism, Audit & Governed Autonomy** — PARTIAL/N/A for this story. No
  device feed, alarm, or command state is touched by ZIQ-101, so determinism and
  audit-event requirements do not yet apply; no gate violation.

No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
database/
├── schema.sql              # authoritative; add portfolios/buildings/floors/zones tables
├── seed.sql                # dev/test seed rows
└── migrations/             # numbered files for any post-schema.sql changes

backend-python/
├── routers/
│   ├── portfolios.py
│   ├── buildings.py
│   ├── floors.py
│   └── zones.py
├── services/
│   ├── portfolio_service.py
│   ├── building_service.py
│   ├── floor_service.py
│   └── zone_service.py
├── repositories/
│   ├── portfolio_repository.py
│   ├── building_repository.py
│   ├── floor_repository.py
│   └── zone_repository.py
├── schemas/                 # Pydantic request/response models
├── db.py                    # connection/session setup (reads config, not raw .env)
├── main.py                  # FastAPI app assembly
└── tests/
    ├── unit/                # service-layer validation tests
    └── integration/         # router + real test-DB CRUD round-trips
```

**Structure Decision**: Backend-only web-service slice. Single Python backend
(`backend-python/`) per constitution's allowed stack choices, layered
Router → Service → Repository. Frontend is explicitly deferred for this story
(per user decision) and will reuse this same REST contract when built.

## Complexity Tracking

> No constitution violations identified; table intentionally left empty.
