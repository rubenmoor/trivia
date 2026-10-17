// Linux: the executable (`living-room-trivia`, the demo's `living-room-trivia-demo`) is a launcher adding --no-sandbox (no SUID chrome-sandbox in a tar.gz; plan 56).
import { chmod, rename, writeFile } from "node:fs/promises";
import path from "node:path";

const LAUNCHER = `#!/bin/sh
here=$(dirname "$(readlink -f "$0")")
exec "$here/@NAME@-bin" --no-sandbox "$@"
`;

export default async function afterPack({ electronPlatformName, appOutDir, packager }) {
  if (electronPlatformName !== "linux") return;
  const name = packager.executableName; // the config's executableName
  const bin = path.join(appOutDir, name);
  await rename(bin, path.join(appOutDir, `${name}-bin`));
  await writeFile(bin, LAUNCHER.replace("@NAME@", name));
  await chmod(bin, 0o755);
}
