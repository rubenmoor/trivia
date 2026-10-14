// Before packaging (plan 85): Steamworks SDK libs present; koffi's win32-x64 binary beside the host's (npm installs only the host's).
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SDK = path.join(HERE, "steamworks_sdk", "redistributable_bin");

for (const lib of ["linux64/libsteam_api.so", "win64/steam_api64.dll"])
  if (!existsSync(path.join(SDK, lib))) {
    console.error(`steam-libs: missing ${path.join(SDK, lib)} (Steamworks SDK zip, plan 85)`);
    process.exit(1);
  }

const modules = path.join(HERE, "node_modules");
const { version } = JSON.parse(readFileSync(path.join(modules, "koffi", "package.json"), "utf8"));
for (const target of ["linux-x64", "win32-x64"]) {
  const dir = path.join(modules, "@koromix", `koffi-${target}`);
  const have = existsSync(dir) && JSON.parse(readFileSync(path.join(dir, "package.json"), "utf8")).version;
  if (have === version) continue;
  const tmp = mkdtempSync(path.join(tmpdir(), "koffi-"));
  try {
    const tgz = execFileSync("npm", ["pack", `@koromix/koffi-${target}@${version}`, "--silent"], { cwd: tmp, encoding: "utf8" }).trim();
    rmSync(dir, { recursive: true, force: true });
    mkdirSync(dir, { recursive: true });
    execFileSync("tar", ["xzf", path.join(tmp, tgz), "-C", dir, "--strip-components=1"]);
    console.log(`steam-libs: @koromix/koffi-${target}@${version}`);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}
