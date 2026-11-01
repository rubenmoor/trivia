/** A random item, never `last` unless it is the only one; undefined for an empty list. */
export function pickVariant<T>(items: readonly T[], last?: T, random = Math.random): T | undefined {
  const others = items.filter((x) => x !== last);
  const from = others.length ? others : items;
  return from[Math.floor(random() * from.length)];
}
