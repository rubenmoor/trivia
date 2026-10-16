<script lang="ts">
  // The Player screen (plans/04-ui-tv-display.md, "Player", D-28, UI-16): «¿Quién juega?» with the
  // known names and a field for a new one (NamePicker). Names are labels; what the
  // family saw counts for the whole save (plan 65). Each name can be deleted with its games, after a
  // confirmation (GF-7); its seen questions stay seen. The Choice screen comes next (plan 151).
  import { onMount } from "svelte";
  import { deletePlayer, fetchPlayers } from "../../lib/api.ts";
  import { errorText } from "../../lib/errors.ts";
  import { t } from "../../lib/i18n.ts";
  import { focusControl, pushScope } from "../../lib/input.svelte.ts";
  import type { Player } from "../../lib/types.ts";
  import Icon from "../Icon.svelte";
  import NamePicker from "../NamePicker.svelte";
  import Prompt from "../Prompt.svelte";

  let {
    busy,
    onchoose,
    ondeleted,
  }: {
    busy: boolean;
    onchoose: (name: string) => void;
    /** A player was deleted (their running game may be gone too). */
    ondeleted: () => void;
  } = $props();

  let players = $state<Player[]>([]);
  let loaded = $state(false);
  let error = $state<string | null>(null);
  /** The player waiting for «¿Borrar…?» to be confirmed, or null. */
  let doomed = $state<Player | null>(null);
  let deleting = $state(false);
  let cancelButton = $state<HTMLButtonElement>();
  let dialog = $state<HTMLDivElement>();

  onMount(async () => {
    try {
      players = await fetchPlayers();
    } catch (e) {
      error = errorText(e);
    }
    loaded = true;
  });

  async function confirmDelete() {
    if (!doomed || deleting) return;
    deleting = true;
    try {
      players = await deletePlayer(doomed.name);
      error = null;
      ondeleted();
    } catch (e) {
      error = errorText(e);
    } finally {
      deleting = false;
      doomed = null;
    }
  }

  // The delete confirmation gets every action; Esc/Backspace cancel, Enter and Tab work on its buttons.
  $effect(() => {
    if (!doomed) return;
    const pop = pushScope({
      name: "player-delete",
      modal: true,
      whileBusy: true,
      root: () => dialog,
      handle: (a) => {
        if (a.type !== "back" && a.type !== "menu") return false;
        doomed = null;
        return true;
      },
    });
    focusControl(cancelButton); // a stray Enter must not delete anyone
    return pop;
  });
</script>

<section class="player">
  <h1 class="title">{t("screen.player.title")}</h1>

  {#if loaded}<NamePicker {players} {busy} scope="player" {onchoose} ondelete={(p) => (doomed = p)} />{/if}

  {#if error}<p class="error">{error}</p>{/if}

  {#if doomed}
    <div class="backdrop">
      <div class="dialog" bind:this={dialog} role="alertdialog" aria-labelledby="delete-title">
        <h2 id="delete-title">{t("screen.player.confirmOpen")}<span class="doomed">{doomed.name}</span>{t("screen.player.confirmClose")}</h2>
        <p>
          {t("screen.player.confirmBody", {
            lose: doomed.games ? t("screen.player.lose", { n: doomed.games }) : t("screen.player.loseNone"),
          })}
        </p>
        <div class="row">
          <button class="secondary" bind:this={cancelButton} onclick={() => (doomed = null)} data-focus-default><Icon name="back" /> {t("action.cancel")} <Prompt action="menu" pad="back" /></button>
          <button class="danger" onclick={confirmDelete} disabled={deleting}><Icon name="trash" /> {t("screen.player.confirm")}</button>
        </div>
      </div>
    </div>
  {/if}
</section>

<style>
  .player {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(2 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    text-align: center;
  }
  .title {
    animation: arrive 0.6s var(--spring) backwards;
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
    max-width: calc(48 * var(--u));
    padding: calc(2.2 * var(--u)) calc(2.6 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(1.6 * var(--u));
    background: var(--night-700);
    box-shadow: 0 calc(1.5 * var(--u)) calc(4 * var(--u)) rgba(0, 0, 0, 0.6);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1.2 * var(--u));
    animation: arrive 0.35s var(--spring) backwards;
  }
  .dialog h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.4 * var(--u));
    font-weight: 800;
  }
  .doomed {
    color: var(--coral);
  }
  .dialog p {
    margin: 0;
    color: var(--slate-200);
  }
  .danger {
    padding: calc(0.7 * var(--u)) calc(2 * var(--u));
    border: none;
    border-radius: calc(1 * var(--u));
    background: var(--coral);
    color: var(--night-900);
    font-family: var(--font-display);
    font-size: calc(1.6 * var(--u));
    font-weight: 800;
  }
  .danger:focus-visible,
  .danger:global([data-nav]) {
    outline-color: var(--paper);
  }
  .row {
    display: flex;
    gap: calc(1 * var(--u));
    align-items: center;
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
</style>
