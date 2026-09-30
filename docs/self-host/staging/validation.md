# Staging validation — 2026-09-30

Fork source: `main` commit `6ee11b1278eff8b5123280e740fa6983b501952b`.
[Native ARM64 production build](https://github.com/felipebaez/wealthfolio/actions/runs/36716582110).
Image: `wealthfolio-staging:6ee11b1278eff8b5123280e740fa6983b501952b`; ID
`sha256:4f271d67f98d74319fe46ba0694d5f5a9151519adc5088023434af5c567574f3`. Running URL:
<http://localhost:18088>. Application code is unchanged.

| Check                                           | Status                       | Evidence / limitation                                                                                                                                                                      |
| ----------------------------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| OS/resources and existing services inspected    | Passed                       | macOS 27 ARM64 guest, 4 CPUs, 16 GiB RAM, 64 GiB initially free; unrelated listeners preserved                                                                                             |
| Isolated branch/worktree                        | Passed                       | `deploy/docker-staging`; main checkout audit edits untouched                                                                                                                               |
| Native Apple VZ runtime                         | Failed                       | Nested virtualization unavailable: `VZErrorDomain Code=2`, `kern.hv_support=0`                                                                                                             |
| ARM64 software-emulation runtime                | Passed                       | Dedicated Colima/QEMU profile, Docker `aarch64`, 3 CPUs, 8 GiB guest memory                                                                                                                |
| Production image build from fork                | Passed                       | Actual fork Dockerfile on native ARM64 runner; frontend type check/build and Rust release build succeeded; no Connect arguments                                                            |
| Compose syntax                                  | Passed                       | `config --quiet` succeeds; no secret-expanded output published                                                                                                                             |
| Container start/health                          | Passed                       | Compose wait succeeds; service healthy before/after recreation and restored instance healthy                                                                                               |
| Frontend/API reachability                       | Passed                       | Frontend HTML and `/api/v1/healthz` return 200; actual browser UI loads                                                                                                                    |
| Authentication and cookie attributes            | Passed                       | Correct password succeeds, incorrect password rejected; cookie has HttpOnly, SameSite=Lax, Path=/api; Secure omitted intentionally for local HTTP                                          |
| Unauthenticated financial access                | Passed                       | Accounts request returns 401 without login                                                                                                                                                 |
| Synthetic profile/account/activity              | Passed                       | Created Staging Synthetic profile, USD securities account and $5,000 deposit through supported APIs; visible in UI                                                                         |
| Portfolio views                                 | Passed                       | Dashboard and holdings show $14,775 cash; dashboard shows $25 gain; no portfolio failure after setting USD base currency                                                                   |
| CSV preview and commit                          | Passed                       | Browser preview showed three rows; mapping/review accepted all; Import Complete reported 3 imported, 0 skipped                                                                             |
| Data/key persistence after recreation           | Passed                       | Force-recreated only staging container; same profile/account IDs and 4 activities; password still works and encryption enabled                                                             |
| Consistent complete backup                      | Passed                       | Controlled stop, complete `/data` archive plus matching config/key/password; checksums and archive safety verified                                                                         |
| Isolated restore                                | Passed                       | New project `wealthfolio-staging-restore-20260930`, new volume and port 18089; same IDs, 4 activities, encryption, login, and browser $14,775 portfolio; original instance remains healthy |
| Optional integrations                           | Passed for tested core flow  | All market-data providers disabled; device sync false; Connect/MCP/OIDC/AI credentials absent; cash import and portfolio work offline; no AI prompt sent                                   |
| Outbound network limitation                     | Passed for direct HTTP probe | Bridge IP masquerading disabled; HTTP request to public IP 1.1.1.1 timed out. This is not a comprehensive firewall audit                                                                   |
| Localhost-only access                           | Passed                       | Docker and host listener bind 127.0.0.1:18088; host LAN-address connection refused; guest DNS port 53 not forwarded                                                                        |
| Runtime permissions/limits                      | Passed                       | App UID/GID 1000; readable mode-0400 key in separate read-only volume; read-only root, 768 MiB cap, logs 10 MiB × 3, restart unless-stopped                                                |
| Recovery safety regression tests                | Passed                       | Six tests: valid bundle, altered-key checksum, archive traversal, existing destination, live project and repeated initialization guards                                                    |
| Python compile / diff / changed-file formatting | Passed                       | Compile and diff checks; Prettier for changed Markdown/YAML/JSON                                                                                                                           |
| Secret scan of files and GitHub issue/PR        | Passed                       | Generated password, master key and hash absent from repository files/diff and issue/PR body/comments; values withheld from scan output                                                     |
| Standard app E2E suite                          | Not run                      | Its native dev-server/fresh-DB setup differs; browser automation exercised the deployed production Docker service directly                                                                 |
| Older-image migration downgrade                 | Not run                      | No older migrated deployment exists. Rollback uses the tested isolated restore mechanism with the matching prior image and pre-update snapshot; backwards DB compatibility is not assumed  |
| Machine reboot/sleep                            | Not run                      | Restart policy inspected; no system-wide sleep/login settings changed. Reboot requires starting named Colima profile; sleep suspends service                                               |
| Chat/issue synchronization                      | Partial                      | Issue/title verified. Category tool acknowledges moves, but subsequent list still reports this chat in Tasks; no verified category move claimed                                            |

Private evidence: `/Users/felipebaez/Development/Wealthfolio-staging-runtime/evidence/`.
Screenshots: `csv-preview.jpg`, `csv-import-complete.jpg`, `holdings.jpg`, `portfolio-verified.jpg`,
`restored-portfolio.jpg`. API reports/logs and runtime security checks are alongside them.
Credentials are kept separately in `secrets/`; do not publish recovery bundles.

Verified backup:
`/Users/felipebaez/Development/Wealthfolio-staging-runtime/backups/20260930T131221163417Z`. The
restored project's data is retained; its server is stopped after verification. No volumes, backups
or prior images were deleted.

Initial setup corrections: the API harness used one-based pagination; the API uses zero-based pages.
The harness also skipped onboarding before setting base currency; setting USD corrected the
resulting FX warning. An internal-only Docker network ignored port publishing; the final bridge
disables NAT and preserves loopback publication. These changes require no application patch.

**Architecture impact:** application API/auth, business logic, persistence/schema, events/background
execution and user-edit precedence remain unchanged. Deployment changes network/build configuration
and adds protected key staging to handle host/container UID differences. Tested guarantees cover
synthetic cash data, authentication, local exposure, recreation and complete restore. Provider quote
retrieval, cross-currency valuation, real broker/device sync and AI are intentionally unverified.

[PR #12](https://github.com/felipebaez/wealthfolio/pull/12) remains In Progress awaiting review. The
previous PR CI passed frontend, Rust, Android, iOS and translations; formatting failed on the new
guide/validation files, which were subsequently formatted. Final-revision CI is tracked in the PR;
earlier results are not claimed as final-revision passes. No merge or production deployment.
