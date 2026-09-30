# Baseline — 2026-09-30

## Confirmed

- Fork: https://github.com/felipebaez/wealthfolio, public, default branch main.
- Fork main and upstream main: `6ee11b1278eff8b5123280e740fa6983b501952b`.
- Fork-only/upstream-only commit counts: 0/0 (`git rev-list --left-right --count origin/main...upstream/main`).
- Initial checkout main, clean; orchestrator documentation branch `audit/advisory-orchestration`.
- Source package/workspace version: 3.9.2.
- Latest upstream release: v3.9.1, published 2026-09-27T13:23:17Z, tag commit `392f272c5b15a4af45dc2ff71dcbec474f47112a`. Source HEAD is not that release.
- compose.yml references mutable `wealthfolio/wealthfolio:latest`; published image tags/digests are to be independently verified by operations audit.
- Root AGENTS.md is the only repository AGENTS.md discovered. No ancestor instructions found.
- GitHub CLI authenticated as repository owner; repository admin/push access verified. Issues initially disabled; enabled successfully as prerequisite to requested issue workflow. No fork issues or open PRs existed at startup.
- Codex create/read/message/wait/sidebar/PR attachment tools available.
- Local folder initially empty; cloned via gh with origin/upstream remotes.

## Prerequisites and checks

Repository asks for Node 24, pnpm 10.33.4, Rust 1.98.1. Cargo and Docker were not found on PATH at initial inspection. Runtime checks will be recorded by the assigned audit workers. No real client data used. No production service started. No continuous monitor configured.

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

`node --test scripts/tauri.test.mjs`: 4 tests passed under installed Node 26.10.0. Installed pnpm 11.19.0 differs from required pnpm 10.33.4; no dependency installation performed. This does not establish frontend, Rust, profile-security or deployment correctness. Cargo/Docker absent on PATH.
