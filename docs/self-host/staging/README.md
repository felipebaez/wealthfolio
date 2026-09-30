# Development computer staging

This installation belongs to fork issue
[#7](https://github.com/felipebaez/wealthfolio/issues/7). Use synthetic data
only. Profiles are application profiles sharing an installation; they do not
establish secure multi-client tenancy.

## Recorded installation

See [deployment-state.json](deployment-state.json) for the source/deployed
revision, image, issue/chat status and last synchronization. Runtime files and
protected credentials live outside Git at:

```text
/Users/felipebaez/Development/Wealthfolio-staging-runtime
```

The dedicated worktree is `/Users/felipebaez/Development/Wealthfolio-staging`,
branch `deploy/docker-staging`. The main checkout's audit changes are unrelated.
The running URL is <http://localhost:18088> (also <http://127.0.0.1:18088>).

**Architecture impact:** reuse the production Dockerfile, Axum web API, password
login, profiles, encrypted secret store and SQLite. Application code, provider
settings semantics, events, business logic and user-edit precedence do not
change. The staging bridge disables outbound IP masquerading; localhost port
publishing remains enabled. Native ARM64 GitHub Actions builds transfer only
repository source and image artifacts; financial data, credentials and local
configuration stay on this computer.

## Runtime and prerequisites

Installed through Homebrew: `docker`, `docker-compose`, `docker-buildx`,
`colima`, `qemu`, and `argon2`. Docker plugins use Homebrew's CLI-plugin
directory; existing Docker configuration keys are preserved. No existing Docker
daemon/resources were present at initial inspection. Other listeners were
preserved.

This machine is macOS 27 in an Apple M2 virtual machine, 4 CPU cores, 16 GiB
RAM, and approximately 64 GiB initially free. `kern.hv_support=0`: Apple VZ
refused nested virtualization. The isolated Colima profile uses ARM64 QEMU
software emulation (3 CPUs, 8 GiB memory, 48 GiB sparse data disk). Source
builds in this runtime will be slow. The abandoned, empty VZ profile
`wealthfolio-staging` is preserved; it contains no application data. The working
profile is `wealthfolio-staging-qemu`, Docker context
`colima-wealthfolio-staging-qemu`. The new Colima installation also has a Lima
override at `~/.colima/_lima/_config/override.yaml` that ignores guest port 53,
preventing Lima from publishing its guest DNS resolver on the host. No existing
Colima configuration was replaced.

Wealthfolio's production Dockerfile supports both ARM64 and AMD64. Rosetta does
not remove the requirement for an available Apple hypervisor.

Start the VM without changing the active global Docker context:

```bash
colima start --profile wealthfolio-staging-qemu --activate=false
```

First creation used these settings:

```bash
colima start --profile wealthfolio-staging-qemu --cpu 3 --memory 8 --disk 48 \
  --vm-type qemu --mount-type 9p --cpu-type max --activate=false \
  --ssh-config=false \
  --mount /Users/felipebaez/Development/Wealthfolio-staging-runtime:w
```

No system sleep or login settings are changed. `restart: unless-stopped`
restarts an already-running service after the Docker daemon/VM restarts,
provided it was not deliberately stopped. A computer reboot still requires
starting Colima and then staging. Computer sleep suspends availability; this is
not an always-on server. Do not use `brew services start colima` as a shortcut:
it would start a default profile, not necessarily this named one. Any future
login/sleep change requires the user's agreement.

## Commands

Run from the dedicated worktree. All commands explicitly use the staging Docker
context and Compose project. Python 3 and Homebrew Argon2 are required.

```bash
cd /Users/felipebaez/Development/Wealthfolio-staging
python3 docs/self-host/staging/staging.py start
python3 docs/self-host/staging/staging.py stop
python3 docs/self-host/staging/staging.py status
python3 docs/self-host/staging/staging.py logs
python3 docs/self-host/staging/staging.py backup
```

`stop` preserves the container, named volume and all backups. On this image,
Docker stop reached its 60-second timeout and terminated the process (exit 137).
Backups include SQLite WAL state after the process stops; the isolated restore
passed. Allow this shutdown delay plus startup health checks for backup/update
downtime. Logs are bounded to three files of 10 MiB. `status` displays Compose
health and non-secret deployment metadata. Do not publish `docker inspect` or
expanded `compose config` output: container environment contains the
authentication hash. The helper never prints credentials or hashes. Initial
setup (`init`) is only for a fresh directory and refuses to overwrite an
existing configuration.

Retrieve the password locally, without putting it into chat or GitHub:

```bash
cat /Users/felipebaez/Development/Wealthfolio-staging-runtime/secrets/login-password
```

The login is password-only. Generated password/key files have mode `0400`; their
parent directory has mode `0700`. `deployment.env` has mode `0600`; the Argon2id
hash is single-quoted to preserve its dollar signs through Compose. The server
runs as image UID/GID `1000:1000`. The 9p guest mount preserves host UID 501, so
the helper copies the master key through stdin into a separate named `keys`
volume, owned by `1000:1000` with mode `0400`. Compose mounts it read-only at
`/run/secrets`; keys remain distinct from `/data`. Subsequent starts refuse a
changed key. Host key permissions are never relaxed.

For this localhost HTTP URL, session cookies intentionally omit `Secure`, but
retain `HttpOnly`, `SameSite=Lax`, and `Path=/api`. Explicit allowed origins
cover only localhost and 127.0.0.1 on the selected port. Docker publishes only
on `127.0.0.1`. This configuration is not appropriate for public HTTP
deployment.

## Reproducible build and update

Select an exact commit available in the fork/local Git history. Local builds
export a clean `git archive` into the runtime directory; uncommitted checkout
files and local `.env` files are not included. Build the actual fork Dockerfile:

```bash
python3 docs/self-host/staging/staging.py deploy FULL_COMMIT_SHA
```

On this emulated machine prefer the native ARM64 artifact workflow. It performs
the same production Docker build without Connect build arguments. Nothing is
pushed to a container registry. Use authenticated `gh` and explicitly name the
fork. Until the deployment PR is merged, use `--ref deploy/docker-staging`:

```bash
gh workflow run staging-image.yml --repo felipebaez/wealthfolio \
  --ref deploy/docker-staging -f revision=FULL_COMMIT_SHA
gh run list --repo felipebaez/wealthfolio --workflow staging-image.yml
gh run view RUN_ID --repo felipebaez/wealthfolio
gh run download RUN_ID --repo felipebaez/wealthfolio \
  --name staging-image-FULL_COMMIT_SHA \
  --dir /Users/felipebaez/Development/Wealthfolio-staging-runtime/releases/FULL_COMMIT_SHA-image
python3 docs/self-host/staging/staging.py deploy FULL_COMMIT_SHA \
  --image-archive /Users/felipebaez/Development/Wealthfolio-staging-runtime/releases/FULL_COMMIT_SHA-image/staging-image.tar.gz
```

Download into a fresh directory. The helper verifies the archive checksum,
recorded source revision and Docker image revision label before touching the
running service. Image tags are `wealthfolio-staging:FULL_COMMIT_SHA`; previous
images are retained. A checksum detects corruption, not artifact authenticity:
obtain the artifact only from the authenticated fork workflow/run.

Every update first records the old revision and stops the current server for a
complete consistent backup. The backup includes all `/data` contents (registry,
profile databases, WAL files, encrypted vault, profile keys, add-ons and managed
snapshots), matching Compose/env/metadata and protected recovery key/password
files. The server resumes after backup; deploy then stops it before replacement.
Only one process owns the live volume/vault. Migrations run using the existing
server startup behavior. If the new image fails health checks, preserve its data
and use the compatible pre-update snapshot; never assume the old image can read
newly migrated databases. A failed update is reported as a failure, not success.

The full source SHA, image ID, last update and pre-update snapshot path are in
runtime `deployment.json`. Keep the issue/chat record in sync when changing the
deployment; do not commit the runtime configuration or protected key files.

## Backup, isolated restore and rollback

Backups are directories under the runtime `backups/`. They are private recovery
bundles, not portable password-encrypted exports. The keys in `secrets/` are
separate files from `data.tar.gz`, with private file/directory permissions. Copy
recovery bundles to independently protected storage for protection against loss
of this machine. No automatic backup/image/volume deletion is implemented.

The master key derives session signing and vault/database encryption keys. The
vault also stores profile key material. Losing or changing the master key can
make the encrypted databases and saved credentials unrecoverable. Preserve the
matching key together with every compatible recovery point, in protected
storage.

Restore always creates a NEW directory, Compose project, port and named volume;
it refuses existing destinations/projects and verifies checksums before loading.
The same in-container `/data` paths preserve registry compatibility.

```bash
python3 docs/self-host/staging/staging.py \
  --root /Users/felipebaez/Development/Wealthfolio-staging-runtime/restore-UNIQUE \
  restore /Users/felipebaez/Development/Wealthfolio-staging-runtime/backups/BACKUP_ID \
  --project wealthfolio-staging-restore-UNIQUE --port 18089
```

Verify login, accounts, activity counts and portfolio views in the restored
instance. The source staging volume remains untouched. Stop a verified
disposable instance with the same helper `--root RESTORE_DIRECTORY stop`. Do not
remove its volume until any wanted evidence/data has been retained and deletion
authorized.

Rollback uses the recorded prior image AND its compatible pre-update bundle,
using exactly the same isolated restore mechanism:

```bash
python3 docs/self-host/staging/staging.py \
  --root /Users/felipebaez/Development/Wealthfolio-staging-runtime/rollback-UNIQUE \
  rollback /ABSOLUTE/PATH/TO/PRE_UPDATE_BACKUP \
  --project wealthfolio-staging-rollback-UNIQUE --port 18090
```

The prior image must still exist in the Docker context; otherwise reload its
saved authenticated artifact. Inspect the old snapshot at the alternate URL
before stopping a failed newer deployment. This intentionally keeps both data
sets available. Use the alternate recovered URL as the staging URL and update
issue/deployment records; do not destructively overwrite the newer volume.

The server's UI-managed and password-protected portable backups are also
available; see [backups.md](../backups.md). They serve a different purpose from
this complete stopped-installation recovery bundle.

## Optional rapid development

The supplied `compose.dev.yml` builds a production image. It does not provide
source hot reload and disables authentication. Do not apply it to staging.

The supported reload workflow is native `pnpm dev:web`: Vite reloads frontend
source; the runner starts `cargo run`, so restart it for Rust changes. Use a
separate checkout, fresh installation root/key, separate ports and `.env.web`;
see [the server README](../../../apps/server/README.md) and `.env.web.example`.
There is no existing useful Docker hot-reload workflow to reuse, so none is
invented here. This opt-in workflow is not needed for staging acceptance. On
this guest, Docker source builds are slow; hardware/nested-virtualization access
would improve turnaround, but changing the VM host is outside this installation.

## Features and troubleshooting

Manual accounts, cash activities, CSV imports, manually priced holdings and
portfolio calculations do not need external credentials. Built-in market-data
providers can normally obtain some quotes without a key; keyed providers require
their own credentials. Staging disables providers and outbound NAT; a direct
public-IP HTTP probe timed out; quote search, automatic enrichment, FX/history
and live prices are limited. Manual input/price overrides support synthetic test
flows.

Connect/broker/device-sync need Connect configuration/subscription/credentials;
none are configured. AI chat requires an external provider or a separately
configured local provider; none are configured and no synthetic data is sent to
AI. OIDC and MCP are also disabled. Add-ons with external network dependencies
will not function with this staging network configuration.

- If Docker is unreachable, start the named Colima profile and inspect
  `colima status --profile wealthfolio-staging-qemu`. Preserve profiles/volumes.
- If health fails, use `status` and `logs`; do not dump secret environment
  values.
- If login fails after changing an env file, check hash quoting and restart.
- If registry/database encryption errors occur, stop staging and restore the
  complete matching bundle/key; follow
  [registry recovery](../backups.md#profile-registry-startup-failures).
- If a port is occupied, preserve the other service. Select a free port and
  update both `deployment.env` and runtime metadata; Compose derives origins
  from it.
- The VM's slow emulated CPU can make startup/imports slower than native
  hardware. Keep the issue In Progress when required validation is still
  incomplete.

See [validation.md](validation.md) for actual passed/failed/not-run checks.

Run recovery safety checks without Docker or real credentials:

```bash
python3 -m unittest discover -s docs/self-host/staging -p '*_test.py' -v
```
