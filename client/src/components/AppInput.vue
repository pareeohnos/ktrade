<template>
  <div class="flex flex-col mb-4">
    <label class="text-lg">{{ label }}</label>
    <span v-if="description" class="text-sm mb-2">{{ description }}</span>
    <input
      class="border border-gray-400 p-2 rounded"
      :value="modelValue"
      type="text"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Input",
  props: {
    label: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: false,
      default: null,
    },
    modelValue: {
      type: [String, Number],
      required: false,
      default: null,
    },
  },
});
</script>
