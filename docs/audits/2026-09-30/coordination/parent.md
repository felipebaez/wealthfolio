Business purpose: establish whether this personal-finance application can support a self-hosted financial advisory service with private client access and verified Czech imports.

This is an investigative, documentation-only audit. No product implementation, merge, production deployment, data deletion, paid subscriptions or third-party contact. Use synthetic data only.

Baseline: fork/upstream main 6ee11b1278eff8b5123280e740fa6983b501952b, divergence 0/0, source 3.9.2 versus published release v3.9.1 at 392f272c5b15a4af45dc2ff71dcbec474f47112a.

Architecture impact: documentation and reproducible investigation only; implementation boundaries require a later user-selected direction.

Validation: read AGENTS.md, trace code paths, use pinned repository evidence and dated official external sources, record checks and missing prerequisites. Label conclusions confirmed/inferred/unknown. No synthetic fixture proves actual bank compatibility.

BUSINESS OBJECTIVE

I am starting a financial advisory business. Clients who hire me will receive access to this application as part of the service. I will host the application on my own infrastructure.

Each client must have private access to their own financial data. Investigate advisor access as a separate, explicitly authorized permission model; do not assume advisors should automatically see every client’s portfolio.

My initial priorities are:
1. Secure multi-user client access and data isolation.
2. Imports from Czech institutions, initially Komerční banka (KB), Raiffeisenbank, ČSOB, and Česká spořitelna.
3. A maintainable self-hosted product that can continue receiving upstream improvements.

YOUR ROLE AND AUTHORIZATION

Act as the long-lived coordination chat for this project.

For every new actionable project request I make:
- Create a GitHub issue in felipebaez/wealthfolio.
- Create a dedicated Codex chat to handle that issue.
- Send that chat a complete brief and coordinate its progress.
- Keep the issue, chat, branch, pull request, dependencies, and status connected.

I explicitly authorize you to create these issues and chats, send instructions and follow-up messages to project worker chats, and inspect their progress. You may use subagents for focused research or review when useful.

Questions, status requests, corrections, and clarifications about existing work should update the existing issue and chat instead of creating duplicates. If one request contains several independent deliverables, create a parent issue and appropriately scoped child issues.

Verify which GitHub and Codex tools are actually available. Use authenticated GitHub tools or the GitHub CLI when supported. Never claim an issue, chat, PR, or background monitor exists unless its creation succeeded. If a capability is unavailable, complete independent work and report the exact missing setup.

Do not treat this prompt as authorization to merge PRs, deploy production changes, delete data, incur paid subscriptions, or contact banks, vendors, clients, or other third parties.

FIRST ASSIGNMENT: INITIAL AUDIT

Create a parent issue titled:
“Audit: self-hosted advisory platform, client isolation, and Czech bank imports”

Create dedicated audit chats for:
1. Architecture and upstream maintenance.
2. Client identity, isolation, and advisor permissions.
3. Czech bank imports and connectivity.
4. Self-hosted operations, licensing, and commercial readiness.

Keep the first phase investigative. Produce documentation, evidence, reproducible checks, recommendations, and implementation issues. Do not implement the product changes before I select the proposed direction. Keep necessary audit documentation changes reviewable.

ESTABLISH THE BASELINE

- Read applicable AGENTS.md instructions.
- Record the fork branch, commit SHA, upstream SHA, and divergence.
- Distinguish current source, released versions, and published container images.
- Inspect the architecture, manifests, migrations, deployment files, CI, tests, and existing issues.
- Trace representative frontend-to-backend-to-database execution paths.
- Identify contradictions between documentation and code.
- Run appropriate baseline checks where feasible; report failures, missing prerequisites, and checks not run.
- Use synthetic data. Never put client statements, credentials, personal data, or portfolio details into public issues, logs, PRs, or test fixtures.

A previous inspection found commit 6ee11b1278eff8b5123280e740fa6983b501952b in both fork and upstream. Treat this as historical context and verify the current baseline.

AUDIT 1: PROJECT ARCHITECTURE

Explain what the application does, its intended users, and how it works.

Map:
- React frontend and shared TypeScript packages.
- Web and Tauri adapters.
- Axum handlers and Tauri commands.
- Shared Rust business logic.
- SQLite repositories, migrations, and derived financial data.
- Profiles, secrets, workers, events, imports, exports, and backups.
- Market data and exchange-rate providers.
- Connect, brokerage sync, device sync, AI, MCP, and add-ons.
- External dependencies, paid services, and outbound financial-data flows.

Trace representative flows:
- Login and profile admission.
- Portfolio read.
- Activity creation and import.
- Holdings and performance calculation.
- Background synchronization.
- Export, backup, and restore.

Identify reusable extension points and the smallest viable changes. Avoid proposing a rewrite or a new database before establishing why the existing mechanisms are insufficient.

Recommend an upstream update strategy and identify the changes likely to create persistent merge conflicts.

AUDIT 2: MULTI-USER SECURITY

Do not equate profiles, financial accounts, browser sessions, SSO users, or Connect identities with business tenants.

Investigate the existing profile architecture, including:
- Separate databases and secret namespaces.
- Profile registry and profile listing.
- Profile passwords and recovery.
- Browser session ownership and profile grants.
- OIDC issuer/subject handling and identity retained after login.
- Installation authentication versus client authorization.
- Profile creation, selection, deletion, and administration.
- Legacy unscoped routes and default-profile behavior.

Inspect relevant code, including apps/server/src/auth.rs, oidc.rs, profiles.rs, crates/core/src/profiles/, and profile-related tests.

Evaluate three options:
A. A separate application instance, database, vault, and keys for each client.
B. One application deployment using the existing database-per-profile model with explicit identity ownership and permission enforcement.
C. Shared tenant-aware storage.

Compare isolation, implementation effort, cost, onboarding, advisor access, backups, scaling, and upstream compatibility. Recommend a pilot option and a longer-term option, with evidence and tradeoffs.

Define client, advisor, and operator permissions. Cover invitation, onboarding, authentication, MFA through an identity provider, recovery, suspension, revocation, offboarding, and authorized advisor access.

Trace every relevant data surface:
- API reads and writes.
- Profile metadata.
- Imports, exports, uploaded files, and temporary files.
- SSE and other streaming.
- Background jobs, caches, and derived data.
- Secrets and bank authorization callbacks.
- AI conversations and tools.
- MCP access.
- Add-ons.
- Sync and backups.

Require backend enforcement. Specify tests proving client A cannot enumerate, read, alter, export, restore, or receive events belonging to client B, including forged identifiers, stale grants, revoked sessions, concurrent browsers, and asynchronous jobs.

Distinguish client-to-client privacy from privacy against the trusted infrastructure operator. Do not claim encryption prevents operator access unless demonstrated by the architecture.

AUDIT 3: CZECH BANK IMPORTS

Research each bank separately using current official documentation:
- Komerční banka / KB.
- Raiffeisenbank Czech Republic.
- ČSOB Czech Republic.
- Česká spořitelna / George.

Separate:
1. Client-uploaded bank transaction exports.
2. Securities trades, holdings, funds, and investment statements.
3. Automated read-only API connectivity.

Do not assume payment-account APIs expose investment portfolios.

For each institution and product, document:
- Supported export formats and verified sample availability.
- Retail versus business account eligibility.
- API products and actual data coverage.
- Sandbox versus production access.
- Consent, authentication, certificates, registration, and contractual requirements.
- Rate limits, historical coverage, pagination, and consent renewal.
- Direct integration versus a licensed aggregator.
- Whether external providers are compatible with my self-hosting and privacy requirements.

Mark unsupported formats and unverified coverage as unknown. Request sanitized representative exports when needed; do not invent schemas or treat synthetic fixtures as proof of bank compatibility.

Trace the existing CSV parser, mapping templates, validation, preview, import persistence, deduplication, and reconciliation. Decide whether each proposed importer belongs in templates, shared core logic, an add-on, or a connector.

Cover Czech-specific parsing:
- CZK and foreign currencies.
- Czech headers and diacritics.
- UTF-8 and legacy encodings where verified.
- Semicolon delimiters, decimal commas, and thousands separators.
- Czech dates and booking versus value dates.
- IBAN and local account identifiers.
- Variable, specific, and constant symbols.
- Fees, interest, reversals, pending/booked transactions, transfers, and duplicate statements.
- Investment identifiers, quantities, prices, fees, and taxes where available.

Require preview before commit, clear row errors, deterministic money handling, repeat-import idempotency, provenance, and balance reconciliation. Prevent transfers from being counted as income or investment gains.

Recommend an initial file-import MVP and a separate automatic-connectivity roadmap. Keep payment initiation outside scope.

AUDIT 4: OPERATIONS AND COMMERCIAL READINESS

Evaluate:
- Reproducible builds and version-pinned deployment.
- HTTPS, reverse proxy, trusted headers, CORS, cookies, and CSRF.
- Secret management and key recovery.
- Database/vault concurrency and process assumptions.
- Resource usage as client count grows.
- Health checks, monitoring, and logs without financial data.
- Backup consistency across databases, registry, and secrets.
- Per-client restore, disaster recovery, upgrades, migrations, and rollback.
- Data retention, export, deletion, and offboarding.
- Staging with synthetic data.

Inspect the actual LICENSE and TRADEMARKS.md. Document AGPL source-availability obligations, branding changes, attribution, and dependency licenses. Identify third-party market-data and Connect terms that could affect a commercial hosted service.

Prepare questions for qualified Czech/EU legal review concerning GDPR, advisory activities, bank-data access, and applicable contractual obligations. Distinguish verified technical requirements from legal questions. Do not present the audit as legal approval.

DELIVERABLES

Produce:
1. An executive recommendation in plain English.
2. A project architecture map.
3. An evidence-backed findings register with severity, affected paths, reproduction or verification method, impact, and proposed action.
4. A decision record comparing the three isolation approaches.
5. A bank-by-bank import/connectivity matrix.
6. A client/advisor/operator permission matrix and threat model.
7. A deployment and recovery proposal.
8. A phased roadmap with dependencies, acceptance criteria, effort ranges, confidence, and external blockers.
9. An issue backlog linked to the audit parent issue.
10. A short list of business decisions needed from me.

Use repository permalinks pinned to the audited commit and dated official external sources. Label each conclusion as confirmed, inferred, or unknown. Include validation limitations.

Store durable project documentation in an appropriate repository location and maintain an orchestration index mapping issues to chats, branches, PRs, and statuses.

ONGOING ISSUE-TO-CHAT WORKFLOW

Each issue should describe:
- Business purpose and user-visible outcome.
- Scope and exclusions.
- Relevant architecture and evidence.
- Dependencies.
- Acceptance criteria.
- Validation plan.
- Architecture impact.
- Decisions still required.

Each worker chat should receive:
- Repository, issue URL, and baseline.
- Full requirements and acceptance criteria.
- Relevant audit findings.
- Applicable repository instructions.
- Authorization boundaries.
- Expected deliverables and reporting location.

Use isolated worktrees for implementation work. Prevent overlapping workers from changing the same files without coordination.

Workers should open reviewable PRs with linked issues, appropriate checks, and clear limitations. Attach created PRs to their Codex chats when supported. Keep an issue open until its acceptance criteria are satisfied; a worker finishing a turn is not sufficient.

Inspect progress using available coordination tools. Report meaningful changes and blockers. Do not promise unattended monitoring unless a supported continuation or automation mechanism is actually configured.

START NOW

Verify repository and tool access, establish the baseline, create the parent audit issue and dedicated audit chats, dispatch their briefs, and coordinate them through a consolidated recommendation. Continue independently where possible and ask only for information that materially affects the outcome.