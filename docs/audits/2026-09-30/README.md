# Self-hosted advisory platform audit — 2026-09-30

Parent [#1](https://github.com/felipebaez/wealthfolio/issues/1), synthesis
[#8](https://github.com/felipebaez/wealthfolio/issues/8), consolidated
documentation [PR #6](https://github.com/felipebaez/wealthfolio/pull/6). Audited
application source: `6ee11b1278eff8b5123280e740fa6983b501952b`. Documentation
review remains In Progress; this report does not approve client launch.

## Executive recommendation

**Inferred recommendation:** keep Wealthfolio's React frontend, shared Rust
financial services, SQLite repositories and database-per-profile runtimes. They
are useful foundations, but installation login and profile passwords do not
assign data to business clients. Current source loses the OIDC issuer/subject in
a generic installation session, exposes the profile registry and permits
selection of unprotected profiles. Do not admit unrelated clients to an
unmodified shared installation.

Use **A, a separate application instance/database/vault/keys per client**, for a
two-synthetic-client isolation and recovery trial. For the accepted >50-client
single-VM launch, choose an automated A fleet with measured capacity or
implement **B, one deployment with explicit identity ownership and backend
client/advisor/operator permissions on existing profiles**. B is the preferred
product direction if integrated advisor access is essential; it needs a security
project before client onboarding. A has the smallest source delta, but fleet
operation and gateway revocation still need work. **C, shared tenant-aware
financial storage, is deferred**; no measured evidence justifies a database
rewrite. All three share trusted host/operator and single-VM failure boundaries.
[Isolation comparison](isolation.md),
[roadmap and pending decisions](roadmap.md).

**Inferred advisor policy:** explicit client-specific read-only grant, with
edit/export as separate capabilities. Current app admission is broad access;
adding an advisor to an OIDC allowlist cannot make them read-only. A can
initially use a client-authorized export workflow. Clients remain private from
one another; host/root and application-held keys do not provide privacy from the
trusted infrastructure operator.
[Permission matrix and threat model](permissions-threat-model.md).

**Inferred import direction:** certify one actual bank/product/channel/export
variant using authorized sanitized structure and independent expected results.
Reuse preview/templates/parser/core validation/writer/events. Address lost
parser diagnostics, permissive number normalization/CASH float sums, missing
bank source identity, best-effort run provenance and statement/transfer
reconciliation. George's general CSV export is publicly documented; KB+ CSV
evidence is business-tariff-specific; RB business variants and ČSOB CEB
structured formats differ. No named-bank compatibility is established yet.
Payment-account histories do not reconstruct investment trades, cost basis or
returns. Automatic read-only connectivity has separate eligibility, consent,
certificates, privacy and commercial gates; payment initiation stays excluded.
[Bank/product matrix](banks.md), [import pipeline](imports.md).

**Inferred financial-output gate:** reproduce and correct missing/error FX
lookup being presented as 1:1 in live holdings and exports. Decide how
unavailable/stale/rebuilding data is displayed. Investigate interrupted
historical recalculation before adding any persisted recovery mechanism.
[Findings F08–F14](findings.md).

**Inferred operations/commercial gate:** promote an exact source/image digest
through synthetic staging; validate trusted HTTPS ingress, no backend bypass,
safe logs and measured load. Reuse stopped whole-installation backups containing
registry, all databases/sidecars, encrypted vault and external paths, with
separately held matching keys. Rehearse per-client and full recovery,
upgrades/rollback and current access revocation after restore. A database export
is not that recovery set. Distinguish AGPL/deployed-source obligations and fork
branding from bank/Connect/market-data service rights. Connect terms updated
2026-09-23 restrict unauthorized commercial use; counsel/vendor entitlement is
not established by a subscription or client consent.
[Operations](operations.md),
[commercial and Czech/EU review questions](commercial-readiness.md).

**Confirmed user requirement:** the initial deployment proposal targets more
than 50 clients. The pilot infrastructure is a single private server or VM.
Hardware, concurrent users and portfolio sizes are unverified. A small technical
isolation pilot is distinct from launch capacity. Automated provisioning,
lifecycle operations, per-client recovery and measured capacity gates are
required in the proposal; no capacity is claimed without tests.

**Confirmed limitation:** this is an investigative source audit with limited
diagnostic checks, not a passed penetration test, financial-calculation
certification, load test, disaster-recovery drill or legal approval. Four
launcher tests, 22 Python CI-script unit tests and seven isolated bank-helper
checks passed in the documented environments; no complete runtime/security
guarantee follows. Focused Vitest attempts never executed, and Node/pnpm
differed from repository pins. Cargo/Docker were absent during specialist
checks; separately authorized staging #7 later installed tools, but its
application/recovery evidence remains separate and pending. Source 3.9.2 is 38
commits beyond release v3.9.1 and cannot be equated with a published container.
No product implementation, merge or production deployment occurred in this
audit.

## Ten requested deliverables

| Deliverable                                                      | Reviewable artifact                                                                                   |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 1. Plain-English executive recommendation                        | This document                                                                                         |
| 2. Architecture map and upstream strategy                        | [architecture.md](architecture.md), [architecture-validation.md](architecture-validation.md)          |
| 3. Severity, paths, evidence, method, impact and action register | [findings.md](findings.md)                                                                            |
| 4. A/B/C isolation decision                                      | [isolation.md](isolation.md), [roadmap decision](roadmap.md#decision-record-awaiting-human-selection) |
| 5. Bank-by-bank export/investment/connectivity matrix            | [banks.md](banks.md), [imports.md](imports.md)                                                        |
| 6. Client/advisor/operator permission matrix and threat model    | [permissions-threat-model.md](permissions-threat-model.md)                                            |
| 7. Deployment and recovery proposal                              | [operations.md](operations.md)                                                                        |
| 8. Phased roadmap, dependencies, effort/confidence and gates     | [roadmap.md](roadmap.md)                                                                              |
| 9. Created issue backlog linked to parent #1                     | [roadmap issue map](roadmap.md#deduplicated-issue-backlog): #13–#28, Not Started/pending direction    |
| 10. Business decisions                                           | [roadmap decisions](roadmap.md#business-decisions-needed)                                             |

## Evidence, ownership and review status

- [brief.md](brief.md) is the preserved original authorized request.
  Later >50/single-VM steering, command-center handoff and status addendum are
  in [workflow.md](workflow.md); historical assumptions are not current
  requirements.
- [baseline.md](baseline.md) distinguishes source/release/image and exact
  executed versus unrun checks. [coordination/review.md](coordination/review.md)
  records reviewed specialist PR revisions, independent evidence checks,
  limitations and reconciliation.
- [index.json](index.json) maps parent, specialists, synthesis, staging and
  proposal backlog. **Wealth Command Center** owns
  issues/dispatch/status/business choices; synthesis #8 owns technical
  review/files. No continuous monitor is configured.
- Specialist documentation is copied only from reviewed exact revisions into PR
  #6. Their independent PRs remain open; no GitHub PR or main merge occurred.
  Acceptance review is pending, so all audit issues/chats stay In Progress.
- Separately authorized localhost staging
  [#7](https://github.com/felipebaez/wealthfolio/issues/7),
  [PR #12](https://github.com/felipebaez/wealthfolio/pull/12), is not production
  authorization or evidence that its checks passed. The audit never modifies its
  worktree.

**Architecture impact:** documentation and audit-only reproductions.
Runtime/network/provider settings, synchronous/background timing,
persistence/events, business-logic ownership, failures/retries and user-edit
precedence remain unchanged. The future boundary changes and their required
invariants are explicit in the issue briefs. No proposed fix is verified by
documentation acceptance.
