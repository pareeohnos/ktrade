import { createStore } from "vuex";

// Create a new store instance.
const store = createStore({
  state() {
    return {};
  },
  mutations: {},
  actions: {
    SOCKET_TICKER_UPDATE(message) {
      console.log(message);
    },
  },
});

export default store;
