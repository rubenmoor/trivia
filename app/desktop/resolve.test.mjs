// makeResolver: mod layers and path safety (plan 112). `npm test`
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { after, test } from "node:test";
import { makeResolver } from "./resolve.mjs";

const tmp = mkdtempSync(path.join(tmpdir(), "trivia-resolve-"));
after(() => rmSync(tmp, { recursive: true, force: true }));

const put = (rel, text) => {
  const file = path.join(tmp, rel);
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, text);
};
put("dist/index.html", "ours index");
put("dist/game/theme.css", "ours theme");
put("dist/only-ours.js", "ours only");
put("data/pool.json", '{"questions":[]}');
put("data/bundles.json", "ours bundles");
put("top/mod.json", "{}");
put("top/game/theme.css", "top theme");
put("top/data/bundles.json", "top bundles");
put("low/mod.json", "{}");
put("low/game/theme.css", "low theme");
put("low/index.html", "low index");
put("low/sub/x.txt", "x");
put("secret/key", "secret");
mkdirSync(path.join(tmp, "media"));
symlinkSync(path.join(tmp, "secret/key"), path.join(tmp, "top/leak.txt"));
symlinkSync(path.join(tmp, "secret"), path.join(tmp, "top/dir"));
symlinkSync(path.join(tmp, "secret/key"), path.join(tmp, "dist/leak.txt"));

const dirs = { dist: path.join(tmp, "dist"), data: path.join(tmp, "data"), media: path.join(tmp, "media") };
const plain = makeResolver(dirs);
const modded = makeResolver({ ...dirs, layers: [path.join(tmp, "top"), path.join(tmp, "low")] });

const get = async (resolve, p) => {
  const res = await resolve(new Request("app://trivia" + p));
  return { status: res.status, text: await res.text(), type: res.headers.get("content-type") };
};
const text = async (resolve, p) => (await get(resolve, p)).text;

test("no layers: ours, SPA fallback", async () => {
  assert.equal(await text(plain, "/game/theme.css"), "ours theme");
  assert.equal(await text(plain, "/"), "ours index");
  assert.equal(await text(plain, "/no/such"), "ours index");
});

test("layer order: top mod wins, ours last", async () => {
  assert.equal(await text(modded, "/game/theme.css"), "top theme");
  assert.equal(await text(modded, "/only-ours.js"), "ours only");
  assert.equal(await text(modded, "/sub/x.txt"), "x");
});

test("mod index.html is the fallback", async () => {
  assert.equal(await text(modded, "/"), "low index");
  assert.equal(await text(modded, "/no/such"), "low index");
});

test("mod.json not served", async () => {
  assert.equal(await text(modded, "/mod.json"), "low index");
  assert.equal(await text(modded, "/./sub/../mod.json"), "low index");
});

test("/data/ layering", async () => {
  assert.equal(await text(modded, "/data/bundles.json"), "top bundles");
  assert.equal(await text(modded, "/data/pool.json"), '{"questions":[]}');
  assert.equal((await get(modded, "/data/nope.json")).status, 404);
});

test("escapes stay inside or miss", async () => {
  for (const p of ["/../secret/key", "/%2e%2e/secret/key", "/%2E%2E%2Fsecret%2Fkey", "/..%5Csecret%5Ckey", "/" + path.join(tmp, "secret/key"), "/C:/Windows/win.ini", "/%5C%5Cserver%5Cshare"])
    assert.equal(await text(modded, p), "low index", p);
  for (const p of ["/data/..%2F..%2Fsecret%2Fkey", "/data/..%2F..%2Fdist%2Findex.html", "/data//etc/passwd"])
    assert.equal((await get(modded, p)).status, 404, p);
});

test("symlinks out of a root: never followed", async () => {
  assert.equal(await text(modded, "/leak.txt"), "low index");
  assert.equal(await text(modded, "/dir/key"), "low index");
  assert.equal(await text(plain, "/leak.txt"), "ours index");
});

test("directory request misses", async () => {
  assert.equal(await text(modded, "/sub"), "low index");
  assert.equal((await get(modded, "/data/")).status, 404);
});

test("MIME", async () => {
  assert.equal((await get(modded, "/sub/x.txt")).type, "text/plain; charset=utf-8");
  assert.equal((await get(modded, "/game/theme.css")).type, "text/css; charset=utf-8");
});
