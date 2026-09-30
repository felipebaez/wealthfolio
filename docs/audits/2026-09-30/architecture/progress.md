# Architecture issue checkpoint

This is the initial progress comment posted 2026-09-30 at 12:37:55 UTC to
[issue #2](https://github.com/felipebaez/wealthfolio/issues/2#issuecomment-5911452146).
Later accepted steering fixes the target to more than 50 clients on one private
server/VM; the final report/ledger and final issue handoff supersede the
preliminary recommendation below.

Architecture investigation is in progress on `audit/2-architecture`, isolated
worktree `/Users/felipebaez/Development/Wealthfolio-audits/architecture`, source
baseline `6ee11b1278eff8b5123280e740fa6983b501952b`.

Confirmed source traces: shared Rust services support both adapters; web
profiles bind requests to separate database runtimes; current OIDC mints
installation sessions without retaining issuer/subject as a client owner. I am
documenting extension points rather than recommending a database rewrite.

Additional source findings to consolidate with security/import/operations lanes:
missing FX in live holdings substitutes 1.0; CSV import-run metadata is
best-effort outside the activity transaction; domain recalculation events are in
memory; Docker pins pnpm 9.9.0 while the root manifest requests 10.33.4. These
are static findings, with focused runtime reproduction pending.

Checks: four `node --test scripts/tauri.test.mjs` tests passed in this worktree.
The parity-test command did not execute: installed pnpm 11.19.0 unexpectedly
launched a dependency install, which was interrupted; tracked files remained
unchanged. Node is 26.10.0 rather than requested 24; Cargo and Docker are absent
on PATH. No application build/security/bank-compatibility guarantee follows from
these checks.

Documentation-only PR pending. Issue remains open and `status:in-progress` for
orchestration review.
