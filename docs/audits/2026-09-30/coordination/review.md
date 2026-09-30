# Synthesis evidence review and acceptance ledger

Date: 2026-09-30. Synthesis
[#8](https://github.com/felipebaez/wealthfolio/issues/8), parent
[#1](https://github.com/felipebaez/wealthfolio/issues/1), consolidation
[PR #6](https://github.com/felipebaez/wealthfolio/pull/6). Application source
remains `6ee11b1278eff8b5123280e740fa6983b501952b`. This ledger records
documentation/source review; launch and audit acceptance remain pending human
review.

## Reviewed specialist revisions

| Lane            | PR / exact reviewed head                                                                             | Review and evidence limits                                                                                                                                                                                                                   |
| --------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Architecture #2 | [#29](https://github.com/felipebaez/wealthfolio/pull/29), `86bc13b654e6c94d3e85effb401a075977317188` | Reports, source inventory/validation/progress and formatter config; representative flows, nine findings and >50-client distinctions reviewed. Dependency-free inventory/link helper independently passes. Final source/runtime checks unrun. |
| Security #3     | [#9](https://github.com/felipebaez/wealthfolio/pull/9), `b09f7467bb2f61931d250bf5dbd4aca6fcf79129`   | Nine findings, A/B/C comparison, permission/lifecycle surface map, two-browser recipe and T01–T14 negative families reviewed; final docs checker independently passes. Recipes are unexecuted.                                               |
| Banks #4        | [#10](https://github.com/felipebaez/wealthfolio/pull/10), `948bded343172d5258f2f71a4ec1f0812dc69a9d` | Product/retail/business export and API matrices, sources/unknowns, two-runtime import trace, six pipeline findings and diagnostic helper reviewed. Seven helper tests independently pass; no real export/API eligibility test.               |
| Operations #5   | [#11](https://github.com/felipebaez/wealthfolio/pull/11), `f9e05baa97c9f9d821b235ba0d0b5825cd018062` | Nine operating/six commercial findings, single-VM fleet/profile alternatives, restore/key/authorization and terms reviewed. 4/22 script checks reported by worker, not live recovery/encryption evidence.                                    |

Only documentation/audit helper/state files from these exact heads were copied
using read-only `git show` from specialist checkouts into the sole consolidation
branch. Their PR file lists were inspected through authenticated `gh`,
explicitly targeting `felipebaez/wealthfolio`, before copying. No product path,
another worker checkout, GitHub PR merge or main update occurred. Independently
formatting synthesis copies changes presentation only; exact substantive source
remains attributed above. Publication-time state files can say CI pending; final
issue/check evidence below supersedes those historical snapshots.

## Independent evidence checks

**Confirmed source checks by synthesis:**

- Login: fixed `wealthfolio-web` claims in `auth.rs`, verified OIDC callback
  issuing generic cookie, no owner relation in profile model; unconditional
  registry/pending list; unlock proof absent for unprotected target; fixed
  request AppState and post-handler/body scope rechecks. This verifies the
  mechanism, not a live two-client exploit.
- Revocation: JWT validation has no principal revocation lookup; profile
  lock/grant revocation differs from scheduled workers/PATs; MCP cold runtime is
  selected before profile-local PAT validation. Existing delayed-write tests
  describe completed original-profile writes despite later denied response. Full
  stream/tool/job lifecycle is not executed here.
- Financial/import: live holdings error uses/caches FX `Decimal::ONE`; bank
  helper implementation strips malformed text and CASH expression uses binary
  float sum; parser diagnostics omitted from wizard state; semantic fingerprint
  depends on day/economics/notes, CSV source reference absent; import run
  create/finalize failures warn while activity insertion continues. Real
  currency/statement/performance outcomes still require runtime tests.
- Persistence/operations: vault's process mutex/direct `fs::write` is not
  crash-atomic; per-profile snapshots exclude registry/vault/master keys;
  portable restore preserves PAT records; logs serialize malformed
  performance/account names/debug financial values; Docker pnpm differs from
  root requirement. Actual crashes, token resurrection, leaks, Docker failure or
  CSRF exploit were not reproduced.
- Baseline: fresh authenticated commit lookups still matched pinned
  fork/upstream main. Final specialist changes were confined to owned audit
  docs/helpers/state; no tracked application/lockfile change is included.

**Official external spot checks, accessed 2026-09-30:**

| Source                                                                                               | Supported conclusion / limit                                                                                                                               |
| ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [OIDC Core §5.7](https://openid.net/specs/openid-connect-core-1_0.html#ClaimStability), errata set 2 | Issuer/subject stable-identity guidance supports B's principal design; does not prove implementation.                                                      |
| [Connect terms](https://wealthfolio.app/connect/legal/terms-of-use/), updated 2026-09-23             | Unauthorized commercial use restricted; personal/household plan does not establish entitlement. Signed permissions unknown.                                |
| [Connect product page](https://wealthfolio.app/connect/)                                             | Optional individual prices/household marketing and third-party transit are attributed public statements, not measured privacy/SLAs or advisor permissions. |
| [George export FAQ](https://www.csas.cz/cs/caste-dotazy/jak-z-george-exportovat-transakce)           | Published formats/selectable fields confirmed; actual variant/sample and current customer eligibility untested.                                            |
| [KB+ export help](https://www.kb.cz/cs/podpora/ucty-a-platby/jak-stahnout-ucetni-data-v-kbplus)      | Business export documentation consulted separately from unverified retail/investment schemas.                                                              |
| [Enable Banking CZ](https://enablebanking.com/docs/markets/cz)                                       | Current stated restriction for Czech-resident payment-service users; authorized TPP technical use is a distinct model.                                     |
| [SQLite WAL](https://www.sqlite.org/wal.html)                                                        | Snapshot/sidecar/shared-host constraints support complete-backup practice; no Wealthfolio throughput guarantee.                                            |

Specialists reviewed the remaining dated official
bank/provider/CNB/EDPB/Commission/ÚOOÚ references in their reports. Synthesis
spot-checked critical sources and inspected their evidence register; it did not
independently fetch every external page, authenticate gated portals or approve
contracts/legal classifications. Inaccessible manuals/portals and unknown
applicability remain explicitly unknown. Actual repository LICENSE/TRADEMARKS
were independently read; commercial scope requires qualified review, not this
ledger's approval.

## Reconciliation and scope control

- More than 50 clients/single VM supersedes early <=10 assumptions;
  60/100-client counts, concurrency/size/headroom/latency values are proposed
  workloads/thresholds only. A two-client trial is distinct from target
  > launch. Registered/opened/concurrent/connected states are separate.
- A is the smallest technical safety trial, not an accepted 50-plus production
  topology. Choose measured automated A or implemented B. Preferred B for
  integrated advisor workflow is an inferred recommendation; C database rewrite
  remains deferred.
- Browser scope isolation is useful existing infrastructure, not business
  ownership. Stream denial is not rollback; sign-out, lock, suspension,
  offboarding and restored authorization are separate policies. Advisor app
  admission under A is broad; client-authorized export is the narrow initial
  alternative.
- Existing Decimal domain math is retained; permissive numeric helpers/CASH
  summation and live FX fallback are bounded findings. Investment file
  histories, payment transactions and holdings snapshots cannot be substituted
  for one another.
- Provenance, source identity and reconciliation proposals are deduplicated into
  PROV; safety fixes preserve current transfer/user-edit/provider mechanisms. No
  alternate accounting DB, queue or worker is proposed.
- Vault atomic persistence is optional resilience pending explicit agreement;
  historical-event recovery is an investigation before any dirty marker. Runtime
  eviction/drain/new retry mechanisms require a demonstrated failure and
  selected scope.
- DB export is distinct from installation DR; off-host recovery custody is
  necessary for a lost single VM. Shared B offline restore downtime must be
  measured. Current authoritative revocations/retention are reconciled before
  restored access.
- AGPL, trademark/dependency obligations and proprietary
  Connect/bank/market-data permissions are separate. Technical
  access/BYOK/client consent does not establish commercial entitlement or legal
  approval.
- #7/PR #12 is separately authorized localhost synthetic staging. Its
  tools/build progress and shared-host constraints are recorded as coordination
  metadata only; no staging files copied or application acceptance assumed.
  Later completed evidence can supplement the audit through review.
- Sixteen deduplicated proposals #13–#28 were created, all open
  `status:not-started`, each linked as a subissue of #1. Full
  dependency/effort/confidence/acceptance/architecture briefs are present; no
  implementation chat/branch/PR was dispatched. Existing staging scope is not
  duplicated or expanded.

## Executed validation and remaining gates

| Check                      | Result / meaning                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bank audit helper rerun    | 7/7 pass under installed Node 26.10.0; reproduces bounded current helper behavior, not named-bank support or fixes                                                                                                                                                                                                                                                                                                         |
| Security docs helper rerun | 3 documents, 56 pinned source links, 8 local links pass; documentation consistency only                                                                                                                                                                                                                                                                                                                                    |
| Architecture helper rerun  | 305 web/315 Tauri literal calls, 314 mappings/357 registrations, zero missing; 62 pinned source links/2 local links pass. Static inventory does not replace adapter Vitest or runtime parity                                                                                                                                                                                                                               |
| Consolidated docs helper   | `python3 docs/audits/2026-09-30/coordination/check-docs.py`; checks pinned source paths/ranges, local links/headings, evidence definitions, fences, >50 state, command-center exception and 16 parent-linked undispatched issues; final counts below                                                                                                                                                                       |
| Formatting                 | Standalone Prettier 3.8.1 with actual root settings, Markdown 80/prose wrap, JSON/MJS 100. Tailwind plugin omitted for these file types; no application dependency install. Original brief receives whitespace formatting only, no steering or wording change                                                                                                                                                              |
| Whitespace/scope           | `git diff --check`, staged diff check, changed-path inventory and final product diff; documentation-only scope required                                                                                                                                                                                                                                                                                                    |
| Specialist exact-head CI   | #9 [run 36717640736](https://github.com/felipebaez/wealthfolio/actions/runs/36717640736), #10 [36717463912](https://github.com/felipebaez/wealthfolio/actions/runs/36717463912), #11 [36717737667](https://github.com/felipebaez/wealthfolio/actions/runs/36717737667): formatting/detect/aggregate pass; frontend/Rust/native/translation jobs skipped. Architecture and consolidation final CI separately recorded below |

No synthesis frontend lint/types/build/E2E, Cargo/fmt/Clippy/consumer
compilation, live container/IdP/CSRF/isolation/provider-invariant/financial
performance/load/DR drill, full dependency license scan or legal approval was
run. Documentation-only work does not require application checks; their absence
prevents product guarantees. Do not count repeated worker script runs as
additional coverage or mocked CI script output as encryption validation.
Required matching tools, samples, VM workload/thresholds, policies and signed
commercial/qualified legal decisions remain launch blockers.

**Acceptance:** ten artifacts and proposal backlog are reviewable; completeness
review may accept documentation separately from those unverified launch
requirements. Issues #1–#5 and #8 stay open/In Progress while review is pending.
Completion requires accepted criteria, recorded validation and completed
closure. No continuous monitor exists.

Final consolidated local validation: 22 Markdown documents, 247 pinned source
links across 131 source paths, 52 local links/headings and 16 parent-linked
proposal records passed. All MD/JSON/MJS formatting and whitespace checks
passed. Original brief word sequence was asserted unchanged after
whitespace-only formatting. Architecture formatting correction supersedes its
earlier 76fa14c failure. Exact final architecture head
86bc13b654e6c94d3e85effb401a075977317188 passed formatting, change detection and
aggregate status in
[run 36718435502](https://github.com/felipebaez/wealthfolio/actions/runs/36718435502);
product checks were skipped. Consolidation publication revision and exact-head
CI are recorded in issue #8 and PR #6 after publication, avoiding a
self-referential commit claim.
