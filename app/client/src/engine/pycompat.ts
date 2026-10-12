// The few Python semantics the referee port needs (PORT-3): names, coercion, repr.

/** str.casefold for the scripts players type (lowercase plus ß and final sigma). */
export function casefold(s: string): string {
  return s.toLowerCase().replace(/ß/g, "ss").replace(/ς/g, "σ");
}

/** len(str): code points, not UTF-16 units. */
export function pyLen(s: string): number {
  return [...s].length;
}

// str.isspace characters.
const SPACE = /[\t\n\v\f\r\x1c-\x1f \x85\xa0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+/;

/** " ".join(s.split()) */
export function pySplitJoin(s: string): string {
  return s.split(SPACE).filter((w) => w !== "").join(" ");
}

/** repr(str): single quotes unless the text has ' and no ". */
export function pyRepr(s: string): string {
  const q = s.includes("'") && !s.includes('"') ? '"' : "'";
  let out = "";
  for (const c of s) {
    const n = c.codePointAt(0)!;
    if (c === "\\" || c === q) out += "\\" + c;
    else if (c === "\n") out += "\\n";
    else if (c === "\r") out += "\\r";
    else if (c === "\t") out += "\\t";
    else if (n < 0x20 || (n >= 0x7f && n < 0xa0)) out += "\\x" + n.toString(16).padStart(2, "0");
    else out += c;
  }
  return q + out + q;
}

/** bool(x) for parsed JSON. */
export function pyTruthy(x: unknown): boolean {
  if (Array.isArray(x)) return x.length > 0;
  if (x !== null && typeof x === "object") return Object.keys(x).length > 0;
  return Boolean(x);
}

/** int(x) for parsed JSON; throws where Python raises. */
export function pyInt(x: unknown): number {
  if (typeof x === "boolean") return x ? 1 : 0;
  if (typeof x === "number") {
    if (!Number.isFinite(x)) throw new Error(`cannot convert float ${x} to integer`);
    return Math.trunc(x) || 0;
  }
  if (typeof x === "string") {
    const t = pySplitJoin(x);
    if (/^[+-]?\d+(_\d+)*$/.test(t)) return Number(t.replace(/_/g, "")) || 0;
    throw new Error(`invalid literal for int() with base 10: ${pyRepr(x)}`);
  }
  throw new Error(`int() argument must be a string or a number, not ${pyType(x)}`);
}

/** str(x) for parsed JSON. */
export function pyStr(x: unknown): string {
  return typeof x === "string" ? x : pyValue(x);
}

function pyValue(x: unknown): string {
  if (x === null || x === undefined) return "None";
  if (typeof x === "boolean") return x ? "True" : "False";
  if (typeof x === "string") return pyRepr(x);
  if (Array.isArray(x)) return "[" + x.map(pyValue).join(", ") + "]";
  if (typeof x === "object")
    return "{" + Object.entries(x).map(([k, v]) => `${pyRepr(k)}: ${pyValue(v)}`).join(", ") + "}";
  return String(x);
}

function pyType(x: unknown): string {
  if (x === null || x === undefined) return "NoneType";
  return Array.isArray(x) ? "list" : typeof x === "object" ? "dict" : typeof x;
}
