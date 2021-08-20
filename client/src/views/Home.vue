<template>
  <div class="flex flex-row">
    <app-panel class="flex-1 mr-4">
      <app-header class="mb-8">Trades</app-header>
      <trades-table />
      <app-button @click="test">Buy TSLA</app-button>
    </app-panel>

    <app-panel class="flex-initial w-1/4">
      <app-header>Account</app-header>
    </app-panel>
  </div>
</template>

<script lang="ts">
import axios from "axios";
import { defineComponent } from "vue";
import AppButton from "@/components/AppButton.vue";
import AppHeader from "@/components/AppHeader.vue";
import AppPanel from "@/components/AppPanel.vue";
import TradesTable from "@/components/TradesTable.vue";

export default defineComponent({
  components: {
    AppButton,
    AppHeader,
    AppPanel,
    TradesTable,
  },
  methods: {
    test() {
      axios.post("/buy");
    },
  },
});
</script>
