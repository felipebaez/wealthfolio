# Staging validation — 2026-09-30

Source selected: fork `main` commit `6ee11b1278eff8b5123280e740fa6983b501952b`.
Native ARM64 source build: [GitHub Actions run](https://github.com/felipebaez/wealthfolio/actions/runs/36716582110).
Application code is unchanged; validation targets the actual Docker staging service.

| Check | Status | Evidence / limitation |
| --- | --- | --- |
| OS/resources and existing services inspected | Passed | macOS 27 ARM64 guest; 4 CPUs, 16 GiB RAM, 64 GiB initially free; existing listeners preserved |
| Isolated branch/worktree | Passed | `deploy/docker-staging`; main checkout audit edits untouched |
| Native VZ runtime | Failed | `VZErrorDomain Code=2`, virtualization unavailable; `kern.hv_support=0` |
| Docker software-emulation fallback | In progress | Dedicated `wealthfolio-staging-qemu` profile, ARM64; provisioning |
| Production image build from fork | In progress | Native ARM64 workflow, no Connect arguments |
| Secrets outside Git | Passed (initial setup) | Private runtime directory, key/password `0400`, env `0600`; values not printed |
| Compose syntax | Pending | Verify with `config --quiet`, avoiding expanded hashes |
| Container start and health | Not run | Await image and daemon |
| Frontend/API reachable | Not run | Await running service |
| Authentication + cookie security | Not run | Await running service |
| Reject unauthenticated financial access | Not run | Await running service |
| Synthetic profile/account/activity | Not run | Await running service |
| Portfolio views | Not run | Await running service |
| CSV preview and commit | Not run | Await running service |
| Persistence after recreation | Not run | Await running service |
| Consistent backup and isolated restore | Not run | Await populated service |
| Optional integrations disabled | Pending | Internal Docker network configured; provider settings still need verification |
| Localhost-only listeners | Pending | Port 18088 free initially; running bindings still need verification |
| Secret scan of commits/issue | Pending | Final scan after artifacts are complete |
| Chat/issue status synchronization | Partial | Issue and title verified; sidebar move acknowledged but list view did not retain current chat's category. Retrying; no claim of full success |

Required checks remain outstanding. Status is In Progress. No standard app E2E
suite has been claimed: its native dev-server/fresh-DB setup differs from this
production Docker acceptance flow. Available browser automation will exercise
this service directly. No personal financial data or external credentials used.
