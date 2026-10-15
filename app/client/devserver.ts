// Dev server for browser checks (plan 99): `vite` and `vite preview` serve /data/, /media and /mods.js by the desktop's
// rules (resolve.mjs) and the save from a dir (save.mjs) through a page shim (devshell.js); nothing of it in dist/.
import { mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import type { Connect, Plugin } from "vite";
import { makeResolver } from "../desktop/resolve.mjs";
import { makeSaveFile } from "../desktop/save.mjs";
import { muteReason } from "../desktop/mute.mjs";

const client = fileURLToPath(new URL(".", import.meta.url));
const repo = `${client}../../`;
const SHIM = "/@trivia/shell.js";
const SAVE = "/@trivia/save";

/** `TRIVIA_SAVE_DIR`, else a fresh temp dir: never the family's save (decision 111's dev switch). */
let dir: string | null = null;
function saveDir(): string {
  if (!dir) {
    dir = process.env.TRIVIA_SAVE_DIR || mkdtempSync(join(tmpdir(), "trivia-dev-"));
    console.log(`trivia dev: save ${dir}`);
  }
  return dir;
}

/** What we read of Node's request (no @types/node). */
interface Req {
  url?: string;
  method?: string;
  headers: Record<string, string | undefined>;
  [Symbol.asyncIterator](): AsyncIterator<Uint8Array>;
}
const node = (req: Connect.IncomingMessage) => req as unknown as Req;
type Res = Parameters<Connect.NextHandleFunction>[1];

async function send(res: Res, r: Response): Promise<void> {
  res.statusCode = r.status;
  r.headers.forEach((v, k) => res.setHeader(k, v));
  // Backpressure, and stop when the page drops it (video seek): else a whole video sits in memory.
  if (r.body)
    for await (const chunk of r.body) {
      if (res.destroyed) break;
      if (!res.write(chunk)) await drained(res);
    }
  res.end();
}

const drained = (res: Res) =>
  new Promise<void>((go) => {
    const done = () => {
      res.off("drain", done);
      res.off("close", done);
      go();
    };
    res.on("drain", done);
    res.on("close", done);
  });

async function text(req: Req): Promise<string> {
  const chunks: Uint8Array[] = [];
  for await (const chunk of req) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}

const json = (status: number, body: unknown) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json; charset=utf-8" } });

function mount(app: Connect.Server, dist: string | null): void {
  const resolve = makeResolver({
    dist: dist ?? client,
    data: `${repo}app/data`,
    media: process.env.TRIVIA_MEDIA || `${repo}media`,
  });
  const save = makeSaveFile(saveDir());
  void save.dropStaleTemp();
  const muted = muteReason(process.env);
  if (muted) console.log(`trivia dev: muted (${muted}); TRIVIA_SOUND=1 to hear`);

  app.use(SHIM, (_req, res) => {
    res.setHeader("content-type", "text/javascript; charset=utf-8");
    res.end(readFileSync(`${client}devshell.js`, "utf8") + (muted ? "window.triviaShell.muted = true;\n" : ""));
  });

  app.use(SAVE, (incoming, res) => {
    const req = node(incoming);
    const url = new URL(req.url ?? "/", "http://dev");
    const run = async (): Promise<Response> => {
      if (url.pathname === "/" && req.method === "GET") {
        const doc = await save.read();
        return doc === null ? new Response(null, { status: 204 }) : new Response(doc, { status: 200 });
      }
      if (url.pathname === "/" && req.method === "PUT") {
        await save.write(await text(req));
        return new Response(null, { status: 204 });
      }
      if (url.pathname === "/backup" && req.method === "POST") return json(200, { path: await save.backup(url.searchParams.get("kind")) });
      return json(404, { error: "not_found" });
    };
    run()
      .catch((e: { code?: string; message?: string }) => json(e.code ? 409 : 500, { error: e.code ?? e.message }))
      .then((r) => send(res, r));
  });

  app.use((incoming, res, next) => {
    const req = node(incoming);
    const path = new URL(req.url ?? "/", "http://dev").pathname;
    if (dist && (path === "/" || path === "/index.html")) {
      res.setHeader("content-type", "text/html; charset=utf-8");
      res.setHeader("cache-control", "no-cache");
      res.end(readFileSync(`${dist}index.html`, "utf8").replace("<head>", `<head>\n    <script src="${SHIM}"></script>`));
      return;
    }
    if (!(path.startsWith("/data/") || path === "/media" || path === "/mods.js")) return next();
    const range = req.headers.range;
    resolve(new Request(`http://dev${req.url}`, { headers: range ? { range } : {} })).then((r: Response) => send(res, r), next);
  });
}

/** Dev (`vite`) and built client (`vite preview`); fixed ports in vite.config.ts. */
export function devServer(): Plugin {
  return {
    name: "trivia-dev-server",
    apply: "serve",
    configureServer(server) {
      mount(server.middlewares, null);
    },
    configurePreviewServer(server) {
      mount(server.middlewares, `${client}dist/`);
    },
    transformIndexHtml: () => [{ tag: "script", attrs: { src: SHIM }, injectTo: "head-prepend" }],
  };
}
