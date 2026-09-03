# Research: ZIQ-101 — Manage the spatial portfolio hierarchy

No NEEDS CLARIFICATION markers remain in Technical Context — all resolved via the
constitution (stack constraints) and the `/speckit.clarify` session in `spec.md`.
This phase documents the concrete choices made and why.

## Decision: Backend framework — FastAPI
- **Rationale**: Constitution permits .NET/Python/Java; user selected Python.
  FastAPI gives native Pydantic request/response validation (maps directly to the
  `422` error contract) and async-ready routing with minimal boilerplate.
- **Alternatives considered**: Flask (no built-in validation/typing — would require
  manual `422` mapping), Django REST Framework (heavier, ORM-centric — conflicts
  with constitution's "no ORM auto-migrations" rule).

## Decision: Database access — psycopg (raw SQL), no ORM auto-migration
- **Rationale**: Constitution Principle II forbids `create_all()` / `ddl-auto`.
  Repository layer owns all SQL; using an ORM purely as a query builder (e.g.
  SQLAlchemy Core) is acceptable, but auto-generated schema management is not.
  For this CRUD slice, parameterized SQL via psycopg is simplest and keeps
  repositories thin and testable.
- **Alternatives considered**: SQLAlchemy ORM with Alembic (Alembic migrations
  would satisfy "numbered migration files" but the ORM session/model layer adds
  complexity not needed for four simple hierarchical tables).

## Decision: Global uniqueness for `code`
- **Rationale**: Confirmed via `/speckit.clarify` — enforced with a `UNIQUE`
  constraint per table (`portfolios.code`, `buildings.code`, `floors.code`,
  `zones.code`), independent of parent. A duplicate insert/update raises a DB
  constraint violation, caught and mapped to `422` by the service layer.
- **Alternatives considered**: Composite uniqueness (parent_id, code) — rejected
  per clarification answer favoring simpler global uniqueness for this story.

## Decision: Pagination — limit/offset query params
- **Rationale**: Confirmed via `/speckit.clarify`. Simple, well-understood,
  sufficient at capstone scale; avoids cursor-token bookkeeping.
- **Alternatives considered**: Cursor-based pagination — more robust under
  concurrent inserts but unnecessary complexity for this scale; can be introduced
  later without breaking the response envelope (`items` + pagination metadata).

## Decision: Concurrency — last-write-wins
- **Rationale**: Confirmed via `/speckit.clarify`. No `version`/`ETag` column is
  added to the four tables in this story.
- **Alternatives considered**: Optimistic concurrency via a `version` int column —
  deferred; can be added later as a non-breaking column addition if needed.

## Decision: Timestamps — database-owned only
- **Rationale**: Constitution Principle II: `created_at`/`updated_at` are
  `DEFAULT now()` at the DB layer; any client-supplied value is ignored. Pydantic
  response models expose them as read-only fields (absent from request schemas).
- **Alternatives considered**: Application-set timestamps (`datetime.utcnow()` in
  service layer) — rejected; DB clock is the single source of truth and avoids
  clock-skew inconsistency across the API/DB boundary.
