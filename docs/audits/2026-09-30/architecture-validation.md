# Architecture audit validation ledger

Date: **2026-09-30**. Assignment:
[issue #2](https://github.com/felipebaez/wealthfolio/issues/2). Report:
[architecture.md](architecture.md). Accepted launch target: **more than 50
clients on one private server or VM**. No real client data, bank credentials or
paid service calls were used. All commands in this lane ran with explicit
working directory
`/Users/felipebaez/Development/Wealthfolio-audits/architecture`; the primary
checkout was read only for the authorized brief/workflow.

## Coordination state

| Field                | Recorded value                                                                                                                                      |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Issue                | `2`, open, `status:in-progress`; PR review and synthesis review pending                                                                             |
| Chat                 | `01a0f24e-6909-7ec2-9daf-cb4f56346fab`                                                                                                              |
| Chat title           | `🟡-2-Audit: architecture and upstream maintenance`                                                                                                 |
| Category             | In Progress, `6573f0da-218d-4936-853c-a076264f9ef9`                                                                                                 |
| Branch/worktree      | `audit/2-architecture`, `/Users/felipebaez/Development/Wealthfolio-audits/architecture`                                                             |
| PR                   | [PR #29](https://github.com/felipebaez/wealthfolio/pull/29), open against fork `main`; exact final revision recorded in issue #2                    |
| Technical synthesis  | [Issue #8](https://github.com/felipebaez/wealthfolio/issues/8), chat `01a0f256-6938-71a1-b66a-30bd1f26609d`; owns consolidated review/index updates |
| Blockers             | Runtime reproduction/capacity tests need matching toolchain/dependencies and a synthetic runtime; no blocker to delivering documentation            |
| Last synchronization | 2026-09-30 12:56 UTC: issue reread and chat title/category synchronized; final issue comment records exact revision/checkpoint                      |
| Monitoring           | No continuous monitor configured                                                                                                                    |

This record supplements the synthesis-owned index without editing it. The human
workflow addendum was read through authenticated `gh` at
[parent comment](https://github.com/felipebaez/wealthfolio/issues/1#issuecomment-5911547424).
Issue title/body/comments/labels were read at startup and transitions; final
title/state/labels/comments were reread before handoff. Title/category
synchronization succeeded again at the final checkpoint; the issue records the
final revision.

## Baseline and environment

| Check                                                           | Observed evidence / limitation                                                                                                                                                                                                                                            |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `git status --short`, `git log -1`, `git branch --show-current` | Initially clean, branch `audit/2-architecture`, HEAD `6ee11b1278eff8b5123280e740fa6983b501952b`. No product edits authorized.                                                                                                                                             |
| Fork comparison                                                 | Authenticated `gh api repos/felipebaez/wealthfolio/compare/6ee11b1278eff8b5123280e740fa6983b501952b...main` returned identical, 0 ahead/0 behind.                                                                                                                         |
| Release comparison                                              | Authenticated fork compare of `392f272c5b15a4af45dc2ff71dcbec474f47112a...6ee11b1278eff8b5123280e740fa6983b501952b` returned ahead, 38 ahead/0 behind.                                                                                                                    |
| Release metadata                                                | Fork `/releases/latest` returned HTTP 404. v3.9.1 publication date and release commit came from supplied coordination baseline, not a fresh upstream release query in this lane. No container digest/provenance verified.                                                 |
| Node                                                            | Installed 26.10.0; `.node-version` requests 24.                                                                                                                                                                                                                           |
| Package manager                                                 | Installed pnpm 11.19.0; root manifest requests 10.33.4; Dockerfile explicitly installs 9.9.0. Local pnpm warns root `pnpm.overrides` is ignored.                                                                                                                          |
| Rust                                                            | `command -v cargo` found no executable on PATH. `rust-toolchain.toml` requests 1.98.1 with rustfmt/clippy. No Rust tests/compilation run.                                                                                                                                 |
| Containers                                                      | `command -v docker` found no executable on PATH. No container/server boot, image build or deployment run.                                                                                                                                                                 |
| JS dependencies                                                 | Fresh worktree had no complete dependency setup. Attempted pnpm exec triggered an automatic install and was interrupted. Cache/partial ignored dependency artifacts may remain; no tracked manifest/lockfile changes were observed. No broad tool installation attempted. |
| External research                                               | Official Git, SQLite and Wealthfolio Connect pages accessed 2026-09-30. Product statements are attributed, not independently verified remote-service guarantees.                                                                                                          |

Metadata is a dated observation, not a guarantee that branches/releases remain
unchanged later. All source links in the report pin the audited SHA.

## Executed checks

| Command/check                                                                        | Result                                                                                                                                                                                                                                                                       | What it establishes                                                                                                                                   |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `node --test scripts/tauri.test.mjs`                                                 | **Passed: 4 tests, 0 failures** in this assigned worktree, Node 26.10.0                                                                                                                                                                                                      | Launcher config/identity/exit forwarding behavior covered by those tests. Not app compilation, desktop startup, encryption, bank support or security. |
| `pnpm --filter frontend exec vitest run src/adapters/adapter-command-parity.test.ts` | **Did not run.** pnpm 11 automatically started dependency installation/resolution; interrupted with SIGINT, exit 130.                                                                                                                                                        | No Vitest pass/fail result. The dependency side effect is recorded, not represented as a compliant frozen-lock install.                               |
| `git status --short`, `git diff -- pnpm-lock.yaml package.json` after interruption   | **Passed inspection: no tracked product/lockfile changes**                                                                                                                                                                                                                   | Scope preserved. Does not prove complete dependency setup or clean global cache.                                                                      |
| `node docs/audits/2026-09-30/architecture/check-source.mjs`                          | **Passed:** 305 web literal calls, 315 Tauri literal calls, 314 mapped commands and 357 registrations, zero missing; 62 pinned links and two local links validated. An initial run before this ledger existed correctly failed its local-link check; the final rerun passed. | Dependency-free static inventory and documentation source path/line/reference checks. No runtime DTO, auth, event or network behavior.                |
| Isolated Prettier 3.8.1 formatting/check                                             | **Passed locally**; initial CI identified two documents formatted at width 100 because overrides resolve relative to the nested config. Corrected the parent-document glob and reformatted all five files; final CI result recorded in issue #2                              | Formatter fetched into npm exec cache; no project dependency install or product lockfile edit. Full repository format job not run.                    |
| Final `git diff --cached --check`, scoped diff/status review                         | **Passed** on all five staged, owned documentation/auxiliary files; no product paths included. Rechecked after coordination update.                                                                                                                                          | Whitespace and owned documentation scope. No product behavior guarantee.                                                                              |

The audit helper reads adapter source and uses the same general
literal-call/registration patterns as the existing parity test. It omits
test/spec files and scans feature-local adapter directories. It is deliberately
**not a replacement for Vitest**: regex cannot validate runtime exports,
aliased/dynamic calls, handler routing, payload compatibility or authorization.
It checks each commit-pinned documentation source path through `git show`, line
bounds, local Markdown links and evidence references. It does not check remote
page availability or assert that an entire claim is proven merely because a link
exists.

No product test was added. The helper is an auxiliary
documentation/investigation artifact, requiring only Node and Git.

### Reproduce the static observations

Run from this audit worktree/repository root; each command is independent:

```sh
node --test scripts/tauri.test.mjs
node docs/audits/2026-09-30/architecture/check-source.mjs
git diff --check
git log --oneline 392f272c5b15a4af45dc2ff71dcbec474f47112a..6ee11b1278eff8b5123280e740fa6983b501952b
git log --format= --name-only 392f272c5b15a4af45dc2ff71dcbec474f47112a..6ee11b1278eff8b5123280e740fa6983b501952b
```

For the report's path-frequency observation, count occurrences of each nonempty
path in the last command's output. It counts commits touching the path, not line
churn. The two asset paths each occurred 11 times, activity service and quote
client six each, profile shell/auth context five each.

## Source traces completed

| Flow                    | Source entry points inspected                                                                                                                                       | Status                                                                                  |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Runtime composition     | Vite aliases/shared platform; web `COMMANDS`; Tauri command registry; server `main_lib.rs`; native `context/`, `profiles.rs`                                        | **Confirmed source trace**, not both runtime builds.                                    |
| Login/profile admission | Frontend profile API/immutable session, server auth/OIDC/profile router/admission, core registry/sessions                                                           | **Confirmed source trace**, no IdP or concurrent-browser reproduction.                  |
| Portfolio read          | Shared portfolio adapter → web holdings handler / Tauri portfolio command → PortfolioService/HoldingsService → snapshots/quotes/FX                                  | **Confirmed source trace**, no synthetic portfolio response exercised.                  |
| Activity create/import  | Web/native activity entry points, Rust byte parser, frontend review mutations/mapping context, core import/create/idempotency, repository `exec_tx`                 | **Confirmed source trace**, no bank sample or runtime import.                           |
| Holdings/performance    | Snapshot/holdings calculator, valuation service, runtime job worker/planner, performance service/quality/solver                                                     | **Confirmed source trace**, no numerical correctness certification.                     |
| Sync/events             | Web/native domain sinks/queue workers, broadcast/SSE bridge, broker scheduler/orchestrator, device engine/crypto/outbox                                             | **Confirmed source trace**, no actual cloud requests, timer soak or failure injections. |
| Export/backup/restore   | Shared formatter; web data/snapshot/portable exports; offline server restore; shared maintenance; native restore/profile lifecycle                                  | **Confirmed source trace**, no file recovery operation performed.                       |
| Optional integrations   | Built-in/custom market providers, Connect settings/build guide, AI catalog/chat loop/tools, MCP PAT/scopes, addon iframe/network validation, institution image URLs | **Confirmed source inventory**, not exhaustive packet/retention/permission audit.       |

Formatting used
`npm exec --yes --package=prettier@3.8.1 -- prettier --config docs/audits/2026-09-30/architecture/format-config.json`
with `--write` then `--check` on owned files only. Markdown overrides include
`../*.md` because patterns resolve from the nested config directory; the initial
`**/*.md` glob missed the parent report/ledger. GitHub formatting failed on
initial handoff revision `76fa14c23bd67bd4bfaf8f1b70887f5c922ef4fb`; the
corrected configuration and formatting replace that handoff. The final issue
comment identifies the replacement revision and CI result. This narrowly scoped
formatter is distinct from the aborted project dependency installation.

Source-level contradictions are recorded in ARCH-05 (package manager), ARCH-09
(adapter docs/actual files and restore difference), and the report's
product-marketing distinction (household/coming-soon features vs server client
authorization). No unrelated code/docs were corrected.

## Architecture invariants: inspected versus tested

| Invariant required by AGENTS.md                | Source evidence                                                                                                                                                         | Executed guarantee / remaining work                                                                                                                                          |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Disabled providers receive no requests         | QuoteService filters enabled configs before constructing MarketDataClient; client builds only those configs; tests cover preferred disabled-provider behavior.          | **Not runtime-tested here.** Spy/mocked transports should cover startup, preview, explicit preference, scheduled sync, fallback and restore.                                 |
| Local resolution has no new network dependency | ResolverChain uses overrides and deterministic rules; holdings live read gets local quote pairs and FX. Import preview is a separate provider-capable path.             | **No changes made**, source boundary traced. No packet-capture or runtime request-count guarantee.                                                                           |
| Provider failures remain isolated              | Provider registry/circuit breaker/rate policy and worker error/complete events; market failure handling proceeds through existing job logic.                            | **Not tested here.** Inject one-provider/entire-provider failure and verify unaffected inputs remain available, quality/errors are honest and no cross-client contamination. |
| Enrichment preserves user edits                | AssetService rereads current asset after awaited fetch, checks identity/mode/provider config, fills missing data; existing tests exercise concurrent edit preservation. | **Not run here.** Shared backend change needs focused asset tests, both runtime consumers and sync/restore coverage.                                                         |
| Writes and outbox use same transaction         | Repository `exec_tx`, projected outbox flush and writer commit observer inspected. Domain notifications are separate.                                                   | **Not runtime-tested here.** Database/outbox tests require Cargo and `CONNECT_API_URL=http://test.local`.                                                                    |
| Admission binds work to original profile       | Owner/scope grant, fixed request AppState, response/stream rechecks, native context capture, frontend immutable session.                                                | **Not runtime-tested here.** Does not establish durable client ownership or role policy.                                                                                     |
| Private data not logged                        | Source contains malformed performance response serialization and broker account name logging (ARCH-06).                                                                 | **No guarantee; contrary paths confirmed statically.** Synthetic log capture needed, no real financial data used.                                                            |

## Focused failure recipes awaiting runtime prerequisites

These recipes deliberately use synthetic finance/identity data. They are
acceptance proposals, not executed reproductions or claimed fixes.

### ARCH-02: live FX substitution

1. Create a synthetic CZK-base profile with 100 EUR cash and a EUR security
   position, no EUR/CZK, inverse or cross rates, and an empty currency
   converter. Use locally supplied quotes; disable providers.
2. Read live holdings, totals and holdings export on web and Tauri. Trace the
   cash/security `get_fx_rate_or_fallback` calls; source currently returns
   `Decimal::ONE` on lookup error and assigns `Some(1)` to holding FX.
3. Verify a known synthetic rate (e.g. 25 CZK/EUR) yields 2,500 CZK for the cash
   control; then verify missing FX cannot present 100 CZK as a verified
   conversion after any selected fix.
4. Verify no network requests are added to a holdings read. Validate
   representation in UI, aggregated totals, export and historical quality
   separately; historical FX behavior is not assumed identical to live fallback.

Source confirmation does not prove how every UI currently displays the result.
No numerical runtime result was produced.

### ARCH-03: commit/event interruption

1. Seed a synthetic transaction account with existing snapshots and daily
   valuation rows.
2. Edit an old transaction/date and interrupt after repository commit before
   domain-event emission or worker processing. The 500 ms event debounce is not
   itself a guaranteed deterministic injection point; use a controlled test
   hook/mock in a future test, not timed production termination.
3. Restart; inspect latest/historical holdings/valuations and compare to
   explicit full rebuild. Test normal reopen, failed provider refresh and
   transfers/manual snapshots separately.
4. If existing mechanisms recover, narrow/retire the finding. If not, document
   the exact recovery gap before designing a transactional dirty marker in the
   current writer path. Do not equate device-sync outbox durability with domain
   recalculation durability.

### ARCH-04: provenance failure

1. Inject failure in import-run create; import two valid synthetic rows through
   the existing service. Inspect activities/run IDs/summary and separate failure
   diagnostics.
2. Independently fail final run summary update after successful insertion;
   verify stale/incomplete run state and returned result.
3. Include two-account files, skipped row policy, duplicate preview/reimport,
   force import and transaction failure. The present source permits best-effort
   run metadata; proposed required provenance is a product decision.

### ARCH-01/06/07/08: delegated consolidation checks

- Identity/isolation: two different synthetic IdP subjects, fixed profile IDs,
  forged/stale/revoked selectors and streams; backend client/advisor/operator
  grants after topology decision. Installation login success alone is
  insufficient.
- Logging: malformed synthetic performance payload with amounts and missing
  scope ID, plus a synthetic `NOT_SET` broker account name. Capture
  frontend/native/server logs; assert selected nonfinancial diagnostic policy.
- Capacity: 60/100 registered clients, opened/runtime/connected/concurrent
  counts separately, agreed active workload and activity-history sizes, 24-hour
  timer soak, restart bursts and reserved VM resources. Report measured
  percentiles/RSS/CPU/disk/connection/queue counts; no estimated capacity is
  presented as observed.
- Recovery: restore one synthetic client and full registry/vault/key set;
  compare neighbor availability (A vs shared B offline outage), retained manual
  inputs and revoked PAT behavior. Select RPO/RTO before judging pass. No real
  data or destructive operation is authorized by these recipes.

## Checks not run and prerequisites

| Check                                         | Reason / later required scope                                                                                                                                                                                                                  |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Full Vitest and adapter parity                | Incomplete worktree dependencies, wrong pnpm/Node; aborted auto-install. Use Node 24/pnpm 10.33.4 and explicitly reviewed `pnpm install --frozen-lockfile` first.                                                                              |
| `pnpm check`, `pnpm type-check`               | No complete dependencies; not required for documentation-only app scope. Build declarations before standalone checks; `type-check` includes this.                                                                                              |
| `pnpm build`, `pnpm build:tauri`              | No complete dependencies; not required for documentation-only change. Both required for future runtime wiring/shared bundle changes.                                                                                                           |
| Focused Rust tests / fmt / Clippy / consumers | Cargo absent on PATH. Future shared backend checks: focused crate tests; `cargo fmt --all -- --check`; affected-crate Clippy; `cargo check --locked -p wealthfolio-app -p wealthfolio-server`. Tauri assets/system dependencies also required. |
| E2E/client isolation/import/browser flow      | No runtime/browser setup; consult `.claude/skills/run-e2e-tests/SKILL.md` and `e2e/README.md` before running selected suite. No dev server used as build evidence.                                                                             |
| Docker build/VM workload/recovery             | Docker absent; hardware/VM access and objectives unspecified. Do not install a container platform or claim a running deployment.                                                                                                               |
| Banks/Connect/market provider/remote AI       | No real data/credentials or contracts used. Synthetic fixtures do not prove institution support or paid-provider compatibility.                                                                                                                |
| Full CI/source HEAD or image attestation      | Coordination reported Warm Rust Cache at source HEAD, not full CI. That cache run and other worker launcher/Python tests are not this lane's full runtime assurance. Documentation PR checks, if available, are reported separately.           |

The findings are **not verified fixes**. All implementation is deferred; review
can approve documentation completeness while runtime, security, capacity and
bank-compatibility gates remain unresolved.
