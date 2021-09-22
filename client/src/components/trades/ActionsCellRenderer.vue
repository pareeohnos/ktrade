<template>
<div class="flex flex-row">
  
  <app-button @click="clicked('TRIM_THIRD')">Trim 1/3</app-button>
  <app-button @click="clicked('TRIM_HALF')">Trim 1/2</app-button>
  <app-button class="ml-4" @click="clicked('SELL')">Sell</app-button>
</div>  
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AppButton from "@/components/AppButton.vue";

export default defineComponent({
  components: {
    AppButton
  },
  props: ["params"],
  methods: {
    clicked(type: string) {
      this.params.click(type, this.params.data);
    }
  }
})
</script>