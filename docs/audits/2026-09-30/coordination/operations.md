Business purpose: establish whether this personal-finance application can support a self-hosted financial advisory service with private client access and verified Czech imports.

This is an investigative, documentation-only audit. No product implementation, merge, production deployment, data deletion, paid subscriptions or third-party contact. Use synthetic data only.

Baseline: fork/upstream main 6ee11b1278eff8b5123280e740fa6983b501952b, divergence 0/0, source 3.9.2 versus published release v3.9.1 at 392f272c5b15a4af45dc2ff71dcbec474f47112a.

Architecture impact: documentation and reproducible investigation only; implementation boundaries require a later user-selected direction.

Validation: read AGENTS.md, trace code paths, use pinned repository evidence and dated official external sources, record checks and missing prerequisites. Label conclusions confirmed/inferred/unknown. No synthetic fixture proves actual bank compatibility.

Parent: https://github.com/felipebaez/wealthfolio/issues/1

Scope and acceptance criteria:



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


Expected documentation: docs/audits/2026-09-30/operations.md and commercial-readiness.md. Include executive recommendations, findings with severity/impact/evidence/proposed action, proposed backlog entries with effort/confidence/dependencies, business decisions, and limitations.

Dependencies: baseline and parent coordination; coordinate overlapping findings with other audits.

Decisions required: user selects implementation approach after consolidated review.
