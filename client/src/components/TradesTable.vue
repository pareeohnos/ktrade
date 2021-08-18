<template>
  <table class="w-full divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th class="header">Ticker</th>
        <th class="header">Entry</th>
        <th class="header">Stop</th>
        <th class="header">Shares</th>
        <th class="header">Actions</th>
      </tr>
    </thead>
  </table>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
// import TradeManager from "@/data/trade-manager";

export default defineComponent({
  name: "TradesTable",
  setup() {
    // const tradeManager = new TradeManager();
    const trades = ref([]);
    const loadTrades = async () => {
      // trades.value = await tradeManager.allTrades();
    };

    onMounted(loadTrades);

    return {
      // tradeManager,
      trades,
    };
  },
});
</script>

<style lang="postcss" scoped>
.header {
  @apply px-6;
  @apply py-3;
  @apply text-left;
  @apply text-xs;
  @apply font-medium;
  @apply text-gray-500;
  @apply uppercase;
  @apply tracking-wider;
}
</style>
