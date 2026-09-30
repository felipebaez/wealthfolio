# Decision, roadmap and implementation backlog

Date: 2026-09-30. Parent
[#1](https://github.com/felipebaez/wealthfolio/issues/1); synthesis
[#8](https://github.com/felipebaez/wealthfolio/issues/8); documentation
[PR #6](https://github.com/felipebaez/wealthfolio/pull/6). Accepted requirement:
**more than 50 clients on one private server or VM**. All
estimates/recommendations below are **inferred**. Hardware, active concurrency,
histories, permissions, external-service entitlements and recovery objectives
remain **unknown**. No launch capacity is measured.

**Architecture impact:** this PR changes documentation only. Future proposals
explicitly name changes to deployment, identity/persistence, action permission,
background lifecycle, financial outputs and import provenance. Existing
React/adapters/shared Rust/SQLite/profile runtimes, writer/events, SecretStore
and opt-in provider mechanisms are reused. Product implementation, production
deployment, merge, data deletion, purchase and third-party contact are not
authorized. No implementation chat was dispatched.

## Decision record awaiting human selection

**Recommendation — inferred:** retain SQLite and the financial services. Run a
two-synthetic-client option-A safety and recovery rehearsal first. For
a >50-client launch on one VM, choose either an automated A fleet with measured
fit or authorization-complete B. Prefer B as the product direction if integrated
advisor access/one application is essential and the security implementation
budget is acceptable. A offers the smallest application delta and simplest
per-client recovery, but operating 50-plus instances manually is not the
proposed service. C is deferred until measurements establish a requirement that
A/B cannot meet.

| Option                                        | Immediate suitability                                                                                   | Cost and required work                                                                                                                             | Advisor and restore boundary                                                                                                   | Selection rule                                                                                       |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| A: separate instance/DB/vault/keys per client | Smallest source delta for a safety trial; still needs trusted ingress, unique keys and session controls | Automated onboarding/suspension/patch/backup/offboard fleet; aggregate process/provider resources unmeasured                                       | No existing read-only app role; authorized export initially. Individual installation restore; common host/root still trusted   | Choose if export-based advice is sufficient and measured fleet fits the VM and operating budget      |
| B: one deployment, owned database-per-profile | Existing profiles alone fail ownership/role requirements                                                | Durable verified principals, ownership/invitations, revocable sessions, action grants and lifecycle enforcement; retained runtimes need load tests | Explicit client-authorized read/edit/export grants. Shared registry/vault/master and stopped shared server for offline restore | Choose if integrated advisor workflow is required and backend enforcement will precede client launch |
| C: shared tenant-aware financial storage      | No established need; auth problem still remains                                                         | Tenant filtering across every row/query/job/cache/export plus migration/per-client recovery and upstream conflict cost                             | Same permission project plus broad shared-storage blast radius                                                                 | Reconsider only after a reproduced A/B limitation or required multi-server/reporting need            |

Full tradeoffs, permission cells and lifecycle/adversarial requirements:
[isolation.md](isolation.md) and
[permissions-threat-model.md](permissions-threat-model.md). Option A also needs
revocation at its actual gateway and all alternate access paths; disabling an
IdP account alone does not revoke an already issued application JWT. Do not
expose a backend path that bypasses the selected gateway.

Required new state for B has a concrete purpose: current browser grants express
temporary scope possession, cannot retain a contractual owner across
login/restart, cannot distinguish advisor/operator and cannot persist
suspension. Any minimal schema/registry extension must preserve existing
UUIDs/paths/secret key names and fail closed on unassigned legacy profiles. No
migration location is chosen by this audit.

## Phases and release gates

| Phase                                  | Work and dependencies                                                                                                                         | Exit evidence                                                                                                                                                                                                         | Deferred                                                                                                    |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| 0: review and policies                 | Review all ten audit deliverables; DEC selects A/B, permissions, first product, reporting, providers, VM workload and recovery/retention      | Decision recorded, unknowns explicitly block affected scope; no silent acceptance                                                                                                                                     | Real-client onboarding, C storage rewrite                                                                   |
| 1: synthetic safety and artifact       | Reuse existing localhost staging #7 when its evidence is complete; MAINT exact artifact/toolchain; A two-client trial or B identity/ownership | Cross-client no-side-effect denials, no backend ingress bypass, unique appropriate keys, selected source/digest, operator trust disclosed                                                                             | A trial cannot demonstrate >50 fit; local HTTP staging cannot prove production HTTPS/IdP                    |
| 2: useful and accurate files           | IMPORT + PROV + FX; privately verify first BANK variant and expected ledger                                                                   | Preview errors, exact cash/date handling, honest missing-FX quality, repeated/overlap identity, account/currency totals and transfers; authoritative history limits visible                                           | Four guessed templates, investment returns inferred from payment/holdings snapshots, automatic APIs/PDF OCR |
| 3: permission and operations readiness | B PERM lifecycle if selected; A fleet lifecycle; DR + OBS + COM; EVENT investigation before persistence remedy                                | Approved advisor policy, complete recovery/rollback/offboarding, current revocations survive recovery, safe logs/probes, exact source/brand/provider rights and qualified legal decisions                             | Atomic vault resilience only by agreement; new queues/workers/retry/eviction only after concrete failure    |
| 4: >50-client launch gate              | SCALE tests selected complete topology on target VM after previous gates                                                                      | At least 60 synthetic clients with agreed concurrent/connected/opened workload; measured resources/service limits, randomized foreign-target checks, fleet backup/restore/upgrade evidence; failed gates block launch | No production rollout in this audit; no client-count guarantee from SQLite, script tests or hardware alone  |
| 5: expansion and automation            | Certified bank/product variants by demand; AUTO access/privacy/contract choice then one read-only connector                                   | Production rights and bank-specific coverage, callback/secret isolation, consent/certificate/page/rate/revocation tests; file fallback retained                                                                       | Payment initiation; unverified aggregator onboarding; unauthorized vendor contact/purchase                  |

Estimates in the issue map are person-days for experienced
engineering/preparation after decisions and prerequisites, excluding
sample/vendor/counsel waiting. They overlap and must not be summed as a delivery
promise. Scope confidence is separate from runtime-security assurance. An
initial missing-FX or parser fix can be selected independently, but named-bank
certification and client launch remain gated by ownership/accuracy/operations
evidence.

## Measurement contract

**Inferred proposed workload, not approved SLA:** step through 1/5/20/50/**60**
synthetic clients on the chosen single VM. Record registered client count
separately from opened/retained runtimes, active browser sessions, connected
background profiles and concurrent jobs. For A measure all instance
processes/volumes plus ingress/fleet resources; for B use authorization-complete
profiles, not the unsafe baseline profile chooser.

Use matched provisional 10-account/10,000-activity histories and a
100,000-activity stress case; 5/15/30 active-user scenarios from the security
proposal are trial workloads, not known real demand. Include idle/cold
startup/admission, import/preview/commit, holdings reads, historical
recalculation, concurrent export, scheduler bursts, restart under work, low disk
and a soak that exercises timer cycles using mocks. Agree numeric
latency/resource, suspension, backup-window and RPO/RTO limits before accepting
the run. Proposed security targets (70% resource headroom, cached read p95 <2s,
cold admission p95 <10s, stream closure <=2s) are negotiable hypotheses, not
measured promises.

Capture SHA/image architecture digest/features, VM vCPU/RAM/disk/OS, database
sizes and activity mix, p50/p95/p99 latency, RSS/CPU/disk I/O/WAL,
connection/queue waits, rate-limit outcomes, failed jobs and unaffected-client
evidence. Run the cross-client matrix with colliding IDs and randomized target
routing. Zero forbidden rows/files/events/secrets/outbound calls is a required
safety property, rather than a percentile budget. A denial status alone is
insufficient. Provider-disabled/local-resolution/failure-isolation/user-edit
invariants must be measured.

At full count rehearse complete backup plus one random client's restore,
whole-VM recovery, upgrade/rollback and offboarding. Shared host failure affects
A/B/C alike. Off-host encrypted recovery storage and separately held keys need a
business-approved location/access/retention choice; backups only on the same VM
cannot recover a lost host. The local staging VM's characteristics are not the
future production sizing specification.

## Deduplicated issue backlog

Every entry below is a created open issue linked to #1, status **Not Started**,
explicitly pending direction. No chat, branch, worktree or implementation PR
exists for these proposals. This differs from already authorized local staging
#7. Full briefs include scope/exclusions, pinned source-evidence references,
dependencies, acceptance, validation, architecture impact and decisions;
[index.json](index.json) records mappings. An implementation issue gets its
dedicated isolated worker only after human selection through the command center.

| Key / issue / outcome                                                                                                                       | Lane / dependencies                                                                                                                                                                                                                                                               | Effort / confidence                                  | Findings                   |
| ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | -------------------------- |
| DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13) — Select isolation, advisor access, and launch policies                      | decision; audit review                                                                                                                                                                                                                                                            | 2–4; medium                                          | F01–07, F15, F18, F20, F22 |
| A [#14](https://github.com/felipebaez/wealthfolio/issues/14) — Provision isolated client instances and lifecycle on one VM                  | A only; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13)                                                                                                                                                                                                            | 7–15; medium/low                                     | F01–07, F17, F18, F20      |
| B [#15](https://github.com/felipebaez/wealthfolio/issues/15) — Retain revocable principals and enforce profile ownership                    | B only; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13)                                                                                                                                                                                                            | 9–18; medium                                         | F01, F02, F04, F05         |
| PERM [#16](https://github.com/felipebaez/wealthfolio/issues/16) — Enforce advisor capabilities and revocation across tools and jobs         | B or later advisor app; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13), B [#15](https://github.com/felipebaez/wealthfolio/issues/15)                                                                                                                              | 14–28; low/medium                                    | F03–06, F18                |
| BANK [#17](https://github.com/felipebaez/wealthfolio/issues/17) — Verify first Czech bank product and file-import variant                   | file MVP; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13), IMPORT [#18](https://github.com/felipebaez/wealthfolio/issues/18), PROV [#19](https://github.com/felipebaez/wealthfolio/issues/19)                                                                      | 4–8 per CSV variant; medium after sample             | F15                        |
| IMPORT [#18](https://github.com/felipebaez/wealthfolio/issues/18) — Preserve parser errors and enforce exact money and date input           | shared correctness; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13)                                                                                                                                                                                                | 5–10; medium/high                                    | F10, F11                   |
| PROV [#19](https://github.com/felipebaez/wealthfolio/issues/19) — Make bank import provenance, repeat identity, and reconciliation reliable | shared correctness; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13), IMPORT [#18](https://github.com/felipebaez/wealthfolio/issues/18)                                                                                                                             | 10–20; medium                                        | F12–14                     |
| FX [#20](https://github.com/felipebaez/wealthfolio/issues/20) — Represent unavailable FX honestly in holdings and exports                   | shared correctness; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13)                                                                                                                                                                                                | 2–5; medium                                          | F08                        |
| DR [#21](https://github.com/felipebaez/wealthfolio/issues/21) — Rehearse complete backup, per-client restore, and revocation-safe recovery  | launch gate; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13), MAINT [#24](https://github.com/felipebaez/wealthfolio/issues/24)                                                                                                                                     | 4–8; medium                                          | F18, F19                   |
| OBS [#22](https://github.com/felipebaez/wealthfolio/issues/22) — Remove financial log payloads and validate safe operational monitoring     | launch gate; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13)                                                                                                                                                                                                       | 3–6; medium/high                                     | F21, F17                   |
| SCALE [#23](https://github.com/felipebaez/wealthfolio/issues/23) — Measure more-than-50-client isolation and capacity on one VM             | launch gate; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13), MAINT [#24](https://github.com/felipebaez/wealthfolio/issues/24), DR [#21](https://github.com/felipebaez/wealthfolio/issues/21)                                                                      | 4–8; medium                                          | F20, F04, F17              |
| MAINT [#24](https://github.com/felipebaez/wealthfolio/issues/24) — Pin deployment artifacts and establish upstream upgrade verification     | launch gate; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13)                                                                                                                                                                                                       | 3–6; medium                                          | F16, F23                   |
| COM [#25](https://github.com/felipebaez/wealthfolio/issues/25) — Prepare source, branding, provider rights, and Czech/EU launch review      | launch gate; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13), MAINT [#24](https://github.com/felipebaez/wealthfolio/issues/24)                                                                                                                                     | 6–14 preparation; medium; external time unknown      | F22, F15                   |
| AUTO [#26](https://github.com/felipebaez/wealthfolio/issues/26) — Decide lawful read-only bank connectivity before one connector pilot      | later optional; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13), PROV [#19](https://github.com/felipebaez/wealthfolio/issues/19), COM [#25](https://github.com/felipebaez/wealthfolio/issues/25), SCALE [#23](https://github.com/felipebaez/wealthfolio/issues/23) | 3–5 analysis; 10–20 implementation; low until access | F15, F22                   |
| EVENT [#27](https://github.com/felipebaez/wealthfolio/issues/27) — Investigate interrupted historical recalculation recovery                | investigation first; DEC [#13](https://github.com/felipebaez/wealthfolio/issues/13), MAINT [#24](https://github.com/felipebaez/wealthfolio/issues/24)                                                                                                                             | 1–3 investigation; medium                            | F09                        |
| VAULT [#28](https://github.com/felipebaez/wealthfolio/issues/28) — Evaluate crash-atomic vault persistence only after failure evidence      | optional resilience; DR [#21](https://github.com/felipebaez/wealthfolio/issues/21)                                                                                                                                                                                                | 3–7 after agreement; medium                          | F19                        |

## Specialist proposal reconciliation

| Specialist candidate                                            | Consolidated outcome                                                                                                                                                                |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ARCH-B1/B5/B7/B8/B6/B9/B10; SEC-PILOT/ID/OWN/PERM/LIFE/REC/GATE | MAINT; A or B/PERM; SCALE; DR; OBS. ARCH-B5's 10–25-day coarse scope is superseded by separate B/PERM estimates; it is not an additional budget                                     |
| ARCH-B2/B3/B4                                                   | FX; EVENT investigation; PROV. No durable recalculation mechanism approved from source hypothesis alone                                                                             |
| BANK-01/02/03 and BANK-06–10                                    | BANK first verified variant; later variants/investments remain within selected demand or separately scoped follow-ups; access/privacy choice in AUTO                                |
| IMP-07/08/09/10                                                 | IMPORT combines diagnostics/number/date fixes; PROV combines source identity/run integrity/reconciliation because their tests share account/currency/source contracts               |
| BANK-04/05                                                      | AUTO decision first, connector implementation only after contracts/ownership/import guarantees; not part of file MVP                                                                |
| OPS-B1/B2/B3/B4/B5/B6/B7/B8                                     | Existing staging #7 plus A/B, MAINT, DR, OBS, SCALE; VAULT optional; PERM/DR restore policy. B8 eviction/drain/export-budget changes deferred until measurement establishes failure |
| COM-B1/B2/B3/B4/B5                                              | COM preparation, actual-artifact rights/notices and qualified review; operating evidence owned by DR/OBS/SCALE, no duplicate launch-readiness implementation issue                  |

## Business decisions needed

1. **Isolation and advisor service:** automated A/export-based advice or
   implement B/in-app explicit grants? One person or household per client?
   Read-only proposed default, export/edit separately granted, expiry/revocation
   and operator break-glass policy?
2. **Workload and recovery:** production VM resources/region, active
   concurrency, histories/growth, downtime tolerance, RPO/RTO, off-host backup
   custody, retention/legal holds and suspension deadline? Client target >50 and
   single VM are already fixed.
3. **First useful import/report:** actual bank/product/channel/tariff/export
   variant and private authorized sample intake; cash ledger vs dated holdings
   vs reconstructed performance? Missing FX/stale/rebuilding output policy and
   minimum provenance/reconciliation requirements?
4. **External services:** permitted
   quote/identifier/Connect/AI/agent/add-on/aggregator recipients and financial
   data transit? Contract rights and quotas for advisor/client display,
   export/derived values and backups; keep unapproved integrations disabled
   until selected/tested.
5. **Commercial/legal:** legal entity and exact advice activity, independent
   brand/domain, exact-source distribution, client terms, qualified Czech/EU
   review owner, incident/support obligations and budget? Audit is not legal
   approval; no contact or spending authorized.
6. **Maintenance scope:** hosted web first or native/mobile too;
   release/security update cadence and support budget; whether to authorize
   evidence-gated optional resilience or later read-only connectivity? No
   automatic product implementation follows from this report.

## Acceptance state

All ten requested artifacts are mapped in [README.md](README.md), with exact
specialist documentation revisions and evidence review in
[coordination/review.md](coordination/review.md). Audit issues and PRs stay
open/In Progress while acceptance review is pending. Completed requires criteria
accepted, recorded validation and issue closed completed. Technical
investigation delivered is distinct from approved launch, merged implementation,
measured capacity and legal/contractual entitlement.
