<script lang="ts">
  // The Join screen (plans/04-ui-tv-display.md, "Join"; plan 162, decision 292): who plays a local multiplayer
  // session, with which device. An unbound pad's A joins it, a bound pad's B leaves its seat, the keyboard joins by its
  // card; every device drives the rest. Keyboard-only `timed` seats pick their claim key (decision 290). Seats, names
  // and groups are Game.svelte's draft; «Seguir» goes to the Bundles screen.
  import { onMount, tick, untrack } from "svelte";
  import { casefold } from "../../engine/pycompat.ts";
  import { MIN_SEATS } from "../../engine/game.ts";
  import { DEFAULT_AGE_GROUP, fetchChoice, fetchChoiceOptions, fetchPlayers, type ChoiceOptions } from "../../lib/api.ts";
  import { errorText } from "../../lib/errors.ts";
  import { padStyle, padStyleOf } from "../../lib/gamepad.svelte.ts";
  import { t } from "../../lib/i18n.ts";
  import { focusControl, pushScope } from "../../lib/input.svelte.ts";
  import { joinKeyboard, joinPad, unboundPad, type Binding } from "../../lib/seats.ts";
  import type { GameMode, Player } from "../../lib/types.ts";
  import Glyph from "../Glyph.svelte";
  import Icon from "../Icon.svelte";
  import NamePicker from "../NamePicker.svelte";
  import Prompt from "../Prompt.svelte";
  import SeatDevice from "../SeatDevice.svelte";
  import { claimKeyOk } from "../question/keys.ts";
  import { seatColor, type SeatDraft } from "../seats.ts";

  let {
    mode,
    player,
    busy,
    seats,
    onseats,
    onnext,
    onback,
  }: {
    mode: GameMode;
    /** The Player screen's name: the first seat's preset. */
    player: string;
    busy: boolean;
    /** The draft from an earlier visit, else empty. */
    seats: SeatDraft[];
    onseats: (seats: SeatDraft[]) => void;
    onnext: () => void;
    onback: () => void;
  } = $props();

  const timed = untrack(() => mode) === "timed";
  const padOf = (b: Binding) => (typeof b === "object" && "pad" in b ? b.pad : null);
  const keyOf = (b: Binding) => (typeof b === "object" && "key" in b ? b.key : null);

  /** Keyboard seats as the mode needs them: no pad seated, no `kbm`; round-robin, no keys (decisions 273, 274). */
  function fit(list: SeatDraft[]): SeatDraft[] {
    const pads = list.some((s) => padOf(s.binding) !== null);
    return list.map((s) => (!pads && s.binding === "kbm") || (!timed && keyOf(s.binding)) ? { ...s, binding: "shared" } : s);
  }

  let list = $state(fit(untrack(() => seats)));
  untrack(() => onseats($state.snapshot(list) as SeatDraft[]));
  let players = $state<Player[]>([]);
  let options = $state<ChoiceOptions | null>(null);
  let error = $state<string | null>(null);
  /** Why a pad's A didn't join. */
  let notice = $state<string | null>(null);
  /** The seat whose name dialog is open. */
  let naming = $state<number | null>(null);
  let nameRefusal = $state<string | null>(null);
  /** The key capture: for a new seat (`seat` null) or a seat's re-pick. */
  let capture = $state<{ seat: number | null } | null>(null);
  let keyRefusal = $state<string | null>(null);
  let keyField = $state<HTMLInputElement>();
  let section = $state<HTMLElement>();
  let padTick = $state(0);

  onMount(() => {
    void (async () => {
      try {
        [players, options] = await Promise.all([fetchPlayers(), fetchChoiceOptions()]);
      } catch (e) {
        error = errorText(e);
      }
    })();
    const bump = () => padTick++;
    window.addEventListener("gamepadconnected", bump);
    window.addEventListener("gamepaddisconnected", bump);
    return () => {
      window.removeEventListener("gamepadconnected", bump);
      window.removeEventListener("gamepaddisconnected", bump);
    };
  });

  const bindings = $derived(list.map((s) => s.binding));
  const hasPad = $derived(bindings.some((b) => padOf(b) !== null));
  /** Connected pads bound to no seat. */
  const freePads = $derived.by(() => {
    void padTick;
    return navigator.getGamepads()
      .filter((g): g is Gamepad => g !== null && g.mapping === "standard" && !bindings.some((b) => padOf(b) === g.index))
      .map((g) => g.index);
  });
  const keyboardOpen = $derived(joinKeyboard(bindings, null) !== null);
  const why = $derived(
    list.length < MIN_SEATS ? t("screen.join.tooFew", { min: MIN_SEATS })
    : list.some((s) => !s.name) ? t("screen.join.unnamed")
    : timed && list.some((s) => s.binding === "shared") ? t("screen.join.keyless")
    : null,
  );

  function update(next: SeatDraft[]) {
    list = fit(next);
    onseats($state.snapshot(list) as SeatDraft[]);
  }

  /** `next` bindings over the seats so far, a new seat last. */
  async function seated(next: Binding[]) {
    notice = null;
    const name = list.length === 0 ? player : null;
    update(next.map((binding, i) => (i < list.length ? { ...list[i], binding } : { binding, name, group: DEFAULT_AGE_GROUP })));
    const at = list.length - 1;
    if (name) void presetGroup(at, name);
    await tick();
    focusControl(section?.querySelector<HTMLElement>(`[data-focus-id="seat-name-${at}"]`));
  }

  function joinWithPad(pad: number) {
    const next = joinPad(bindings, pad);
    if (next) void seated(next);
    else notice = t("screen.join.padRefused");
  }

  function joinWithKeyboard() {
    if (busy) return;
    if (timed && !hasPad) return void (capture = { seat: null });
    const next = joinKeyboard(bindings, null);
    if (next) void seated(next);
  }

  function leave(i: number) {
    if (busy) return;
    notice = null;
    update(list.filter((_, j) => j !== i));
  }

  /** That player's newest group (their `playerChoice`), else the default. */
  async function presetGroup(i: number, name: string) {
    const group = await fetchChoice({ player: name }).then((c) => c.choice.age_group, () => null);
    if (list[i]?.name === name) update(list.map((s, j) => (j === i ? { ...s, group: group ?? DEFAULT_AGE_GROUP } : s)));
  }

  const sameName = (a: string, b: string) => casefold(a) === casefold(b);
  const otherNames = (i: number) => list.flatMap((s, j) => (j !== i && s.name ? [s.name] : []));

  function named(name: string) {
    const i = naming;
    if (i === null) return;
    if (otherNames(i).some((n) => sameName(n, name))) return void (nameRefusal = t("screen.join.nameTaken", { name }));
    update(list.map((s, j) => (j === i ? { ...s, name } : s)));
    closeNaming();
    void presetGroup(i, name);
  }

  function closeNaming() {
    naming = null;
    nameRefusal = null;
  }

  function stepGroup(i: number, by: number) {
    if (busy || !options) return;
    const ids = options.groups.map((g) => g.id);
    const at = Math.max(0, ids.indexOf(list[i].group));
    update(list.map((s, j) => (j === i ? { ...s, group: ids[(at + by + ids.length) % ids.length] } : s)));
  }

  const keyText = (k: string) => (k === " " ? t("picker.space") : k.toUpperCase());

  /** A key typed into the capture field: the seat's claim key, or why not (decision 290). */
  function typedKey(e: Event) {
    const field = e.currentTarget as HTMLInputElement;
    const k = [...field.value].at(-1)?.toLowerCase() ?? "";
    field.value = "";
    if (!k || !capture) return;
    const seat = capture.seat;
    const taken = list.flatMap((s, j) => (j !== seat && keyOf(s.binding) ? [keyOf(s.binding)!] : []));
    if (!claimKeyOk(k, taken)) {
      keyRefusal = t(claimKeyOk(k, []) ? "screen.join.keyTaken" : "screen.join.keyReserved", { key: keyText(k) });
      return;
    }
    closeCapture();
    if (seat !== null) update(list.map((s, j) => (j === seat ? { ...s, binding: { key: k } } : s)));
    else {
      const next = joinKeyboard(bindings, k);
      if (next) void seated(next);
    }
  }

  function closeCapture() {
    capture = null;
    keyRefusal = null;
  }

  function next() {
    if (busy || why) return;
    onnext();
  }

  // An unbound pad's A joins, a bound pad's B leaves; Backspace and an unbound pad's B go back; ←/→ on a seat's group.
  $effect(() =>
    pushScope({
      name: "join",
      root: () => section,
      pressable: (el, a) => unboundPad(a.source, a, bindings) === null && !el.dataset.step,
      handle: (a) => {
        padTick++;
        const pad = unboundPad(a.source, a, bindings);
        const stepping = document.activeElement instanceof HTMLElement ? document.activeElement.dataset.step : undefined;
        if (pad !== null) joinWithPad(pad);
        else if (a.type === "back") {
          const at = typeof a.source === "object" ? bindings.findIndex((b) => padOf(b) === (a.source as { pad: number }).pad) : -1;
          if (at >= 0) leave(at);
          else onback();
        }
        else if (a.type === "navigate" && (a.dir === "left" || a.dir === "right") && stepping) stepGroup(Number(stepping), a.dir === "right" ? 1 : -1);
        else if (a.type === "confirm" && !stepping) next();
        else return false;
        return true;
      },
    }),
  );

  // The key capture: the next letter or digit typed is the key; Esc, Backspace or B cancel.
  $effect(() => {
    if (!capture) return;
    const pop = pushScope({
      name: "join-key",
      modal: true,
      handle: (a) => {
        if (a.type === "back" || a.type === "menu") closeCapture();
        return true;
      },
    });
    keyField?.focus();
    return pop;
  });
</script>

<section class="join" bind:this={section}>
  <h1 class="title">{t("screen.join.title")}</h1>

  <div class="seats" data-nav-scroll>
    {#each list as s, i (i)}
      {@const key = keyOf(s.binding)}
      {@const pad = padOf(s.binding)}
      <div class="seat glass" style:--seat={seatColor(i)}>
        <div class="device">
          {#if pad !== null}<SeatDevice binding={s.binding} />
          {:else if s.binding === "kbm" || !timed}<SeatDevice binding={s.binding} /> {t("screen.join.keyboardMouse")}
          {:else}
            <button class="secondary small" onclick={() => (capture = { seat: i })} disabled={busy} data-focus-id="seat-key-{i}">
              {#if key}<SeatDevice binding={s.binding} /> {t("screen.join.changeKey")}{:else}<Icon name="keyboard" /> {t("screen.join.pickKey")}{/if}
            </button>
          {/if}
          <button class="remove" onclick={() => leave(i)} disabled={busy} title={t("screen.join.remove")} data-focus-id="seat-remove-{i}">
            {#if pad !== null}<Glyph button={1} set={padStyleOf(pad)} />{:else}<Icon name="cross" />{/if}
          </button>
        </div>
        <button class="name" class:empty={!s.name} onclick={() => (naming = i)} disabled={busy} data-focus-id="seat-name-{i}">
          <Icon name={s.name ? "person" : "pencil"} /> {s.name ?? t("screen.join.pickName")}
        </button>
        {#if mode === "rr-competitive" && options}
          {@const g = options.groups.find((x) => x.id === s.group)}
          <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
          <div class="group" data-step={i} data-focusable tabindex="0" role="group" aria-label={t("choice.groups")} data-focus-id="seat-group-{i}">
            <button class="step" onclick={() => stepGroup(i, -1)} disabled={busy} tabindex="-1" aria-label={t("overlay.less")}>−</button>
            <span>{g?.name ?? s.group}</span>
            <button class="step" onclick={() => stepGroup(i, 1)} disabled={busy} tabindex="-1" aria-label={t("overlay.more")}>+</button>
          </div>
        {/if}
      </div>
    {/each}

    {#each freePads.length ? freePads : [null] as p (p ?? "any")}
      <div class="seat open glass">
        <Glyph button={0} set={p === null ? padStyle.current : padStyleOf(p)} size="2.2em" />
        <span>{t("screen.join.padJoin")}</span>
      </div>
    {/each}
    {#if keyboardOpen}
      <button class="seat open glass" onclick={joinWithKeyboard} disabled={busy} data-focus-default data-focus-id="join-keyboard">
        <Icon name="keyboard" size="2.2em" />
        <span>{t("screen.join.keyboardJoin")}</span>
      </button>
    {/if}
  </div>

  {#if notice}<p class="notice">{notice}</p>{/if}

  <div class="actions">
    <button class="secondary" onclick={onback} disabled={busy} data-focus-id="back"><Icon name="back" /> {t("action.back")} <Prompt action="back" /></button>
    <button class="candy" onclick={next} disabled={busy || why !== null} data-focus-id="next"><Icon name="next" /> {t("action.next")} <Prompt action="confirm" off={why !== null} /></button>
  </div>
  {#if why}<p class="label">{why}</p>{/if}
  {#if error}<p class="error">{error}</p>{/if}
</section>

{#if naming !== null}
  <div class="backdrop">
    <div class="dialog" role="dialog" aria-labelledby="join-name-title" style:--seat={seatColor(naming)}>
      <h2 id="join-name-title">{t("screen.join.nameTitle")}</h2>
      <NamePicker
        players={players.filter((p) => !otherNames(naming!).some((n) => sameName(n, p.name)))}
        {busy}
        scope="join-name"
        modal
        refusal={nameRefusal}
        submitLabel={t("picker.done")}
        onchoose={named}
        onclose={closeNaming}
      />
      <button class="secondary" onclick={closeNaming}><Icon name="back" /> {t("action.cancel")} <Prompt action="menu" pad="back" /></button>
    </div>
  </div>
{/if}

{#if capture}
  <div class="backdrop">
    <div class="dialog" role="dialog" aria-labelledby="join-key-title">
      <h2 id="join-key-title">{t("screen.join.keyTitle")}</h2>
      <p>{t("screen.join.keyBody")}</p>
      <input class="key-field" bind:this={keyField} oninput={typedKey} onblur={() => keyField?.focus()} autocomplete="off" spellcheck="false" aria-labelledby="join-key-title" />
      {#if keyRefusal}<p class="error">{keyRefusal}</p>{/if}
      <button class="secondary" onclick={closeCapture}><Icon name="back" /> {t("action.cancel")} <Prompt action="menu" pad="back" /></button>
    </div>
  </div>
{/if}

<style>
  .join {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(1.2 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    text-align: center;
  }
  .title {
    animation: arrive 0.6s var(--spring) backwards;
  }
  .seats {
    display: grid;
    grid-template-columns: repeat(auto-fill, calc(24 * var(--u)));
    grid-auto-rows: max-content;
    justify-content: center;
    gap: calc(1.2 * var(--u));
    width: 100%;
    max-width: calc(106 * var(--u));
    max-height: calc(38 * var(--u));
    padding: calc(0.6 * var(--u));
    overflow-y: auto;
    scrollbar-width: thin;
  }
  .seat.glass {
    display: flex;
    flex-direction: column;
    gap: calc(0.6 * var(--u));
    min-height: calc(10 * var(--u));
    padding: calc(0.8 * var(--u)) calc(1 * var(--u));
    border-color: var(--seat);
    border-width: calc(0.25 * var(--u));
    text-align: left;
    animation: arrive 0.4s var(--spring) backwards;
  }
  .seat.open.glass {
    align-items: center;
    justify-content: center;
    border-style: dashed;
    border-width: 1px;
    border-color: var(--slate-400);
    color: var(--slate-200);
    font-size: calc(1.3 * var(--u));
    font-weight: 700;
    text-align: center;
  }
  button.seat.open:hover:not(:disabled),
  button.seat.open:focus-visible,
  button.seat.open:global([data-nav]) {
    border-color: var(--sky);
    color: var(--paper);
  }
  .device {
    display: flex;
    align-items: center;
    gap: calc(0.6 * var(--u));
    min-height: calc(2.6 * var(--u));
    color: var(--seat);
    font-size: calc(1.3 * var(--u));
    font-weight: 700;
  }
  .device > :global(.icon) {
    font-size: calc(2.2 * var(--u));
  }
  .small {
    padding: calc(0.2 * var(--u)) calc(0.7 * var(--u));
    font-size: calc(1.1 * var(--u));
  }
  .small > :global(.seat-key) {
    font-size: calc(1.6 * var(--u));
    color: var(--seat);
  }
  .remove {
    display: grid;
    place-items: center;
    width: calc(2.2 * var(--u));
    height: calc(2.2 * var(--u));
    margin-left: auto;
    padding: 0;
    border: 1px solid var(--slate-600);
    border-radius: 50%;
    background: var(--night-700);
    color: var(--slate-400);
    font-size: calc(1.1 * var(--u));
  }
  .remove:hover:not(:disabled),
  .remove:focus-visible,
  .remove:global([data-nav]) {
    color: var(--coral);
    border-color: var(--coral);
  }
  .name {
    padding: calc(0.3 * var(--u)) calc(0.6 * var(--u));
    border: 1px solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: none;
    color: var(--paper);
    font-family: var(--font-display);
    font-size: calc(1.9 * var(--u));
    font-weight: 800;
    line-height: 1.1;
    text-align: left;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .name.empty {
    color: var(--amber);
  }
  .name:hover:not(:disabled),
  .name:focus-visible,
  .name:global([data-nav]) {
    border-color: var(--seat);
  }
  .group {
    display: grid;
    grid-template-columns: calc(2.2 * var(--u)) 1fr calc(2.2 * var(--u));
    align-items: center;
    gap: calc(0.5 * var(--u));
    padding: calc(0.2 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(0.8 * var(--u));
    font-size: calc(1.2 * var(--u));
    font-weight: 700;
    text-align: center;
    outline: none;
  }
  .group:focus,
  .group:global([data-nav]),
  .group:hover {
    border-color: var(--amber);
  }
  .step {
    display: grid;
    place-items: center;
    height: calc(2 * var(--u));
    padding: 0;
    border-radius: calc(0.6 * var(--u));
    background: var(--slate-600);
    font-size: calc(1.3 * var(--u));
    font-weight: 700;
  }
  .notice {
    margin: 0;
    color: var(--amber);
    font-size: calc(1.2 * var(--u));
  }
  .actions {
    display: flex;
    gap: calc(1.2 * var(--u));
    align-items: center;
    margin-top: calc(0.6 * var(--u));
  }
  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 10;
    display: grid;
    place-items: center;
    background: var(--dim);
  }
  .dialog {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1.2 * var(--u));
    max-width: calc(100 * var(--u));
    padding: calc(2.2 * var(--u)) calc(2.6 * var(--u));
    border: 1px solid var(--seat, var(--slate-600));
    border-radius: calc(1.6 * var(--u));
    background: var(--night-700);
    box-shadow: 0 calc(1.5 * var(--u)) calc(4 * var(--u)) rgba(0, 0, 0, 0.6);
    animation: arrive 0.35s var(--spring) backwards;
  }
  .dialog h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.4 * var(--u));
    font-weight: 800;
  }
  .dialog p {
    margin: 0;
    color: var(--slate-200);
  }
  .key-field {
    width: calc(5 * var(--u));
    padding: calc(0.4 * var(--u));
    border: 1px solid var(--sky);
    border-radius: calc(0.8 * var(--u));
    background: rgba(11, 17, 32, 0.6);
    color: transparent;
    caret-color: var(--sky);
    font-size: calc(2.4 * var(--u));
    text-align: center;
    outline: none;
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
</style>
