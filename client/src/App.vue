<template>
  <div class="ktrade bg-gray-200 overflow-auto flex flex-col">
    <navigation class="flex-initial" v-if="!isSetup" />
    <NotificationGroup group="notifications">
      <div
        class="fixed inset-0 flex items-start justify-end p-6 px-4 py-6 pointer-events-none"
      >
        <div class="w-full max-w-sm">
          <Notification
            v-slot="{ notifications }"
            enter="transform ease-out duration-300 transition"
            enter-from="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
            enter-to="translate-y-0 opacity-100 sm:translate-x-0"
            leave="transition ease-in duration-500"
            leave-from="opacity-100"
            leave-to="opacity-0"
            move="transition duration-500"
            move-delay="delay-300"
          >
            <div
              class="flex w-full max-w-sm mx-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md"
              v-for="notification in notifications"
              :key="notification.id"
            >
              <div class="flex items-center justify-center w-12 bg-green-500">
                <svg class="w-6 h-6 text-white fill-current" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
                  <path d="M20 3.33331C10.8 3.33331 3.33337 10.8 3.33337 20C3.33337 29.2 10.8 36.6666 20 36.6666C29.2 36.6666 36.6667 29.2 36.6667 20C36.6667 10.8 29.2 3.33331 20 3.33331ZM16.6667 28.3333L8.33337 20L10.6834 17.65L16.6667 23.6166L29.3167 10.9666L31.6667 13.3333L16.6667 28.3333Z" />
                </svg>
              </div>

              <div class="px-4 py-2 -mx-3">
                <div class="mx-3">
                  <span class="font-semibold text-green-500">{{ notification.title }}</span>
                  <p class="text-sm text-gray-600">{{ notification.text }}</p>
                </div>
              </div>
            </div>
          </Notification>
        </div>
      </div>
    </NotificationGroup>

    <div class="flex-1 p-8">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { useRoute } from "vue-router";
import { defineComponent, computed, onMounted } from "vue";
import Navigation from "@/components/Navigation.vue";
// @ts-ignore
import { notify } from "notiwind";

export default defineComponent({
  components: {
    Navigation,
  },
  name: "App",
  sockets: {
    info({ message }: { message: string }) {
      notify({
        group: "notifications",
        title: "Info",
        text: message,
        type: "info"
      }, 5000);
    },
    warning({ message }: { message: string }) {
      notify({
        group: "notifications",
        title: "Warning",
        text: message,
        type: "warning"
      }, 5000);
    },
    error({ message }: { message: string }) {
      notify({
        group: "notifications",
        title: "Error",
        text: message,
        type: "error"
      }, 5000);
    },
    success({ message }: { message: string }) {
      notify({
        group: "notifications",
        title: "Success",
        text: message,
        type: "success"
      }, 5000);
    }
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
