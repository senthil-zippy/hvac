# Traceability: ZIQ-101

| Requirement | Covering Test(s) |
|---|---|
| FR-001 (create Portfolio) | test_portfolio_service.py::test_create_and_get_roundtrip; test_portfolio_hierarchy_crud.py::test_full_chain_create_and_get |
| FR-002 (create Building) | test_building_service.py::test_create_success; test_portfolio_hierarchy_crud.py::test_full_chain_create_and_get |
| FR-003 (create Floor) | test_floor_service.py::test_create_success; test_portfolio_hierarchy_crud.py::test_full_chain_create_and_get |
| FR-004 (create Zone) | test_zone_service.py::test_create_success; test_portfolio_hierarchy_crud.py::test_full_chain_create_and_get |
| FR-005 (view + paginated list) | test_portfolio_hierarchy_crud.py::test_paginated_list |
| FR-006 (update) | test_portfolio_hierarchy_update.py::test_update_building_address, test_update_zone_area_and_occupancy |
| FR-007 (remove) | test_portfolio_hierarchy_delete.py::test_delete_zone_then_404, test_delete_empty_portfolio |
| FR-008 (single-parent integrity) | database/schema.sql FK NOT NULL constraints; test_building_service.py::test_create_rejects_unknown_portfolio_id |
| FR-009 (404 on missing) | test_portfolio_hierarchy_crud.py::test_get_missing_returns_404; test_portfolio_hierarchy_delete.py::test_delete_zone_then_404 |
| FR-010 (422 on invalid body) | test_portfolio_hierarchy_crud.py::test_create_with_missing_required_field_returns_422; unit test_*_service.py validation tests |
| FR-011 (DB-owned timestamps) | database/schema.sql DEFAULT now(); test_portfolio_hierarchy_update.py (updated_at behavior) |
| FR-012 (Building address required) | test_building_service.py::test_create_rejects_blank_address |
| FR-013 (Zone non-negative area/occupancy) | test_zone_service.py::test_create_rejects_negative_area, test_create_rejects_negative_occupancy |
| FR-014 (UI workflow) | Out of scope for this backend-only increment (frontend deferred; see spec.md Assumptions) |
| FR-015 (global code uniqueness) | test_portfolio_service.py::test_create_rejects_duplicate_code; test_building_service.py/test_floor_service.py/test_zone_service.py::test_create_rejects_duplicate_code |
| FR-016 (last-write-wins) | test_portfolio_hierarchy_update.py::test_update_building_address, test_update_zone_area_and_occupancy (no version check enforced) |
