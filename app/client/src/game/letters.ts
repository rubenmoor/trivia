// The letter picker's typing (plan 46, SW-4): auto-capital after start, space or `-`; the field's 30 chars.
// A note (flag dialog): capital only at a sentence start, up to 500 chars.
import { MAX_NAME } from "../engine/game";
import { MAX_NOTE } from "../engine/save";

export { MAX_NAME, MAX_NOTE };

/** `name` with `key` typed: upper case at the start and after a space or `-` (`note`: after `.?!¿¡`), else lower case. */
export function typeKey(name: string, key: string, note = false): string {
  if (name.length >= (note ? MAX_NOTE : MAX_NAME)) return name;
  if (key === " " && (name === "" || name.endsWith(" "))) return name;
  const prev = name.at(-1);
  const upper = note ? /^$|[.?!\u00bf\u00a1]\s*$/.test(name) : prev === undefined || prev === " " || prev === "-";
  const up = key.toUpperCase();
  return name + (upper && up.length === key.length ? up : key.toLowerCase()); // ß stays ß, not SS
}
