<script lang="ts" module>
  export type { BundleMark } from "../lib/api.ts";
</script>

<script lang="ts">
  import type { BundleMark } from "../lib/api.ts";
  // A bundle's mark: its country's flag for a regional one, else its symbol (decision 367).
  import { bundleIcon } from "./BundleSelector.svelte";
  import Flags from "./Flags.svelte";
  import Icon from "./Icon.svelte";

  let { bundle }: { bundle: BundleMark } = $props();
</script>

{#if bundle.region}<Flags country={bundle.country} />{:else}<Icon name={bundleIcon(bundle)} />{/if}
