<template>
  <div class="flex flex-col">
    <app-panel>
      <base-table
        class="mb-8"
        :columns="watchColumns"
        :row-data="watchedTickers"
      />
    </app-panel>

    <app-panel class="p-8">
      <div class="w-64">
        <app-input v-model="newTicker" label="Watch a new ticker" />
        <app-button @click="addTicker">Add</app-button>
      </div>
    </app-panel>
  </div>
</template>

<script lang="ts">
import axios from "axios";
import { defineComponent, ref } from "vue";
import AppInput from "../components/AppInput.vue";
import AppButton from "../components/AppButton.vue";
import AppHeader from "../components/AppHeader.vue";
import BaseTable from "../components/BaseTable.vue";
import watchColumns from "../components/watched_tickers/columns";
import AppPanel from "../components/AppPanel.vue";

export default defineComponent({
  components: {
    AppInput,
    AppButton,
    AppHeader,
    AppPanel,
    BaseTable,
  },
  setup() {
    const newTicker = ref("");
    const watchedTickers = ref([]);
    const addTicker = () => {
      axios
        .post("/watch", {
          ticker: newTicker.value,
        })
        .then((result) => {
          watchedTickers.value.push(result);
          console.log(result);
        })
        .catch(({ response }) => {
          // console.log(error.response.data.error);
          alert(response.data.error);
          // alert(error);
        });
    };
    return {
      addTicker,
      newTicker,
      watchColumns,
    };
  },
  methods: {
    test() {
      axios.post("/buy");
    },
  },
});
</script>
