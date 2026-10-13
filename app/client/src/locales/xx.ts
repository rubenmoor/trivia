// Dev-only pseudo-locale (plans/15a-ui-translation.md, LUI-2): `es` with look-alike letters,
// ~40 % `~` padding and `[ ]` brackets, so missed literals and overflow show. `{param}` kept.
import type { Catalog } from "./es";

/** Left as in `es`: the shortcut letters, so key handling still works (LUI-4), and the picker's keys. */
const EXEMPT = [/^joker\.\w+\.key$/, /^flag\.key$/, /Key$/, /^picker\.(letters|marks)$/];

const LOOK: Record<string, string> = {
  a: "å", e: "é", i: "î", o: "ø", u: "ü", c: "ç", n: "ñ", y: "ý",
  A: "Å", E: "É", I: "Î", O: "Ø", U: "Ü", C: "Ç", N: "Ñ", Y: "Ý",
};

export function pseudoText(s: string): string {
  const body = s
    .split(/(\{\w+\})/)
    .map((part, i) => (i % 2 ? part : part.replace(/[a-zA-Z]/g, (c) => LOOK[c] ?? c)))
    .join("");
  return `[${body}${"~".repeat(Math.max(2, Math.ceil(s.length * 0.4)))}]`;
}

function walk(node: unknown, path: string): unknown {
  if (typeof node === "string") return EXEMPT.some((r) => r.test(path)) ? node : pseudoText(node);
  if (Array.isArray(node)) return node.map((v, i) => walk(v, `${path}.${i}`));
  if (node && typeof node === "object")
    return Object.fromEntries(Object.entries(node).map(([k, v]) => [k, walk(v, path ? `${path}.${k}` : k)]));
  return node;
}

export function pseudo(es: Catalog): Catalog {
  return walk(es, "") as Catalog;
}
