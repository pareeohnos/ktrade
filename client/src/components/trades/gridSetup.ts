import { ref } from "vue";
import Trade from "@/data/models/trade";
import { trim } from "./actions";
// @ts-ignore
import { notify } from "notiwind"
import { GridReadyEvent, GridApi, ColumnApi } from "@ag-grid-community/all-modules";

const gridOptions = {
  getRowNodeId: (data: Trade) => {
    return data.orderId;
  }
};

const gridApi = ref<GridApi>();
const colApi = ref<ColumnApi>();
const rowData = ref<{ [key: string]: Trade; }>({});
const rowActionClicked = (action: string, trade: Trade) => {
  if (action === "SELL") {
    // Get rid of the lot!
  } else {
    let trimAmount = action === "TRIM_THIRD" ? "THIRD" : "HALF";
    trim(trade, trimAmount).then(() => {
      notify({
        group: "notifications",
        title: "Pending",
        text: `Requested sell of 1/3 of ${trade.ticker}`
      }, 2000);
    });
  }
};

const columnDefs = [
  { field: "ticker", headerName: "Ticker" },
  { field: "current_position_size", headerName: "Current position" },
  { field: "filled", headerName: "Filled" },
  { field: "price_at_order", headerName: "Price when ordered" },
  { field: "ordered_at", headerName: "Ordered at" },
  { 
    field: "actions",
    headerName: "Actions",
    cellRenderer: "ActionsCellRenderer",
    cellRendererParams: {
      click(type: string, trade: Trade) {
        rowActionClicked(type, trade);
      }
    }
  },
];

const gridReady = (params: GridReadyEvent) => {
  gridApi.value = params.api;
  colApi.value = params.columnApi;
  gridApi.value.setRowData(Object.values(rowData.value));
}

export { 
  gridOptions,
  colApi,
  columnDefs,
  gridApi,
  gridReady,
  rowActionClicked,
  rowData,
};