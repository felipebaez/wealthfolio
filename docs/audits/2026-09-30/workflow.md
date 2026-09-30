# Advisory audit coordination

Use authenticated `gh` for all GitHub operations, explicitly targeting
`felipebaez/wealthfolio`. Read root `AGENTS.md` and this audit's `brief.md`. No
product implementation, production deployment, merging, deleting data,
purchases, or third-party contact is authorized. Synthetic data only.

Each actionable request has an issue and dedicated chat. Corrections/status
requests update existing work. The command center owns parent issue coordination
and business decisions. The synthesis worker (#8) owns technical consolidation
in the existing primary checkout on `audit/advisory-orchestration`, PR #6.
Specialist workers use their existing isolated documentation worktrees; workers
must not change one another's files.

## Ownership

- Synthesis worker #8: baseline.md, workflow.md, index.json, README.md,
  findings.md, roadmap.md and coordination notes. Preserve brief.md as the
  original request; record subsequent steering separately.
- Architecture worker: architecture.md and architecture-validation.md.
- Security worker: isolation.md and permissions-threat-model.md.
- Bank worker: banks.md and imports.md.
- Operations worker: operations.md and commercial-readiness.md.

Workers may create auxiliary files only inside their own named audit
subdirectory. Deliver documentation-only PRs against main; attach them with the
Codex artifact tool. Do not create implementation issues or extra worker chats;
return proposed backlog entries for synthesis to review and deduplicate. The
command center dispatches implementation only after human selection. Do not
close an audit issue before its criteria and consolidation review are satisfied.

## Status synchronization

At startup, resumption, meaningful status changes, and turn completion: read the
issue and comments through gh; post material evidence/checks/blockers; maintain
one status label while preserving unrelated labels; synchronize chat
title/category. Chat names use StatusEmoji-IssueNumber-Title.

| State                                         | Emoji | Label              | Sidebar     |
| --------------------------------------------- | ----- | ------------------ | ----------- |
| Not started                                   | ⚪    | status:not-started | Not Started |
| In progress (including PR review)             | 🟡    | status:in-progress | In Progress |
| Specific unresolved blocker                   | 🔴    | status:blocked     | Blocked     |
| Criteria satisfied and issue closed completed | ✅    | status:completed   | Completed   |

Only the synthesis worker edits index.json. Workers report their branch, PR,
state, checks, limitations and blockers in their issue and final response. The
synthesis worker reconciles the index at observed checkpoints. No unattended
monitor has been configured.

## Evidence and acceptance

Use commit-pinned repository links at 6ee11b1278eff8b5123280e740fa6983b501952b.
Label conclusions confirmed, inferred or unknown. Official external sources must
be dated. Include reproduction or verification method and validation
limitations. Runtime prerequisites absent locally must be recorded; do not
install broad system tools or claim unrun tests passed. Documentation validation
follows AGENTS.md.

## Accepted steering and handoff — 2026-09-30

- More than 50 clients; one private server or VM. Hardware, concurrency, data
  volumes and recovery objectives remain unknown. Earlier <=10 assumptions are
  superseded. A small technical isolation trial does not establish launch
  capacity.
- The human explicitly restricted the command-center chat to coordination. Its
  exact title remains **Wealth Command Center**, an exception to issue-title
  naming. Audit/source review, file edits and synthesis are worker
  responsibilities.
- #8 continues PR #6; reviewed specialist documentation may be copied to that
  branch. No product changes, GitHub PR merge or changes to another worker
  checkout.
- Existing local staging task #7 is separately authorized and coordinated by the
  command center; its existence does not prove runtime checks passed or
  authorize a production deployment.
- Proposed implementation issues stay not started, with no dispatched
  implementation chat, until selected. Audit issues stay open while
  review/acceptance remains pending.

## GitHub CLI and chat-status addendum

The
[human addendum](https://github.com/felipebaez/wealthfolio/issues/1#issuecomment-5911547424),
received 2026-09-30, applies at startup, resumption, meaningful transitions and
turn completion. Read the current issue title/body/comments/state/labels with
authenticated `gh` using each repository-aware subcommand’s
`--repo felipebaez/wealthfolio` option (or an API path explicitly under
`repos/felipebaez/wealthfolio`). Post material progress/checks/blockers,
maintain exactly one status label while preserving unrelated labels, and
synchronize the exact `StatusEmoji-IssueNumber-currentIssueTitle` and one
existing status sidebar category. The four user entries literally said “status”;
the working interpretation is the existing four distinct labels listed above,
rather than four identical labels.

Review-awaiting PRs remain In Progress. Completed requires satisfied acceptance
and a completed issue closure; merely finishing a turn or awaiting a merge does
not qualify. A blocker records the specific unavailable decision/prerequisite;
record failed synchronization and retry honestly. No continuous monitor exists.

Conflict-free durable synchronization: workers report current
issue/chat/title/category/status/branch/worktree/PR/blockers and last sync
through their issue. Only synthesis writes index.json from observed checkpoints,
recording exact reviewed PR revisions separately from live worker state. Command
Center and specialists request corrections through issues/messages, never edit
the synthesis checkout. Staging #7 reports separately; its local authorization
does not expand audit or production scope. Preserve the named/pinned Wealth
Command Center exception.
