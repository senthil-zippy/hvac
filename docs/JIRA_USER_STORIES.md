# ZoneIQ Jira User Story Backlog

## Conventions

- **Jira Epic:** each `HFP-nn` section is an Epic; its child `ZIQ-nnn` entries are Stories.
- **Priority:** P0 is needed for the first operational release; P1 follows the core flow.
- Each story should become its own `spec.md`, `plan.md`, and `tasks.md` before implementation.
- Acceptance criteria use observable outcomes and are intended to seed test cases and the traceability matrix.

## Jira Epic: HFP-01 - Portfolio and Asset Model

### ZIQ-101 - Manage the spatial portfolio hierarchy
**Priority:** P0  
**User story:** As a Facilities Manager, I want to create, view, update, and remove portfolios, buildings, floors, and zones so that the platform reflects the spaces we operate.

**Acceptance criteria**
- CRUD endpoints and UI workflows exist for each hierarchy level.
- A building records its address; a zone records area and occupancy.
- A zone can belong to only one floor and a floor to only one building.
- Missing resources return `404`; invalid bodies return `422`.
- Creation and updates record database-owned timestamps.

### ZIQ-102 - Protect hierarchy integrity
**Priority:** P0  
**User story:** As a Facilities Manager, I want unsafe hierarchy deletions refused so that no operated assets are orphaned.

**Acceptance criteria**
- Deleting a building with floors or zones is refused.
- Deleting a floor with zones is refused.
- A clear validation response identifies the blocking relationship.
- Deletion succeeds only after child assets have been removed or moved.

### ZIQ-103 - Manage zone controllers
**Priority:** P0  
**User story:** As a Controls Engineer, I want to register and maintain a zone controller against a zone so that telemetry and commands have an unambiguous target.

**Acceptance criteria**
- A device stores serial, model, protocol, firmware version, commissioning state, zone, and last-seen.
- Device serial is unique and a device belongs to exactly one zone.
- Base-build validation permits no more than one device per zone.
- Device CRUD enforces valid protocols and commissioning states.

### ZIQ-104 - Find fleet assets by operational attributes
**Priority:** P0  
**User story:** As a Field Technician, I want to filter zones and devices by location, protocol, commissioning state, and health so that I can quickly identify the assets needing attention.

**Acceptance criteria**
- Zone and device lists support filters for building, floor, protocol, commissioning state, and health where applicable.
- Multiple supplied filters are combined predictably.
- Results include the location and current device health needed to act on the list.

## Jira Epic: HFP-02 - Point Catalogue

### ZIQ-201 - Maintain device points from a controlled vocabulary
**Priority:** P0  
**User story:** As a Controls Engineer, I want to manage each device's telemetry and command points using approved keys so that all fleet data has consistent meaning.

**Acceptance criteria**
- A point records device, key, unit, data type, scaling, direction, register type, and register address.
- Point CRUD is available only under an existing device.
- A key outside the controlled vocabulary is rejected with `422`.
- A `(device, point key)` combination is unique.

### ZIQ-202 - Enforce the declared device profile
**Priority:** P0  
**User story:** As a Controls Engineer, I want the point catalogue validated against its declared register-map profile so that adapter behavior cannot drift from the controller contract.

**Acceptance criteria**
- A device declares a named, versioned device profile.
- The `hvac-zone-controller-v1` profile captures every point in the documented register map.
- Validation rejects missing required points and contradictory direction, type, register mapping, or scaling.
- A contract test fails when the profile and documented mapping diverge.

## Jira Epic: HFP-03 - Telemetry Ingestion

### ZIQ-301 - Receive bulk device telemetry
**Priority:** P0  
**User story:** As a simulated device feed, I want to submit a batch of timestamped point readings for a device so that the platform has a current operational snapshot.

**Acceptance criteria**
- `POST /api/ingest/readings` accepts device serial plus one or more `{pointKey, value, quality, timestamp}` readings.
- A valid batch returns `202 Accepted` and a per-reading result list.
- Empty or malformed batches and unknown quality values return `422`.
- An unknown device serial returns `404`.
- The deterministic simulator can exercise the endpoint without wall-clock or network dependencies.

### ZIQ-302 - Validate and retain incoming readings
**Priority:** P0  
**User story:** As a platform operator, I want readings checked and retained within a bounded history so that downstream decisions use trustworthy, recent data.

**Acceptance criteria**
- Unknown points and readings outside the configured staleness window are individually rejected with reasons.
- Accepted readings persist point, value, quality, source timestamp, and database-set received timestamp.
- Any accepted reading updates the device last-seen value.
- Retention purges readings older than the configured per-point window.
- Non-good readings are stored but excluded from alarm evaluation and optimization inputs.

### ZIQ-303 - Detect missing telemetry
**Priority:** P0  
**User story:** As a Facilities Manager, I want the platform to flag a controller that stops reporting so that communications failures are visible without a site visit.

**Acceptance criteria**
- A deterministic scheduled check evaluates device last-seen against the configured absence threshold.
- A device past the threshold raises the defined comms alarm through the alarm service.
- Fresh telemetry clears the comms condition according to alarm clear rules.

## Jira Epic: HFP-04 - Comfort and Air-Quality Evaluation

### ZIQ-401 - Evaluate a fresh zone snapshot against its comfort profile
**Priority:** P0  
**User story:** As a Facilities Manager, I want each fresh, good zone snapshot evaluated against its comfort profile so that I know whether occupants are comfortable and healthy.

**Acceptance criteria**
- Evaluation uses temperature, RH, CO2, and PM2.5 readings together with the effective zone profile.
- The result identifies temperature and RH in/out-of-band status.
- The result exposes a distinct `air_quality_status` based on CO2 and PM2.5 even when thermal comfort is acceptable.
- Only fresh good readings can initiate evaluation.

### ZIQ-402 - Stabilize comfort and IAQ status transitions
**Priority:** P0  
**User story:** As a Facilities Manager, I want status changes to apply hysteresis so that threshold noise does not make the dashboard and alarms flap.

**Acceptance criteria**
- Threshold, deadband, and on/off-delay values are documented and configurable through the domain policy/profile design.
- A value hovering around a threshold does not repeatedly alternate status.
- Unit tests prove enter-band and return-to-band behavior at boundaries.

## Jira Epic: HFP-05 - Supervisory Optimization Policy

### ZIQ-501 - Calculate a base supervisory zone target
**Priority:** P0  
**User story:** As a Controls Engineer, I want a deterministic optimization policy to calculate zone temperature setpoint, ventilation minimum, and mode so that controllers receive consistent supervisory intent.

**Acceptance criteria**
- The policy accepts a zone snapshot, comfort profile, active schedule, and optimization policy.
- It returns `{temp setpoint, ventilation minimum, mode}` without HTTP, database, or device transport dependencies.
- The base policy is covered by isolated unit tests.
- Adaptive behavior, if later added, is separately toggled and cannot alter base-policy tests.

### ZIQ-502 - Apply demand-controlled ventilation for IAQ excursions
**Priority:** P0  
**User story:** As a Facilities Manager, I want ventilation increased when air quality is poor even if temperature is comfortable so that health is protected at an explicit energy cost.

**Acceptance criteria**
- When CO2 or PM2.5 is out of band while temperature is in band, the target ventilation minimum increases according to configured DCV policy.
- The target respects configured limits.
- Tests prove the IAQ-only scenario increases ventilation without a temperature excursion.
- Policy documentation records the comfort/air-quality versus conditioning-energy tradeoff.

### ZIQ-503 - Prepare zones for scheduled occupancy
**Priority:** P1  
**User story:** As an Energy Analyst, I want the policy to pre-cool or pre-heat before occupancy begins so that spaces reach the target envelope when needed.

**Acceptance criteria**
- The policy identifies the next occupancy block from the active schedule.
- Within configured lead time, it shifts the target appropriately for pre-cool or pre-heat.
- Outside lead time, normal occupied/unoccupied logic applies.
- Boundary tests cover lead-time start and schedule transitions.

## Jira Epic: HFP-06 - Fleet Alarm and Event Management

### ZIQ-601 - Raise and clear deduplicated fleet alarms
**Priority:** P0  
**User story:** As a Facilities Manager, I want sustained comfort, IAQ, device-health, and comms conditions to become lifecycle-managed alarms so that actionable issues are not lost in raw telemetry.

**Acceptance criteria**
- The alarm service supports comfort, air-quality, device-health, and comms categories with defined priority rules.
- Excursions raise only after the configured on-delay and clear only after the off-delay and deadband conditions hold.
- No duplicate active alarm exists for the same zone/device and rule.
- Alarm records include source, current value, priority, state, and lifecycle timestamps.

### ZIQ-602 - Find and acknowledge active alarms
**Priority:** P0  
**User story:** As a Field Technician, I want to locate active alarms and acknowledge one or many so that the team can demonstrate ownership of active incidents.

**Acceptance criteria**
- Active alarms can be filtered by building, zone, category, priority, and state.
- Results can sort by raised-at or priority.
- Single and batch acknowledge actions record actor and acknowledgement time.
- Invalid state transitions are rejected and missing alarms return `404`.

### ZIQ-603 - Shelve alarms with governed expiry
**Priority:** P0  
**User story:** As a Field Technician, I want to temporarily shelve a known alarm with a reason and expiry so that planned work does not obscure new actionable alarms.

**Acceptance criteria**
- Shelving requires a non-empty reason and expiry.
- Shelving within the maximum duration is available to the authorized role.
- Longer shelving requires Facilities Manager approval.
- Expiry auto-unshelves an alarm; authorized manual unshelving is supported.
- All shelving and unshelving transitions are audited.

### ZIQ-604 - Report alarm operational analytics
**Priority:** P1  
**User story:** As a Facilities Manager, I want fleet alarm analytics so that I can identify recurring failures and measure response performance.

**Acceptance criteria**
- Reports provide alarm rate per 10-minute window for a building and the fleet.
- Reports identify top zones and points by alarm count, standing alarms, and currently shelved alarms.
- MTTA calculation and its data assumptions are documented and exposed.

## Jira Epic: HFP-07 - Command Dispatch

### ZIQ-701 - Draft validated supervisory commands
**Priority:** P0  
**User story:** As a Controls Engineer, I want to create draft setpoint, mode-override, return-to-auto, and schedule-push commands so that proposed field changes can be reviewed before reaching a controller.

**Acceptance criteria**
- `POST /api/zones/{id}/commands` creates a draft for a valid command type and target zone/device.
- Payloads are evaluated against a documented safe envelope.
- Unsafe values are rejected with `422` or clamped according to the selected documented policy.
- A clamp is retained on the command and captured in its audit event.

### ZIQ-702 - Approve commands under role control
**Priority:** P0  
**User story:** As an authorized approver, I want to approve a draft command so that dispatch happens only after human governance.

**Acceptance criteria**
- Only the owning authorized role can approve a draft command.
- Approval records approver and timestamp and transitions the command to `approved`.
- Denied approvals are audited.
- A command outside the approved state cannot be dispatched.

### ZIQ-703 - Dispatch and confirm approved commands through the adapter
**Priority:** P0  
**User story:** As a Controls Engineer, I want an approved command encoded, sent, and confirmed against device state so that platform intent is safely applied in the field.

**Acceptance criteria**
- The adapter converts only approved commands into documented register writes.
- Successful device echo transitions the command through `dispatched` to `confirmed`.
- A failed write or echo transitions the command to `failed` and raises a device-health alarm.
- A failed dispatch preserves the zone's last-known-good target.
- Adapter contract tests round-trip every `hvac-zone-controller-v1` point against the simulated master.

## Jira Epic: HFP-08 - Setpoint Schedules and Comfort Profiles

### ZIQ-801 - Maintain effective comfort profiles
**Priority:** P0  
**User story:** As a Controls Engineer, I want to maintain a zone comfort profile or inherit a building default so that evaluation and optimization share an approved target envelope.

**Acceptance criteria**
- A profile defines temperature band, RH band, CO2 threshold, PM2.5 threshold, and occupied hours.
- A zone-specific profile overrides a building default; otherwise the default is effective.
- Profile values are validated against documented safe bounds.
- Profile changes are audited and become effective on the next optimization cycle only.

### ZIQ-802 - Maintain non-contradictory setpoint schedules
**Priority:** P0  
**User story:** As a Controls Engineer, I want to manage day-type schedule blocks per zone so that targets are applied at the intended times.

**Acceptance criteria**
- A schedule block includes day type, time range, temperature setpoint, and ventilation minimum.
- Setpoint and ventilation values obey the safe envelope and non-negative constraint.
- Overlapping or contradictory blocks are rejected with `422`.
- Changes are audited and affect only subsequent optimization cycles.

## Jira Epic: HFP-09 - Occupant Complaint Intake

### ZIQ-901 - Record a comfort complaint with operational context
**Priority:** P0  
**User story:** As a Tenant-Experience user, I want to record an occupant complaint against a zone and view its current evidence so that triage starts with facts rather than recollection.

**Acceptance criteria**
- A complaint records zone, reporter, text, received time, and status.
- Complaint detail displays recent comfort and IAQ status plus active zone alarms.
- A missing zone or invalid complaint body receives the standard error response.

### ZIQ-902 - Convert a complaint into a work order
**Priority:** P0  
**User story:** As a Tenant-Experience user, I want to turn a complaint into a pre-filled work order so that maintenance can act without re-entering known context.

**Acceptance criteria**
- Conversion creates a work order linked to the complaint and its zone.
- The work order description contains a current status summary.
- The complaint status and linkage are updated consistently.

## Jira Epic: HFP-10 - Work Order Management

### ZIQ-1001 - Create and progress maintenance work orders
**Priority:** P0  
**User story:** As a Facilities Manager, I want to create work orders from alarms, complaints, devices, or direct requests and track them to closure so that operational issues reach maintenance.

**Acceptance criteria**
- A work order can link a zone and, when applicable, alarm, complaint, and device.
- It captures title, description, priority, assigned team, status, and raised-by.
- Valid status progression is `open` to `in-progress` to `done` or `cancelled`.
- Closing records the user and timestamp.

### ZIQ-1002 - Find work assigned to a maintenance team
**Priority:** P0  
**User story:** As a maintenance coordinator, I want to filter work orders by location, team, status, and priority so that the team can organize its active workload.

**Acceptance criteria**
- Work-order listing filters by building, zone, assigned team, status, and priority.
- Results retain linked source context for alarms and complaints.

## Jira Epic: HFP-11 - Portfolio Dashboards and KPIs

### ZIQ-1101 - View the portfolio operational overview
**Priority:** P0  
**User story:** As a Facilities Manager, I want a portfolio overview of building health so that I can prioritize facilities action across the fleet.

**Acceptance criteria**
- Each building shows zone count, comfort-compliance percentage, open alarms by priority, and offline-device count.
- Metrics have defined time windows and exclude non-good readings where appropriate.
- The UI retrieves data through frontend services, not direct HTTP calls from components.

### ZIQ-1102 - Inspect a live zone operational view
**Priority:** P0  
**User story:** As a Field Technician, I want a zone view with live conditions, trend, target, alarms, and commands so that I can diagnose a local problem efficiently.

**Acceptance criteria**
- The view shows current temperature, RH, CO2, and PM2.5 with a short trend.
- It compares current actual values with the current target.
- Active alarms and recent commands are visible in the same zone context.

### ZIQ-1103 - Report comfort, IAQ, energy, and service KPIs
**Priority:** P1  
**User story:** As an Energy Analyst, I want period-based operational KPIs so that I can quantify building performance and tradeoffs.

**Acceptance criteria**
- Reports include comfort-compliance percentage, CO2 and PM2.5 exceedance hours, ventilation effectiveness, energy-versus-comfort indicator, MTTA, and complaint resolution time.
- Each KPI defines its calculation period, denominator, and treatment of missing/bad data.
- KPI results can be scoped to the portfolio and relevant building or zone context.

## Jira Epic: HFP-12 - Audit, Access Control, and Traceability

### ZIQ-1201 - Enforce role-based access to operational actions
**Priority:** P0  
**User story:** As a platform administrator, I want roles to gate platform actions so that risky controls changes are made only by accountable users.

**Acceptance criteria**
- The system supports Facilities Manager, Controls Engineer, Field Technician, Energy Analyst, Tenant-Experience, and Viewer roles.
- Viewer has read-only access.
- Command approval, profile/schedule editing, envelope override, and extended shelving are restricted to their owning roles.
- Extended shelving and envelope override additionally require Facilities Manager approval.
- Every denied action generates an audit event.

### ZIQ-1202 - Preserve an immutable safety audit trail
**Priority:** P0  
**User story:** As a compliance reviewer, I want every safety-relevant transition recorded immutably so that platform decisions are accountable and reconstructable.

**Acceptance criteria**
- Command and alarm transitions, shelving actions, and profile, schedule, and policy changes append actor, action, entity, before/after snapshot, and timestamp.
- Audit events cannot be edited or deleted through the API.
- Audit event timestamps are database-set.

### ZIQ-1203 - Query audit evidence by operational context
**Priority:** P1  
**User story:** As a compliance reviewer, I want to query the audit trail by asset, event, actor, action, and time so that I can investigate a decision efficiently.

**Acceptance criteria**
- Audit search filters by zone, device, alarm, command, user, action type, and time range.
- Filter combinations yield deterministic, paginated results with stable ordering.

## Jira Epic: HFP-13 - Assistant Agents

### ZIQ-1301 - Produce grounded IAQ-triage drafts
**Priority:** P1  
**User story:** As a Facilities Manager, I want an IAQ-triage assistant to investigate an air-quality alarm and draft the next action so that human responders start from correlated evidence.

**Acceptance criteria**
- The agent reads the relevant point trend, comfort profile, recent commands, and approved weather MCP data.
- It returns likely cause, urgency, and a draft work order or ventilation-override command.
- The response cites the platform records and documents used.
- The agent has read-only platform permissions and cannot acknowledge, shelve, approve, dispatch, or otherwise mutate state.
- Tool failures produce a transparent incomplete-analysis response and no state change.

### ZIQ-1302 - Produce grounded complaint-triage drafts
**Priority:** P1  
**User story:** As a Tenant-Experience user, I want a complaint-triage assistant to correlate a complaint with operating history and draft a work order so that the handoff to maintenance is better informed.

**Acceptance criteria**
- The agent reads the complaint, associated zone history, comfort/IAQ status, and open alarms.
- It returns a grounded triage summary and draft work order for human review.
- It cites the source records used and never makes a state change itself.
- Missing, inaccessible, or conflicting evidence is explicitly identified.

### ZIQ-1303 - Govern and observe assistant operation
**Priority:** P1  
**User story:** As an engineering lead, I want assistant permissions, context boundaries, failures, and costs documented and observable so that agentic workflows remain safe and measurable.

**Acceptance criteria**
- Each agent has an explicit tool allow-list and context boundary.
- Every proposed state change stops at a human approval step.
- Failure-handling behavior is documented and tested for unavailable tools and incomplete platform data.
- Agent traces and token/cost metrics are available through Agent Prism and relate to an IAQ or comfort KPI.

## Suggested Delivery Order

1. ZIQ-101 through ZIQ-104: asset foundation.
2. ZIQ-201 through ZIQ-202: point and profile contract.
3. ZIQ-301, ZIQ-302, and ZIQ-401 through ZIQ-402: ingest, evaluate, and stabilize conditions.
4. ZIQ-601 through ZIQ-603, ZIQ-303, ZIQ-1101, and ZIQ-1102: visible alarm-management loop.
5. ZIQ-501 through ZIQ-503, ZIQ-701 through ZIQ-703, and ZIQ-801 through ZIQ-802: governed optimization and supervisory write path.
6. ZIQ-901 through ZIQ-1002, ZIQ-604, ZIQ-1103, and ZIQ-1201 through ZIQ-1203: operational workflow, analytics, and governance hardening.
7. ZIQ-1301 through ZIQ-1303: governed assistant workflows and observability.

## Planning Metadata

Estimates are initial relative sizing in story points. Dependencies name the minimum
stories that must be complete before a story can be accepted; teams may implement
technical foundations earlier when they do not expose user-facing behavior.

| Story | Story Points | Depends on |
|---|---:|---|
| ZIQ-101 | 8 | None |
| ZIQ-102 | 3 | ZIQ-101 |
| ZIQ-103 | 5 | ZIQ-101 |
| ZIQ-104 | 5 | ZIQ-101, ZIQ-103 |
| ZIQ-201 | 5 | ZIQ-103 |
| ZIQ-202 | 8 | ZIQ-201 |
| ZIQ-301 | 8 | ZIQ-103, ZIQ-201 |
| ZIQ-302 | 8 | ZIQ-301 |
| ZIQ-303 | 5 | ZIQ-103, ZIQ-601 |
| ZIQ-401 | 8 | ZIQ-302, ZIQ-801 |
| ZIQ-402 | 5 | ZIQ-401 |
| ZIQ-501 | 8 | ZIQ-401, ZIQ-801, ZIQ-802 |
| ZIQ-502 | 5 | ZIQ-501 |
| ZIQ-503 | 5 | ZIQ-501, ZIQ-802 |
| ZIQ-601 | 8 | ZIQ-402 |
| ZIQ-602 | 5 | ZIQ-601, ZIQ-1201, ZIQ-1202 |
| ZIQ-603 | 8 | ZIQ-601, ZIQ-1201, ZIQ-1202 |
| ZIQ-604 | 8 | ZIQ-601, ZIQ-602 |
| ZIQ-701 | 8 | ZIQ-103, ZIQ-202, ZIQ-1202 |
| ZIQ-702 | 5 | ZIQ-701, ZIQ-1201, ZIQ-1202 |
| ZIQ-703 | 13 | ZIQ-202, ZIQ-601, ZIQ-702 |
| ZIQ-801 | 5 | ZIQ-101, ZIQ-1201, ZIQ-1202 |
| ZIQ-802 | 8 | ZIQ-101, ZIQ-1201, ZIQ-1202 |
| ZIQ-901 | 5 | ZIQ-401, ZIQ-601, ZIQ-1201 |
| ZIQ-902 | 5 | ZIQ-901, ZIQ-1001 |
| ZIQ-1001 | 8 | ZIQ-101, ZIQ-1201 |
| ZIQ-1002 | 5 | ZIQ-1001 |
| ZIQ-1101 | 8 | ZIQ-104, ZIQ-401, ZIQ-601 |
| ZIQ-1102 | 8 | ZIQ-401, ZIQ-501, ZIQ-601, ZIQ-701 |
| ZIQ-1103 | 13 | ZIQ-401, ZIQ-502, ZIQ-604, ZIQ-1001 |
| ZIQ-1201 | 8 | ZIQ-101 |
| ZIQ-1202 | 8 | ZIQ-101 |
| ZIQ-1203 | 5 | ZIQ-1202 |
| ZIQ-1301 | 13 | ZIQ-401, ZIQ-601, ZIQ-701, ZIQ-1001, ZIQ-1201 |
| ZIQ-1302 | 8 | ZIQ-901, ZIQ-1001, ZIQ-1201 |
| ZIQ-1303 | 8 | ZIQ-1301, ZIQ-1302 |

## Traceability Summary

| Requirement | Stories |
|---|---|
| HFP-01 | ZIQ-101 to ZIQ-104 |
| HFP-02 | ZIQ-201 to ZIQ-202 |
| HFP-03 | ZIQ-301 to ZIQ-303 |
| HFP-04 | ZIQ-401 to ZIQ-402 |
| HFP-05 | ZIQ-501 to ZIQ-503 |
| HFP-06 | ZIQ-601 to ZIQ-604 |
| HFP-07 | ZIQ-701 to ZIQ-703 |
| HFP-08 | ZIQ-801 to ZIQ-802 |
| HFP-09 | ZIQ-901 to ZIQ-902 |
| HFP-10 | ZIQ-1001 to ZIQ-1002 |
| HFP-11 | ZIQ-1101 to ZIQ-1103 |
| HFP-12 | ZIQ-1201 to ZIQ-1203 |
| HFP-13 | ZIQ-1301 to ZIQ-1303 |