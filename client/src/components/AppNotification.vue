<template>
  <div class="flex w-full max-w-sm mx-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md">
    <div :class="colourBoxClasses">
      <svg class="w-6 h-6 text-white fill-current" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <path v-if="notification.type === 'success'" d="M20 3.33331C10.8 3.33331 3.33337 10.8 3.33337 20C3.33337 29.2 10.8 36.6666 20 36.6666C29.2 36.6666 36.6667 29.2 36.6667 20C36.6667 10.8 29.2 3.33331 20 3.33331ZM16.6667 28.3333L8.33337 20L10.6834 17.65L16.6667 23.6166L29.3167 10.9666L31.6667 13.3333L16.6667 28.3333Z" />
        <path v-if="notification.type === 'error'" d="M20 3.36667C10.8167 3.36667 3.3667 10.8167 3.3667 20C3.3667 29.1833 10.8167 36.6333 20 36.6333C29.1834 36.6333 36.6334 29.1833 36.6334 20C36.6334 10.8167 29.1834 3.36667 20 3.36667ZM19.1334 33.3333V22.9H13.3334L21.6667 6.66667V17.1H27.25L19.1334 33.3333Z"/>
        <path v-if="notification.type === 'info'" d="M20 3.33331C10.8 3.33331 3.33337 10.8 3.33337 20C3.33337 29.2 10.8 36.6666 20 36.6666C29.2 36.6666 36.6667 29.2 36.6667 20C36.6667 10.8 29.2 3.33331 20 3.33331ZM21.6667 28.3333H18.3334V25H21.6667V28.3333ZM21.6667 21.6666H18.3334V11.6666H21.6667V21.6666Z"/>
        <path v-if="notification.type === 'warning'" d="M20 3.33331C10.8 3.33331 3.33337 10.8 3.33337 20C3.33337 29.2 10.8 36.6666 20 36.6666C29.2 36.6666 36.6667 29.2 36.6667 20C36.6667 10.8 29.2 3.33331 20 3.33331ZM21.6667 28.3333H18.3334V25H21.6667V28.3333ZM21.6667 21.6666H18.3334V11.6666H21.6667V21.6666Z" />
      </svg>
    </div>

    <div class="px-4 py-2 -mx-3">
      <div class="mx-3">
        <span :class="titleClasses">{{ notification.title }}</span>
        <p class="text-sm text-gray-600">{{ notification.text }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";

const bgColours = {
  info: "bg-blue-500",
  error: "bg-red-500",
  success: "bg-green-500",
  warning: "bg-yellow-500"
};

const titleColours = {
  info: "text-blue-500",
  error: "text-red-500",
  success: "text-green-500",
  warning: "text-yellow-500"
};

export default defineComponent({
  props: {
    notification: { 
      type: Object,
      required: true
    }
  },
  setup(props) {
    const colourBoxClasses = computed(() => {
      let classes = ["flex", "items-center", "justify-center", "w-12"];
      classes.push(bgColours[props.notification.type]);

      return classes;
    });

    const titleClasses = computed(() => {
      return ["font-semibold", titleColours[props.notification.type]];
    });

    return {
      colourBoxClasses,
      titleClasses
    };
  }
});
</script>