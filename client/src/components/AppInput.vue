<template>
  <div class="flex flex-col mb-4">
    <label class="text-lg">{{ label }}</label>
    <span v-if="description" class="text-sm mb-2">{{ description }}</span>
    <input
      class="border border-gray-400 p-2 rounded"
      :value="modelValue"
      type="text"
      @input="onInput"
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
    setup(_props, { emit }) {
      const onInput = (e: Event) => {
        const target = <HTMLInputElement>e.target;
        const val = target.value;

        emit("update:modelValue", val);
      };
      return {
        onInput,
      };
    },
  });
</script>
