#!/usr/bin/env python3
"""Local-only staging operations. No passwords or keys are printed by default."""
import argparse
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import socket
import subprocess
import sys
import tarfile

DEFAULT_ROOT = Path.home() / "Development/Wealthfolio-staging-runtime"
CONTEXT = "colima-wealthfolio-staging-qemu"
PROJECT = "wealthfolio-staging"
TEMPLATE = Path(__file__).with_name("compose.yml")


def run(args, **kwargs):
    return subprocess.run([str(arg) for arg in args], check=True, **kwargs)


def docker(root, *args, **kwargs):
    context = metadata(root).get("docker_context", CONTEXT)
    return run(["docker", "--context", context, *args], **kwargs)


def metadata(root):
    path = root / "deployment.json"
    return json.loads(path.read_text()) if path.exists() else {}


def save_metadata(root, data):
    data["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    path = root / "deployment.json"
    path.write_text(json.dumps(data, indent=2) + "\n")
    path.chmod(0o600)


def compose(root, *args, **kwargs):
    return docker(root, "compose", "--project-name", metadata(root).get("project", PROJECT),
                  "--project-directory", root, "--env-file", root / "deployment.env",
                  "-f", root / "compose.yml", *args, **kwargs)


def init(root, port):
    if (root / "deployment.env").exists():
        raise ValueError("Already initialized; existing keys and configuration were preserved")
    with socket.socket() as check:
        check.bind(("127.0.0.1", port))
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    root.chmod(0o700)
    for name in ("secrets", "backups", "releases", "evidence"):
        (root / name).mkdir(exist_ok=True, mode=0o700)
    password = secrets.token_urlsafe(32)
    password_hash = run(["argon2", secrets.token_hex(16), "-id", "-t", "3", "-m", "16", "-p", "1", "-e"],
                        input=password.encode(), stdout=subprocess.PIPE).stdout.decode().strip()
    for name, value in (("login-password", password),
                        ("master-key", base64.b64encode(secrets.token_bytes(32)).decode())):
        path = root / "secrets" / name
        path.write_text(value + "\n")
        path.chmod(0o400)
    (root / "deployment.env").write_text(
        "WF_IMAGE=wealthfolio-staging:unbuilt\n"
        f"WF_PORT={port}\nWF_AUTH_PASSWORD_HASH='{password_hash}'\n")
    (root / "deployment.env").chmod(0o600)
    shutil.copyfile(TEMPLATE, root / "compose.yml")
    save_metadata(root, {"project": PROJECT, "docker_context": CONTEXT,
                        "port": port, "image": None, "revision": None})
    print(f"Initialized {root}; retrieve login with: cat {root}/secrets/login-password")


def prepare_key(root):
    info = metadata(root)
    volume = f"{info.get('project', PROJECT)}_keys"
    docker(root, "volume", "create", "--label", f"com.docker.compose.project={info.get('project', PROJECT)}",
           "--label", "com.docker.compose.volume=keys", volume, stdout=subprocess.PIPE)
    # The 9p guest mount keeps host UID 501; the app UID 1000 cannot read a
    # protected host file. Copy through stdin into a separate restricted volume.
    # Refuse a different existing key: changing it would strand encrypted data.
    script = ("umask 077; cat > /tmp/input-key; "
              "if [ -e /keys/wealthfolio-key ]; then "
              "cmp -s /tmp/input-key /keys/wealthfolio-key || exit 1; "
              "else cp /tmp/input-key /keys/wealthfolio-key; "
              "chown 1000:1000 /keys/wealthfolio-key; chmod 400 /keys/wealthfolio-key; fi")
    docker(root, "run", "--rm", "--interactive", "--user", "0:0", "--network", "none",
           "--volume", f"{volume}:/keys", "--tmpfs", "/tmp", "--entrypoint", "sh",
           info["image"], "-ec", script, input=(root / "secrets/master-key").read_bytes())


def current_container(root):
    return compose(root, "ps", "--all", "--quiet", "wealthfolio", stdout=subprocess.PIPE).stdout.decode().strip()


def backup(root):
    info = metadata(root)
    if not info.get("image"):
        raise ValueError("No deployed image to back up")
    container = current_container(root)
    if not container:
        raise ValueError("No staging container to back up")
    running = docker(root, "inspect", "--format", "{{.State.Running}}", container,
                     stdout=subprocess.PIPE).stdout.decode().strip() == "true"
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    bundle = root / "backups" / stamp
    bundle.mkdir(mode=0o700)
    try:
        compose(root, "stop", "--timeout", "60", "wealthfolio")
        with (bundle / "data.tar.gz").open("wb") as output:
            docker(root, "run", "--rm", "--user", "0:0", "--network", "none",
                   "--volumes-from", f"{container}:ro", "--entrypoint", "tar", info["image"],
                   "czf", "-", "-C", "/data", ".", stdout=output)
        for name in ("deployment.env", "deployment.json", "compose.yml"):
            shutil.copyfile(root / name, bundle / name)
        shutil.copytree(root / "secrets", bundle / "secrets")
        sums = {}
        for path in bundle.rglob("*"):
            if path.is_file():
                path.chmod(0o600)
                sums[str(path.relative_to(bundle))] = hashlib.sha256(path.read_bytes()).hexdigest()
            elif path.is_dir():
                path.chmod(0o700)
        (bundle / "checksums.json").write_text(json.dumps(sums, indent=2) + "\n")
        (bundle / "checksums.json").chmod(0o600)
    finally:
        if running:
            compose(root, "start", "wealthfolio")
    print(f"Backup (contains protected recovery keys): {bundle}")
    return bundle


def verify_bundle(bundle):
    sums = json.loads((bundle / "checksums.json").read_text())
    required = {"data.tar.gz", "deployment.env", "deployment.json", "compose.yml",
                "secrets/master-key", "secrets/login-password"}
    if not required.issubset(sums):
        raise ValueError("Incomplete backup")
    for name, expected in sums.items():
        path = Path(name)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("Unsafe backup file path")
        if hashlib.sha256((bundle / path).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Backup checksum failed: {name}")
    with tarfile.open(bundle / "data.tar.gz") as archive:
        for member in archive.getmembers():
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts or member.issym() or member.islnk():
                raise ValueError("Unsafe data archive member")


def restore(root, bundle, project, port):
    """Restore only into a NEW project/volume. Never overwrite current state."""
    verify_bundle(bundle)
    if not project.startswith("wealthfolio-staging-") or project == PROJECT:
        raise ValueError("Use a distinct wealthfolio-staging-* project name")
    if root.exists():
        raise ValueError("Restore destination must not exist; preserved existing files")
    existing = docker(bundle, "volume", "ls", "--filter", f"label=com.docker.compose.project={project}",
                      "--quiet", stdout=subprocess.PIPE).stdout.decode().strip()
    named = docker(bundle, "volume", "ls", "--filter", f"name=^{project}_data$",
                   "--quiet", stdout=subprocess.PIPE).stdout.decode().strip()
    if existing or named:
        raise ValueError("Restore project already has volumes; choose a fresh project")
    with socket.socket() as check:
        check.bind(("127.0.0.1", port))
    root.mkdir(parents=True, mode=0o700)
    for name in ("compose.yml", "deployment.env", "deployment.json"):
        shutil.copyfile(bundle / name, root / name)
        (root / name).chmod(0o600)
    shutil.copytree(bundle / "secrets", root / "secrets")
    info = metadata(root)
    info.update(project=project, port=port, restored_from=str(bundle))
    save_metadata(root, info)
    lines = (root / "deployment.env").read_text().splitlines()
    (root / "deployment.env").write_text("\n".join(
        f"WF_PORT={port}" if line.startswith("WF_PORT=") else line for line in lines) + "\n")
    (root / "backups").mkdir(mode=0o700)
    prepare_key(root)
    compose(root, "create", "wealthfolio")
    container = current_container(root)
    with (bundle / "data.tar.gz").open("rb") as source:
        docker(root, "run", "--rm", "--interactive", "--user", "0:0", "--network", "none",
               "--volumes-from", container, "--entrypoint", "tar", info["image"],
               "xzf", "-", "-C", "/data", stdin=source)
    compose(root, "up", "--detach", "--wait", "--wait-timeout", "300")
    print(f"Restored {project} at http://localhost:{port}; original data remains intact")


def deploy(root, revision, image=None):
    """Build/load first, snapshot old state, then replace the one server."""
    repository = Path(__file__).resolve().parents[3]
    commit = run(["git", "-C", repository, "rev-parse", "--verify", f"{revision}^{{commit}}"],
                 stdout=subprocess.PIPE).stdout.decode().strip()
    tag = f"wealthfolio-staging:{commit}"
    if image:
        image = Path(image).resolve()
        expected = image.with_name(image.name + ".sha256").read_text().split()[0]
        if hashlib.sha256(image.read_bytes()).hexdigest() != expected:
            raise ValueError("Image archive checksum mismatch")
        recorded = image.with_name("source-revision.txt").read_text().strip()
        if recorded != commit:
            raise ValueError("Image artifact source differs from selected revision")
        docker(root, "load", "--input", image)
    else:
        source = root / "releases" / commit
        if not source.exists():
            source.mkdir(parents=True, mode=0o700)
            archive = run(["git", "-C", repository, "archive", commit], stdout=subprocess.PIPE).stdout
            run(["tar", "xf", "-", "-C", source], input=archive)
        docker(root, "build", "--platform", "linux/arm64", "--tag", tag,
               "--label", f"org.opencontainers.image.revision={commit}",
               "--label", "org.opencontainers.image.source=https://github.com/felipebaez/wealthfolio",
               source)
    label = docker(root, "image", "inspect", "--format",
                   '{{index .Config.Labels "org.opencontainers.image.revision"}}', tag,
                   stdout=subprocess.PIPE).stdout.decode().strip()
    if label != commit:
        raise ValueError("Image revision label mismatch")
    info = metadata(root)
    if info.get("image") and current_container(root):
        info["pre_update_backup"] = str(backup(root))
        compose(root, "stop", "--timeout", "60", "wealthfolio")
    env = root / "deployment.env"
    env.write_text("\n".join(f"WF_IMAGE={tag}" if line.startswith("WF_IMAGE=") else line
                             for line in env.read_text().splitlines()) + "\n")
    info.update(image=tag, revision=commit, image_id=docker(root, "image", "inspect", "--format", "{{.Id}}", tag,
                                                        stdout=subprocess.PIPE).stdout.decode().strip())
    save_metadata(root, info)
    prepare_key(root)
    compose(root, "up", "--detach", "--wait", "--wait-timeout", "300")
    print(f"Deployed {commit} at http://localhost:{info['port']}")


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    setup = sub.add_parser("init")
    setup.add_argument("--port", type=int, default=18088)
    for command in ("start", "stop", "status", "logs", "backup"):
        sub.add_parser(command)
    build = sub.add_parser("deploy")
    build.add_argument("revision")
    build.add_argument("--image-archive", type=Path)
    for command in ("restore", "rollback"):
        load = sub.add_parser(command, help="Start compatible snapshot + image in a NEW project")
        load.add_argument("bundle", type=Path)
        load.add_argument("--project", required=True)
        load.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == "init":
        init(root, args.port)
    elif args.command == "start":
        prepare_key(root)
        compose(root, "up", "--detach", "--wait", "--wait-timeout", "300")
    elif args.command == "stop":
        compose(root, "stop", "--timeout", "60")
    elif args.command == "status":
        compose(root, "ps", "--all")
        print(json.dumps(metadata(root), indent=2))
    elif args.command == "logs":
        compose(root, "logs", "--tail", "100", "--follow")
    elif args.command == "backup":
        backup(root)
    elif args.command == "deploy":
        deploy(root, args.revision, args.image_archive)
    else:
        restore(root, args.bundle.resolve(), args.project, args.port)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Staging operation failed: {error}", file=sys.stderr)
        sys.exit(1)
