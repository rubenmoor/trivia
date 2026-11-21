/** One key per bundle (plan 29): the first letter of its name (after a «Regional:»-style prefix), accents
 * stripped, not taken by an earlier bundle nor in `reserved`, else the name's next letter; "" if none is left.
 * Only Latin letters count (decision 671: a chip must be typable); a name without any (CJK) gets the next free a-z. */
export function bundleKeys(names: string[], reserved: string[]): string[] {
  const taken = new Set(reserved.map((k) => k.toLowerCase()));
  return names.map((name) => {
    const ordered = name.includes(":") ? name.slice(name.lastIndexOf(":") + 1) + name : name;
    const letters = [...ordered.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase()].filter((c) => /\p{Script=Latin}/u.test(c));
    const key = (letters.length ? letters : [..."abcdefghijklmnopqrstuvwxyz"]).find((c) => !taken.has(c)) ?? "";
    if (key) taken.add(key);
    return key;
  });
}
