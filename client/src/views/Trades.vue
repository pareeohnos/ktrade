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
    gridOptions,
    colApi,
    columnDefs,
    gridApi,
    gridReady,
    rowActionClicked,
    rowData,
  } from "../components/trades/gridSetup";
  import AppPanel from "../components/AppPanel.vue";
  import ActionsCellRenderer from "../components/trades/ActionsCellRenderer.vue";
  import Trade from "@/data/models/trade";

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
      tradeFilled({ order_id, amount }: { order_id: number; amount: number }) {
        let itemToUpdate: Trade = this.gridApi!.getRowNode(
          order_id.toString()
        )?.data;

        if (itemToUpdate) {
          // @ts-ignore
          itemToUpdate.filled += amount;
          itemToUpdate.currentPositionSize += amount;

          this.gridApi?.applyTransactionAsync({
            update: [itemToUpdate],
          });
        }
      },
      tradeSold({ order_id, amount }: { order_id: number; amount: number }) {
        let itemToUpdate: Trade = this.gridApi!.getRowNode(
          order_id.toString()
        )?.data;

        if (itemToUpdate) {
          // @ts-ignore
          itemToUpdate.currentPositionSize -= amount;

          this.gridApi?.applyTransactionAsync({
            update: [itemToUpdate],
          });
        }
      },
      tradeStatus({
        order_id,
        status,
        description,
      }: {
        order_id: number;
        status: string;
        description: string;
      }) {
        let itemToUpdate: Trade = this.gridApi!.getRowNode(
          order_id.toString()
        )?.data;

        if (itemToUpdate) {
          // @ts-ignore
          itemToUpdate.orderStatus = status;
          itemToUpdate.orderStatusDesc = description;

          this.gridApi?.applyTransactionAsync({
            update: [itemToUpdate],
          });
        }
      },
    },
    setup() {
      // const newTicker = ref("");

      onMounted(async () => {
        // Get our list of watched tickers and load them into
        // memory, and the table
        await axios.get("/trades").then(({ data }) => {
          data.forEach((trade: Trade) => {
            rowData.value[trade.orderId] = trade;
          });

          if (gridApi.value) {
            gridApi.value.setRowData(data);
          }
        });
      });

      return {
        // addTicker,
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
