<template>
  <div class="config flex justify-center">
    <app-panel class="w-1/2 p-8">
      <config-form></config-form>
    </app-panel>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from "vue";
  import ConfigForm from "@/views/ConfigForm.vue";
  import AppPanel from "@/components/AppPanel.vue";

  export default defineComponent({
    components: {
      ConfigForm,
      AppPanel,
    },
  });
</script>
