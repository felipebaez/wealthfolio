# Self-hosted advisory platform audit — 2026-09-30

Parent issue: https://github.com/felipebaez/wealthfolio/issues/1. Consolidated documentation PR: https://github.com/felipebaez/wealthfolio/pull/6.

## Executive recommendation (provisional; worker review underway)

**Inferred recommendation:** pilot with a separate application instance, database, secret vault and keys per client. This avoids sharing the existing installation-wide profile chooser among unrelated clients. Keep access at a trusted identity-provider/reverse-proxy boundary with MFA and client-specific authorization. Separate instances still require validated deployment, session revocation, backups, recovery and operational procedures. Sharing a password or protecting profile selection is insufficient as a business permission model.

**Inferred longer-term direction:** evaluate one deployment using existing database-per-profile storage, adding durable issuer/subject identity, ownership, explicit advisor grants, operator administration and backend enforcement. Preserve the existing SQLite repositories and profile service contexts. Defer shared tenant-aware storage until measurements demonstrate a need; there is no established requirement for a database rewrite.

**Inferred import direction:** start with client-uploaded files for verified bank/product/export variants. Reuse preview, mappings and shared import services; strengthen provenance, repeat-import identity, deterministic monetary handling, transfers and reconciliation where evidence shows gaps. No named-bank compatibility is established merely by a parser feature or synthetic fixture. Automated read-only connectivity needs a separate bank/product, consent, certificate, licensing and privacy decision. Investment coverage remains distinct from payment-account coverage.

**Confirmed limitation:** this is an investigative source audit, not a passing client-isolation penetration test, financial calculation certification, load test, complete disaster-recovery drill, or legal approval. Source HEAD is 38 commits beyond the latest release and cannot be equated with published images. No product changes, merge or production deployment are authorized.

For capacity planning, the provisional assumption is up to 10 pilot clients on a single private server/VM; user clarification is pending. This assumption is not a measured capacity claim.

## Deliverable map

| Deliverable | Location |
|---|---|
| Baseline and validation limits | [baseline](baseline.md) |
| Full authorized requirements | [brief](brief.md) |
| Issue/chat/branch/PR state | [index](index.json), [workflow](workflow.md) |
| Architecture and upstream strategy | architecture.md; architecture-validation.md (worker #2) |
| Isolation decision record | isolation.md (worker #3) |
| Permissions and threat model | permissions-threat-model.md (worker #3) |
| Bank coverage and source matrix | banks.md (worker #4) |
| Import pipeline and proposed MVP | imports.md (worker #4) |
| Deployment and recovery | operations.md (worker #5) |
| License, terms and legal questions | commercial-readiness.md (worker #5) |
| Consolidated findings | findings.md (after worker review) |
| Roadmap, backlog and business decisions | roadmap.md (after worker review) |

## Business decisions to resolve after consolidated review

1. Pilot client count and infrastructure; choose separate instances versus implementing ownership on profiles.
2. Whether advisors may receive optional read-only access, what it includes, and how clients authorize/revoke it.
3. First actual bank, product and account tier: payment transactions, investment transactions, or holdings.
4. Availability of sanitized representative exports through a private intake process; never attach real statements publicly.
5. Whether any portfolio data may go to external AI, broker/device sync, market-data or aggregation services.
6. Recovery objectives, offboarding/retention policy, branding and qualified Czech/EU legal review.

These are selection questions, not authorization inferred from silence. No unattended monitor is configured; synchronization occurs at observed coordination checkpoints.
