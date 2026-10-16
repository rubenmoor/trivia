#!/usr/bin/env node
// Credits complete both ways in a packaged build (plan 92, SW-6): node credits_check.mjs <unpacked dir>...
// Exit 1 with every missing/extra name. Not checked: modding/ (player kit; its template image is ours, CC0).
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { cacheName, shippedName } from "../../app/desktop/resolve.mjs";

const asar = createRequire(new URL("../../app/desktop/package.json", import.meta.url))("@electron/asar");

const AUDIO = /\.(m4a|mp3|ogg|oga|opus|wav)$/i;
const HORIZON = /\.webp$/i;
const FONT = /\.(woff2?|ttf|otf)$/i;
const SDK = "Steamworks SDK";

const files = (dir) => (existsSync(dir) ? readdirSync(dir).filter((f) => statSync(path.join(dir, f)).isFile()) : []);

/** Package names under node_modules in app.asar and app.asar.unpacked. */
function packages(res) {
  const pkg = /\/node_modules\/((?:@[^/]+\/)?[^/@][^/]*)\/package\.json$/;
  const names = new Set();
  for (const f of asar.listPackage(path.join(res, "app.asar"))) {
    const m = f.replaceAll("\\", "/").match(pkg);
    if (m) names.add(m[1]);
  }
  const walk = (dir) => {
    for (const e of existsSync(dir) ? readdirSync(dir, { withFileTypes: true }) : []) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) walk(p);
      else if (e.name === "package.json") {
        const m = ("/" + path.relative(res, p).replaceAll("\\", "/")).match(pkg);
        if (m) names.add(m[1]);
      }
    }
  };
  walk(path.join(res, "app.asar.unpacked"));
  return names;
}

function check(root) {
  const res = path.join(root, "resources");
  const client = path.join(res, "client");
  const problems = [];
  const credits = JSON.parse(readFileSync(path.join(client, "credits.json"), "utf8"));

  const shipped = new Set(files(path.join(res, "media")));
  const media = new Map();
  for (const m of credits.media) {
    const name = shipped.has(cacheName(m.file_url)) ? cacheName(m.file_url) : shippedName(m.file_url);
    media.set(name, (media.get(name) ?? 0) + 1);
  }
  for (const f of shipped) if (!media.has(f)) problems.push(`media file without credit: media/${f}`);
  for (const [f, n] of media) {
    if (!shipped.has(f)) problems.push(`media credit without file: media/${f}`);
    if (n > 1) problems.push(`media/${f}: ${n} credits`);
  }

  const sounds = new Set(credits.sounds.entries.map((s) => s.file));
  const audio = files(path.join(client, "audio")).filter((f) => AUDIO.test(f));
  for (const f of audio) if (!sounds.has(f)) problems.push(`sound without row: audio/${f}`);
  for (const f of sounds) if (!audio.includes(f)) problems.push(`sound row without file: audio/${f}`);

  const horizonRows = new Set(credits.horizon.entries.map((s) => s.file));
  const horizon = files(path.join(client, "horizon")).filter((f) => HORIZON.test(f));
  for (const f of horizon) if (!horizonRows.has(f)) problems.push(`horizon image without row: horizon/${f}`);
  for (const f of horizonRows) if (!horizon.includes(f)) problems.push(`horizon row without file: horizon/${f}`);

  const fonts = new Set(credits.fonts.map((f) => f.file));
  const fontFiles = files(path.join(client, "fonts")).filter((f) => FONT.test(f)).map((f) => `fonts/${f}`);
  for (const f of fontFiles) if (!fonts.has(f)) problems.push(`font without entry: ${f}`);
  for (const f of credits.fonts) {
    if (!fontFiles.includes(f.file)) problems.push(`font entry without file: ${f.file}`);
    if (!existsSync(path.join(client, f.license_file))) problems.push(`font licence missing: ${f.license_file}`);
  }

  const libs = new Set(credits.libraries.map((l) => l.name));
  for (const p of packages(res)) if (!libs.has(p)) problems.push(`package without library entry: ${p}`);
  const sdk = path.join(res, "steamworks_sdk");
  if (existsSync(sdk) && !libs.has(SDK)) {
    for (const g of readdirSync(sdk)) problems.push(`steamworks_sdk/${g} without library entry "${SDK}"`);
  }

  for (const f of [path.join(root, "CREDITS.md"), path.join(client, "CREDITS.md")]) {
    if (!existsSync(f)) problems.push(`missing ${path.relative(root, f)}`);
  }
  console.log(
    `${problems.length ? "✗" : "✓"} credits ${root}: ${shipped.size} media, ${audio.length} sounds, ${horizon.length} horizon images, ` +
      `${fontFiles.length} fonts, ${libs.size} libraries`,
  );
  for (const p of problems) console.log(`  ${p}`);
  return problems.length;
}

const dirs = process.argv.slice(2);
if (!dirs.length) {
  console.error("usage: credits_check.mjs <unpacked dir>...");
  process.exit(2);
}
process.exit(dirs.map(check).some(Boolean) ? 1 : 0);
