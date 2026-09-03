<!--
Sync Impact Report
Version change: 1.0.0 → 2.0.0
Modified principles: full replacement — prior ZoneIQ HVAC-platform principles
  (Layered Architecture No Skipping; Schema Owned Once; Spec-First Test-First;
  Contract-Driven Interfaces & Cross-Backend Parity; Determinism, Audit & Governed
  Autonomy) superseded by Engineering Task Board principles below.
Added sections:
  - Core Principles: I. Layered Architecture (Non-Negotiable); II. Single Schema
    Owner; III. Error Contract; IV. Cross-Backend Parity; V. Tests-First-Class;
    VI. Spec Is the Source of Truth; VII. Scoped Context
Removed sections: prior Additional Constraints and Development Workflow sections
  (HVAC/capstone-specific) removed as out of scope for the Task Board project.
Deferred items:
  - TODO(SOURCE_DOCS): principles were requested to derive from
    `.github/copilot-instructions.md` and `CONTEXT.md`, but neither file exists in
    this repository. Principles below are captured as directly specified; revisit
    once those files are authored.
Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending manual review
  - .specify/templates/spec-template.md ⚠ pending manual review
  - .specify/templates/tasks-template.md ⚠ pending manual review
Follow-up TODOs: TODO(SOURCE_DOCS) above.
-->

# Engineering Task Board Constitution

## Core Principles

### I. Layered Architecture (NON-NEGOTIABLE)
Every backend change MUST respect Controller/Router → Service → Repository. All
database access and all data aggregation live in the repository layer; controllers
MUST NOT contain business logic or SQL; services MUST NOT contain HTTP or raw SQL.
Rationale: enforcing the boundary keeps each layer independently testable and
prevents logic and data-access concerns from leaking into the wrong tier.

### II. Single Schema Owner
`database/schema.sql` is the only place the schema is defined. Schema changes are
reviewed edits to that file, not migrations. No migration tooling (ORM
auto-migration, `create_all()`, `ddl-auto`, or equivalent) is used.
Rationale: one authoritative, human-reviewed schema file avoids drift between
migration history and the live schema and keeps every schema change visible in
review.

### III. Error Contract
CRUD endpoints return `404` for a missing resource and `422` for a bad request body.
No other status codes are invented for CRUD operations.
Rationale: a fixed, minimal error contract keeps client handling predictable across
every endpoint and backend.

### IV. Cross-Backend Parity
The .NET, Python, and Java backends expose every feature identically and return
byte-identical JSON for the same request, timestamp key casing aside.
Rationale: parity across backends is the guarantee that lets any backend be swapped
in without client-visible behavior change.

### V. Tests-First-Class
No task is done until it has tests in the same layer as the change, and those tests
pass.
Rationale: tests are part of the definition of done, not an afterthought; layer-local
tests catch regressions closest to where they are introduced.

### VI. Spec Is the Source of Truth
Code changes for a requirement change start with a spec change. Ad hoc requirement
changes made only in chat or the editor, without an updated spec, are not permitted.
Rationale: the spec must remain the record of intent; skipping it breaks
traceability between requirements and implementation.

### VII. Scoped Context
Implementation work uses a compressed, task-scoped context brief (see
`.github/prompts/context-brief.prompt.md`), not whole-repo dumps.
Rationale: scoped context keeps AI-assisted implementation focused and token-
efficient, and avoids irrelevant or stale context influencing a change.

## Governance

This constitution supersedes conflicting team practices for the Engineering Task
Board project. Amendments require a documented rationale and an explicit version
bump following semantic versioning — MAJOR for backward-incompatible governance or
principle removal/redefinition, MINOR for a new or materially expanded principle,
PATCH for clarification or wording fixes. Every PR and review MUST verify compliance
with these principles; unavoidable complexity or a deviation MUST be justified in
the PR description.

**Version**: 2.0.0 | **Ratified**: 2026-09-03 | **Last Amended**: 2026-09-03
