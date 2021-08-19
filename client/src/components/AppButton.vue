<template>
  <div
    class="
      rounded rounded
      bg-blue-500
      hover:bg-blue-600
      text-white
      p-2
      cursor-pointer
      inline-block
    "
  >
    <slot />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Button",
});
</script>
