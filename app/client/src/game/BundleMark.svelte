<script lang="ts" module>
  import type { Bundle } from "./BundleSelector.svelte";

  export type BundleMark = Pick<Bundle, "base" | "region" | "country" | "icon" | "source">;
</script>

<script lang="ts">
  // A bundle's mark: its country's flag for a regional one, else its symbol (decision 367).
  import { bundleIcon } from "./BundleSelector.svelte";
  import Flags from "./Flags.svelte";
  import Icon from "./Icon.svelte";

  let { bundle }: { bundle: BundleMark } = $props();
</script>

{#if bundle.region}<Flags country={bundle.country} />{:else}<Icon name={bundleIcon(bundle)} />{/if}
