<template>
<div class="flex flex-row">
  <app-button @click="clicked('BUY')">Buy</app-button>
  <app-button @click="clicked('UNWATCH')">Unwatch</app-button>
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