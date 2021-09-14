import { ref } from "vue";
import Trade from "@/data/models/trade";
// import { unwatch, buy } from "@/components/watched_tickers/actions";
import { trim } from "./actions";
import { notify } from "notiwind"

const gridOptions = {
  getRowNodeId: (data: Trade) => {
    return data.orderId;
  }
};

const gridApi = ref(null);
const colApi = ref(null);
const rowData = ref({});
const rowActionClicked = (action: String, trade: Trade) => {
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
      click(type: String, trade) {
        rowActionClicked(type, trade);
      }
    }
  },
];

const gridReady = params => {
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