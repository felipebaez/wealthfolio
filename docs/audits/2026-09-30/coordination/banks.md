Business purpose: establish whether this personal-finance application can support a self-hosted financial advisory service with private client access and verified Czech imports.

This is an investigative, documentation-only audit. No product implementation, merge, production deployment, data deletion, paid subscriptions or third-party contact. Use synthetic data only.

Baseline: fork/upstream main 6ee11b1278eff8b5123280e740fa6983b501952b, divergence 0/0, source 3.9.2 versus published release v3.9.1 at 392f272c5b15a4af45dc2ff71dcbec474f47112a.

Architecture impact: documentation and reproducible investigation only; implementation boundaries require a later user-selected direction.

Validation: read AGENTS.md, trace code paths, use pinned repository evidence and dated official external sources, record checks and missing prerequisites. Label conclusions confirmed/inferred/unknown. No synthetic fixture proves actual bank compatibility.

Parent: https://github.com/felipebaez/wealthfolio/issues/1

Scope and acceptance criteria:



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


Expected documentation: docs/audits/2026-09-30/banks.md and imports.md. Include executive recommendations, findings with severity/impact/evidence/proposed action, proposed backlog entries with effort/confidence/dependencies, business decisions, and limitations.

Dependencies: baseline and parent coordination; coordinate overlapping findings with other audits.

Decisions required: user selects implementation approach after consolidated review.
