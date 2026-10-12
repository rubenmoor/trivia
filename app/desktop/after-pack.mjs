// Linux: `trivia` is a launcher adding --no-sandbox (no SUID chrome-sandbox in a tar.gz; plan 56).
import { chmod, rename, writeFile } from "node:fs/promises";
import path from "node:path";

const LAUNCHER = `#!/bin/sh
here=$(dirname "$(readlink -f "$0")")
exec "$here/trivia-bin" --no-sandbox "$@"
`;

export default async function afterPack({ electronPlatformName, appOutDir }) {
  if (electronPlatformName !== "linux") return;
  const bin = path.join(appOutDir, "trivia");
  await rename(bin, path.join(appOutDir, "trivia-bin"));
  await writeFile(bin, LAUNCHER);
  await chmod(bin, 0o755);
}
