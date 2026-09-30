# Security audit validation record

Date: 2026-09-30. Worktree:
`/Users/felipebaez/Development/Wealthfolio-audits/security`; local branch
`audit/3-security`; source parent `6ee11b1278eff8b5123280e740fa6983b501952b`.
[Issue #3](https://github.com/felipebaez/wealthfolio/issues/3) remains open/in
progress for review and consolidation under
[issue #8](https://github.com/felipebaez/wealthfolio/issues/8).

## Executed observations

- Worktree HEAD, branch, remote names and clean initial tracked status checked.
  Authenticated `gh api repos/felipebaez/wealthfolio/branches/main` returned the
  source parent. No main-checkout files/branch were changed.
- Root AGENTS.md and full issue body/comments read at startup and checkpoints.
  Human brief/workflow read from supplied absolute paths because they were
  absent in this worktree. Later steering incorporated: more than 50 clients on
  one private server/VM; no capacity measurements or container platform assumed.
- Source traced through installation auth/OIDC, profile
  registry/lock/recovery/sessions, main router/admission, profile runtimes and
  services, upload/import/export/backup paths, SSE/NDJSON, scheduler, AI,
  MCP/PAT scopes, add-on sandbox/network and Connect identity/auth flows.
  Source-confirmed behavior is separated from inferred risk and unexecuted
  runtime reproduction.
- `node --test scripts/tauri.test.mjs`: **4 passed, 0 failed**. Only
  script/build-command configuration; not security isolation, product build,
  Rust or E2E evidence.
- Focused
  `pnpm --filter frontend exec vitest run src/features/profiles/session.test.ts src/features/profiles/api.test.ts src/features/profiles/auth-bridge.test.ts`:
  **tests did not run**. pnpm initiated an automatic dependency install in the
  dependency-free worktree. It was interrupted with SIGINT/exit 130; progress
  showed downloaded packages and zero added at the last reported checkpoint.
  Tracked status remained unchanged. No follow-up install or claim of passing
  tests.
- Node is 26.10.0 versus required 24; pnpm is 11.19.0 versus pinned 10.33.4;
  neither was changed. Cargo and Docker were absent on PATH; Rust toolchain
  requests 1.98.1.
- The fork's `gh api repos/felipebaez/wealthfolio/releases/latest` returned
  **404**. Release v3.9.1/SHA/date are supplied upstream baseline context, not a
  release queried or executed by this lane.
- Official external references reviewed on 2026-09-30:
  [OIDC Core §5.7](https://openid.net/specs/openid-connect-core-1_0.html#ClaimStability)
  (errata set 2 dated 2023-12-15),
  [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html),
  and
  [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).
  They support identity/policy requirements, not claims about application
  runtime behavior.

## Documentation checks

Run from this worktree root:

```sh
node docs/audits/2026-09-30/security/check-docs.mjs
git diff --check
git diff --cached --check
```

The dependency-free helper verifies source-link baseline/path/range existence
against Git, local documentation links/headings and code-fence balance. It does
not fetch source websites or validate that a line range proves a claim; those
were reviewed manually. It does not execute auth middleware, dependencies,
provider requests, migrations or financial computations. **Executed result:** 3
documents, 56 pinned source links and 8 local links validated; unstaged and
staged whitespace checks passed. The final staged diff is restricted to the two
assigned reports and this lane's validation/helper files.

## Formatting repair

Initial remote Formatting check at revision
`5dc8945ee451ac96a1f0a4a8ecc87dbd394d3676` identified four owned files requiring
Prettier. Downloaded only standalone Prettier 3.8.1 from the official npm
registry into this lane's untracked auxiliary directory, then formatted and
checked the five PR files using repository formatting options. No full
application dependency install or system tool installation was performed for
this repair. Tailwind's plugin is irrelevant to these Markdown/JSON/helper
files; remote CI remains the authoritative full-repository formatting check.
Documentation link/range and whitespace checks were repeated after formatting.

## Not run / unknown

Rust profile/auth/MCP/portable-backup tests, compilation, formatting and Clippy
were not run because Cargo is unavailable. Frontend tests/build/type/lint/E2E
are unverified due to missing dependencies and mismatched tools; they are not
necessary to validate this documentation-only change but are prerequisites for
product/security assurances. Docker-based staging cannot run here. No live
IdP/MFA, mocked end-to-end provider network, curl two-browser exploit, restored
database, 60-client capacity test or production image was run. No
client/credential data, external message, deployment, product implementation,
merge, paid service or third-party contact occurred.

The
[two-browser recipe and adversarial matrix](../permissions-threat-model.md#concrete-baseline-two-browser-recipe-not-executed)
specify future checks. The
[capacity gates](../isolation.md#more-than-50-clients-on-one-private-servervm)
are provisional targets pending VM resources, concurrency, portfolio sizes,
backup retention and RPO/RTO. Current source does not establish client
ownership/advisor permissions or complete business revocation. A passing
documentation check must never be described as passing tenant isolation.
