// makeResolver: mod layers, path safety (plan 112), mod bundles (plan 115), /mods.js and /mods/<id>/ (plan 117). `npm test`
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { after, test } from "node:test";
import { arrange, bundleRows, modsScript, readManifest } from "./mods.mjs";
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
put("data/bundles.json", JSON.stringify({ about: "x", bundles: [{ id: "base", kind: "base" }] }));
put("top/mod.json", "{}");
put("top/game/theme.css", "top theme");
put(
  "top/data/bundles.json",
  JSON.stringify({
    bundles: [
      { id: "cats", kind: "pets", languages: ["es"], name: "Gatos", description: "d", rule: "r" },
      { id: "Bad", kind: "pets", languages: [], name: "n", description: "d" },
      { id: "cats", kind: "pets", languages: [], name: "n", description: "d" },
      { id: "dogs", kind: "base", languages: "es", name: "n", description: "d" },
    ],
  }),
);
put("top/data/pool.json", "top pool");
put("top/data/bundles/cats/pool.json", "cats pool");
put("top/data/bundles/cats/img/owl.jpg", "owl");
put("top/data/bundles/hidden/pool.json", "hidden pool");
put("low/data/bundles.json", JSON.stringify({ bundles: [{ id: "cats", kind: "base", languages: ["en"], name: "L", description: "" }] }));
put("low/data/bundles/cats/pool.json", "low cats pool");
put("off/data/bundles.json", JSON.stringify({ bundles: [{ id: "x", kind: "base", languages: [], name: "", description: "" }] }));
put("off/data/bundles/x/pool.json", "off pool");
put("broken/data/bundles.json", "{nope");
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
const top = await bundleRows(path.join(tmp, "top"));
const low = await bundleRows(path.join(tmp, "low"));
const modded = makeResolver({
  ...dirs,
  layers: [path.join(tmp, "top"), path.join(tmp, "low")],
  mods: [
    { id: "top", name: "Top Mod", dir: path.join(tmp, "top"), bundles: top.rows },
    { id: "low", name: "Low Mod", dir: path.join(tmp, "low"), bundles: low.rows },
  ],
});

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

test("bundleRows: bad rows dropped with warnings, bad JSON, none", async () => {
  assert.deepEqual(top.rows.map((r) => r.id), ["cats"]);
  assert.deepEqual(top.warnings, [
    { code: "bundle_row", id: "Bad" },
    { code: "bundle_row", id: "cats" },
    { code: "bundle_row", id: "dogs" },
  ]);
  assert.deepEqual(await bundleRows(path.join(tmp, "broken")), { rows: [], warnings: [{ code: "bundle_json" }] });
  assert.deepEqual(await bundleRows(path.join(tmp, "secret")), { rows: [], warnings: [] });
});

test("bundles.json: ours first, then mods top first, tagged", async () => {
  const doc = JSON.parse(await text(modded, "/data/bundles.json"));
  assert.equal(doc.about, "x");
  assert.deepEqual(doc.bundles.map((b) => b.id), ["base", "top:cats", "low:cats"]);
  assert.deepEqual(doc.bundles[0], { id: "base", kind: "base" });
  assert.deepEqual(doc.bundles[1], {
    id: "top:cats",
    kind: "pets",
    languages: ["es"],
    name: "Gatos",
    description: "d",
    rule: "r",
    source: "mod",
    mod: "top",
    modName: "Top Mod",
  });
  assert.equal(JSON.parse(await text(plain, "/data/bundles.json")).bundles.length, 1);
});

test("namespaced bundle folders: that mod only", async () => {
  assert.equal(await text(modded, "/data/bundles/top:cats/pool.json"), "cats pool");
  assert.equal(await text(modded, "/data/bundles/top%3Acats/img/owl.jpg"), "owl");
  assert.equal((await get(modded, "/data/bundles/top:cats/img/owl.jpg")).type, "image/jpeg");
  assert.equal(await text(modded, "/data/bundles/low:cats/pool.json"), "low cats pool");
  for (const p of [
    "/data/bundles/top:hidden/pool.json",
    "/data/bundles/off:x/pool.json",
    "/data/bundles/top:Bad/pool.json",
    "/data/bundles/top:cats/../hidden/pool.json",
    "/data/bundles/top:cats/%2e%2e/hidden/pool.json",
    "/data/bundles/top:cats/..%2F..%2F..%2Fmod.json",
    "/data/bundles/top:cats:x/pool.json",
    "/data/bundles/top:cats",
  ])
    assert.equal((await get(modded, p)).status, 404, p);
  assert.equal(await text(modded, "/data/bundles/top:cats/%2e%2e%2f%2e%2e%2fpool.json"), "cats pool"); // clamped
});

test("other /data/ files: ours only", async () => {
  assert.equal(await text(modded, "/data/pool.json"), '{"questions":[]}');
  assert.equal((await get(modded, "/data/bundles/cats/pool.json")).status, 404);
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

// Code add-ons (decision 131).
const manifest = (id, extra = {}) => JSON.stringify({ id, name: `Mod ${id}`, description: "", version: "1.0.0", game: "1.0.0", ...extra });
put("code/aa/mod.json", manifest("aa", { entry: "./src/main.js" }));
put("code/aa/src/main.js", "export default () => {};");
put("code/aa/src/util.mjs", "export {};");
put("code/aa/style.css", "body{}");
put("code/bb/mod.json", manifest("bb"));
put("code/bb/sub/style.css", "not root");
put("code/cc/mod.json", manifest("cc", { entry: "main.js" }));
put("code/cc/main.js", "off");
put("code/dd/mod.json", manifest("dd", { version: 2 }));
put("code/dd/main.js", "invalid");
symlinkSync(path.join(tmp, "secret/key"), path.join(tmp, "code/aa/leak.js"));
symlinkSync(path.join(tmp, "secret"), path.join(tmp, "code/aa/dir"));

const found = await Promise.all(["aa", "bb", "cc", "dd"].map((id) => readManifest(path.join(tmp, "code", id), "1.0.0")));
const settings = { version: 1, mods: ["aa", "bb", "cc", "dd"].map((id) => ({ id, on: id !== "cc" })) };
const { list } = arrange(found, settings, { validUser: true });
const loaded = list.filter((m) => m.state === "loaded");
const coded = makeResolver({
  ...dirs,
  layers: loaded.map((m) => m.dir),
  mods: loaded.map((m) => ({ id: m.id, name: m.manifest.name, dir: m.dir, bundles: m.bundles })),
  modsJs: modsScript(list),
});
const exported = async (src) => (await import("data:text/javascript," + encodeURIComponent(src))).default;

test("/mods.js: none", async () => {
  assert.equal(modsScript([]), "export default [];\n");
  assert.equal(modsScript(arrange(found, settings, { validUser: false }).list), "export default [];\n");
  const res = await get(plain, "/mods.js");
  assert.equal(res.text, "export default [];\n");
  assert.equal(res.type, "text/javascript; charset=utf-8");
});

test("/mods.js: loaded mods bottom-up, style only when a root style.css exists", async () => {
  assert.deepEqual(await exported(await text(coded, "/mods.js")), [
    { id: "bb", name: "Mod bb", version: "1.0.0", entry: null, style: null },
    { id: "aa", name: "Mod aa", version: "1.0.0", entry: "/mods/aa/src/main.js", style: "/mods/aa/style.css" },
  ]);
  assert.ok(!(await text(coded, "/mods.js")).includes(tmp));
});

test("/mods/<id>/: loaded mods' files only", async () => {
  assert.equal(await text(coded, "/mods/aa/src/main.js"), "export default () => {};");
  assert.equal((await get(coded, "/mods/aa/src/util.mjs")).type, "text/javascript; charset=utf-8");
  assert.equal(await text(coded, "/mods/aa/style.css"), "body{}");
  for (const p of [
    "/mods/aa/mod.json",
    "/mods/aa/./src/../mod.json",
    "/mods/aa/src",
    "/mods/aa/",
    "/mods/aa/../bb/mod.json",
    "/mods/aa/..%2F..%2F..%2Fsecret%2Fkey",
    "/mods/aa/..%2Fbb%2Fmod.json",
    "/mods/aa/leak.js",
    "/mods/aa/dir/key",
    "/mods/cc/main.js",
    "/mods/dd/main.js",
    "/mods/zz/main.js",
    "/mods/",
  ])
    assert.equal((await get(coded, p)).status, 404, p);
  assert.equal(await text(coded, "/mods/aa/%2e%2e/%2e%2e/secret/key"), "ours index"); // URL-normalised out of /mods/
  assert.equal((await get(plain, "/mods/aa/src/main.js")).status, 404);
});
