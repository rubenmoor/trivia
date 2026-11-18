import { test } from "node:test";
import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { DEFAULT_SOUNDTRACK, REQUIRED_TRACKS, SOUNDTRACKS, resolveSoundtrack, soundtrackFile, soundtrackIds, soundtrackOf } from "./soundtracks.ts";

const audio = (name: string) => fileURLToPath(new URL(`../../public/audio/${name}.m4a`, import.meta.url));

test("Soundtracks: unknown and old ids fall back to the default", () => {
  for (const id of ["variaciones", "caja", "sin-prisa", "reflejos", "nope", "", null, undefined, 3, "__proto__", "toString"]) {
    assert.equal(resolveSoundtrack(id), DEFAULT_SOUNDTRACK);
  }
  for (const id of soundtrackIds) assert.equal(resolveSoundtrack(id), id);
});

test("Soundtracks: file name is musica-<set>-<track>, null for a variant the set lacks", () => {
  for (const id of soundtrackIds) {
    for (const t of REQUIRED_TRACKS) {
      const has = (soundtrackOf(id).tracks as readonly string[]).includes(t);
      assert.equal(soundtrackFile(id, t), has ? `musica-${id}-${t}` : null);
    }
  }
});

test("Soundtracks: a recorded set lists every required variant and its files exist", () => {
  for (const id of soundtrackIds) {
    const st = soundtrackOf(id);
    if (!st.tracks.length) continue; // generated or not installed
    assert.deepEqual([...st.tracks].sort(), [...REQUIRED_TRACKS].sort(), id);
    assert.ok(st.loopEnd > st.loopStart, `${id}: loop points`);
    for (const t of st.tracks) assert.ok(existsSync(audio(`musica-${id}-${t}`)), `${id}: ${t} file`);
  }
});

test("Soundtracks: no entry named like an old set", () => {
  for (const id of ["variaciones", "caja", "sin-prisa", "reflejos"]) assert.ok(!Object.hasOwn(SOUNDTRACKS, id));
});
