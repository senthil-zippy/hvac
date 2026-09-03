# Quickstart: ZIQ-101 — Manage the spatial portfolio hierarchy

## Prerequisites
- PostgreSQL reachable per `.env` (`DATABASE_URL`); verified reachable at
  `localhost:5432` in this environment.
- Python 3.12 environment with backend dependencies installed
  (`backend-python/requirements.txt`, added during implementation).

## Setup
```powershell
# Apply schema (once implemented)
psql -h localhost -p 5432 -U postgres -d zoneiq -f database/schema.sql

# Run the API
cd backend-python
uvicorn main:app --reload --port 8000
```

## Validation scenarios (map to spec.md Acceptance Scenarios)

1. **Create full chain (User Story 1)**
   ```powershell
   # Create portfolio
   curl -X POST http://localhost:8000/api/portfolios -H "Content-Type: application/json" -d '{"name":"Acme West","code":"ACME-WEST"}'
   # Create building under it (use returned portfolio id)
   curl -X POST http://localhost:8000/api/buildings -H "Content-Type: application/json" -d '{"portfolio_id":"<id>","name":"Tower 1","code":"T1","address":"1 Main St"}'
   # Create floor, then zone similarly
   ```
   Expected: each POST returns `201` with a database-generated `id` and timestamps;
   each GET by id returns the same record; listing returns it in the paginated
   `items` array.

2. **Update a record (User Story 2)**
   ```powershell
   curl -X PUT http://localhost:8000/api/buildings/<id> -H "Content-Type: application/json" -d '{"name":"Tower 1","code":"T1","address":"2 Main St"}'
   ```
   Expected: `200`, `address` reflects new value, `updated_at` > `created_at`.

3. **Reject invalid update**
   ```powershell
   curl -X PUT http://localhost:8000/api/zones/<id> -H "Content-Type: application/json" -d '{"name":"Room A","code":"Z1","area":10,"occupancy":-1}'
   ```
   Expected: `422` with field-level detail on `occupancy`; stored record unchanged.

4. **Remove a leaf record (User Story 3)**
   ```powershell
   curl -X DELETE http://localhost:8000/api/zones/<id>
   curl http://localhost:8000/api/zones/<id>
   ```
   Expected: `DELETE` returns `204`; subsequent `GET` returns `404`.

5. **Not-found and validation contract**
   - `GET /api/zones/00000000-0000-0000-0000-000000000000` → `404`.
   - `POST /api/buildings` with missing `address` → `422` identifying `address`.
   - `POST /api/floors` with unknown `building_id` → `422`.

## Automated tests
```powershell
cd backend-python
pytest tests/unit          # service-layer validation
pytest tests/integration   # full CRUD round-trip against test DB
```
