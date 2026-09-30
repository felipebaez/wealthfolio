"""Read-only audit documentation checks, not application/runtime validation."""

from pathlib import Path
import json
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[4]
AUDIT = ROOT / "docs/audits/2026-09-30"
BASELINE = "6ee11b1278eff8b5123280e740fa6983b501952b"
source_cache = {}
errors = []
source_links = 0
local_links = 0
documents = list(AUDIT.rglob("*.md"))


def slug(heading):
    heading = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", heading)
    return "".join(
        c for c in heading.lower()
        if c in " _-" or unicodedata.category(c)[0] in "LN"
    ).replace(" ", "-")


for path in documents:
    content = path.read_text()
    if len(re.findall(r"^```", content, re.M)) % 2:
        errors.append(f"{path.relative_to(ROOT)}: unbalanced code fence")
    for match in re.finditer(
        r"https://github.com/felipebaez/wealthfolio/blob/([^/\s]+)/([^\s)#>]+)"
        r"(?:#L(\d+)(?:-L(\d+))?)?", content
    ):
        revision, source_path, first, last = match.groups()
        # Links to the evolving audit branch are not application source evidence.
        if source_path.startswith("docs/audits/") and revision == "audit":
            continue
        if revision != BASELINE:
            errors.append(f"{path.name}: unpinned source {match.group(0)}")
            continue
        if source_path not in source_cache:
            result = subprocess.run(
                ["git", "show", f"{BASELINE}:{source_path}"], cwd=ROOT,
                text=True, capture_output=True, check=False,
            )
            source_cache[source_path] = result.stdout if result.returncode == 0 else None
        source = source_cache[source_path]
        if source is None:
            errors.append(f"{path.name}: absent source {source_path}")
        elif first and not (1 <= int(first) <= int(last or first) <= len(source.splitlines())):
            errors.append(f"{path.name}: invalid source range {match.group(0)}")
        source_links += 1
    definitions = dict(re.findall(r"^\[([^]]+)\]:\s*\n?\s*(\S+)", content, re.M))
    targets = re.findall(r"\[[^]]+\]\(([^)]+)\)", content) + list(definitions.values())
    for target in targets:
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        target = target.strip("<>")
        local, _, anchor = target.partition("#")
        destination = path.parent / local if local else path
        if not destination.exists():
            errors.append(f"{path.name}: missing local link {target}")
        elif anchor and destination.suffix == ".md":
            headings = re.findall(r"^#+ (.+)$", destination.read_text(), re.M)
            if anchor not in [slug(h) for h in headings]:
                errors.append(f"{path.name}: missing heading {target}")
        local_links += 1
    for evidence in re.findall(r"\[(E\d+|X\d+|KB-\d+|RB-\d+|CB-\d+|CS-\d+|AG-\d+)\](?!:)", content):
        if evidence not in definitions:
            errors.append(f"{path.name}: undefined evidence {evidence}")

state = json.loads((AUDIT / "index.json").read_text())
assert state["business_requirements"] == {
    "target_clients": ">50", "infrastructure": "single private server or VM"
}
assert state["parent"]["chat_name"] == "Wealth Command Center"
assert state["consolidation"]["number"] == 8
assert len(state["backlog"]) == len({x["number"] for x in state["backlog"]}) == 16
assert all(x["chat_id"] is None and x["status"] == "not-started" and x["parent_linked"] for x in state["backlog"])
if errors:
    raise SystemExit("\n".join(errors))
print(json.dumps({
    "documents": len(documents), "pinned_source_links": source_links,
    "unique_source_paths": len(source_cache), "local_links": local_links,
    "backlog_links": 16, "result": "pass",
    "scope": "Documentation paths/ranges/references/state only; not runtime or external-site validation."
}))
