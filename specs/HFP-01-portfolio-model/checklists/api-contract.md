# API & Data Contract Checklist: Manage the spatial portfolio hierarchy

**Purpose**: Validate requirements quality (completeness, clarity, consistency) for the ZIQ-101 CRUD/API contract before implementation
**Created**: 2026-09-03
**Feature**: [spec.md](../spec.md)
**Focus**: API contract, validation rules, pagination, concurrency (informed by the 2026-09-03 `/speckit.clarify` session)
**Depth**: Standard — reviewer-owned, pre-implementation gate
**Audience**: Author / reviewer before `/speckit.implement`

## Requirement Completeness

- [ ] CHK001 Are the required fields for each of the four entities (Portfolio, Building, Floor, Zone) fully enumerated, including which are read-only (`id`, `created_at`, `updated_at`)? [Spec §Key Entities, §FR-001-004]
- [ ] CHK002 Is the response envelope shape for paginated list endpoints (`items`/`total`/`limit`/`offset`) specified anywhere in the requirements, not just in a downstream contract artifact? [Gap, Spec §FR-005]
- [ ] CHK003 Are default and maximum values for pagination `limit` specified in the requirements (not only in `.env`/config)? [Gap]
- [ ] CHK004 Is the behavior when `limit`/`offset` are omitted, negative, or non-numeric defined? [Gap, Edge Case]
- [ ] CHK005 Are the requirements for re-parenting a Zone to a different Floor (crossing Building boundaries) fully specified, including whether it is allowed at all? [Spec §Edge Cases]

## Requirement Clarity

- [ ] CHK006 Is "non-empty" for `name`/`code` fields defined precisely (e.g., does whitespace-only count as empty)? [Ambiguity, Spec §FR-010, §FR-013]
- [ ] CHK007 Is the global uniqueness scope for `code` (FR-015) unambiguous about case-sensitivity (is `"Z1"` distinct from `"z1"`)? [Ambiguity, Spec §FR-015]
- [ ] CHK008 Is "last-write-wins" (FR-016) precise about what happens to the `updated_at` timestamp when two near-simultaneous updates race (which write's timestamp survives)? [Ambiguity, Spec §FR-016]
- [ ] CHK009 Is the distinction between a `404` (missing resource) and `422` (invalid/missing parent reference in a request body) unambiguous for every entity's create/update path? [Clarity, Spec §FR-009, §FR-010]

## Requirement Consistency

- [ ] CHK010 Do the acceptance scenarios in User Story 1-3 use consistent terminology for "area" and "occupancy" units/semantics as used in FR-013 and data-model.md? [Consistency]
- [ ] CHK011 Is the `422` field-level error format consistent across all four entities and all four operations (create/update), not just described once and assumed elsewhere? [Consistency, Spec §FR-010]

## Acceptance Criteria Quality

- [ ] CHK012 Is SC-005 ("0% of Zones or Floors can exist without a valid parent") measurable via an automatable check (e.g., a query or test), or only asserted narratively? [Measurability, Spec §SC-005]
- [ ] CHK013 Are the Independent Test criteria for User Story 2 and User Story 3 sufficient to prove the feature increment without depending on unstated setup steps? [Spec §User Story 2, §User Story 3]

## Scenario Coverage

- [ ] CHK014 Are concurrent-create scenarios for duplicate `code` values (two simultaneous POSTs with the same code) addressed, given last-write-wins applies to updates but uniqueness applies to creates? [Coverage, Gap]
- [ ] CHK015 Is the behavior specified when a delete request targets a Building/Floor/Portfolio that still has children, given ZIQ-102 (not ZIQ-101) owns the refusal logic — is the ZIQ-101 boundary explicit enough to avoid an implementer guessing? [Coverage, Spec §Assumptions]

## Dependencies & Assumptions

- [ ] CHK016 Is the assumption that "UI workflows" reuse the existing admin surface validated against an actual existing surface, or is this assumption unverified? [Assumption, Spec §Assumptions]
- [ ] CHK017 Is the dependency on the platform's existing auth/authorization model (to determine "who may act as a Facilities Manager") documented with enough detail to know if it already exists or is itself a gap? [Dependency, Spec §Assumptions]

## Notes

- Items above are unresolved as of generation; reviewer should check them off after confirming the corresponding requirement is adequately specified (editing spec.md if a gap is found), not after checking the implementation.
- This checklist does not duplicate `checklists/requirements.md` (already complete); it targets the API/data-contract dimension specifically, informed by the pagination/uniqueness/concurrency clarifications.
