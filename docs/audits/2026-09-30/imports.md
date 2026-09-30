# Czech import pipeline audit

Audit date: 2026-09-30. Assignment:
[issue #4](https://github.com/felipebaez/wealthfolio/issues/4), under
[parent #1](https://github.com/felipebaez/wealthfolio/issues/1). Companion:
[bank/product evidence](banks.md).

**Recommendation — inferred:** start with reviewed file imports for a small set
of verified bank/product/export variants. Reuse the existing CSV parser,
templates, transaction profile, shared activity service, SQLite writer and
change events. Before advertising named bank compatibility, preserve parser
diagnostics and bank record identity, enforce statement reconciliation, and
validate against representative exports. A general CSV importer is useful
infrastructure; it is not proof that any Czech institution is supported.

**Architecture impact:** documentation and audit-only reproductions. No
application network calls, provider settings, execution timing, storage, events,
retries, user-edit precedence or ownership boundaries changed. Proposed
implementation below requires a later human-selected direction. No new worker,
queue, database or migration is approved.

## Baseline and method

**Confirmed:** this worktree's initial HEAD and branch were
`6ee11b1278eff8b5123280e740fa6983b501952b`, `audit/4-banks`; local `main` and
`upstream/main` resolve to that SHA, divergence `0/0`. Authenticated
`gh api repos/felipebaez/wealthfolio/commits/main --jq .sha` returned the same
SHA. This verifies the fork and local upstream reference, not a new live fetch
of upstream. Source manifests are 3.9.2; published v3.9.1 at
`392f272c5b15a4af45dc2ff71dcbec474f47112a` is the coordination baseline, not a
source or container equivalence claim. All repository evidence below is pinned
to the source SHA.

Read root AGENTS.md in this worktree, and the orchestrator-owned brief/workflow
from the primary checkout read-only. Traced parser, frontend drafts, both
adapters/runtimes, shared validation/apply, storage and financial flow
classification. External evidence is in banks.md. Only synthetic strings were
executed. No bank account, consent, paid API, real statement, application
runtime or production database was used.

## Actual execution path

| Stage                   | Confirmed source behavior                                                                                                                                                                                                                                                                                 | Boundary / consequence                                                                                                                                                                                                                                                             |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Upload and parse        | [Upload step][upload] invokes `parseCsv`; [web adapter][webparse] submits file/config multipart using `profileFetch`, while [Tauri adapter][tauriparse] reads bytes and invokes `parse_csv`.                                                                                                              | Web files reach the self-hosted server; desktop parsing is through the local command. Neither parser inherently needs a bank or market-data API. Tenant admission is a dependency on the security audit.                                                                           |
| Runtime wiring          | [Web activities router][api] exposes `/activities/import/parse`, `/check`, `/assets/preview`, `/activities/import` and template/mapping routes. [Web command mapping][webcore] maps shared invocations; [Tauri commands][tauri] call the profile context and [registration][registration] registers them. | Existing runtime paths should both be extended and covered by adapter parity tests. Parsing is a runtime-specific operation, not a shared `invoke` alias in web.                                                                                                                   |
| CSV bytes               | [Core parser][parser] detects BOM, then valid UTF-8, then chardetng legacy encoding; supports comma, semicolon, tab, quoting, configurable headers and top/bottom skips. Records remain strings. It returns recoverable `errors` separately from rows.                                                    | Encoding detection is heuristic and no explicit encoding override exists in `ParseConfig`. Numeric/date options are carried to the frontend, not applied by this Rust byte parser.                                                                                                 |
| Templates and mapping   | [Mapping hook][mapping] auto-maps mostly English aliases; [template models][models] persist field/activity/symbol/account mappings and parse settings. [Transaction profiles][profiles] disable asset resolution for cash/card imports, restrict fields and activity types.                               | Prefer an existing template when verified file fields map directly. Czech headers can be manually mapped; Czech aliases and variant recognition need tests. No verified Czech template or bank export fixture was identified in the traced importer.                               |
| Drafts                  | [Draft utilities][drafts] read selected fields, normalize date and numbers, map types, resolve accounts and produce row errors. [Account matching][accounts] refuses ambiguous matches and preserves explicit account mappings.                                                                           | Account matching is by app ID/name/accountNumber after case/whitespace normalization; it does not convert Czech local account numbers to IBAN. Do not turn unknown accounts into silently chosen client accounts.                                                                  |
| Review                  | [Import context][context] tracks draft revisions, backend validation, errors/warnings and asset preview. [Confirmation][confirm] follows review; [mutation hook][mutations] calls shared `importActivities` and invalidates activity/import-run, spending and performance caches.                         | The UI offers preview before commit and revalidation after edits. That is not an enforced server-side receipt proving the user reviewed a particular file. No new receipt mechanism should be added without identifying the necessary threat and reviewing existing authorization. |
| Backend check           | [Shared adapters][shared] invoke `check_activities_import`; [core activity service][service] validates per account, normalizes, resolves assets in preview, identifies DB/batch duplicates and returns row issues.                                                                                        | “Read-only preview” means it avoids committing activities/assets/FX pairs; it is not evidence of zero outbound requests for investment resolution. Inspect provider behavior in the selected pilot configuration.                                                                  |
| Apply                   | [Core apply][apply] rechecks account/date/resolved identity and account-policy constraints, partitions duplicates, links eligible transfers, ensures FX pairs, creates an import run and calls `create_activities`.                                                                                       | Apply rejects missing resolved security fields, but may create prepared assets, manual quotes or FX pairs. The adapter's “persistence-only” comment should not be interpreted as “no other side effects.”                                                                          |
| Persistence and events  | [SQLite repository][repository] validates records and inserts all insertable activities with `writer.exec_tx`; the [schema migration][schema] has a unique non-null idempotency index. Apply emits activities/split changes after insertion.                                                              | Activity insertion is transactional; import-run creation/finalization is separate and best effort. Asset/FX preparation is outside that activity transaction. Events drive derived financial recalculation. No blanket whole-import atomicity claim is justified.                  |
| Other import surfaces   | [MCP import tools][mcptool] let an agent map rows, prepare them, then commit through check → apply. Commit's description requires user confirmation; scope/access checks are separate. [AI CSV tool][aitool] is another import entry point.                                                               | The MVP must explicitly choose whether these remain available. They cannot be assumed to preserve the UI's exact parsing, decimal, provenance or preview guarantees. MCP's mapped numbers are `f64`.                                                                               |
| Automatic broker ingest | [Connect client][connectclient], [broker service][brokerservice], [pagination][pagination] and [core adapter][brokeradapter] provide cloud-backed broker orchestration and existing ingest extension points.                                                                                              | Existing provider defaults to SnapTrade. A comment mentioning Plaid in an import-run enum is not a working Czech bank connector. No live Connect institution catalog or Czech bank coverage was verified.                                                                          |

## Findings register

Severity is relative to a hosted financial-advisory pilot: **high** risks silent
financial misstatement or an unsupported launch promise; **medium** creates
repair/audit problems. “Confirmed” describes inspected code or executed isolated
helper behavior. It does not imply an end-to-end application reproduction. No
product fixes were made: **fix not verified** for every proposed remedy.

| ID / severity / status                                                          | Affected paths and evidence                                                                                                                                                                                                                                                                                                                                                                | Verification / reproduction                                                                                                                                                                                                                                                                                                                            | Impact and proposed action                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IMP-01 / high / confirmed                                                       | [Parser][parser] returns encoding/parse/structure diagnostics. [Upload][upload] success and reparse handlers dispatch only `headers`, `rows`, `detectedConfig` and clear local parseError; [mapping reparse][mappingstep] also omits diagnostics; [context][context] has no parser-error state.                                                                                            | Follow `parseCsv` → `onSuccess` at upload lines 799–806 and `SET_PARSED_DATA`. Parser uses `had_errors` and records failed records without throwing the entire parse. Static trace; malformed-file runtime not run.                                                                                                                                    | Partial rows or replacement characters may proceed to review without source diagnostics. Preserve the existing error list and original source row/record identity in the existing wizard. Block commit for unresolved structural/encoding damage, distinguish warnings from accepted omissions, and test every reparse path. A valid subset must not look like a complete statement.                                                                                         |
| IMP-02 / high / confirmed omission; collision impact inferred                   | [ActivityImport][models] has no bank record/reference, booking/value-date pair, counterparty or Czech payment-symbol fields. `From<ActivityImport> for NewActivity` assigns `source_system=CSV`, `source_record_id=None`. [Fingerprint][fingerprint] hashes account, day, type, asset, quantity, price, amount, nonzero fee, currency and notes; [apply][apply] drops DB/batch duplicates. | Two genuinely different bank payments with all hashed fields equal on the same day have the same key; a changed description on an overlapping export changes the key. Source trace establishes this deterministically; storage execution not run.                                                                                                      | Semantic dedupe can drop legitimate equal payments or import a duplicate after textual differences. Reuse persisted source identity fields and existing ingest matching before adding schema. Preserve authentic stable bank references where available; absent references require an explicit occurrence-aware overlap/reconciliation policy, not file-row number or variable symbol as a universal ID. Keep deliberate force-import separate and explain its consequences. |
| IMP-03 / high / confirmed helper behavior                                       | [Numeric helper][numeric] removes nonnumeric characters and joins repeated decimal separators; `thousandsSeparator=none` still removes the opposite separator. [Holdings utility][holdings] sums CASH entries with `parseFloat` and serializes binary addition.                                                                                                                            | Audit-only `node --test docs/audits/2026-09-30/banks/numeric-audit.test.mjs`: `1foo2` → `12`; `1,2,3` → `12.3`; `0.1 + 0.2` CASH expression → `0.30000000000000004`. Seven assertions passed, including valid Czech-style separator and precision-string checks. CASH check executes the exact arithmetic expression, not the whole holdings function. | Bank input must fail clearly when its format is malformed or ambiguous. Valid activity values largely remain decimal strings before Rust Decimal conversion; do not incorrectly describe the whole importer as floating point. Add strict variant-specific numeric validation and decimal aggregation in the owning existing utilities/core boundary. Ensure fees/tax and final cash follow established economics; never recompute exact source money with floats.           |
| IMP-04 / high / inferred gap with confirmed model limits                        | [CSV config/result][parser], [ActivityImport][models], [apply][apply] and [import-run model][run] contain no statement opening/closing balance contract or reconciliation gate in this flow. The frontend “reconcileExpenseReversalBoundary” function concerns flow semantics, not statement balances.                                                                                     | Search/read the traced upload → draft → check → apply path for balance totals and currency-specific statement checks; none found. This is bounded source evidence, not a claim about all application reconciliation features.                                                                                                                          | A syntactically valid partial statement may be accepted. Reuse existing Decimal economics and run model; require opening + booked signed movements = closing per account/currency/period with explicit rounding policy before calling a statement reconciled. Partial history files lacking balances must be labeled unreconciled. Holdings snapshots must not masquerade as trades or performance history.                                                                  |
| IMP-05 / medium / confirmed                                                     | [Apply][apply] creates one import run using the first account, tolerates run creation failure, then inserts activities; run completion also warns on failure. [Run model][run] has checkpoints/summary but CSV apply does not persist file digest, template version or statement identifier.                                                                                               | Inspect steps 7, 9 and 10 in apply. Multi-account CSV can link rows to the first account's run. No failure injection executed.                                                                                                                                                                                                                         | Existing run metadata is insufficient for a strong source trail and complete per-account repair history. Define needed provenance first, extend existing metadata/checkpoints and choose per-account runs or a documented aggregate model. A persistence change requires failure/restore/offboarding tests and an explained need; audit alone does not authorize a migration.                                                                                                |
| IMP-06 / high / inferred misclassification risk; existing protections confirmed | [Draft mapping][drafts], [transfer linking][transfers], [performance flow classifier][flows] distinguish deposits/withdrawals, interest/fees/tax, credit reversals and transfers. Standard auto-pairing uses same date/currency/symbol/amount and only the submitted insertable batch.                                                                                                     | Read `link_imported_transfer_pairs`; inspect same-account FX opt-in requirements. No bank export, cross-period import or full performance run tested.                                                                                                                                                                                                  | “All positive amounts = income” would distort advisory reports. Require explicit reviewed operation mappings; preserve sign until type selection. Match own-account transfers using bank evidence and user intent, including transfers booked on different days or imported separately. Reuse existing linking UI/service for ambiguous or cross-batch pairs. Do not turn every bank payment into BUY/SELL or infer investment gain from incoming proceeds.                  |

## Czech parsing and financial semantics requirements

The following are **proposed acceptance criteria**, not verified bank schemas.
Sample-specific availability remains unknown as listed in banks.md.

| Concern                        | Current support / limit                                                                                                 | Required pilot behavior and test                                                                                                                                                                                                                                                                                                                             |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| CZK / foreign currencies       | String currency columns/default and core Decimal/FX support exist.                                                      | ISO currency validation, account and transaction currency shown separately; retain original/instructed currency and bank FX when present. Reconcile each currency folder independently; no guessed CZK conversion from symbol text.                                                                                                                          |
| Czech headers / diacritics     | Raw strings and manual mapping work; aliases largely English.                                                           | Keep exact headers and decoded values, map Czech aliases only from real samples. Test Unicode normalization without stripping diacritics from persisted text. Reject ambiguous duplicate headers.                                                                                                                                                            |
| Encoding                       | UTF BOM/UTF-8/heuristic legacy decoding implemented. No explicit override.                                              | Verify actual bytes per product; do not assert Windows-1250 or ISO-8859-2 bank support without evidence. Test damaged bytes and short files, expose selected encoding/uncertainty and diagnostics. Consider an override only where verified exports require it.                                                                                              |
| Delimiters / quotes / grouping | Semicolon/tab/comma and quoting supported; auto-detection counts raw separators in first ten lines.                     | Explicit template delimiter for verified variants; quoted delimiters, multi-line notes, preambles, trailing summaries and CSV BOM tests. Validate decimal comma, dot/space/NBSP grouping under a fixed declared format; malformed separators must give row/field errors.                                                                                     |
| Dates                          | [Date presets][dates] include `DD.MM.YYYY`; [drafts][drafts] parse explicit format then fall back and serialize to ISO. | Choose booking date for posted cash ledger; preserve value date as provenance. Keep date-only bank values stable across Prague/São Paulo/UTC and DST, reject ambiguous day/month cases rather than relying on browser timezone. Existing frontend `toISOString()` introduces a timezone boundary that needs verification.                                    |
| IBAN / local account / symbols | App-account matching exists; no structured CSV counterparty/symbol fields.                                              | Preserve local prefix/account/bank code, IBAN and VS/SS/KS as strings including zeros. Only owner-side account identity maps to an app account; counterparty must not select the destination client. Variable/specific/constant symbols are not guaranteed transaction IDs.                                                                                  |
| Pending / booked / reversals   | Core has draft/posted status and credit/reversal semantics. CSV status/record lifecycle is not a bank connector.        | MVP commits booked entries only. Pending items must be excluded with counts or remain explicitly nonposted; never double-count pending then booked. Preserve reversal relationship where authentic source provides it, handle interest and fee/tax rows distinctly.                                                                                          |
| Transfers                      | Transfer types, boundary metadata, pairing and flow classifier exist.                                                   | Own tracked accounts produce internal flows with correct per-account cash effects and zero false portfolio income/gain. Untracked counterpart or ambiguous transfer requires explicit choice. Test same/different dates, currencies, split files, fees and duplicate-skipped legs.                                                                           |
| Investments                    | Trade/ISIN/quantity/price/fee/tax fields, asset preview and holdings mode exist.                                        | Accept a trade only with verified transaction evidence; preserve instrument identity, settled quantities, trade currency, charges and tax. Review fund switches, dividends/reinvestments and security transfers. A holdings statement gives a dated snapshot, not purchase history, acquisition cost or realized returns unless those are actually supplied. |

## Where proposed importers belong

**Inferred:** a KB+ business CSV, RB verified CSV variant or George
selected-field export should start as an existing mapping template when no
preprocessing is required. Template selection must validate the expected variant
and required fields; a CSV extension alone is insufficient. Shared core/owning
importer logic handles deterministic validation, source identity and
reconciliation that must hold across web, Tauri and other callers.

ČSOB structured CEB formats, KB GPC/BEST/XML and RB ABO/Gemini/XML need a
dedicated local format parser producing the same reviewed domain rows. An XML or
fixed-width format cannot be made supported by renaming it `.csv` or adding a
mapping. Implement only the verified demanded format, in the existing import
domain; avoid a generic framework or new service. PDF/OCR is deferred: manual
approved conversion or a later format-specific extraction workflow needs its own
accuracy and privacy decision.

An add-on can distribute a deterministic local converter/template where its
sandbox and file/network permissions meet the tenant model. It must not bypass
core validation, duplicate checks or preview. Add-ons alone cannot provide bank
contractual access, safely own arbitrary server credentials or fix core
provenance. Automatic bank access belongs in a connector: explicit per-client
authorization, secrets, checkpoints, bank pagination and consent/certificate
renewal. Reuse existing ingest/run/writer/events where appropriate; do not route
payment data through SnapTrade merely because it is the existing default.

## Proposed backlog and phases (pending human direction)

Estimates are engineering person-days for an experienced contributor after
prerequisites, not promises or bank/legal waiting time. Confidence applies to
scope/estimate, not current bank compatibility. Every item depends on the parent
security decision before real-client testing.

| Candidate                                                                 | Dependency / effort / confidence                                                                                                          | Acceptance criteria                                                                                                                                                                                                                                                              | Validation and architecture impact                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| BANK-01 — identify pilot products and obtain authorized sanitized exports | Business selection; 2–4 days analysis once samples exist; medium. External blocker: none received.                                        | Product/channel/tariff/format/export settings/version recorded for each sample; headers/encoding/layout preserved; independent expected row counts, money/date values and balances; overlapping exports and repeated equal payments included. Unknown support stays unknown.     | Private intake under approved handling, synthetic replacements before repository use; no source/network changes.                                                                                                                                                                                                                                    |
| IMP-07 — retain parser diagnostics and reject damaged input               | Independent of named bank formats; 2–4 days; high.                                                                                        | Errors and original source row positions survive all reparse/template flows; no unresolved structural/encoding damage reaches commit; skip counts explicit.                                                                                                                      | Focused parser/UI regression tests and flow test, lint/types; adapter parity/both builds if payload contract changes. Reuses parser/error state, no new network or worker.                                                                                                                                                                          |
| IMP-08 — strict money/date normalization                                  | BANK-01 for bank variants; 3–6 days; medium.                                                                                              | Decimal strings and exact CASH aggregation; damaged/mixed separators fail visibly; date-only values stable across tested timezones; fees/tax consistent with final-cash model.                                                                                                   | Helper and core boundary tests with large/high-precision/zero/negative/space/NBSP/invalid values and DST; both frontend types and affected Rust checks. No optional parser engine or currency storage change.                                                                                                                                       |
| IMP-09 — bank provenance and safe repeat import                           | BANK-01 and tenant/account ownership; 5–10 days; medium.                                                                                  | Stable source refs survive mapping → backend → SQLite; same file and overlapping file repeats add zero duplicate booked events; distinct equal payments retained; description edits, reversal and force-import policies documented; provenance sufficient for per-account audit. | Real-shaped sanitized fixtures plus synthetic collisions; concurrent duplicate writes; preservation of user edits and profile isolation; runtime wiring/storage tests. Extend existing source fields/run metadata first. Migration only if specific required metadata cannot fit existing ownership/contracts.                                      |
| IMP-10 — statement reconciliation and transfer review                     | IMP-08/09; 5–10 days; medium.                                                                                                             | Opening + movements = closing by account/currency; mismatch/partial/unavailable balances explicit; ambiguous own-account transfers reviewed; no transfer classified as investment gain; imports remain attributable.                                                             | Dropped-row/duplicate/multi-currency/fee/interest/reversal/split-period fixtures; holdings/performance integration checks and UI flow. Extend existing service/run/events. No separate accounting database approved.                                                                                                                                |
| BANK-02 — first verified CSV template, then bank/product variants         | BANK-01, IMP-07/08/09/10; 2–4 days per simple variant; medium.                                                                            | Exact supported product/channel/settings/version documented; verified expected results, preview and repeat-import behavior pass; unsupported file variants rejected clearly.                                                                                                     | Tests against each representative shape; focused wizard E2E after reading E2E setup skill/README. Reuses templates; no external financial-data flow.                                                                                                                                                                                                |
| BANK-03 — verified investments/snapshots or non-CSV format                | Product samples and BANK-02 shared guarantees; 4–10 days per structured format, 3–6 per straightforward investment CSV; low until sample. | Holdings versus trades clearly separated; verified identifiers, quantities, fees/taxes; snapshot cannot imply reconstructed performance; PDF/OCR requires a separate decision.                                                                                                   | Golden parsing/domain outputs and monetary/position reconciliation; provider-disabled no-request tests. Local owning parser/add-on candidate, no new cloud extraction.                                                                                                                                                                              |
| BANK-04 — automation access/privacy decision record                       | Business privacy choice and qualified legal review; 3–5 days analysis excluding external approval; medium.                                | Bank-by-bank product/retail eligibility, production rights, exact rate/history/page/renewal constraints, DPA/retention/hosting and current aggregator onboarding verified; read-only scope only.                                                                                 | Review official current contracts/specs after authorized access. No registrations, calls with client consent, purchases or vendor contact authorized by this audit.                                                                                                                                                                                 |
| BANK-05 — one read-only connector pilot                                   | BANK-04, IMP-09/10 and tenant-isolation checks; 10–20 days plus external onboarding; low.                                                 | Client-bound callback/state/secret ownership, booked-only import, correct pages/checkpoints, retry/rate handling, renewal/revocation/offboarding, zero payment scopes; file fallback retained.                                                                                   | Synthetic bank responses: 429/5xx, partial pages, 204, repeated pages, revoked tokens, expired certificates, stale callback and concurrent clients. Reuse broker ingest/run/events but keep new bank calls opt-in. Explain any new persisted checkpoint/retry needed to avoid missed/duplicate history; existing orchestration may already suffice. |

**Phasing:** (1) select products and evidence; fix shared accuracy gaps; (2)
certify one CSV variant, then expand by measured client demand; (3) separately
assess investment and structured formats; (4) choose lawful read-only
connectivity and test one bank/provider. Do not make automatic connectivity or
payment initiation part of file-import acceptance. Avoid four parallel bank
parsers before common correctness work.

## Verification record and limitations

- **Passed:** seven audit-only Node assertions in
  [numeric-audit.test.mjs](banks/numeric-audit.test.mjs), on Node 26.10.0. Six
  execute the extracted real baseline numeric helpers via Node's experimental
  type stripping; the seventh checks/exercises the CASH arithmetic expression.
  This is diagnostic reproduction, not a replacement for repository Vitest, Rust
  or E2E checks. The assertions intentionally establish current permissive
  behavior, not desired behavior.
- **Passed:** `node --test scripts/tauri.test.mjs`, four wrapper tests in this
  worktree. This is not import, security, build or bank coverage validation.
- **Not run:** focused
  `pnpm --filter frontend exec vitest run src/pages/activity/import/utils/review-draft-utils.test.ts`.
  Installed pnpm 11.19.0 unexpectedly auto-installed dependencies then exited on
  ignored build scripts before test execution. Its changes to pnpm-lock.yaml and
  pnpm-workspace.yaml were restored to the clean starting baseline. Ignored
  node_modules from that attempt remain local, uncommitted. No build scripts
  were approved; no further pnpm test attempt was made.
- **Not run:** Rust parser/service/storage tests, fmt/Clippy and server/Tauri
  compile: cargo absent on PATH. Docker absent. Node/pnpm differ from repository
  requirements (Node 24 / pnpm 10.33.4). No broad system tool installation
  attempted.
- **Not run:** full frontend tests/type-check/builds or E2E; no product files
  changed and the environment is not established with requested
  toolchain/browser/server prerequisites. Documentation verification is
  path/line checks, formatting and diff review, recorded in the PR.
- **Unknown:** real export schemas, availability of fields/stable references and
  named importer accuracy, bank/aggregator production access, full
  balance/performance correctness and tenant enforcement at runtime. Source
  invariants (disabled providers receive no requests, failures isolated, user
  edits preserved) require the future integration tests; this audit does not
  claim they passed.

## Evidence links

[upload]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/steps/upload-step.tsx#L799
[webparse]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/adapters/web/activities.ts#L38
[tauriparse]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/adapters/tauri/activities.ts#L9
[api]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/api/activities.rs#L395
[webcore]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/adapters/web/core.ts#L123
[tauri]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/tauri/src/commands/activity.rs#L303
[registration]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/tauri/src/lib.rs#L318
[parser]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/activities/csv_parser.rs#L148
[mapping]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/hooks/use-import-mapping.ts#L22
[models]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/activities/activities_model.rs#L960
[profiles]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/utils/activity-import-profile.ts#L122
[drafts]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/utils/draft-utils.ts#L196
[accounts]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/utils/account-matching.ts#L76
[context]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/context/import-context.tsx#L119
[confirm]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/steps/confirm-step.tsx#L330
[mutations]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/hooks/use-activity-import-mutations.ts#L21
[shared]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/adapters/shared/activities.ts#L240
[service]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/activities/activities_service.rs#L5292
[apply]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/activities/activities_service.rs#L5499
[repository]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/storage-sqlite/src/activities/repository.rs#L2082
[schema]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/storage-sqlite/migrations/2026-01-01-000000_refactor_asset_model/up.sql#L638
[mcptool]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/agent-tools/src/tools/activity_import.rs#L441
[aitool]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/ai/src/tools/import_csv.rs
[connectclient]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/connect/src/client.rs#L146
[brokerservice]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/connect/src/broker/service.rs#L45
[pagination]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/connect/src/broker/orchestrator/activity_pagination.rs#L13
[brokeradapter]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/connect/src/broker_ingest/core_adapter.rs
[mappingstep]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/steps/mapping-step-unified.tsx#L615
[fingerprint]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/activities/idempotency.rs#L29
[numeric]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/utils/review-draft-utils.ts#L8
[holdings]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/utils/holdings-import-utils.ts#L414
[run]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/activities/import_run_model.rs#L65
[transfers]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/activities/activities_service.rs#L6912
[flows]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/portfolio/performance/flow_classifier.rs#L62
[dates]:
  https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/pages/activity/import/utils/date-format-options.ts
