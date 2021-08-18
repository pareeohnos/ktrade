import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import Dashboard from "../views/Home.vue";
import Trades from "../views/Home.vue";
import Config from "../views/Config.vue";
import Setup from "../views/Setup.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "/trades",
    name: "Trades",
    component: Trades,
  },
  {
    path: "/config",
    name: "Config",
    component: Config
  },
  {
    path: "/initial_setup",
    name: "Setup",
    component: Setup,
  }
  // {
  //   path: "/config",
  //   name: "Config",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/Config.vue"),
  // },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
