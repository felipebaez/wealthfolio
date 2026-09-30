# Advisory audit coordination

Use authenticated `gh` for all GitHub operations, explicitly targeting `felipebaez/wealthfolio`. Read root `AGENTS.md` and this audit's `brief.md`. No product implementation, production deployment, merging, deleting data, purchases, or third-party contact is authorized. Synthetic data only.

Each actionable request has an issue and dedicated chat. Corrections/status requests update existing work. Parent issue belongs to the orchestrator. Use isolated worktrees for documentation too; workers must not change one another's files.

## Ownership

- Orchestrator: baseline.md, brief.md, workflow.md, index.json, README.md, findings.md, roadmap.md.
- Architecture worker: architecture.md and architecture-validation.md.
- Security worker: isolation.md and permissions-threat-model.md.
- Bank worker: banks.md and imports.md.
- Operations worker: operations.md and commercial-readiness.md.

Workers may create auxiliary files only inside their own named audit subdirectory. Deliver documentation-only PRs against main; attach them with the Codex artifact tool. Do not create implementation issues or extra worker chats; return proposed backlog entries for the orchestrator to deduplicate and dispatch. Do not close an audit issue before its criteria and consolidation review are satisfied.

## Status synchronization

At startup, resumption, meaningful status changes, and turn completion: read the issue and comments through gh; post material evidence/checks/blockers; maintain one status label while preserving unrelated labels; synchronize chat title/category. Chat names use StatusEmoji-IssueNumber-Title.

| State | Emoji | Label | Sidebar |
|---|---|---|---|
| Not started | ⚪ | status:not-started | Not Started |
| In progress (including PR review) | 🟡 | status:in-progress | In Progress |
| Specific unresolved blocker | 🔴 | status:blocked | Blocked |
| Criteria satisfied and issue closed completed | ✅ | status:completed | Completed |

Only the orchestrator edits index.json. Workers report their branch, PR, state, checks, limitations and blockers in their issue and final response. The orchestrator reconciles the index at observed checkpoints. No unattended monitor has been configured.

## Evidence and acceptance

Use commit-pinned repository links at 6ee11b1278eff8b5123280e740fa6983b501952b. Label conclusions confirmed, inferred or unknown. Official external sources must be dated. Include reproduction or verification method and validation limitations. Runtime prerequisites absent locally must be recorded; do not install broad system tools or claim unrun tests passed. Documentation validation follows AGENTS.md.
