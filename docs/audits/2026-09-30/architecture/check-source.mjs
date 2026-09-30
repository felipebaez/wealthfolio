// Documentation-only audit helper. Run from the repository root.
// Uses source patterns, not a TS parser or runtime integration tests.
import assert from "node:assert/strict";
import { readFileSync, readdirSync, existsSync } from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const baseline = "6ee11b1278eff8b5123280e740fa6983b501952b";
const root = process.cwd();
const read = (p) => readFileSync(path.join(root, p), "utf8");
const walk = (p) =>
  readdirSync(p, { withFileTypes: true }).flatMap((e) => {
    const item = path.join(p, e.name);
    return e.isDirectory()
      ? walk(item)
      : /\.(ts|tsx)$/.test(e.name) && !/\.(test|spec)\./.test(e.name)
        ? [item]
        : [];
  });
const commandsIn = (files) =>
  new Set(
    files.flatMap((file) =>
      [
        ...readFileSync(file, "utf8").matchAll(/invoke(?:<[^>]+>)?\(\s*['"`]([a-zA-Z0-9_]+)['"`]/g),
      ].map((m) => m[1]),
    ),
  );
const adapterRoot = path.join(root, "apps/frontend/src/adapters");
const featureRoot = path.join(root, "apps/frontend/src/features");
const featureFiles = readdirSync(featureRoot, { withFileTypes: true }).flatMap((e) => {
  const p = path.join(featureRoot, e.name, "adapters");
  return e.isDirectory() && existsSync(p) ? walk(p) : [];
});
const shared = walk(path.join(adapterRoot, "shared"));
const web = commandsIn([...shared, ...walk(path.join(adapterRoot, "web")), ...featureFiles]);
const tauri = commandsIn([...shared, ...walk(path.join(adapterRoot, "tauri")), ...featureFiles]);
const webSource = read("apps/frontend/src/adapters/web/core.ts");
const mappingStart = webSource.indexOf("export const COMMANDS:");
const mappingEnd = webSource.indexOf("\n};", mappingStart);
assert.ok(mappingStart >= 0 && mappingEnd > mappingStart, "COMMANDS source block missing");
const mappingBlock = webSource.slice(mappingStart, mappingEnd);
// Includes literal method/path mapping keys only.
const mapped = new Set(
  [...mappingBlock.matchAll(/^\s*([a-zA-Z0-9_]+):\s*\{\s*(?:\n\s*)?method:/gm)].map((m) => m[1]),
);
const registered = new Set(
  [...read("apps/tauri/src/lib.rs").matchAll(/commands::[a-z_]+::([a-zA-Z0-9_]+)/g)].map(
    (m) => m[1],
  ),
);
const missingWeb = [...web].filter((c) => !mapped.has(c));
const missingTauri = [...tauri].filter((c) => !registered.has(c));
assert.deepEqual(missingWeb, [], "Static web mapping gaps");
assert.deepEqual(missingTauri, [], "Static Tauri registration gaps");
console.log(
  JSON.stringify({
    staticCommands: {
      webInvoked: web.size,
      tauriInvoked: tauri.size,
      mapped: mapped.size,
      registered: registered.size,
      missingWeb,
      missingTauri,
    },
  }),
);

let pinnedLinks = 0;
let localLinks = 0;
for (const doc of ["architecture.md", "architecture-validation.md"]) {
  const relative = `docs/audits/2026-09-30/${doc}`;
  const content = read(relative);
  const defs = new Set([...content.matchAll(/^\[([EX]\d+)\]:/gm)].map((m) => m[1]));
  for (const m of content.matchAll(/\[([EX]\d+)\](?!:)/g))
    assert.ok(defs.has(m[1]), `Undefined evidence ${m[1]} in ${doc}`);
  for (const m of content.matchAll(
    /https:\/\/github\.com\/felipebaez\/wealthfolio\/blob\/([^/\s]+)\/([^\s)#]+)(?:#L(\d+))?/g,
  )) {
    assert.equal(m[1], baseline, `Unpinned source link in ${doc}`);
    const source = execFileSync("git", ["show", `${baseline}:${m[2]}`], { encoding: "utf8" });
    if (m[3]) assert.ok(Number(m[3]) <= source.split("\n").length, `Invalid line ${m[2]}:${m[3]}`);
    pinnedLinks += 1;
  }
  for (const m of content.matchAll(/\]\((?!https?:|#)([^)#]+)(?:#[^)]*)?\)/g)) {
    assert.ok(
      existsSync(path.resolve(root, path.dirname(relative), m[1])),
      `Missing local link ${m[1]}`,
    );
    localLinks += 1;
  }
}
console.log(JSON.stringify({ documentation: { pinnedLinks, localLinks, result: "pass" } }));
console.log(
  "Static source/link checks only; no DTO semantics, backend authorization, network silence, bank compatibility, build, or runtime guarantee.",
);
