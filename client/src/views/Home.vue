<template>
  <div class="flex flex-col">
    <app-panel>
      <base-table class="mb-8" :columns="watchColumns" :row-data="watchedTickers" />
      <app-input v-model="newTicker" />
      <app-button>Add</app-button>
    </app-panel>
  </div>
</template>

<script lang="ts">
import axios from "axios";
import { defineComponent } from "vue";
import AppInput from "@/components/AppInput.vue";
import AppButton from "@/components/AppButton.vue";
import AppHeader from "@/components/AppHeader.vue";
import AppPanel from "@/components/AppPanel.vue";
import BaseTable from "@/components/BaseTable.vue";
import watchColumns from "@/components/watched_tickers/columns";

export default defineComponent({
  components: {
    AppInput,
    AppButton,
    AppHeader,
    AppPanel,
    BaseTable
  },
  setup() {
    return {
      watchColumns
    }
  },
  methods: {
    test() {
      axios.post("/buy");
    },
  },
});
</script>
