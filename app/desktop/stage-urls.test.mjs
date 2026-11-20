// stageUrls: a `kind: base` pack's media in the content depot, shared with base once, no DLC entry (decision 753). `npm test`
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { after, test } from "node:test";
import { cacheName, shippedName } from "./resolve.mjs";
import { stageUrls } from "./stage-urls.mjs";

const tmp = mkdtempSync(path.join(tmpdir(), "trivia-stage-urls-"));
after(() => rmSync(tmp, { recursive: true, force: true }));
const put = (rel, obj) => {
  const file = path.join(tmp, rel);
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, JSON.stringify(obj));
};
const SHARED = "https://upload.wikimedia.org/a/ab/Shared.jpg";
const CLIP = "https://upload.wikimedia.org/a/ab/Clip.ogg";
const ONLY_BASE_PACK = "https://upload.wikimedia.org/a/ab/Chinese.jpg";
const ONLY_DLC = "https://upload.wikimedia.org/a/ab/Dlc.jpg";
const q = (id, file_url, extra = {}) => ({ id, status: "approved", media: { type: file_url.endsWith(".ogg") ? "audio" : "image", file_url, ...extra } });

put("bundles.json", {
  bundles: [
    { id: "base", kind: "base" },
    { id: "chinese-base", kind: "base" },
    { id: "colombia", kind: "region" },
  ],
});
put("pool.json", { questions: [q("b1", SHARED), q("b2", CLIP, { excerpt: { start: 1, end: 5 } })] });
// The copy: same media record as its source; pool.en.json only, no es pool.
put("bundles/chinese-base/pool.en.json", { questions: [q("c1", SHARED), q("c2", CLIP, { excerpt: { start: 1, end: 5 } }), q("c3", ONLY_BASE_PACK)] });
put("bundles/chinese-base/pool.zh-Hans.json", { questions: [q("c1", SHARED), q("c3", ONLY_BASE_PACK)] });
put("bundles/colombia/pool.json", { questions: [q("k1", SHARED), q("k2", ONLY_DLC)] });

test("a base pack's media: content depot, once, shared with base", () => {
  const { urls, packMedia, baseMedia } = stageUrls(tmp);
  assert.equal(urls.size, 4); // SHARED, CLIP#t, Chinese, Dlc: the copy adds no URL
  assert.ok(urls.has(SHARED) && urls.has(ONLY_BASE_PACK) && urls.has(ONLY_DLC));
  assert.ok(urls.has(`${CLIP}#t=1,5`));
  assert.deepEqual([...baseMedia.keys()], ["chinese-base"]);
  assert.equal(new Set(baseMedia.get("chinese-base")).size, 3);
  assert.ok(baseMedia.get("chinese-base").includes(shippedName(SHARED)));
  assert.equal(shippedName(SHARED), shippedName(SHARED)); // by URL: source and copy name the same file
  assert.equal(cacheName(SHARED), cacheName(SHARED));
});

test("no pack-media entry for a base pack; a DLC pack keeps only its own media", () => {
  const { packMedia } = stageUrls(tmp);
  assert.deepEqual(Object.keys(packMedia), ["colombia"]);
  assert.deepEqual(packMedia.colombia, [shippedName(ONLY_DLC)]);
});

test("without the base pack: today's sets", () => {
  put("bundles.json", { bundles: [{ id: "base", kind: "base" }, { id: "colombia", kind: "region" }] });
  rmSync(path.join(tmp, "bundles", "chinese-base"), { recursive: true });
  const { urls, packMedia, baseMedia } = stageUrls(tmp);
  assert.equal(baseMedia.size, 0);
  assert.equal(urls.size, 3);
  assert.deepEqual(packMedia.colombia, [shippedName(ONLY_DLC)]);
});
