// Build-time credits (PUB-5, plan 47): credits.json for the Credits screen, CREDITS.md shipped in dist/.
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import type { Plugin } from "vite";
import type { Credits, CreditKind as Kind, MediaCredit, SoundCredit } from "./src/lib/types.ts";

const client = fileURLToPath(new URL(".", import.meta.url));
const repo = `${client}../../`;
const dataDir = `${client}../data/`;
/** es pool files: base's and every pack's (decision 66). */
const pools = (): string[] => [
  `${dataDir}pool.json`,
  ...readdirSync(`${dataDir}bundles`).map((b) => `${dataDir}bundles/${b}/pool.json`).filter((f) => existsSync(f)),
];

const KINDS: Kind[] = ["image", "audio", "video", "background"];
// Same file rules as authoring/steam/credits_check.mjs.
const AUDIO = /\.(m4a|mp3|ogg|oga|opus|wav)$/i;
const PROVIDERS: Record<string, string> = { commons: "Wikimedia Commons", freesound: "Freesound", openverse: "Openverse" };

interface Slot {
  type?: string;
  file_url: string | null;
  source_url: string | null;
  credit: string | null;
  provider?: string | null;
  license?: string | null;
  license_url?: string | null;
  author?: string | null;
  author_url?: string | null;
}

const ELGAR =
  "Victory march: Pomp and Circumstance No. 1, composed by Edward Elgar († 1934, public domain); " +
  "recording by the United States Marine Band, a US government work (public domain).";

const FONTS = [
  { name: "Baloo 2", file: "fonts/baloo-2.woff2", license: "SIL OFL 1.1", license_file: "fonts/OFL-Baloo2.txt" },
  { name: "Nunito", file: "fonts/nunito.woff2", license: "SIL OFL 1.1", license_file: "fonts/OFL-Nunito.txt" },
];

function title(sourceUrl: string): string {
  const path = decodeURIComponent(new URL(sourceUrl).pathname);
  const file = path.match(/\/File:(.+)$/);
  if (file) return file[1].replace(/\.[^.]+$/, "").replace(/_/g, " ");
  return path.split("/").filter(Boolean).pop() ?? sourceUrl;
}

function media(warnings: string[]): MediaCredit[] {
  const questions = pools().flatMap((f) => (JSON.parse(readFileSync(f, "utf8")) as {
    questions: { id: string; media: Slot; background: Slot | null }[];
  }).questions);
  const byFile = new Map<string, MediaCredit>();
  const missing: string[] = [];
  const gfdl = new Set<string>();
  for (const q of questions) {
    for (const [slot, kind] of [[q.media, q.media.type], [q.background, "background"]] as const) {
      if (!slot?.file_url) continue;
      if (!KINDS.includes(kind as Kind)) throw new Error(`credits: ${q.id}: unknown media type ${kind}`);
      if (!slot.license || !slot.source_url) {
        missing.push(`${q.id} (${kind === "background" ? "background" : "media"})`);
        continue;
      }
      if (slot.license.includes("GFDL")) gfdl.add(q.id);
      if (byFile.has(slot.file_url)) continue;
      byFile.set(slot.file_url, {
        kind: kind as Kind,
        title: title(slot.source_url),
        author: slot.author || slot.credit?.split(" · ")[0] || null,
        author_url: slot.author_url ?? null,
        license: slot.license,
        license_url: slot.license_url ?? null,
        source_url: slot.source_url,
        provider: slot.provider ? (PROVIDERS[slot.provider] ?? slot.provider) : null,
        file_url: slot.file_url,
      });
    }
  }
  if (missing.length) throw new Error(`credits: media without license or source_url: ${missing.join(", ")}`);
  if (gfdl.size) warnings.push(`credits: GFDL media (needs the full text; PUB-3 replaces them): ${[...gfdl].join(", ")}`);
  return [...byFile.values()].sort(
    (a, b) => KINDS.indexOf(a.kind) - KINDS.indexOf(b.kind) || a.title.localeCompare(b.title, "en"),
  );
}

/** Rows of public/audio/CREDITS.md, one per sound file. */
function sounds(): { entries: SoundCredit[]; md: string[] } {
  const dir = `${client}public/audio/`;
  const rows = readFileSync(`${dir}CREDITS.md`, "utf8")
    .split("\n")
    .filter((l) => l.startsWith("|") && !/^\|\s*(File|-)/.test(l));
  const entries = rows.map((row) => {
    const cells = row.split("|").slice(1, -1).map((c) => c.trim());
    const file = cells[0]?.match(/^`([^`]+)`$/)?.[1];
    if (cells.length !== 5 || !file) throw new Error(`credits: unparsable row in public/audio/CREDITS.md: ${row}`);
    return {
      file,
      used_for: cells[1],
      source: cells[2].replace(/\[([^\]]*)\]\([^)]*\)/g, "$1"),
      source_url: cells[2].match(/\]\(([^)]+)\)/)?.[1] ?? null,
      author: cells[3],
      license: cells[4],
    };
  });
  const listed = new Set(entries.map((e) => e.file));
  const unlisted = readdirSync(dir).filter((f) => AUDIO.test(f) && !listed.has(f));
  if (unlisted.length) throw new Error(`credits: sounds without a row in public/audio/CREDITS.md: ${unlisted.join(", ")}`);
  const absent = [...listed].filter((f) => !existsSync(dir + f));
  if (absent.length) throw new Error(`credits: rows in public/audio/CREDITS.md without a file: ${absent.join(", ")}`);
  return { entries, md: rows };
}

function game(): Credits["game"] {
  return readdirSync(repo)
    .filter((f) => /^LICEN[CS]E/i.test(f))
    .sort()
    .map((file) => ({ file, title: readFileSync(repo + file, "utf8").trim().split("\n")[0].trim() }));
}

function svelte(): { entry: Credits["libraries"][number]; text: string } {
  const dir = `${repo}node_modules/svelte/`;
  const pkg = JSON.parse(readFileSync(`${dir}package.json`, "utf8")) as { version: string; license: string };
  return {
    entry: { name: "Svelte", version: pkg.version, license: pkg.license, url: "https://svelte.dev" },
    text: readFileSync(`${dir}LICENSE.md`, "utf8").trim(),
  };
}

/** Only where the shell's deps are installed (not in the nix build, which ships no Electron). */
function electron(): { entries: Credits["libraries"]; text: string } | null {
  const dir = `${repo}app/desktop/node_modules/electron/`;
  if (!existsSync(`${dir}package.json`)) return null;
  const pkg = JSON.parse(readFileSync(`${dir}package.json`, "utf8")) as { version: string; license: string };
  return {
    entries: [
      { name: "Electron", version: pkg.version, license: pkg.license, url: "https://www.electronjs.org" },
      { name: "Chromium", version: "", license: "BSD-3-Clause and others", url: "https://www.chromium.org" },
    ],
    text: readFileSync(`${dir}LICENSE`, "utf8").trim(),
  };
}

type Library = Credits["libraries"][number];

const STEAMWORKS_SDK: Library = {
  name: "Steamworks SDK",
  version: "",
  license: "Valve Steamworks SDK Access Agreement",
  url: "https://partner.steamgames.com/documentation/sdk_access_agreement",
};

/** The shell's runtime packages (app/desktop dependencies, transitively, as installed), with licence texts. */
function desktopPackages(): { entries: Library[]; texts: { name: string; text: string }[] } {
  const root = `${repo}app/desktop/`;
  if (!existsSync(`${root}node_modules`)) return { entries: [], texts: [] };
  type Pkg = { name: string; version: string; license?: string; homepage?: string; repository?: string | { url: string } };
  const found = new Map<string, { pkg: Pkg; dir: string; versions: Set<string> }>();
  const walk = (from: string, deps: Record<string, string>, optional: boolean) => {
    for (const name of Object.keys(deps)) {
      let dir = from;
      while (!existsSync(`${dir}node_modules/${name}/package.json`) && dir !== root)
        dir = dir.replace(/node_modules\/(@[^/]+\/)?[^/]+\/$/, "");
      const at = `${dir}node_modules/${name}/`;
      if (!existsSync(`${at}package.json`)) {
        if (optional) continue;
        throw new Error(`credits: desktop package ${name} not installed (npm ci in app/desktop)`);
      }
      const pkg = JSON.parse(readFileSync(`${at}package.json`, "utf8")) as Pkg & {
        dependencies?: Record<string, string>;
        optionalDependencies?: Record<string, string>;
      };
      const seen = found.get(name);
      if (seen?.versions.has(pkg.version)) continue;
      if (seen) seen.versions.add(pkg.version);
      else found.set(name, { pkg, dir: at, versions: new Set([pkg.version]) });
      walk(at, pkg.dependencies ?? {}, false);
      walk(at, pkg.optionalDependencies ?? {}, true);
    }
  };
  const top = JSON.parse(readFileSync(`${root}package.json`, "utf8")) as { dependencies?: Record<string, string> };
  walk(root, top.dependencies ?? {}, false);
  const repoUrl = (r: Pkg["repository"]) =>
    (typeof r === "string" ? r : r?.url)
      ?.replace(/^git\+/, "")
      .replace(/\.git$/, "")
      .replace(/^git:/, "https:")
      .replace(/^(github:)?([\w.-]+\/[\w.-]+)$/, "https://github.com/$2");
  const entries: Library[] = [];
  const texts: { name: string; text: string }[] = [];
  for (const [name, { pkg, dir, versions }] of [...found].sort(([a], [b]) => a.localeCompare(b, "en"))) {
    entries.push({
      name,
      version: [...versions].join(", "),
      license: pkg.license ?? "see package",
      url: pkg.homepage ?? repoUrl(pkg.repository) ?? `https://www.npmjs.com/package/${name}`,
    });
    const file = readdirSync(dir).find((f) => /^(LICEN[CS]E|COPYING)/i.test(f));
    if (file) texts.push({ name, text: readFileSync(dir + file, "utf8").trim() });
  }
  if (found.has("steamworks-ffi-node")) entries.push(STEAMWORKS_SDK);
  return { entries, texts };
}

const cell = (s: string) => s.replace(/\|/g, "\\|").replace(/\n/g, " ");
const link = (text: string, url: string | null) =>
  url ? `[${cell(text).replace(/([[\]])/g, "\\$1")}](${url.replace(/\(/g, "%28").replace(/\)/g, "%29").replace(/ /g, "%20")})` : cell(text);

function markdown(
  c: Credits,
  soundRows: string[],
  svelteLicence: string,
  electronLicence: string | null,
  packageLicences: { name: string; text: string }[],
): string {
  const out = [
    "# Credits",
    "",
    "Everything in this game that its authors did not make themselves, with its licence. Each file keeps its own " +
      "licence. Adaptations of CC BY-SA files, such as the blurred backgrounds behind audio questions and crops, " +
      "are offered under the same licence as the original.",
    "",
  ];
  if (c.game.length) {
    out.push("## Game", "", "The game's own code and content, licensed by these files next to it:", "");
    for (const g of c.game) out.push(`- \`${g.file}\`: ${g.title}`);
    out.push("");
  }
  out.push(
    "## Media in the questions",
    "",
    `${c.media.length} files.`,
    "",
    "| Kind | Title | Author | Licence | Source |",
    "|---|---|---|---|---|",
  );
  for (const m of c.media) {
    const source = link(m.provider ?? "source", m.source_url);
    out.push(
      `| ${m.kind} | ${cell(m.title)} | ${link(m.author ?? "Unknown author", m.author_url)} | ${link(m.license, m.license_url)} | ${source} |`,
    );
  }
  out.push(
    "",
    "## Sounds",
    "",
    "| File | Used for | Source | Author | Licence |",
    "|---|---|---|---|---|",
    ...soundRows,
    "",
    c.sounds.note,
    "",
    "## Fonts",
    "",
  );
  for (const f of c.fonts) out.push(`- ${f.name}: ${f.license}, see \`${f.license_file}\``);
  out.push("");
  if (c.glyphs) out.push("## Controller glyphs", "", "Original, drawn for the game.", "");
  if (c.achievements) out.push("## Steam achievement icons", "", "Original, drawn for the game.", "");
  out.push("## Libraries", "");
  for (const l of c.libraries) out.push(`- ${[l.name, l.version].filter(Boolean).join(" ")} (${l.url}): ${l.license}`);
  out.push("", "### Svelte licence", "", svelteLicence, "");
  if (electronLicence) {
    out.push(
      "### Electron licence",
      "",
      "Desktop build only. Chromium's third-party licences ship as `LICENSES.chromium.html` next to the executable; " +
        "Electron's licence also as `LICENSE.electron.txt`.",
      "",
      electronLicence,
      "",
    );
  }
  if (packageLicences.length) {
    out.push("### Desktop runtime package licences", "", "Desktop build only, inside `resources/app.asar`.", "");
    for (const p of packageLicences) out.push(`#### ${p.name}`, "", p.text, "");
  }
  if (c.libraries.includes(STEAMWORKS_SDK)) {
    out.push(
      "### Steamworks SDK",
      "",
      "Desktop build only: Valve's Steamworks API redistributable (`steam_api64.dll`, `libsteam_api.so`) in " +
        `\`resources/steamworks_sdk/\`, under the Steamworks SDK Access Agreement: ${STEAMWORKS_SDK.url}.`,
      "",
    );
  }
  return out.join("\n");
}

function buildCredits(): { json: Credits; md: string; warnings: string[] } {
  const warnings: string[] = [];
  for (const f of FONTS) {
    for (const file of [f.file, f.license_file])
      if (!existsSync(`${client}public/${file}`)) throw new Error(`credits: missing public/${file}`);
  }
  const s = sounds();
  const lib = svelte();
  const shell = electron();
  const desktop = desktopPackages();
  const json: Credits = {
    version: 1,
    game: game(),
    media: media(warnings),
    sounds: { entries: s.entries, note: ELGAR },
    fonts: FONTS,
    glyphs: existsSync(`${client}src/game/Glyph.svelte`),
    achievements: existsSync(`${repo}app/desktop/achievements/FIRST_WIN.svg`),
    libraries: [lib.entry, ...(shell?.entries ?? []), ...desktop.entries],
  };
  return { json, md: markdown(json, s.md, lib.text, shell?.text ?? null, desktop.texts), warnings };
}

/** Emits credits.json and CREDITS.md into dist/; serves /credits.json in dev. */
export function credits(): Plugin {
  return {
    name: "trivia-credits",
    configureServer(server) {
      server.middlewares.use("/credits.json", (_req, res) => {
        try {
          const body = JSON.stringify(buildCredits().json);
          res.setHeader("Content-Type", "application/json");
          res.end(body);
        } catch (e) {
          res.statusCode = 500;
          res.end(String(e));
        }
      });
    },
    generateBundle() {
      const c = buildCredits();
      for (const w of c.warnings) this.warn(w);
      this.emitFile({ type: "asset", fileName: "credits.json", source: JSON.stringify(c.json) });
      this.emitFile({ type: "asset", fileName: "CREDITS.md", source: c.md });
    },
  };
}
