<template>
  <div class="flex flex-col">
    <app-panel class="overflow-hidden">
      <base-table
        :columns="watchColumns"
        :row-data="rowData">

        <template #actions="{ ticker }">
          <app-button @click="buy(ticker)">Buy</app-button>
          <app-button @click="trim(ticker)" class="ml-4">Trim</app-button>
          <app-button @click="unwatchTicker(ticker)" class="ml-4">Unwatch</app-button>
        </template>
      </base-table>
    </app-panel>

    <app-panel class="p-8 mt-4">
      <div class="w-64">
        <app-input v-model="newTicker" label="Watch a new ticker" />
        <app-button @click="addTicker">Add</app-button>
      </div>
    </app-panel>
  </div>
</template>

<script lang="ts">
import axios from "axios";
import { defineComponent, onMounted, ref, computed } from "vue";
import AppInput from "../components/AppInput.vue";
import AppButton from "../components/AppButton.vue";
import AppHeader from "../components/AppHeader.vue";
import BaseTable from "../components/BaseTable.vue";
import watchColumns from "../components/watched_tickers/columns";
import { unwatch, buy, trim } from "../components/watched_tickers/actions";
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
    const watchedTickers = ref({});
    const addTicker = () => {
      axios
        .post("/watch", {
          ticker: newTicker.value,
        })
        .then(({ data }) => {
          watchedTickers.value[data.id] = { ...data };
        })
        .catch(({ response }) => {
          // console.log(error.response.data.error);
          alert(response.data.error);
          // alert(error);
        });
    };
    const rowData = computed(() => {
      console.log(watchedTickers.value);
      return Object.values(watchedTickers.value);
    });

    const unwatchTicker = (watched) => {
      unwatch(watched).then(() => delete watchedTickers.value[watched.id]);
    }

    onMounted(async () => {
      await axios.get("/watches").then(({ data }) =>
        data.forEach(ticker => watchedTickers.value[ticker.id] = { ...ticker }))
    });

    return {
      addTicker,
      newTicker,
      watchColumns,
      rowData,
      unwatchTicker,
      buy,
      trim
    };
  },
  methods: {
    test() {
      axios.post("/buy");
    },
  },
});
</script>
