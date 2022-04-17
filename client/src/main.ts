import { createApp } from "vue";
import App from "./App.vue";
import router from "./router/index";
import axios from "axios";
import store from "./store/index";
import SocketIO from "socket.io-client";
import VueSocketIO from "vue-socket.io";
// @ts-ignore
import Notifications from "notiwind";

import "./index.css";
import "./global.css";

import "../node_modules/ag-grid-community/dist/styles/ag-grid.css";
import "../node_modules/ag-grid-community/dist/styles/ag-theme-alpine.css";

// Configuration
axios.defaults.baseURL = "http://127.0.0.1:5000";

const app = createApp(App);
app.use(router);
app.use(store);
app.use(Notifications);
app.use(
  new VueSocketIO({
    debug: true,
    connection: SocketIO("http://127.0.0.1:5000", { path: "/socket.io" }),
  })
);

router.isReady().then(() => {
  app.mount("#app");
});
