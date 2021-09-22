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
    }).catch(err => {
      if (err.response?.data?.error) {
        alert(err.response?.data.error);
      } else {
        alert("Unexpected error occurred");
      }
    });
  }
};

const columnDefs = [
  { field: "ticker", headerName: "Ticker" },
  { field: "orderStatus", headerName: "Status" },
  { field: "orderStatusDesc", headerName: "Desc" },
  { field: "currentPositionSize", headerName: "Current position" },
  { field: "filled", headerName: "Filled" },
  { field: "priceAtOrder", headerName: "Price when ordered" },
  { field: "orderedAt", headerName: "Ordered at" },
  { 
    field: "actions",
    headerName: "Actions",
    cellClass: "actions",
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