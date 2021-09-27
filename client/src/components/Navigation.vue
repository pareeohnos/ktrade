<template>
  <div class="bg-gray-700 flex flex-col text-white pt-4 px-8">
    <h1 class="text-2xl">KTrade</h1>
    <div class="flex flex-row mt-auto">
      <router-link class="menu-item" to="/">Dashboard</router-link>
      <router-link class="menu-item" to="/trades">Trades</router-link>
      <router-link class="menu-item" to="/config">Settings</router-link>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from "vue";

  export default defineComponent({
    name: "Navigation",
  });
</script>

<style lang="postcss" scoped>
  .menu-item {
    @apply relative;
    @apply block;
    @apply no-underline;
    @apply pt-4;
    @apply pb-1;
    @apply px-4;
    z-index: 1;

    &.router-link-active {
      @apply text-gray-800;

      &:after {
        content: "";
        @apply absolute;
        @apply left-0;
        @apply right-0;
        @apply bottom-0;
        @apply top-2;
        @apply rounded-t;
        z-index: -1;
        @apply bg-blue-400;
      }
    }
  }
</style>
