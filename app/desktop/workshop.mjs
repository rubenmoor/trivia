// Workshop source (plan 114): subscribed items → mod sources. Pure: no Electron, no binding import.
import { readdirSync } from "node:fs";
import path from "node:path";

// EItemState bits.
const INSTALLED = 4;
const NEEDS_UPDATE = 8;
const DOWNLOADING = 16;
const DOWNLOAD_PENDING = 32;
const DISABLED_LOCALLY = 64;

/** `ugc`: `steam.workshop` or `fakeUgc()` → `[{ dir, publishedFileId, state, warnings }]`, ids as decimal strings. */
export function workshopItems(ugc) {
  return ugc.getSubscribedItems().map((id) => {
    const publishedFileId = String(id);
    const bits = Number(ugc.getItemState(id));
    const item = (state, dir = null, warnings = []) => ({ dir, publishedFileId, state, warnings });
    if (bits & DISABLED_LOCALLY) return item("disabled");
    const folder = bits & INSTALLED ? ugc.getItemInstallInfo(id)?.folder : null;
    if (folder) return item("installed", folder, bits & NEEDS_UPDATE ? [{ code: "needs_update" }] : []);
    if (!(bits & (DOWNLOADING | DOWNLOAD_PENDING))) ugc.downloadItem(id, false);
    return item("downloading");
  });
}

/** Dev stand-in for `steam.workshop`: `<dir>/<id>/` installed, `<dir>/<id>.downloading/` downloading. */
export function fakeUgc(dir) {
  const names = () => {
    try {
      return readdirSync(dir, { withFileTypes: true })
        .filter((e) => e.isDirectory() && /^[1-9]\d*(\.downloading)?$/.test(e.name))
        .map((e) => e.name);
    } catch {
      return [];
    }
  };
  return {
    getSubscribedItems: () => names().map((n) => BigInt(n.split(".")[0])),
    getItemState: (id) => (names().includes(String(id)) ? 1 | INSTALLED : 1 | DOWNLOADING),
    getItemInstallInfo: (id) =>
      names().includes(String(id)) ? { folder: path.resolve(dir, String(id)), sizeOnDisk: 0n, timestamp: 0 } : null,
    downloadItem: () => true,
  };
}
