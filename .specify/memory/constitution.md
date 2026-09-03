<!--
Sync Impact Report
Version change: [TEMPLATE] → 1.0.0
Modified principles: N/A (initial ratification)
Added sections:
  - Core Principles: I. Layered Architecture, No Skipping; II. Schema Owned Once;
    III. Spec-First, Test-First (NON-NEGOTIABLE); IV. Contract-Driven Interfaces &
    Cross-Backend Parity; V. Determinism, Audit & Governed Autonomy
  - Additional Constraints (technology stack, env/secrets discipline, measurement)
  - Development Workflow (spec chain, PR quality gates, brownfield discipline)
  - Governance
Removed sections: none (initial document)
Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending manual review (verify layering/testing gates referenced)
  - .specify/templates/spec-template.md ⚠ pending manual review
  - .specify/templates/tasks-template.md ⚠ pending manual review
Follow-up TODOs: none
-->

# ZoneIQ Constitution

## Core Principles

### I. Layered Architecture, No Skipping
Every backend change MUST respect Controller/Router → Service → Repository, and every
frontend change MUST respect `components/` → `pages/` → `services/`. Business rules
and validation MUST NOT appear in controllers; HTTP and SQL MUST NOT appear in
services; the repository layer is the only place SQL lives. The device
adapter/ingestion layer translates register values into validated telemetry and
approved commands into register writes — it MUST NOT mutate domain state directly.
The optimization policy and alarm engine MUST remain transport-ignorant, operating
only on domain objects.
Rationale: the platform's safety and testability depend on each layer being
independently verifiable; collapsing layers hides defects and blocks unit-level
proof of the optimization and alarm logic required by Section 11 of the capstone
requirements.

### II. Schema Owned Once
The database schema is authored once in `database/schema.sql`. Schema changes are
delivered as new, numbered files under `database/migrations/` — never ORM
auto-migrations, `create_all()`, or `ddl-auto` other than `none`. `created_at` /
`updated_at` (and `received_at`) are database-set and MUST NOT be accepted from a
client; a reading's `source timestamp` is the sole client-supplied exception, by
design.
Rationale: a single source of truth for schema evolution keeps the three backend
implementations (and their tests) aligned and makes every change auditable.

### III. Spec-First, Test-First (NON-NEGOTIABLE)
Every functional requirement MUST have its own `spec.md → plan.md → tasks.md` chain,
written and reviewed before implementation begins. Every new endpoint MUST have a
test in its own layer before it is considered done. A specification-to-test
traceability matrix MUST map every requirement ID to at least one test. A
brownfield change MUST leave the pre-existing test suite green and unmodified, with
an archaeology note and change-impact analysis.
Rationale: spec-driven development at system scale is only trustworthy if the spec
precedes the code and the test suite proves the spec, not the other way around.

### IV. Contract-Driven Interfaces & Cross-Backend Parity
External and inter-layer contracts (telemetry ingestion API, device register-map
mapping, command dispatch, error contract) MUST be documented before implementation
and versioned when changed, reflected in the traceability matrix. The error contract
is fixed: `404` for a missing id, `422` for an invalid request body or an
out-of-envelope value that cannot be clamped — no other invented status codes on
CRUD. The .NET, Python, and Java backends MUST expose every feature identically and
return byte-identical JSON for the same request (timestamp key casing aside). A
contract test MUST fail if the device adapter's mapping drifts from the documented
register map.
Rationale: this platform is a shared contract surface (device adapter, ingestion
API, multi-backend parity); undocumented or backend-specific drift breaks the
capstone's traceability and interoperability requirements.

### V. Determinism, Audit & Governed Autonomy
Simulated device feeds and the simulated Modbus/BACnet master MUST be fully
deterministic — no wall-clock or real-network dependence in test runs. Every
Command transition, Alarm transition, shelve/unshelve, and
ComfortProfile/SetpointSchedule/OptimizationPolicy change MUST produce an immutable
AuditEvent; audit events are never edited or deleted through the API. Safety-relevant
actions (command approval, envelope override, profile/schedule edits, extended
shelving) are gated by role, with extended shelving and envelope override
additionally requiring Supervisor approval; every denied action is audited. Assistant
agents (IAQ-triage, complaint-triage) MUST stay grounded in real platform data, cite
the point/alarm/document used, operate within documented tool permissions, and MUST
NOT acknowledge, shelve, approve, or dispatch anything themselves — every state
change is handed to a human.
Rationale: a supervisory HVAC platform is safety-relevant; determinism makes defects
reproducible, and audit plus governed autonomy make every consequential change
traceable to an authorized human decision.

## Additional Constraints

- **Technology stack**: PostgreSQL (containerized) for persistence; one backend of
  .NET, Python, or Java behind the shared REST contract; React frontend. No EF
  migrations or equivalent auto-schema tooling.
- **Secrets discipline**: no direct reading of `.env` or secrets in application code;
  use the framework's config system. `.env` is git-ignored; `.env.example` is copied
  as a deliberate step.
- **Measurement**: each module's delivery is measured against implementation cycle
  time, quality/regression risk, PR review time, testing effort, token usage, and AI
  cost.

## Development Workflow

- A functional requirement (Section 7 of
  `capstone/HVAC_Fleet_Platform_Requirements.md`) is decomposed into its own
  `spec.md → plan.md → tasks.md` chain under `specs/` before implementation starts.
- PRs undergo spec-compliance, standards, security, test-evidence, and
  regression-risk checks; a safety-relevant change additionally requires an
  LLM-as-Judge review with captured evidence and a human-escalation decision.
- A brownfield change requires an archaeology note, change-impact analysis, and a
  regression report proving the pre-existing suite is green and unmodified.
- At least one MCP-connected workflow and one packaged reusable skill used to build
  or operate the platform must be documented with its permission and context
  boundary.

## Governance

This constitution supersedes conflicting team practices for the ZoneIQ capstone.
Amendments require: a documented rationale, review against the capstone requirements
in `capstone/HVAC_Fleet_Platform_Requirements.md`, and an explicit version bump
following semantic versioning — MAJOR for backward-incompatible governance or
principle removal/redefinition, MINOR for a new or materially expanded principle or
section, PATCH for clarification or wording fixes. Every PR and review MUST verify
compliance with these principles; unavoidable complexity or a deviation MUST be
justified in the PR description. Use `capstone/HVAC_Fleet_Platform_Requirements.md`
for detailed runtime and requirement guidance beyond this document's scope.

**Version**: 1.0.0 | **Ratified**: 2026-09-03 | **Last Amended**: 2026-09-03
