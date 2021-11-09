import { ref } from "vue";
import Trade from "@/data/models/trade";
import { trimPosition, deleteTrade, closePosition } from "./actions";
// @ts-ignore
import { notify } from "notiwind";
import {
  GridReadyEvent,
  GridApi,
  ColumnApi,
} from "@ag-grid-community/all-modules";

const gridOptions = {
  getRowNodeId: (data: Trade) => {
    return data.orderId;
  },
};

const gridApi = ref<GridApi>();
const colApi = ref<ColumnApi>();
const rowData = ref<{ [key: string]: Trade }>({});
const rowActionClicked = (action: string, trade: Trade) => {
  switch (action) {
    case "SELL":
      // Get rid of the lot
      break;

    case "TRIM_THIRD":
    case "TRIM_HALF":
      let trimAmount = action === "TRIM_THIRD" ? "THIRD" : "HALF";
      trimPosition(trade, trimAmount);
      break;

    case "CLOSE":
    case "CANCEL":
      closePosition(trade);
      break;

    case "DELETE":
      deleteTrade(trade).then(() => {
        // All done, remove from the grid now
        gridApi.value?.applyTransaction({
          remove: [trade],
        });
      });
      break;
  }
};

const columnDefs = [
  { field: "ticker", headerName: "Ticker" },
  { field: "orderStatus", headerName: "Status" },
  { field: "orderStatusDesc", headerName: "Desc", flex: 1 },
  { field: "currentPositionSize", headerName: "Current position" },
  { field: "filled", headerName: "Filled" },
  { field: "priceAtOrder", headerName: "Price when ordered" },
  { field: "orderedAt", headerName: "Ordered at" },
  {
    field: "actions",
    headerName: "",
    cellClass: "actions",
    pinned: "right",
    width: 65,
    cellStyle() {
      return {
        padding: "0",
      };
    },
    cellRenderer: "ActionsCellRenderer",
    cellRendererParams: {
      click(type: string, trade: Trade) {
        rowActionClicked(type, trade);
      },
    },
  },
];

const gridReady = (params: GridReadyEvent) => {
  gridApi.value = params.api;
  colApi.value = params.columnApi;
  gridApi.value.setRowData(Object.values(rowData.value));
};

export {
  gridOptions,
  colApi,
  columnDefs,
  gridApi,
  gridReady,
  rowActionClicked,
  rowData,
};
