<template>
  <div class="bg-white border border-gray-300 rounded-lg">
    <slot />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Panel"
});
</script>
