# Everest Project Weekly Status Report Backlog

## Backlog Conventions

- **Priority:** `P0` is required for the first usable report, `P1` is important for the first release, and `P2` is a follow-up enhancement.
- **Dependencies:** A task should not begin until its listed prerequisite is complete.
- **Definition of done:** The task's acceptance criteria are met, the result is reviewed, and any relevant evidence is recorded.

## Phase 1: Setup

- [ ] **SETUP-01 [P0] Confirm unresolved product decisions** — custom skill
  - Decide the squad count and names, reporting week boundary, timezone, deadline, Jira project and board scope, shared-folder platform/path, report naming convention, retention period, and client-facing distribution rules.
  - Decide whether squad sections are required in the first release.
  - Decide whether missing data should warn, block generation, carry forward prior values, or omit the affected section.
  - **Acceptance criteria:** All open decisions in `project_spec.md` have an owner, decision, and recorded rationale.

- [ ] **SETUP-02 [P0] Select the implementation runtime and repository layout** — custom skill
  - Confirm Python or another approved runtime and define the command entry point, source directories, configuration location, test directory, and output directory.
  - **Dependencies:** SETUP-01.
  - **Acceptance criteria:** A documented project layout exists and the chosen runtime can execute a minimal command successfully.

- [ ] **SETUP-03 [P0] Define configuration and secret-handling contracts** — custom skill
  - Specify required configuration keys for Jira, reporting dates, squads, JQL filters, metrics, and the shared-folder output path.
  - Define how credentials are supplied without storing tokens or passwords in source control.
  - Add example configuration with placeholders only.
  - **Dependencies:** SETUP-01, SETUP-02.
  - **Acceptance criteria:** Required and optional settings are documented, invalid or missing secrets are rejected, and no real credential is present in the repository.

- [ ] **SETUP-04 [P1] Establish project quality gates** — custom skill
  - Choose formatting, linting, type-checking, test, and Markdown validation commands.
  - Add an initial `.gitignore` and confirm generated reports, caches, logs, and local secrets are excluded as appropriate.
  - **Dependencies:** SETUP-02.
  - **Acceptance criteria:** A single documented validation command can be run locally and fails for a deliberately invalid change.

## Phase 2: Core Features

- [ ] **CORE-01 [P0] Implement reporting-period resolution** — custom skill
  - Accept an explicit week-ending date or equivalent manual input.
  - Resolve the configured week boundary and timezone into a start and end timestamp.
  - Include the resolved period in report metadata.
  - **Dependencies:** SETUP-01, SETUP-03.
  - **Acceptance criteria:** Boundary dates, timezone conversion, invalid dates, and a repeated run for the same period are deterministic.

- [ ] **CORE-02 [P0] Define the report domain model** — custom skill
  - Model project metadata, overall RAG status, summary, accomplishments, next steps, risks, blockers, dependencies, decisions, metrics, squad updates, warnings, and metadata.
  - Distinguish required fields from optional fields and represent missing values explicitly.
  - **Dependencies:** SETUP-01.
  - **Acceptance criteria:** The model represents every required section from the specification and validates required fields with actionable errors.

- [ ] **CORE-03 [P0] Build Markdown report rendering** — custom skill
  - Implement the report sections and tables defined in the specification.
  - Render project-level content and configurable squad subsections without leaking template placeholders into completed output.
  - **Dependencies:** CORE-01, CORE-02.
  - **Acceptance criteria:** A fixture containing representative data produces readable Markdown with every required section and stable ordering.

- [ ] **CORE-04 [P0] Support manual Delivery Manager review inputs** — custom skill
  - Provide a manual input format for the overall RAG status, delivery-confidence summary, accomplishments, next steps, risks, dependencies, decisions, and squad updates.
  - Validate that the RAG status is explicitly selected rather than inferred.
  - **Dependencies:** CORE-02.
  - **Acceptance criteria:** A user can supply review inputs, validation rejects an absent RAG status, and approved inputs are included in the rendered report.

- [ ] **CORE-05 [P0] Implement missing-data warnings** — custom skill
  - Detect missing squad updates, unavailable metrics, stale data, failed sources, and fields requiring review.
  - Add visible warnings to the report and preserve enough context for the user to correct the issue.
  - **Dependencies:** CORE-02, SETUP-01.
  - **Acceptance criteria:** Each agreed missing-data policy has a testable behavior and no missing source data is silently presented as complete.

- [ ] **CORE-06 [P0] Add manual report-generation command** — custom skill
  - Create a command that accepts configuration and review inputs, validates them, renders the report, and writes a dated Markdown file.
  - Return a useful exit code and concise error message on failure.
  - **Dependencies:** CORE-01 through CORE-05.
  - **Acceptance criteria:** A user can generate a sample report from local fixture data without Jira access.

## Phase 3: Integration

- [ ] **INTEGRATION-01 [P0] Configure read-only Jira access** — MCP
  - Implement the approved authentication mechanism using least privilege.
  - Load the Jira URL and credentials from the agreed secure configuration source.
  - Add connection and permission diagnostics without logging secrets.
  - **Dependencies:** SETUP-01, SETUP-03, SETUP-04.
  - **Acceptance criteria:** Authentication succeeds with approved credentials, fails clearly with invalid credentials, and secrets are absent from logs and output.

- [ ] **INTEGRATION-02 [P0] Implement configurable Jira queries** — MCP
  - Add configuration for project keys, boards, sprints, releases, epics, issue types, statuses, and saved JQL filters.
  - Scope every query to the resolved reporting period where applicable.
  - **Dependencies:** INTEGRATION-01, CORE-01, SETUP-01.
  - **Acceptance criteria:** Query results are limited to configured Everest Project scope and can be reproduced from recorded filter configuration.

- [ ] **INTEGRATION-03 [P0] Implement the mandatory Jira metrics** — custom skill
  - Implement the metric set selected during SETUP-01, with an initial recommendation to start with completed work and planned-versus-completed work.
  - Add risks/blockers, sprint/release progress, and defects only when selected as first-release metrics.
  - Preserve source filters and reporting period with each result.
  - **Dependencies:** SETUP-01, INTEGRATION-02, CORE-02.
  - **Acceptance criteria:** Each selected metric has a documented formula, fixture coverage, source attribution, and report output.

- [ ] **INTEGRATION-04 [P1] Load squad updates** — custom skill
  - Define and implement the approved squad-input source, such as a Markdown, YAML, JSON, or form-based input.
  - Validate squad names against configuration and report missing or duplicate updates.
  - **Dependencies:** SETUP-01, CORE-02, CORE-05.
  - **Acceptance criteria:** Leads can provide one update per configured squad and the generator includes validated updates in the correct sections.

- [ ] **INTEGRATION-05 [P0] Write output to the approved shared folder** — custom skill
  - Implement the configured destination and report naming convention.
  - Prevent accidental overwrite unless explicitly requested.
  - **Dependencies:** SETUP-01, CORE-06.
  - **Acceptance criteria:** A generated report is written to the approved path, the final path is displayed, and an unavailable destination produces a clear failure.

- [ ] **INTEGRATION-06 [P1] Add end-to-end generation flow** — custom skill
  - Combine reporting-period resolution, Jira retrieval, squad inputs, manual review, validation, rendering, warnings, and file output.
  - **Dependencies:** CORE-06, INTEGRATION-01 through INTEGRATION-05.
  - **Acceptance criteria:** A representative end-to-end run produces a stakeholder-ready Markdown report from configured sources.

## Phase 4: Testing

- [ ] **TEST-01 [P0] Add unit tests for configuration and period handling** — custom skill
  - Cover required settings, invalid values, secret references, timezone boundaries, week boundaries, and deterministic report periods.
  - **Dependencies:** SETUP-03, CORE-01.
  - **Acceptance criteria:** Valid inputs pass and each documented invalid-input path has a focused failing assertion.

- [ ] **TEST-02 [P0] Add unit tests for domain validation and warnings** — custom skill
  - Cover missing RAG status, incomplete risk ownership, missing dates, duplicate squads, stale data, unavailable metrics, and the selected missing-data policy.
  - **Dependencies:** CORE-02, CORE-04, CORE-05, SETUP-01.
  - **Acceptance criteria:** Validation errors are actionable and warning output never silently hides missing information.

- [ ] **TEST-03 [P0] Add renderer snapshot or golden-file tests** — custom skill
  - Compare generated Markdown against approved examples for complete data, multiple squads, warnings, and empty optional sections.
  - **Dependencies:** CORE-03.
  - **Acceptance criteria:** Required headings, tables, values, and metadata appear in the expected order without unresolved placeholders.

- [ ] **TEST-04 [P0] Add Jira integration tests with mocked responses** — MCP
  - Cover authentication failures, pagination, query scope, empty results, API errors, rate limits, and metric calculations.
  - **Dependencies:** INTEGRATION-01 through INTEGRATION-03.
  - **Acceptance criteria:** Tests run without live credentials and verify no secrets are exposed in exceptions or logs.

- [ ] **TEST-05 [P0] Run end-to-end and security checks** — custom skill
  - Run the generator with fixture data and approved test configuration.
  - Verify output location, filename, Markdown validity, repeatability, secret scanning, and repository cleanliness.
  - **Dependencies:** INTEGRATION-06, TEST-01 through TEST-04.
  - **Acceptance criteria:** The full validation command passes and produces a reviewable sample report.

- [ ] **TEST-06 [P1] Conduct stakeholder acceptance review** — custom skill
  - Have the Delivery Manager and representative executive, client, and engineering reviewers assess clarity, accuracy, sensitivity, and actionability.
  - Record defects and update backlog priorities.
  - **Dependencies:** TEST-05.
  - **Acceptance criteria:** Reviewers approve the first-release report or all identified gaps have owners and due dates.

## Phase 5: Documentation

- [ ] **DOC-01 [P0] Write setup and configuration documentation** — custom skill
  - Document prerequisites, installation, configuration keys, secure credential setup, Jira scope, squad configuration, and shared-folder setup.
  - **Dependencies:** SETUP-02, SETUP-03, INTEGRATION-01.
  - **Acceptance criteria:** A new maintainer can configure the tool without access to undocumented tribal knowledge.

- [ ] **DOC-02 [P0] Write the operator runbook** — custom skill
  - Document the manual weekly workflow: gather inputs, select the reporting period, review RAG status, run generation, inspect warnings, review output, and share the approved report.
  - Include recovery steps for missing Jira access, missing squad updates, failed output, and stale data.
  - **Dependencies:** CORE-06, INTEGRATION-06, TEST-05.
  - **Acceptance criteria:** A Delivery Manager can complete a weekly run and resolve the documented common failures.

- [ ] **DOC-03 [P0] Document metrics and data lineage** — custom skill
  - Record every selected metric's definition, formula, Jira filters, period, source fields, limitations, and owner.
  - **Dependencies:** SETUP-01, INTEGRATION-03.
  - **Acceptance criteria:** A reviewer can reproduce each metric and explain material changes between weekly reports.

- [ ] **DOC-04 [P1] Document the report template and review standards** — custom skill
  - Explain each report section, RAG criteria, risk-writing standard, audience considerations, sensitivity rules, and approval checklist.
  - **Dependencies:** CORE-03, CORE-04, TEST-06.
  - **Acceptance criteria:** Squad leads and reviewers can provide consistent inputs and identify an unacceptable report before distribution.

- [ ] **DOC-05 [P0] Document support, retention, and change procedures** — custom skill
  - Define ownership, report retention, audit expectations, versioning, incident escalation, Jira schema changes, and how to update filters or metrics safely.
  - **Dependencies:** SETUP-01, TEST-06.
  - **Acceptance criteria:** Operational ownership and change paths are explicit, including who approves changes to sensitive outputs.

- [ ] **DOC-06 [P1] Publish a worked example and release checklist** — custom skill
  - Include a representative generated report, pre-release checks, stakeholder approval, and post-release verification steps.
  - **Dependencies:** TEST-05, DOC-01 through DOC-05.
  - **Acceptance criteria:** The release checklist can be followed from a clean environment and produces an approved sample output.

## Suggested MVP Cut Line

The first usable milestone should include all `P0` tasks through report generation, Jira integration, validation, testing, and operator documentation. `P1` tasks can follow after stakeholder acceptance unless SETUP-01 determines that a particular item is required for the initial release.
