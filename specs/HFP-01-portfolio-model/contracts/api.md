# API Contract: ZIQ-101 — Manage the spatial portfolio hierarchy

Base path: `/api`

## Common conventions
- All timestamps in responses are ISO-8601 UTC, database-generated; never accepted
  in request bodies.
- List endpoints return a paginated envelope:
  ```json
  { "items": [ ... ], "total": 0, "limit": 50, "offset": 0 }
  ```
  Query params: `limit` (default 50, max 200), `offset` (default 0).
- Error contract (fixed per constitution):
  - `404` — id does not exist.
  - `422` — invalid body (missing/blank required field, wrong type, negative
    area/occupancy, duplicate `code`, missing/unknown parent id).
  - `422` body shape: `{ "detail": [ { "field": "...", "message": "..." } ] }`

## Portfolio
| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | /portfolios | — | 200 paginated list | — |
| GET | /portfolios/{id} | — | 200 single | 404 |
| POST | /portfolios | `{name, code}` | 201 created | 422 |
| PUT | /portfolios/{id} | `{name, code}` | 200 updated | 404, 422 |
| DELETE | /portfolios/{id} | — | 204 | 404 |

## Building
| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | /buildings?portfolio_id= | — | 200 paginated list | — |
| GET | /buildings/{id} | — | 200 single | 404 |
| POST | /buildings | `{portfolio_id, name, code, address}` | 201 created | 422 (bad body or unknown portfolio_id) |
| PUT | /buildings/{id} | `{name, code, address}` | 200 updated | 404, 422 |
| DELETE | /buildings/{id} | — | 204 | 404 |

## Floor
| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | /floors?building_id= | — | 200 paginated list | — |
| GET | /floors/{id} | — | 200 single | 404 |
| POST | /floors | `{building_id, name, code}` | 201 created | 422 (bad body or unknown building_id) |
| PUT | /floors/{id} | `{name, code}` | 200 updated | 404, 422 |
| DELETE | /floors/{id} | — | 204 | 404 |

## Zone
| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | /zones?floor_id= | — | 200 paginated list | — |
| GET | /zones/{id} | — | 200 single | 404 |
| POST | /zones | `{floor_id, name, code, area, occupancy}` | 201 created | 422 (bad body, unknown floor_id, negative area/occupancy) |
| PUT | /zones/{id} | `{name, code, area, occupancy}` | 200 updated | 404, 422 |
| DELETE | /zones/{id} | — | 204 | 404 |

## Response body examples

Portfolio (response):
```json
{
  "id": "uuid",
  "name": "Acme West Campus",
  "code": "ACME-WEST",
  "created_at": "2026-09-03T10:00:00Z",
  "updated_at": "2026-09-03T10:00:00Z"
}
```

Zone (response):
```json
{
  "id": "uuid",
  "floor_id": "uuid",
  "name": "Conference Room A",
  "code": "Z-3F-01",
  "area": 42.5,
  "occupancy": 12,
  "created_at": "2026-09-03T10:00:00Z",
  "updated_at": "2026-09-03T10:00:00Z"
}
```
