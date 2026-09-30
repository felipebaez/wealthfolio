Business purpose: establish whether this personal-finance application can support a self-hosted financial advisory service with private client access and verified Czech imports.

This is an investigative, documentation-only audit. No product implementation, merge, production deployment, data deletion, paid subscriptions or third-party contact. Use synthetic data only.

Baseline: fork/upstream main 6ee11b1278eff8b5123280e740fa6983b501952b, divergence 0/0, source 3.9.2 versus published release v3.9.1 at 392f272c5b15a4af45dc2ff71dcbec474f47112a.

Architecture impact: documentation and reproducible investigation only; implementation boundaries require a later user-selected direction.

Validation: read AGENTS.md, trace code paths, use pinned repository evidence and dated official external sources, record checks and missing prerequisites. Label conclusions confirmed/inferred/unknown. No synthetic fixture proves actual bank compatibility.

Parent: https://github.com/felipebaez/wealthfolio/issues/1

Scope and acceptance criteria:



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


Expected documentation: docs/audits/2026-09-30/architecture.md and architecture-validation.md. Include executive recommendations, findings with severity/impact/evidence/proposed action, proposed backlog entries with effort/confidence/dependencies, business decisions, and limitations.

Dependencies: baseline and parent coordination; coordinate overlapping findings with other audits.

Decisions required: user selects implementation approach after consolidated review.
