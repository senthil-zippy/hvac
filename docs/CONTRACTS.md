# ZoneIQ API Contracts

## ZIQ-101: Portfolio Hierarchy (Portfolio/Building/Floor/Zone)

See [specs/HFP-01-portfolio-model/contracts/api.md](../specs/HFP-01-portfolio-model/contracts/api.md)
for the full request/response contract. Implemented in `backend-python/routers/`.

Summary:
- `GET/POST /api/portfolios`, `GET/PUT/DELETE /api/portfolios/{id}`
- `GET/POST /api/buildings`, `GET/PUT/DELETE /api/buildings/{id}` (filter by `portfolio_id`)
- `GET/POST /api/floors`, `GET/PUT/DELETE /api/floors/{id}` (filter by `building_id`)
- `GET/POST /api/zones`, `GET/PUT/DELETE /api/zones/{id}` (filter by `floor_id`)
- List endpoints paginated: `{items, total, limit, offset}`.
- Error contract: `404` missing resource, `422` invalid body (field-level detail).
