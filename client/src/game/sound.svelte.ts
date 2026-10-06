// PLACEHOLDER(UI-8, UI-10): no audio engine and no sound files yet. Music and effects are
// shown as captions in the corner (Captions.svelte) instead of playing. The call sites already
// sit where 04-ui-tv-display.md wants each sound, so UI-8 only has to replace this file.

export type Track = "normal" | "question" | "submitted";

export const sound = $state({
  music: null as Track | null,
  effects: [] as { id: number; name: string }[],
});

let seq = 0;

/** Play a short effect (for now: show its name for a moment). */
export function sfx(name: string) {
  const id = ++seq;
  sound.effects = [...sound.effects, { id, name }].slice(-4);
  setTimeout(() => (sound.effects = sound.effects.filter((e) => e.id !== id)), 2000);
}

/** Switch the music loop; null = silence. */
export function music(track: Track | null) {
  sound.music = track;
}
