<template>
  <div class="ktrade bg-gray-200">
    <navigation />

    <div class="p-8 h-full w-full">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Navigation from "@/components/Navigation.vue";

export default defineComponent({
  components: {
    Navigation,
  },
  name: "App",
});
</script>
