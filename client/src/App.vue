<template>
  <div class="ktrade bg-gray-200 overflow-auto flex flex-col">
    <navigation class="flex-initial" v-if="!isSetup" />
    <app-notifications />

    <div class="flex-1 p-8">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
  import { useRoute } from "vue-router";
  import { defineComponent, computed } from "vue";
  import Navigation from "@/components/Navigation.vue";
  import AppNotifications from "@/components/AppNotifications.vue";
  // @ts-ignore
  import { notify } from "notiwind";

  export default defineComponent({
    components: {
      Navigation,
      AppNotifications,
    },
    name: "App",
    sockets: {
      info({ message }: { message: string }) {
        notify(
          {
            group: "notifications",
            title: "Info",
            text: message,
            type: "info",
          },
          5000
        );
      },
      warning({ message }: { message: string }) {
        notify(
          {
            group: "notifications",
            title: "Warning",
            text: message,
            type: "warning",
          },
          5000
        );
      },
      error({ message }: { message: string }) {
        notify(
          {
            group: "notifications",
            title: "Error",
            text: message,
            type: "error",
          },
          5000
        );
      },
      success({ message }: { message: string }) {
        notify(
          {
            group: "notifications",
            title: "Success",
            text: message,
            type: "success",
          },
          5000
        );
      },
    },
    setup(_, ctx) {
      const route = useRoute();
      const isSetup = computed(() => route.name === "Setup");

      return {
        isSetup,
      };
    },
  });
</script>
