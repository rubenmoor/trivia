// The letter picker's typing (plan 46, SW-4): auto-capital after start, space or `-`; the field's 30 chars.
export const MAX_NAME = 30;

/** `name` with `key` typed: upper case at the start and after a space or `-`, else lower case. */
export function typeKey(name: string, key: string): string {
  if (name.length >= MAX_NAME) return name;
  if (key === " " && (name === "" || name.endsWith(" "))) return name;
  const prev = name.at(-1);
  const upper = prev === undefined || prev === " " || prev === "-";
  return name + (upper ? key.toUpperCase() : key.toLowerCase());
}
