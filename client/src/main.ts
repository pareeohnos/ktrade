import { createApp } from 'vue'
import App from './App.vue'
import router from "./router/index";
import axios from "axios";

import './index.css'

// Configuration
axios.defaults.baseURL = "http://localhost:5000";

const app = createApp(App);
app.use(router);

router.isReady().then(() => {
  app.mount("#app");
})

