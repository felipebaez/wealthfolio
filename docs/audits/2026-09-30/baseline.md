# Baseline — 2026-09-30

## Confirmed

- Fork: https://github.com/felipebaez/wealthfolio, public, default branch main.
- Fork main and upstream main: `6ee11b1278eff8b5123280e740fa6983b501952b`.
- Fork-only/upstream-only commit counts: 0/0
  (`git rev-list --left-right --count origin/main...upstream/main`).
- Initial checkout main, clean; orchestrator documentation branch
  `audit/advisory-orchestration`.
- Source package/workspace version: 3.9.2.
- Latest upstream release: v3.9.1, published 2026-09-27T13:23:17Z, tag commit
  `392f272c5b15a4af45dc2ff71dcbec474f47112a`. Source HEAD is not that release.
- compose.yml references mutable `wealthfolio/wealthfolio:latest`; published
  image tags/digests are to be independently verified by operations audit.
- Root AGENTS.md is the only repository AGENTS.md discovered. No ancestor
  instructions found.
- GitHub CLI authenticated as repository owner; repository admin/push access
  verified. Issues initially disabled; enabled successfully as prerequisite to
  requested issue workflow. No fork issues or open PRs existed at startup.
- Codex create/read/message/wait/sidebar/PR attachment tools available.
- Local folder initially empty; cloned via gh with origin/upstream remotes.

## Prerequisites and checks

Repository asks for Node 24, pnpm 10.33.4, Rust 1.98.1. Cargo and Docker were
not found on PATH at initial inspection. Runtime checks will be recorded by the
assigned audit workers. No real client data used. No production service started.
No continuous monitor configured.

## Reproduction

```sh
gh repo view felipebaez/wealthfolio --json nameWithOwner,defaultBranchRef,isPrivate,url
gh api repos/felipebaez/wealthfolio/commits/main --jq .sha
gh api repos/wealthfolio/wealthfolio/commits/main --jq .sha
git rev-parse HEAD upstream/main
git rev-list --left-right --count origin/main...upstream/main
gh api repos/wealthfolio/wealthfolio/releases/latest
git rev-parse 'v3.9.1^{}'
```

## Initial lightweight validation

`node --test scripts/tauri.test.mjs`: 4 tests passed under installed Node
26.10.0. Installed pnpm 11.19.0 differs from required pnpm 10.33.4; no
dependency installation performed. This does not establish frontend, Rust,
profile-security or deployment correctness. Cargo/Docker absent on PATH.

## Further baseline evidence

- `gh api repos/wealthfolio/wealthfolio/compare/v3.9.1...main`: source is 38
  commits ahead of latest release, zero behind.
- Exact source HEAD Actions API reported one successful Warm Rust Cache run:
  https://github.com/wealthfolio/wealthfolio/actions/runs/36652133048. This is
  not evidence that a full PR check suite passed at HEAD.
- `python3 -m unittest discover -s .github/scripts -p 'test_*.py'`: 22 tests
  passed. These script unit tests do not establish application/container
  encryption, isolation or recovery correctness.

## Synthesis checkpoint — 2026-09-30

Authenticated commit lookup freshly returned the same pinned SHA for fork and
upstream main during synthesis. No new baseline was silently adopted. The
documentation branch contains audit commits above that source; it is not a
product release. This audit's recorded latest-release/38-commit context is
historical metadata, not proof that a deployed image maps to either revision.

The human separately authorized localhost staging #7. Its issue reports standard
Docker/Compose/buildx, Colima/QEMU and Argon2 tooling installed after the
specialist checks. That host is an Apple M2 virtual machine without native
virtualization support; an emulated local runtime/native ARM64 build task is
underway. Its staging PR #12 is not audited or copied here, and
application/login/import/persistence/restore results are not yet accepted.
“Cargo/Docker absent” below describes the audit-worker check time, not an
assertion that no tool can later become available. Synthesis performs
documentation/diagnostic validation without broad tool or dependency
installation.

Synthesis independently reran the bank lane's seven audit-only
numeric/CASH-expression tests: all passed under Node 26.10.0. These
intentionally reproduce permissive normalization/float behavior; they do not
certify an importer or fix. Security's dependency-free documentation check
passed: 3 reports/56 source links/8 local links. Full consolidated
path/range/reference/format/diff and exact PR checks are recorded in
coordination/review.md.

Frontend profile, adapter-parity and import Vitest attempts in specialist
worktrees never ran: pnpm 11 initiated installation; architecture/security
interrupted it and banks restored unintended tracked lock/workspace changes.
Only assigned documentation appears in their final reviewed PRs. Ignored local
downloads/node_modules are not deliverables. No synthesis pnpm
install/type-check/build attempt occurred.

Repository-required Rust, frontend, container, end-to-end isolation,
provider-invariant, load and recovery checks are not claimed passed. They are
unnecessary for a documentation-only diff but required before the corresponding
product/deployment guarantee. CI formatting success and aggregate status on
documentation revisions must be reported with skipped jobs explicitly; they are
not complete product CI evidence.
