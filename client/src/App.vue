<template>
  <div class="ktrade bg-gray-200">
    <navigation v-if="!isSetup" />

    <div class="p-8 h-full w-full">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { useRoute } from 'vue-router';
import { defineComponent, computed, onMounted } from "vue";
import Navigation from "@/components/Navigation.vue";

export default defineComponent({
  components: {
    Navigation,
  },
  name: "App",
  setup(_, ctx) {
    const route = useRoute();
    const isSetup = computed(() => route.name === "Setup");
    
    return {
      isSetup
    }
  }
});
</script>
