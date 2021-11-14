import { ref } from "vue";
import WatchedTicker from "@/data/models/watched-ticker";
import { unwatch, buy } from "@/components/watched_tickers/actions";
// @ts-ignore
import { notify } from "notiwind";
import {
  GridReadyEvent,
  GridApi,
  ColumnApi,
} from "@ag-grid-community/all-modules";

const gridOptions = {
  getRowNodeId: (data: WatchedTicker) => {
    return data.id;
  },
};

const gridApi = ref<GridApi>();
const colApi = ref<ColumnApi>();
const rowData = ref<{ [key: string]: WatchedTicker }>({});
const rowActionClicked = (action: String, watchedTicker: WatchedTicker) => {
  if (action === "UNWATCH") {
    unwatch(watchedTicker).then(() => {
      gridApi?.value?.applyTransaction({ remove: [watchedTicker] });
      notify(
        {
          group: "notifications",
          title: "Success",
          text: `${watchedTicker.ticker} was successfully unwatched`,
          type: "success",
        },
        2000
      );
    });
  } else if (action === "BUY") {
    buy(watchedTicker);
  }
};

const columnDefs = [
  { field: "ticker", headerName: "Ticker" },
  { field: "price", headerName: "Price", enableCellChangeFlash: true },
  { field: "adr", headerName: "ADR" },
  { field: "low", headerName: "LOD" },
  { field: "high", headerName: "HOD" },
  {
    field: "actions",
    headerName: "Actions",
    cellRenderer: "ActionsCellRenderer",
    cellRendererParams: {
      click(type: String, watchedTicker: WatchedTicker) {
        rowActionClicked(type, watchedTicker);
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
