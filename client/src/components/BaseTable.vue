<template>
  <table class="w-full divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th class="header" v-for="col in columns" :key="col.field">{{ col.headerName }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in rowData" :key="row.id">
        <td v-for="col in colums" :key="col.field" class="px-6 py-4 whitespace-nowrap">{{ row[col.field] }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
// import TradeManager from "@/data/trade-manager";

export default defineComponent({
  name: "BaseTable",
  props: {
    columns: {
      type: Array,
      required: true
    },
    rowData: {
      type: Array,
      required: true
    }
  },
});
</script>

<style lang="postcss" scoped>
.header {
  @apply px-6;
  @apply py-3;
  @apply text-left;
  @apply text-xs;
  @apply font-medium;
  @apply text-gray-500;
  @apply uppercase;
  @apply tracking-wider;
}
</style>
