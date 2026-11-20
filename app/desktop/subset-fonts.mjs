// CJK fonts for the zh locales (plan 142, decision 767): subsets of full source fonts → app/client/public/fonts/zh-*.woff2.
// Sources (OFL, gitignored, not in the repo) in work/fonts-src/ (TRIVIA_WORK): Ma Shan Zheng (googlefonts/mashanzheng),
// LXGW WenKai Medium (lxgw/LxgwWenKai), Resource Han Rounded CN/TW Regular + Bold (CyanoHao/Resource-Han-Rounded).
// Characters: GB 2312 level 1 (SC) / Big5 common (TC) ∪ every CJK character of the zh catalogs, names and pools (so content
// patches rarely change a font). Needs fonttools + brotli (dev shell). The subsets are committed: the dev client uses them.
// Default: subset when the sources exist, then check. --check: only the coverage check (exit 1 on a character a font lacks).
import { execFileSync } from "node:child_process";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, "..", "..");
const SRC = path.join(process.env.TRIVIA_WORK || path.join(REPO, "work"), "fonts-src");
const OUT = path.join(REPO, "app", "client", "public", "fonts");
const DATA = path.join(REPO, "app", "data");

// script: which character set the file must cover; `hant` = Traditional locales, `hans` = Simplified ones.
const FONTS = [
  { out: "zh-ma-shan-zheng.woff2", src: "MaShanZheng-Regular.ttf", script: "hans" }, // no Traditional glyphs: zh-Hant falls back to WenKai
  { out: "zh-lxgw-wenkai.woff2", src: "LXGWWenKai-Medium.ttf", script: "both" },
  { out: "zh-rhr-sc-regular.woff2", src: "ResourceHanRoundedCN-Regular.ttf", script: "hans" },
  { out: "zh-rhr-sc-bold.woff2", src: "ResourceHanRoundedCN-Bold.ttf", script: "hans" },
  { out: "zh-rhr-tc-regular.woff2", src: "ResourceHanRoundedTW-Regular.ttf", script: "hant" },
  { out: "zh-rhr-tc-bold.woff2", src: "ResourceHanRoundedTW-Bold.ttf", script: "hant" },
];
const PUNCT = "，。？！：；、“”‘’「」『』（）…—《》·％＋－～＝＜＞／＆";
const BASIC = Array.from({ length: 95 }, (_, i) => String.fromCharCode(32 + i)).join("");
// theme.css `unicode-range` of the zh faces, General Punctuation only as far as PUNCT: –, † stay Baloo / Nunito (decision 767).
const CJK = new RegExp(`[\u2e80-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef${[...PUNCT].filter((c) => c >= "\u2010" && c <= "\u2027").join("")}]`, "gu");

/** Every character of a legacy double-byte range (GB 2312 level 1: B0–D7; Big5 common: A4–C6). */
function range(enc, hi0, hi1, lo0, lo1) {
  const td = new TextDecoder(enc, { fatal: true });
  let out = "";
  for (let h = hi0; h <= hi1; h++) for (let l = lo0; l <= lo1; l++) {
    try { out += td.decode(Uint8Array.of(h, l)); } catch { /* unassigned */ }
  }
  return out;
}
const COMMON = { hans: range("gbk", 0xb0, 0xd7, 0xa1, 0xfe), hant: range("big5", 0xa4, 0xc6, 0x40, 0xfe) };

/** [file, script] of every shipped zh text: catalogs, names, pools (base and bundles). */
function inputs() {
  const list = [];
  const scriptOf = (f) => (/zh-Hant/.test(f) ? "hant" : "hans");
  const locales = path.join(REPO, "app", "client", "src", "locales");
  for (const f of existsSync(locales) ? readdirSync(locales) : []) if (/^zh[\w-]*\.ts$/.test(f)) list.push([path.join(locales, f), scriptOf(f)]);
  const dirs = [DATA, ...(existsSync(path.join(DATA, "bundles")) ? readdirSync(path.join(DATA, "bundles")).map((b) => path.join(DATA, "bundles", b)) : [])];
  for (const d of dirs) for (const f of existsSync(d) ? readdirSync(d) : []) if (/^(names|pool)\.zh[\w-]*\.json$/.test(f)) list.push([path.join(d, f), scriptOf(f)]);
  return list;
}
const used = { hans: new Set(), hant: new Set() };
for (const [f, s] of inputs()) for (const c of readFileSync(f, "utf8").match(CJK) ?? []) used[s].add(c);

const wanted = (script) => {
  const set = new Set([...PUNCT]);
  for (const s of script === "both" ? ["hans", "hant"] : [script]) for (const c of [...COMMON[s], ...used[s]]) set.add(c);
  return set;
};

if (!process.argv.includes("--check")) {
  if (!existsSync(SRC)) console.log(`subset-fonts: no sources in ${SRC}, keeping the committed subsets`);
  else for (const f of FONTS) {
    const text = BASIC + [...wanted(f.script)].join("");
    execFileSync("python3", ["-m", "fontTools.subset", path.join(SRC, f.src), `--text=${text}`, "--flavor=woff2", "--layout-features=*", `--output-file=${path.join(OUT, f.out)}`], { stdio: "inherit" });
  }
}

// Check: the committed files' cmaps against the wanted characters (the font families' real coverage is what ships).
const probe = "import sys,json\nfrom fontTools.ttLib import TTFont\nprint(json.dumps(''.join(map(chr,TTFont(sys.argv[1]).getBestCmap()))))";
let bad = 0;
for (const f of FONTS) {
  const file = path.join(OUT, f.out);
  if (!existsSync(file)) { console.error(`✗ missing ${f.out}`); bad++; continue; }
  const have = new Set(JSON.parse(execFileSync("python3", ["-c", probe, file], { encoding: "utf8" })));
  // Characters only the catalog needs (not the common set) must be in the font; Ma Shan Zheng lacks some Traditional ones by design.
  const need = [...(f.script === "both" ? [...used.hans, ...used.hant] : used[f.script])].filter((c) => !have.has(c));
  const size = (readFileSync(file).length / 1e6).toFixed(2);
  console.log(`${need.length ? "✗" : "✓"} ${f.out}: ${have.size} glyphs, ${size} MB${need.length ? `, missing ${need.join("")}` : ""}`);
  bad += need.length ? 1 : 0;
}
process.exit(bad ? 1 : 0);
