<template>
<div class="flex flex-row">
  <app-dropdown :options="actions" @option-clicked="optionClicked">
    <template #trigger="{ open }">
      <a href="#" @click="open">Actions</a>
    </template>
  </app-dropdown>
  <!-- <app-button @click="clicked('TRIM_THIRD')">Trim 1/3</app-button>
  <app-button @click="clicked('TRIM_HALF')">Trim 1/2</app-button>
  <app-button class="ml-4" @click="clicked('SELL')">Sell</app-button> -->
</div>  
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AppButton from "@/components/AppButton.vue";
import AppDropdown from "@/components/AppDropdown.vue";

export default defineComponent({
  components: {
    AppButton,
    AppDropdown
  },
  props: ["params"],
  setup() {
    const actions = [
      [
        { label: "Trim 1/3", action: "TRIM_THIRD" },
        { label: "Trim 1/2", action: "TRIM_HALF" }
      ],
      [
        { label: "Cancel", action: "CANCEL" }
      ]
    ];
    return {
      actions
    }
  },
  methods: {
    optionClicked({ action }) {
      this.params.click(action, this.params.data);
    },
  }
})
</script>