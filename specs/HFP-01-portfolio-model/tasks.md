---

description: "Task list for ZIQ-101: Manage the spatial portfolio hierarchy"
---

# Tasks: Manage the spatial portfolio hierarchy

**Input**: Design documents from `/specs/HFP-01-portfolio-model/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api.md, quickstart.md

**Tests**: Included — constitution Principle III requires a test per endpoint before it is done.

**Organization**: Tasks are grouped by user story (US1, US2, US3) per spec.md priorities.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 / US2 / US3 / Setup / Foundational / Polish

## Path Conventions

Single Python backend per plan.md: `database/`, `backend-python/routers|services|repositories|schemas`, `backend-python/tests/unit|integration`.

---

## Phase 1: Setup

- [X] T001 Create `backend-python/` project skeleton (`main.py`, `db.py`, `requirements.txt` with fastapi, uvicorn, psycopg[binary], pydantic, pytest, httpx)
- [X] T002 [P] Add `.env`-driven config loader in `backend-python/config.py` (reads `DATABASE_URL`, `DEFAULT_PAGE_SIZE`, `MAX_PAGE_SIZE` via the framework's config system, never raw `.env` parsing in business code, per constitution)
- [X] T003 [P] Wire `backend-python/main.py` FastAPI app assembly (app factory, router registration placeholder, health check endpoint)

## Phase 2: Foundational (blocking prerequisites for all user stories)

- [X] T004 Add `portfolios`, `buildings`, `floors`, `zones` tables to `database/schema.sql` per data-model.md (PK, FK with `ON DELETE RESTRICT`, `UNIQUE` on `code` per table, `NOT NULL` on required fields, `created_at`/`updated_at` `DEFAULT now()`)
- [X] T005 Add seed rows for one full chain (portfolio → building → floor → zone) to `database/seed.sql`
- [X] T006 [P] Define Pydantic request/response schemas in `backend-python/schemas/portfolio.py`, `building.py`, `floor.py`, `zone.py` (response includes `id`/`created_at`/`updated_at`; request excludes them)
- [X] T007 [P] Define shared paginated-list envelope schema in `backend-python/schemas/pagination.py` (`items`, `total`, `limit`, `offset`)
- [X] T008 Implement DB connection/session dependency in `backend-python/db.py` (reads `DATABASE_URL` from config, not raw `.env`)
- [X] T009 [P] Implement shared error-mapping helper in `backend-python/errors.py` (maps not-found → `404`, validation/constraint violation → `422` with `{"detail": [{"field":..., "message":...}]}`)

**Checkpoint**: Schema exists, config/DB wiring works, shared schemas/errors ready — user story implementation can begin.

---

## Phase 3: User Story 1 — Record the operated space hierarchy (P1) 🎯 MVP

**Goal**: Create and view portfolios, buildings, floors, and zones (full chain), enforcing single-parent, required fields, and `code` uniqueness.

**Independent Test**: Create one portfolio → building (with address) → floor → zone (with area/occupancy); retrieve each individually and via paginated list.

### Tests for User Story 1

- [X] T010 [P] [US1] Unit test: `PortfolioService` create/get validation (blank name/code, duplicate code) in `backend-python/tests/unit/test_portfolio_service.py`
- [X] T011 [P] [US1] Unit test: `BuildingService` create/get validation (missing/blank address, unknown `portfolio_id`, duplicate code) in `backend-python/tests/unit/test_building_service.py`
- [X] T012 [P] [US1] Unit test: `FloorService` create/get validation (unknown `building_id`, duplicate code) in `backend-python/tests/unit/test_floor_service.py`
- [X] T013 [P] [US1] Unit test: `ZoneService` create/get validation (unknown `floor_id`, negative area/occupancy, duplicate code) in `backend-python/tests/unit/test_zone_service.py`
- [X] T014 [US1] Integration test: full chain create + get + paginated list round-trip (all 4 levels) in `backend-python/tests/integration/test_portfolio_hierarchy_crud.py`

### Implementation for User Story 1

- [X] T015 [P] [US1] Implement `PortfolioRepository` (insert, get_by_id, list paginated) in `backend-python/repositories/portfolio_repository.py`
- [X] T016 [P] [US1] Implement `BuildingRepository` (insert, get_by_id, list paginated by `portfolio_id`) in `backend-python/repositories/building_repository.py`
- [X] T017 [P] [US1] Implement `FloorRepository` (insert, get_by_id, list paginated by `building_id`) in `backend-python/repositories/floor_repository.py`
- [X] T018 [P] [US1] Implement `ZoneRepository` (insert, get_by_id, list paginated by `floor_id`) in `backend-python/repositories/zone_repository.py`
- [X] T019 [US1] Implement `PortfolioService` (create/get/list, `422` on blank fields or duplicate code) in `backend-python/services/portfolio_service.py`
- [X] T020 [US1] Implement `BuildingService` (create/get/list, validates parent `portfolio_id` exists, required `address`) in `backend-python/services/building_service.py`
- [X] T021 [US1] Implement `FloorService` (create/get/list, validates parent `building_id` exists) in `backend-python/services/floor_service.py`
- [X] T022 [US1] Implement `ZoneService` (create/get/list, validates parent `floor_id` exists, non-negative area/occupancy) in `backend-python/services/zone_service.py`
- [X] T023 [P] [US1] Implement `portfolios` router (`GET`/`GET {id}`/`POST`) in `backend-python/routers/portfolios.py`
- [X] T024 [P] [US1] Implement `buildings` router (`GET`/`GET {id}`/`POST`) in `backend-python/routers/buildings.py`
- [X] T025 [P] [US1] Implement `floors` router (`GET`/`GET {id}`/`POST`) in `backend-python/routers/floors.py`
- [X] T026 [P] [US1] Implement `zones` router (`GET`/`GET {id}`/`POST`) in `backend-python/routers/zones.py`
- [X] T027 [US1] Register all four routers in `backend-python/main.py`

**Checkpoint**: User Story 1 fully functional and testable independently (create + view at every level).

---

## Phase 4: User Story 2 — Keep space records current (P2)

**Goal**: Update editable fields on any hierarchy level; reject invalid updates; leave stored record unchanged on rejection.

**Independent Test**: Update an existing building's address and a zone's area/occupancy; confirm new values and `updated_at` change; submit an invalid update (negative occupancy) and confirm rejection with unchanged stored record.

### Tests for User Story 2

- [X] T028 [P] [US2] Unit test: update validation (invalid values rejected, valid values applied) for all four services in `backend-python/tests/unit/test_*_service.py` (extend existing files)
- [X] T029 [US2] Integration test: update building address + zone area/occupancy, confirm `updated_at` > `created_at`; update with negative occupancy confirms `422` and unchanged record, in `backend-python/tests/integration/test_portfolio_hierarchy_update.py`

### Implementation for User Story 2

- [X] T030 [P] [US2] Add `update` method to each repository (`portfolio_repository.py`, `building_repository.py`, `floor_repository.py`, `zone_repository.py`)
- [X] T031 [US2] Add `update` method to each service applying the same validation rules as create (last-write-wins, no version check)
- [X] T032 [P] [US2] Add `PUT /{id}` route to each of the four routers

**Checkpoint**: User Stories 1 and 2 both independently functional.

---

## Phase 5: User Story 3 — Remove space records no longer in operation (P3)

**Goal**: Remove leaf/empty hierarchy records; removed records return `404` afterward.

**Independent Test**: Create a zone with no dependents, remove it, confirm it no longer appears in listing or direct retrieval; same for an empty portfolio/building/floor.

### Tests for User Story 3

- [X] T033 [US3] Integration test: delete zone → subsequent GET returns `404`, removed from list; delete empty portfolio/building/floor succeeds, in `backend-python/tests/integration/test_portfolio_hierarchy_delete.py`

### Implementation for User Story 3

- [X] T034 [P] [US3] Add `delete` method to each repository
- [X] T035 [US3] Add `delete` method to each service (`404` if id not found)
- [X] T036 [P] [US3] Add `DELETE /{id}` route (returns `204`) to each of the four routers

**Checkpoint**: All three user stories independently functional; full CRUD available at every hierarchy level.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T037 [P] Run quickstart.md validation scenarios end-to-end against a live local Postgres instance
- [X] T038 [P] Update `docs/CONTRACTS.md` (or create if absent) with the finalized ZIQ-101 API surface, cross-referencing `specs/HFP-01-portfolio-model/contracts/api.md`
- [X] T039 Add traceability entries mapping FR-001 through FR-016 to their covering tests (unit/integration test names)

---

## Dependencies & Execution Order

- **Setup (T001-T003)** → **Foundational (T004-T009)** → User Stories, in priority order.
- **US1 (T010-T027)** has no dependency on US2/US3 and is independently testable/deliverable as MVP.
- **US2 (T028-T032)** depends on US1's repositories/services/routers existing (adds methods/routes to the same files).
- **US3 (T033-T036)** depends on US1's repositories/services/routers existing; independent of US2.
- **Polish (T037-T039)** runs after all user stories are complete.

## Parallel Execution Examples

- Within Foundational: T006, T007, T009 can run in parallel (different files); T004/T005/T008 are sequential (schema before seed, DB wiring shared).
- Within US1: T015-T018 (repositories) can run in parallel; T023-T026 (routers) can run in parallel after their respective services (T019-T022, sequential per entity due to shared patterns) are done.
- Within US2/US3: repository update/delete methods (T030, T034) can run in parallel across the four entities.

## Implementation Strategy

**MVP = User Story 1 only** (T001-T027): delivers create + view across the full
Portfolio → Building → Floor → Zone chain, independently testable and demoable.
User Story 2 (update) and User Story 3 (delete) are incremental additions on top of
the same files, deliverable and testable independently once US1 is merged.
