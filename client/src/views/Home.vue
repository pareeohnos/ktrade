<template>
  <div class="flex flex-row">
    <app-panel class="flex-1 mr-4">
      <app-header class="mb-8">Trades</app-header>
      <trades-table />
    </app-panel>

    <app-panel class="flex-initial w-1/4">
      <app-header>Account</app-header>
    </app-panel>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AppHeader from "@/components/AppHeader.vue";
import AppPanel from "@/components/AppPanel.vue";
import TradesTable from "@/components/TradesTable.vue";

export default defineComponent({
  components: {
    AppHeader,
    AppPanel,
    TradesTable,
  },
});
</script>
