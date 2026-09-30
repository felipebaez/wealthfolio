Business purpose: establish whether this personal-finance application can support a self-hosted financial advisory service with private client access and verified Czech imports.

This is an investigative, documentation-only audit. No product implementation, merge, production deployment, data deletion, paid subscriptions or third-party contact. Use synthetic data only.

Baseline: fork/upstream main 6ee11b1278eff8b5123280e740fa6983b501952b, divergence 0/0, source 3.9.2 versus published release v3.9.1 at 392f272c5b15a4af45dc2ff71dcbec474f47112a.

Architecture impact: documentation and reproducible investigation only; implementation boundaries require a later user-selected direction.

Validation: read AGENTS.md, trace code paths, use pinned repository evidence and dated official external sources, record checks and missing prerequisites. Label conclusions confirmed/inferred/unknown. No synthetic fixture proves actual bank compatibility.

Parent: https://github.com/felipebaez/wealthfolio/issues/1

Scope and acceptance criteria:



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


Expected documentation: docs/audits/2026-09-30/isolation.md and permissions-threat-model.md. Include executive recommendations, findings with severity/impact/evidence/proposed action, proposed backlog entries with effort/confidence/dependencies, business decisions, and limitations.

Dependencies: baseline and parent coordination; coordinate overlapping findings with other audits.

Decisions required: user selects implementation approach after consolidated review.
