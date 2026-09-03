import test from "node:test";
import assert from "node:assert/strict";
import { cleanText, validateRequest } from "./server.mjs";

test("cleanText normalizes whitespace and removes null bytes", () => {
  assert.equal(cleanText(" a\r\n\r\n\r\n\u0000b "), "a\n\n\nb");
});

test("validateRequest requires content", () => {
  assert.throws(() => validateRequest({}), /content_required/);
});

test("validateRequest caps oversized content", () => {
  const value = validateRequest({ content: "x".repeat(200_000) });
  assert.equal(value.content.length, 120_000);
});

test("validateRequest provides a safe default instruction", () => {
  assert.match(validateRequest({ content: "正文" }).instruction, /中文总结/);
});
