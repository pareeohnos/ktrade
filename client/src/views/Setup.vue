<template>
  <div class="config flex justify-center">
    <app-panel class="w-1/2">
      <app-header>Welcome to KTrade</app-header>

      <app-input v-model="config.maxRisk" label="Max risk" description="Your % maximum risk per trade" />
    </app-panel>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import AppHeader from "@/components/AppHeader.vue";
import AppInput from "@/components/AppInput.vue";
import AppPanel from "@/components/AppPanel.vue";

export default defineComponent({
  components: {
    AppHeader,
    AppInput,
    AppPanel
  },
  setup() {
    const config = ref({
      maxRisk: 0.5,
      maxSize: 33,
      twsHost: "localhost",
      twsPort: 4000
    });

    return { config };
  }
});
</script>
