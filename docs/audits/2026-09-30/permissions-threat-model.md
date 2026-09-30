# Permissions and threat model for an advisory service

Audit date: 2026-09-30. Source `6ee11b1278eff8b5123280e740fa6983b501952b`;
[issue #3](https://github.com/felipebaez/wealthfolio/issues/3). Read with
[isolation.md](isolation.md), which contains findings SEC-01–09, options A/B/C,
estimates, and validation limitations. This is a proposed business policy and
test specification. The existing application does **not** implement these roles.

## Recommendation and trust boundaries

**Inferred recommendation:** clients own their assigned financial workspace.
Advisors receive explicit, client-specific permissions with read-only as the
default; infrastructure operators maintain the service without automatic
business authorization to inspect portfolios. Backend checks enforce every
action, including direct API, tools, background work and downloads. Hiding
controls in the browser is insufficient. These recommendations follow
[OWASP Authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html),
reviewed 2026-09-30: deny by default and validate permissions on every request.

**Confirmed present boundary:** installation admission → browser-owned profile
grant → fixed profile runtime → that runtime's database/services/secrets.
Separate MCP admission selects a profile then validates its PAT. The shared
process and master key are trusted across profiles. An authenticated
installation user is not yet a contractual client; Connect user/team, financial
account and profile UUID are not alternate ownership proofs.

**Inferred proposed B boundary:** verified identity → active membership and
action permission → owner-bound current grant → fixed runtime. Reuse existing
scope/session mechanics, adding authoritative identity/permission checks before
granting or initializing the target. At sensitive commit or streaming
boundaries, check the authorization revision and suspension state again. This
changes authorization, persistence and job admission; it must not change
provider opt-in, derived-data ownership or user-edit precedence incidentally.

**Operator privacy limit:** a host/root administrator or application process
with the master key can decrypt databases and the vault and observe runtime
plaintext. The matrix below defines business policy, not cryptographic
protection from that operator. Client-held keys with no server decryption would
be a different architecture and could prevent the server from doing existing
calculations, imports and sync; it is not established or proposed as a small
fix.

## Proposed permission matrix

Status of every cell is **inferred proposed policy**. “Own” means an active
verified relationship, not a UUID sent by the caller. Advisor grants need
explicit scope, expiry, client/workspace, and consent provenance. An operator
account is separate from an advisor account, even if one person performs both
duties.

| Action                                                    | Client                                                           | Advisor                                                                     | Operator                                                                                  |
| --------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Sign in / MFA                                             | Own identity; mandatory approved IdP policy                      | Own identity; stronger admin/advisor policy                                 | Separate operator identity and MFA                                                        |
| List profiles / client metadata                           | Own authorized workspaces only                                   | Only clients with active grants; least necessary names                      | Provisioning metadata only through admin interface, audited                               |
| Read portfolio, activities, holdings, performance         | Own                                                              | Explicit read grant                                                         | No routine business read; approved break-glass procedure if required                      |
| Create/edit/delete activities; CSV import; reconciliation | Own                                                              | Denied by default; separately approved edit permission                      | Denied through normal admin role                                                          |
| Read/download/export financial data or backups            | Own, explicit export action                                      | Denied by read-only default; distinct export grant                          | Backup custody for operations; access technically possible, policy-controlled and audited |
| Change workspace name/avatar                              | Own                                                              | Denied by default                                                           | Approved administrative correction only                                                   |
| Create workspace / invite members                         | Claim an approved invitation; household invites only if selected | Cannot create arbitrary clients or invite themselves                        | Provision/invite under approved onboarding; cannot silently grant own advisor access      |
| Grant/revoke advisor                                      | Approve/revoke own narrow grant                                  | Request access, never self-approve                                          | Cannot manufacture consent; emergency access separate                                     |
| Change/recover credentials                                | Own IdP recovery; profile lock proof optional extra barrier      | Own IdP only; cannot recover a client's profile                             | Verify recovery process; reset principal admission with audit, not disclose old passwords |
| Suspend/revoke all sessions                               | Own sign-out/revoke devices/tokens                               | Own sessions only                                                           | Suspend identity/workspace and audit reason; cannot bypass suspension via restore         |
| Configure bank/Connect authorization or device pairing    | Own, consented outbound feature                                  | Denied by read/edit alone; separate connection permission if later selected | Provision technical integration settings; no reuse of client authorization                |
| Read raw secrets / recover refresh tokens                 | Avoid routine raw retrieval; narrowly required client flow only  | Denied, including read-only and ordinary edit grants                        | Technical vault custody; no secret values in admin responses/logs                         |
| AI conversation, attachments and tools                    | Own, approved provider and scopes                                | Only if specifically granted; client conversations private by default       | No conversation access through routine operator role                                      |
| Mint/revoke MCP tokens                                    | Own token within own action ceiling and approved lifetime        | Only separately granted token ability, scoped to that client                | Disable endpoint/revoke for incident; no routine unrestricted minting                     |
| Install/enable add-ons; approve outbound hosts            | Only approved catalog/policy and own scope                       | Denied by default                                                           | Approve catalog/hosts policy; client consent for data release still required              |
| Restore/import whole database                             | Request recovery; server web restore currently unavailable       | Denied                                                                      | Offline, exact target/key/registry, approved recovery audit                               |
| Offboard/delete workspace                                 | Request deletion/export subject to retention policy              | Cannot delete client's workspace                                            | Execute approved retention/deletion; backup expiry documented                             |

**Confirmed mismatch:** browser APIs currently operate on a granted runtime
without client/advisor/operator action roles; profile creation is available at
installation scope. MCP tool scopes exist and are useful, but do not create a
browser advisor role or client membership. Its grant cannot exceed the issuing
principal's capability ceiling in a future implementation. Existing
internal-secret restrictions must be preserved.

## Identity and access lifecycle

All workflow steps below are **inferred required behavior for B**, and
requirements for an A pilot where applicable. They are not presently complete in
the app.

1. **Invitation:** operator provisions a synthetic/client workspace and sends a
   narrowly scoped, expiring invitation through an approved future workflow.
   Invitation contains an opaque claim, not financial data or a reusable app
   password. Bind after successful verified IdP login; require intended
   recipient/approval proof where necessary, consume once atomically, reject
   replay/concurrent claims. Never use a supplied email or Connect token alone
   to claim an existing profile. Sending invitations to real people is outside
   this audit.
2. **Onboarding:** claim assigns a stable `(issuer, subject)` principal and
   workspace relationship. Names/household membership are separate metadata.
   Existing profiles require explicit owner assignment; new subject or changed
   issuer cannot inherit the default profile. Agree on data export/retention and
   allowed outbound features before enabling them.
3. **Authentication/MFA:** use the IdP for password/MFA/WebAuthn and verified
   subject. Mandatory MFA is an IdP application policy with tested evidence; the
   current callback does not enforce an application `acr`/`amr` threshold. If
   app-level step-up is required, define accepted assurance/freshness and verify
   claims. Disable any shared installation password path that would let
   client/advisor traffic evade named identity or MFA. A gateway can enforce an
   A pilot's named admission, but forwarded headers alone are not a demonstrated
   app identity path.
4. **Sessions:** bind session to active principal, installation/workspace
   permissions and revision. Set secure cookies via trusted ingress, idle and
   absolute expiry, and revoke locally on sign-out or incident. The
   [OWASP Session Management guidance](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html),
   reviewed 2026-09-30, supports server-side invalidation and lifetime controls.
   IdP logout is not a substitute for local revocation. Multiple browsers are
   independent sessions and must all be discoverable by principal for
   revoke-all.
5. **Advisor authorization:** client approves a named advisor's
   workspace-specific read grant, purpose, expiry and permitted exports/edits.
   Advisor never becomes profile owner and cannot reset its lock, invite another
   advisor, recover Connect refresh tokens or mint broader PATs. Grant/revoke
   records contain actor, target, capability and timestamp; avoid financial
   values. Do not infer consent from a business relationship or IdP allowlist
   entry.
6. **Recovery:** IdP recovery restores identity after the selected verification
   procedure, then app membership is re-evaluated. A profile code supplements
   identity; it must not claim someone else's workspace. If single-use recovery
   is chosen, consume and rotate atomically and invalidate old sessions/flows.
   The current code can act as repeated unlock proof until reset; the audit has
   not changed it. Lost master keys/portable-backup passwords follow operator
   disaster recovery, not client password reset.
7. **Suspension/revocation:** principal suspension denies new login/admission
   immediately according to an agreed time objective, revokes active grants and
   dependent tokens/flows, closes idle and active streams, and prevents new
   disallowed async commits/outbound work. Browser lock can retain authorized
   scheduled sync; workspace suspension cannot silently do so. Decide whether
   routine sign-out revokes personal PATs; offboarding must do so. A committed
   transaction cannot be undone merely by revoking the response.
8. **Offboarding:** produce client-authorized export, revoke
   advisor/member/session/PAT/device/connection access, disable scheduled work
   and retained callbacks, and execute deletion under approved retention policy.
   Client export is not the same as restoring or exporting the whole
   installation. Historical backups may retain data until expiry; policy must
   say so. Recovery from an older database must preserve the current
   authoritative suspension/revocation record, not resurrect old access.

## Surface-by-surface trace

Claims below are **confirmed source mechanisms** unless explicitly marked
inferred/unknown. The shared API wrapper is
[router composition](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/api.rs#L164-L224)
and
[admission/body checks](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/profiles.rs#L645-L719).
Every surface must receive backend membership/action enforcement for B.

| Surface                                 | Actual source flow and existing boundary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Residual requirement / uncertainty                                                                                                                                                                                                                                                                                                                                                             |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| API reads and writes                    | Web adapter captures `x-wf-profile-scope`; authentication supplies owner, admission fixes runtime; Axum handlers use `Extension<Arc<AppState>>` and its services/repositories. Financial identifiers do not select a different runtime.                                                                                                                                                                                                                                                                                                                                                                                                                    | Foreign profile unlock still possible if unprotected; same-profile advisor needs action restrictions. Forge account/activity/asset/goal IDs and test mixed bulk requests, not just settings reads.                                                                                                                                                                                             |
| Profile metadata and admin              | Installation-authenticated `/profiles/{command}` bypasses selected-profile layer; full lists/pending-deletion metadata. Unlock checks proof, creation no role. Normal update/delete/password require current grant.                                                                                                                                                                                                                                                                                                                                                                                                                                        | Filter enumeration; permission before existence-disclosing errors/credential cooldown. Pending-delete retry and startup cleanup are operator/lifecycle actions, not a client delete override.                                                                                                                                                                                                  |
| CSV upload/import                       | [Web parser adapter](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/adapters/web/activities.ts#L34-L64) POSTs multipart with scope. [Parse handler](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/api/activities.rs#L395-L438) reads bytes in memory and invokes shared parser; no file persisted by this handler. Preview/check/commit use admitted activity service.                                                                                                                                                                | Upload is transmitted to self-hosted server; UI preview does not mean browser-only parsing. Validate destination ownership and role again at commit; enforce upload limits/quotas. Bank schema compatibility is separate/unknown.                                                                                                                                                              |
| Financial export                        | [Export handler](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/api/data_exports.rs#L28-L106) queries admitted services; account `All` means accounts inside this profile, not all business clients.                                                                                                                                                                                                                                                                                                                                                                                              | Read-only advisor cannot implicitly export; attachments/download links need target/session and expiry checks.                                                                                                                                                                                                                                                                                  |
| Backup/download/temp files              | [Snapshots](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/api/database_backups.rs#L26-L123) use `state.data_root`; validated filename/lease. [Portable export](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/api/portable_backups.rs#L131-L205) captures root/key, stages in profile scratch, and ties ticket to `owner:scope`; one-use download, ten-minute expiry, two outstanding exports per runtime.                                                                                                                              | Different profiles may have identical snapshot filenames; root binding must prevail. Verify scratch permissions/cleanup, symlink/traversal and revocation during download. A client able to export their profile can export its whole DB, including AI/PAT metadata; choose policy explicitly.                                                                                                 |
| Restore                                 | Web exposes no restore/upload route. [Backup guide](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/docs/self-host/backups.md#L123-L133) and server CLI select registry/default or explicit UUID offline. Native import validates foreign profile paths.                                                                                                                                                                                                                                                                                                                                                           | Do not invent web restore as an existing bypass. Operator can intentionally replace DBs offline; prevent wrong-client target and old-token resurrection by runbook plus authoritative auth state in B. Native/export compatibility needs rehearsal.                                                                                                                                            |
| SSE / NDJSON                            | [SSE handler](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/api/portfolio.rs#L51-L89) subscribes to admitted runtime bus. Admission rechecks scope after handler, before each body chunk and on one-second idle wake. Frontend SSE passes `profileScope`.                                                                                                                                                                                                                                                                                                                                        | Strong existing stream isolation mechanism; live proxy buffering and closure latency untested. New principal suspension must feed this same revocation mechanism. No claim that business-event contents are safe to log.                                                                                                                                                                       |
| Background jobs / caches / derived data | [Runtime construction](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/main_lib.rs#L509-L542) supplies own pool/writer; services and event bus are per runtime. [Scheduler](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/scheduler.rs#L30-L95) captures state; periodic Connect sync checks profile token/plan. [Runtime startup](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/profiles.rs#L296-L350) retains runtimes and starts connected profiles even without a browser. | Browser selection cannot retarget captured work, but browser lock does not stop it. No client suspension/job permission state. Measure retained memory, scheduler load and shared startup bottleneck; no scale guarantee.                                                                                                                                                                      |
| Secrets                                 | Scoped vault wrapper prefixes keys; API validates reserved keys and namespace injection. [Secrets handler](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/api/secrets.rs#L24-L113) can retrieve provider and add-on secrets inside admitted profile.                                                                                                                                                                                                                                                                                                                                              | Shared encrypted vault/master remains trusted; advisor should never receive raw credentials. No new plaintext secret persistence.                                                                                                                                                                                                                                                              |
| Connect/bank authorization callback     | [Profile auth flows](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/profiles/auth_flow.rs#L20-L170) bind PKCE verifier/flow to browser and profile, expire at ten minutes, cancel on selection/revocation; native callback capture once. [Auth bridge](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/features/profiles/auth-bridge.ts#L1-L86) retains flow ID; callback URL parser rejects access-token callback format. Connect session store rechecks grant after transition wait.                                                  | This is a Connect auth flow, not verified direct Czech bank OAuth. A future bank callback must bind principal/profile/provider/consent and reject stale/switched/revoked flows. Never assume returned account ID establishes business ownership.                                                                                                                                               |
| Connect identity and device sync        | [Token lifecycle binding](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/connect/src/token_lifecycle.rs#L689-L738) retrieves server-reported user/team from configured issuer/API; registry reserves issuer/user per profile, rejects silent changes, confirmed rebind cleans cloud state. [Connect store](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/api/connect.rs#L290-L345) coordinates lifecycle.                                                                                                                                        | Cloud team membership differs from local client membership. Source explicitly acknowledges preflight cannot make later cloud membership atomic; external expected-scope contract is unknown. Pairing/restore approvals must bind original local principal and workspace; server holds decrypting sync identity.                                                                                |
| AI conversations / attachments / tools  | [Runtime](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/src/main_lib.rs#L1013-L1047) constructs chat repository/environment from this pool/services/secrets; thread IDs are local DB lookups. [Attachments](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/ai/src/chat/attachments.rs#L59-L115) cached per ChatService/thread. [Chat producer](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/ai/src/chat/mod.rs#L445-L510) is stream-owned; dropping stream drops work/services.                    | User message persists before producer runs. Output stopping cannot undo already sent provider data or committed writes. Thread privacy within shared client/advisor workspace is undefined. Enforce effective role scopes in tools; approved provider may receive history/attachments/tool data. Do not claim full cancellation or no egress after revocation without a network-observed test. |
| MCP                                     | Separate `/mcp`, optional enabled config; selector header/default resolves runtime; profile-local PAT repository checks hash/revocation/expiry on HTTP request, [MCP handler](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/wealthfolio-mcp/src/handler.rs#L49-L61) requires injected context and [tool execution](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/wealthfolio-mcp/src/handler.rs#L129-L184) enforces scopes. Separate session managers per runtime.                                                                                       | Browser logout/profile lock does not revoke PAT. Ongoing MCP stream/tool revocation is unverified; PAT middleware alone checks new requests. Creation needs membership/role ceiling, expiry, principal ownership and revoke-all policy. Runtime starts before PAT auth (SEC-07).                                                                                                               |
| Add-ons                                 | Each runtime AddonService uses configured profile add-on root and DB storage. [Iframe host](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/addons/iframe/addon-iframe-manager.ts#L480-L531) uses `sandbox=allow-scripts`, host API and permission guard. [Network broker](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/crates/core/src/addons/network.rs#L57-L83) checks destination, resolves/pins public IPs, disables redirects; manifest host approvals required. Web installation submits ZIP bytes.                                            | Frontend add-on guard is not a client/advisor API policy. Approved outbound host can receive data legitimately supplied by addon API; restrict catalog/permissions. Test forged addon IDs, storage/events after switch, staged ZIP isolation, host approval escalation and secret injection. No full sandbox/security audit claimed.                                                           |

## Threat scenarios

All attacks use synthetic identifiers and values. Likelihood is not quantified.
These are design threats, with confirmed gaps distinguished from tests still
needed.

| Threat / actor                                                  | Evidence or status                                                             | Required boundary                                                                                            |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Client A lists names or unlocks unprotected B                   | Confirmed paths SEC-02/03; exploit not run                                     | Membership before list/unlock/runtime construction, independently of profile password                        |
| Advisor gains export/write/secrets through hidden UI/API call   | Confirmed no browser action roles, SEC-08                                      | Distinct action checks for API and tool; token scopes cannot exceed caller                                   |
| Stolen JWT or suspended IdP subject keeps installation access   | Confirmed no local token/principal revocation lookup, SEC-04                   | Server-side active-principal/session check, absolute expiry, all-session invalidation                        |
| Stolen scope ID used from another browser                       | Existing owner-plus-scope check; source test rejects                           | Preserve owner binding; deny foreign scope in header and query; no fallback on malformed values              |
| Late callback stores a token into newly selected client         | Existing flow/profile binding and recheck; future identity revocation untested | Bind state/PKCE/principal/profile/provider and revision; cancel old flows                                    |
| Queued import/export/AI/Connect job changes target on UI switch | Fixed runtime captures prevent retarget; test delayed write covers sample      | Preserve fixed target; reauthorize sensitive new commit after suspension; response denial is not rollback    |
| Revoked client continues to receive idle SSE/MCP output         | Browser stream scope recheck confirmed; MCP active stream revocation unknown   | Revoke all derived sessions, close long-lived bodies, deny further tool/data chunks                          |
| Restore resurrects revoked PAT/advisor permissions              | Inferred risk if auth lives only in restored DB; no restore-to-revocation test | Current authoritative permission state survives financial restore; explicit reconciliation before enablement |
| Add-on or injected AI prompt exports data                       | Approved APIs/hosts and provider tools give legitimate access; exploit unknown | Same backend scope ceiling for untrusted code/tools; prompt text never authorization; outbound opt-in        |
| Compromised common server/operator reads all databases          | Confirmed master-key/runtime trust                                             | Disclose operator trust; isolate instance keys/volumes; least host privilege and audited break-glass         |
| Client induces resource exhaustion / profile cooldown           | Creation no operator permission; cold MCP startup before PAT, shared cooldown  | Authorize before allocation; measured quotas/rate limits, isolation and cancellation                         |

## Adversarial acceptance tests

### Concrete baseline two-browser recipe (not executed)

Use a disposable local synthetic instance built at the pinned commit, never an
existing client data directory. Configure the installation password or a mock
allowlisted IdP, a new lab master key/data directory, and disable outbound
Connect/device sync/AI/MCP/add-ons for this first recipe. Bind loopback only.
Browser A and B below are separate cookie jars or separate browser profiles, not
tabs sharing the same session cookie. The profile selector uses two unprotected
synthetic profiles named `Synthetic A` and `Synthetic B`; those names are not
ownership assignments.

Run the repository's existing integration fixture first, once Cargo is
available:

```sh
CONNECT_API_URL=http://test.local cargo test --locked -p wealthfolio-server --test profiles browsers_databases_credentials_and_stale_scopes_are_isolated -- --exact
CONNECT_API_URL=http://test.local cargo test --locked -p wealthfolio-server --test profiles legacy_automatic_access_cannot_bypass_explicit_lock_or_malformed_scope -- --exact
CONNECT_API_URL=http://test.local cargo test --locked -p wealthfolio-server --test profiles admitted_ndjson_stream_delivers_incrementally_and_closes_on_lock -- --exact
```

For the real router/browser rehearsal, use `http://127.0.0.1:8088/api/v1` (the
**lab-configured** address; not an asserted default). JSON requests use
`Content-Type: application/json`; profile commands use that same loopback Host
and Origin. `POST /auth/login` with a synthetic installation password gives each
browser its own cookie. With mock OIDC, use two separately allowlisted subjects
and retain their separate cookies. Capture response JSON in private lab files;
never publish cookies, keys or raw token values. The steps below use symbolic
captured IDs so they do not invent fixed UUIDs.

| Step                   | Exact request sequence and source-expected result                                                                                                                                                                                                                                                                                                              |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1: preparation         | A: POST `/profiles/create_profile` with `{"name":"Synthetic A","avatarId":"default"}`; B: same with `Synthetic B`. Capture returned `id` as `A_ID`, `B_ID`. Existing default may remain, so no missing-scope auto-open assumption.                                                                                                                             |
| 2: enumerate           | A and B: POST `/profiles/get_profile_state` with `{}` and no scope. Both receive all active summaries, including the other's synthetic name/UUID. This demonstrates installation-wide metadata visibility; a future ownership implementation must filter it.                                                                                                   |
| 3: intended selection  | A: POST `/profiles/unlock_profile` with `{"profileId":"A_ID"}`; B: with `B_ID`. Capture `scopeId` as `A_SCOPE`, `B_SCOPE`. GET `/accounts` with each browser's own `x-wf-profile-scope` succeeds in its own runtime. Seed distinct harmless account/setting markers through the normal synthetic UI, then verify those reads.                                  |
| 4: stolen selector     | B: GET `/accounts` with `x-wf-profile-scope: A_SCOPE`. Expect 423 stale/locked error. Repeat with `/events/stream?profileScope=A_SCOPE`. A scope alone does not authorize B.                                                                                                                                                                                   |
| 5: business gap        | B: POST `/profiles/unlock_profile` with `{"profileId":"A_ID"}` and no proof. It succeeds because A is unprotected, returning a **new B-owned** scope. GET `/accounts` with that scope reads synthetic A. The earlier stolen-scope rejection does not imply client ownership.                                                                                   |
| 6: stale grant         | B: reselect `B_ID`; previous B-owned A scope is now stale. GET with it denied. A's separate grant still reads A. This checks current profile switching, not business tenants.                                                                                                                                                                                  |
| 7: locked proof        | A: POST `/profiles/set_profile_password` with `A_SCOPE` and `{"password":"synthetic profile passphrase"}`. Prior A grants revoked. B cannot unlock without proof, but with A's synthetic passphrase **or returned recovery code** it can unlock; no identity relationship is checked. In a future model, even correct B-held proof must not grant A ownership. |
| 8: lock/stream         | Open A's fresh `/events/stream?profileScope=...`, then POST `/profiles/lock_profile` in A browser. Stream ends through body rechecks; subsequent old-scope requests denied. Test fixture above covers NDJSON idle closure and a delayed mutation whose write completes in A after lock.                                                                        |
| 9: local logout replay | Retain an authorized synthetic JWT privately, logout that browser, then present old JWT as Bearer to `/profiles/get_profile_state` and explicitly unlock an unprotected profile. Source predicts installation JWT still accepted until expiry; exact live result must be recorded. Do not confuse revoked current scope with invalidated JWT.                  |

The recipe proves only the executed cases once run. Profile-list/foreign-unlock
results are **source predictions** today; no curl/browser replay was performed
here. Do not run profile deletion, database restore or real outbound
authorization in this baseline recipe. Extend it with T01–T14 for a production
candidate and record DB/file/event side effects as well as responses.

### Production candidate matrix

**Required future evidence, currently unrun.** Establish two synthetic clients
A/B, advisor D, operator O, two browsers for A, one for B, and a controlled IdP
with two issuers that deliberately reuse the same subject string. Create owned
profiles with both protected and unprotected variants, distinct and colliding
financial row IDs, snapshot names, AI thread IDs and add-on IDs. Use local mock
Connect/AI/provider endpoints that record calls without logging tokens or
financial payloads.

Run tests at the real application router/service/persistence boundary and
include positive authorized controls. For denied requests assert both response
denial and **no** B row/file/secret/cache/outbound-call side effect. Do not
accept only a 4xx response; admitted mutations can finish before response denial
today. “Foreign unknown” responses should not disclose existence. Record exact
commit, compiled features, web/Tauri target, configuration and tool versions.

The accepted target is **more than 50 clients on one private server/VM**. The
two-browser recipe establishes boundary behavior, not capacity. Run this matrix
across a 60-client synthetic fleet/profile inventory together with the
quantitative gates in
[isolation.md](isolation.md#more-than-50-clients-on-one-private-servervm).
Option A includes operator/orchestration credentials, gateway mapping,
per-process OS identities, file permissions, keys, volume paths and backup
targets as independent negative-test surfaces. A single trusted root/operator
and host failure domain remain common to all clients.

| Test family                 | Negative cases / expected guarantee                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| T01 Identity ownership      | A cannot list B or pending B metadata, unlock B with no proof, B's valid password/recovery, forged owner/email/Connect user/team, same subject under different issuer, or invitation for another principal. Ownership still required for unprotected B. Current source is expected to fail relevant cases.                                                                                                                                                  |
| T02 Grant/session isolation | B cookie + A scope, scope query parameter on SSE, conflicting query/header, malformed UUID, missing scope, fabricated `wf_browser`, old scope after switch, A browser 2 after revoke-all, expired/old JWT after logout/suspension. Test unauthorized auth-disabled configuration separately; it is not client identity.                                                                                                                                     |
| T03 API read/write          | Foreign account/activity/goal/asset/taxonomy/template IDs in read, create/update/delete/bulk/import, valuation/performance/export filters and query pagination. Mixed A/B bulk input rejected without partial B mutation. Colliding row IDs resolve only within authorized fixed runtime.                                                                                                                                                                   |
| T04 Profile administration  | A cannot create arbitrary workspaces, rename/set/remove B password, recover B, delete B, retry pending B cleanup or enumerate deletion journal. Concurrent invite claims/owner changes fail closed. Native default migration has no automatic owner.                                                                                                                                                                                                        |
| T05 Advisor permissions     | Read D can read only consented A scope; deny writes, export, raw secret retrieval, Connect session restore, device enrollment, provider config, add-on install/network approvals, PAT creation above role ceiling, AI mutation tools, password/recovery/delete, administration. Expired/revoked grant denied in same browser without reload.                                                                                                                |
| T06 Import/upload/temp      | Parse/check/commit A file to B account denied; switch/revoke between preview and commit; traversal/symlink/encoded filename and oversized ZIP/CSV; canceled/deleted profile leaves no downloadable scratch artifacts. Never persist real bank samples.                                                                                                                                                                                                      |
| T07 Export/backup           | A cannot list/download/delete B snapshots, guess B export ticket, reuse ticket under another browser/unlock, or receive remaining chunks after revoke. Same filename in A/B stays local. Expired/discarded ticket denies access; crash cleanup verified.                                                                                                                                                                                                    |
| T08 Restore/offboarding     | Web restore route remains absent unless explicitly implemented; operator dry-run verifies chosen UUID/key. A archive cannot be installed as B by client path. Restoring old A DB never re-enables revoked sessions/PATs/permissions; whole-root and per-profile recovery rehearsed with current registry/auth records. Retention-managed historical backups are not falsely claimed erased.                                                                 |
| T09 SSE / AI streams        | B subscription receives no A events, including errors/import/sync/derived-data events. Lock/suspend during busy stream and idle stream closes without further protected data. Proxy buffering/backpressure checked. AI history/attachment collision and prompt injection cannot change workspace or tool authority; mock egress shows denied providers/tools are unused.                                                                                    |
| T10 Jobs/cache/derived data | Barrier-controlled queued import, calculation, export, broker sync and AI tool: switch browser target while waiting; work remains on original DB, never B. Suspend before sensitive commit: no new disallowed commit/egress. Already-committed behavior documented. Recalculation/cache invalidation/events affect only correct profile; provider failure stays isolated and enrichment preserves user edits.                                               |
| T11 Connect/callback/sync   | Flow from A in B browser/profile, wrong state/verifier/provider, reused or expired callback, switched/locked/suspended scope while token refresh waits; all denied without storing wrong-profile token. Rebind requires explicit connection permission and cleanup. Remote user/team mutation test documents preflight limitation and tests expected-scope rejection where API supports it. Pairing device/restore/snapshot approvals cannot cross clients. |
| T12 MCP                     | A PAT + B header, B PAT without header (default A), A protocol session ID on B, expired/revoked PAT, principal suspension with still-valid PAT, read-only scope invoking write tools, reconnecting idle stream after revoke, tool already executing, no/invalid PAT on cold profile (no heavy runtime/job start after hardening). Test profile-password lock and principal suspension as different policies.                                                |
| T13 Add-ons                 | Host bridge cannot execute another profile's adapter scope; forged addon ID cannot get B storage/secrets. Permission/host escalation, private-address/redirect/DNS rebinding probes, ZIP traversal, stored code injection and event subscription after switch. Read-only advisor cannot grant add-on capabilities. Disabled add-on/provider performs no request.                                                                                            |
| T14 Operations/key boundary | Cross-instance key/cookie/host/volume routing tests for A; distinct keys never reused. Non-owner OS permissions deny DB/vault/scratch access, log scan excludes credentials/financial values. Demonstrate trusted operator can decrypt with correct key so client-facing claims do not promise operator blindness.                                                                                                                                          |

Test requirements use the smallest existing fixtures and middleware, not a new
mock authorization framework that merely repeats implementation logic. Existing
[profile integration test](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/server/tests/profiles.rs#L72-L409)
is a starting point, but its settings-only sample and shared installation users
do not prove the entire matrix. Shared backend work requires both Rust
consumers; adapter changes require
[parity tests](https://github.com/felipebaez/wealthfolio/blob/6ee11b1278eff8b5123280e740fa6983b501952b/apps/frontend/src/adapters/adapter-command-parity.test.ts),
both frontend bundles, relevant crate tests, formatting and Clippy under
repository instructions.

## Validation handoff

**Confirmed:** this audit made no product change and created no implementation
issue. Feasible check results and missing prerequisites are in
[isolation.md](isolation.md#existing-tests-and-validation-limitations) and
[validation.md](security/validation.md). No live IdP, client data, bank
credential, deployed container or active stream was used. Isolation at the owned
runtime/service layer is supported by code; ownership, advisor permission,
complete revocation, recovery semantics and every negative matrix guarantee
remain **unverified at runtime**. Those gaps prevent approval of a shared-client
deployment today.

Proposed implementation dependencies/estimates are SEC-ID → SEC-OWN → SEC-PERM →
SEC-LIFE/SEC-REC → SEC-GATE; SEC-PILOT is an independent option-A operations
path after human direction. Business decisions and overlaps with
operations/bank/architecture audits are listed in the companion record. No
trusted operator, automatic cloud scope contract, or finite client-scale
capacity should be presumed from the word “local-first.”
