// The soundtrack sets (plans/25-sound.md "Engine"): pure data and lookups, no audio; the engine is sound.svelte.ts.

/** The loops a set can have; `roll` and `victory` are shared files, not per set (the brief). */
export type SetTrack = "normal" | "question" | "submitted" | "timed";

/** Every recorded set has all of these (decision 734: one mixdown per variant). */
export const REQUIRED_TRACKS: readonly SetTrack[] = ["normal", "question", "submitted", "timed"];

/** A soundtrack set. `tracks`: the variants with a file `musica-<set>-<track>.m4a` in `public/audio/`
 * (none: not installed, or generated); recorded variants all have the same length, so a cut between them
 * keeps the beat. The loop plays `loopStart`..`loopEnd` seconds (AAC pads the end: loop on the bars, not the
 * file length); `level` lifts it to the music bus. */
export type Soundtrack = {
  tracks: readonly SetTrack[];
  loopStart: number;
  loopEnd: number;
  level: number;
};

// Loop points and levels come from `authoring/data/music/<set>-<piece>.json` (`app/` can't read it).
export const SOUNDTRACKS = {
  // The brief's sets (plans/25-sound.md "Brief"); a set not installed yet plays the generated loops (plan 224)
  // chill-lofi, Late Night Radio: record lofi-tranquilo-late-night-radio.json, 72 bpm, 8 bars
  "lofi-tranquilo": { tracks: REQUIRED_TRACKS, loopStart: 0, loopEnd: 26.667, level: 1 },
  "acustica-calida": { tracks: [], loopStart: 0, loopEnd: 0, level: 1 }, // warm-acoustic, Bossa Antigua
  "jazz-de-concurso": { tracks: [], loopStart: 0, loopEnd: 0, level: 1 }, // jazz-quiz-show, Backbay Lounge
} as const satisfies Record<string, Soundtrack>;

export type SoundtrackId = keyof typeof SOUNDTRACKS;
export const DEFAULT_SOUNDTRACK: SoundtrackId = "lofi-tranquilo";
export const soundtrackIds = Object.keys(SOUNDTRACKS) as SoundtrackId[];

export const soundtrackOf = (id: SoundtrackId): Soundtrack => SOUNDTRACKS[id];

/** An id that isn't a known soundtrack (old ids included) is the default. */
export function resolveSoundtrack(id: unknown): SoundtrackId {
  return typeof id === "string" && Object.hasOwn(SOUNDTRACKS, id) ? (id as SoundtrackId) : DEFAULT_SOUNDTRACK;
}

/** The file (without `.m4a`) of a set's variant; null when the set has none: the generated loop plays. */
export function soundtrackFile(id: SoundtrackId, track: SetTrack): string | null {
  return (soundtrackOf(id).tracks as readonly SetTrack[]).includes(track) ? `musica-${id}-${track}` : null;
}

/** Every file name of every set. */
export const soundtrackFiles = (): string[] =>
  soundtrackIds.flatMap((id) => soundtrackOf(id).tracks.map((t) => `musica-${id}-${t}`));

/** Equal length per set: a cut between two variants keeps the beat. */
export const sameBeat = (id: SoundtrackId): boolean => soundtrackOf(id).tracks.length > 0;
