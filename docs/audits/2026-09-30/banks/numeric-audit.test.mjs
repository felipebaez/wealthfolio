// Audit-only checks: executes extracted baseline functions, not a bank schema or importer.
// Run from repository root: node --test docs/audits/2026-09-30/banks/numeric-audit.test.mjs
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import assert from "node:assert/strict";
import test from "node:test";

const path = "apps/frontend/src/pages/activity/import/utils/review-draft-utils.ts";
const source = readFileSync(path, "utf8");
const start = source.indexOf("export function parseSignedNumericValue(");
const end = source.indexOf("export function toNumber(");
assert.ok(start >= 0 && end > start, "Extraction boundaries must match baseline source");
const code = stripTypeScriptTypes(source.slice(start, end));
const { parseSignedNumericValue: signed, parseNumericValue: absolute } = await import(
  `data:text/javascript;base64,${Buffer.from(code).toString("base64")}`
);

test("explicit Czech-style separators preserve decimal text", () => {
  assert.equal(signed("1.234,56", ",", "."), "1234.56");
  assert.equal(signed("-1 234,56", ",", " "), "-1234.56");
  assert.equal(signed("1\u00a0234,56", ",", " "), "1234.56");
});
test("precision stays textual through numeric normalization", () => {
  assert.equal(signed("9007199254740993,01", ",", "none"), "9007199254740993.01");
});
test("direction is preserved only by the signed helper", () => {
  assert.equal(signed("-123,45", ",", "none"), "-123.45");
  assert.equal(absolute("-123,45", ",", "none"), "123.45");
});
test("malformed nonnumeric text is silently removed at baseline", () => {
  assert.equal(signed("1foo2", ".", "none"), "12");
});
test("repeated decimal separators are silently joined at baseline", () => {
  assert.equal(signed("1,2,3", ",", "none"), "12.3");
});
test("none still removes the opposite separator at baseline", () => {
  assert.equal(signed("1,234.56", ".", "none"), "1234.56");
});
test("holdings CASH accumulation uses binary arithmetic at baseline", () => {
  const holdings = readFileSync(
    "apps/frontend/src/pages/activity/import/utils/holdings-import-utils.ts",
    "utf8",
  );
  assert.ok(holdings.includes("String(existingAmount + newAmount)"));
  assert.equal(String(parseFloat("0.1") + parseFloat("0.2")), "0.30000000000000004");
});
