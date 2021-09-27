<template>
  <div class="flex flex-col h-full">
    <app-panel class="overflow-hidden flex-1">
      <ag-grid-vue
        class="h-full w-full ag-theme-alpine"
        :columnDefs="columnDefs"
        :gridOptions="gridOptions"
        @grid-ready="gridReady"
      />
    </app-panel>

    <app-panel class="p-8 mt-4 flex-initial">
      <div class="w-64">
        <app-input v-model="newTicker" label="Watch a new ticker" />
        <app-button @click="addTicker">Add</app-button>
      </div>
    </app-panel>
  </div>
</template>

<script lang="ts">
  import { AgGridVue } from "ag-grid-vue3";
  import axios from "axios";
  import { defineComponent, onMounted, ref } from "vue";
  import AppInput from "../components/AppInput.vue";
  import AppButton from "../components/AppButton.vue";
  import AppHeader from "../components/AppHeader.vue";
  import {
    colApi,
    columnDefs,
    gridApi,
    gridReady,
    rowActionClicked,
    rowData,
    gridOptions,
  } from "../components/watched_tickers/gridSetup";
  import AppPanel from "../components/AppPanel.vue";
  import ActionsCellRenderer from "../components/watched_tickers/ActionsCellRenderer.vue";
  import WatchedTicker from "@/data/models/watched-ticker";

  export interface Home {
    rowActionClicked: () => void;
  }

  export default defineComponent({
    components: {
      ActionsCellRenderer,
      AgGridVue,
      AppInput,
      AppButton,
      AppHeader,
      AppPanel,
    },
    sockets: {
      tickerUpdated({
        watched_ticker_id,
        field,
        value,
      }: {
        watched_ticker_id: number;
        field: string;
        value: number;
      }) {
        let itemToUpdate: WatchedTicker = this.gridApi!.getRowNode(
          watched_ticker_id.toString()
        )?.data;

        if (itemToUpdate) {
          // @ts-ignore
          itemToUpdate[field] = value;

          this.gridApi?.applyTransactionAsync({
            update: [itemToUpdate],
          });
        }
      },
    },
    setup() {
      const newTicker = ref<string>("");

      const addTicker = () => {
        axios
          .post("/watch", {
            ticker: newTicker.value,
          })
          .then(({ data }) => {
            gridApi.value?.applyTransaction({
              add: [data],
            });
          })
          .catch((err) => {
            // console.log(error.response.data.error);
            if (err.response?.data?.error) {
              alert(err.response?.data.error);
            } else {
              alert("Unexpected error occurred");
              console.log(err);
            }
            // alert(error);
          });
      };

      onMounted(async () => {
        // Get our list of watched tickers and load them into
        // memory, and the table
        await axios.get("/watches").then(({ data }) => {
          data.forEach((watchedTicker: WatchedTicker) => {
            rowData.value[watchedTicker.id] = watchedTicker;
          });

          if (gridApi.value) {
            gridApi.value.setRowData(data);
          }
        });
      });

      return {
        addTicker,
        newTicker,
        columnDefs,
        rowActionClicked,
        rowData,

        gridApi,
        colApi,
        gridOptions,
        gridReady,
      };
    },
  });
</script>
