<template>
  <NotificationGroup group="notifications">
    <div
      class="
        fixed
        inset-0
        flex
        items-start
        justify-end
        p-6
        px-4
        py-6
        pointer-events-none
        z-10
      "
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
          <app-notification
            v-for="notification in notifications"
            :key="notification.id"
            :notification="notification"
          />
        </Notification>
      </div>
    </div>
  </NotificationGroup>
</template>

<script lang="ts">
  import { defineComponent } from "vue";
  import AppNotification from "@/components/AppNotification.vue";

  export default defineComponent({
    components: {
      AppNotification,
    },
  });
</script>
