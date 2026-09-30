// Documentation consistency only. This does not execute the application.
import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { execFileSync } from "node:child_process";

const baseline = "6ee11b1278eff8b5123280e740fa6983b501952b";
const documents = [
  "docs/audits/2026-09-30/isolation.md",
  "docs/audits/2026-09-30/permissions-threat-model.md",
  "docs/audits/2026-09-30/security/validation.md",
];
let pinnedLinks = 0;
let relativeLinks = 0;
const errors = [];
for (const document of documents) {
  const markdown = readFileSync(document, "utf8");
  if ((markdown.match(/^```/gm) ?? []).length % 2 !== 0) {
    errors.push(`${document}: unbalanced code fences`);
  }
  for (const match of markdown.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
    const target = match[1];
    if (target.startsWith("https://github.com/felipebaez/wealthfolio/blob/")) {
      const parsed = /^https:\/\/github\.com\/felipebaez\/wealthfolio\/blob\/([^/]+)\/([^#]+)(?:#L(\d+)(?:-L(\d+))?)?$/.exec(target);
      if (!parsed || parsed[1] !== baseline) {
        errors.push(`${document}: non-baseline source link ${target}`);
        continue;
      }
      try {
        const source = execFileSync("git", ["show", `${baseline}:${parsed[2]}`], {
          encoding: "utf8",
          stdio: ["ignore", "pipe", "pipe"],
        });
        const lineCount = source.trimEnd().split("\n").length;
        const start = Number(parsed[3] ?? 1);
        const end = Number(parsed[4] ?? start);
        if (start < 1 || end < start || end > lineCount) {
          errors.push(`${document}: invalid line range ${target}`);
        }
        pinnedLinks += 1;
      } catch {
        errors.push(`${document}: source path missing ${target}`);
      }
    } else if (!/^https?:/.test(target)) {
      const [path, fragment] = target.split("#");
      const absolute = resolve(dirname(document), path || ".");
      if (!existsSync(absolute)) {
        errors.push(`${document}: relative target missing ${target}`);
      } else if (fragment && absolute.endsWith(".md")) {
        const headings = readFileSync(absolute, "utf8").match(/^#+ .+$/gm) ?? [];
        const slugs = headings.map((heading) => heading.replace(/^#+ /, "").toLowerCase()
          .replace(/[^\p{L}\p{N}\s_-]/gu, "").replace(/ /g, "-"));
        if (!slugs.includes(fragment)) errors.push(`${document}: heading missing ${target}`);
      }
      relativeLinks += 1;
    }
  }
}
if (errors.length) {
  process.stderr.write(`${errors.join("\n")}\n`);
  process.exitCode = 1;
} else {
  process.stdout.write(`Validated ${documents.length} documents, ${pinnedLinks} pinned source links and ${relativeLinks} local links. No application security tests executed.\n`);
}
