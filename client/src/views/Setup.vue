<template>
  <div class="config flex justify-center">
    <app-panel class="w-1/2">
      <app-header>Welcome to KTrade</app-header>

      <p class="mb-8">
        Lets get setup. Fill in the details below and we can get started
      </p>

      <app-input
        v-model="config.maxRisk"
        label="Max risk"
        description="Your % maximum risk per trade"
      />

      <app-input
        v-model="config.maxSize"
        label="Max trade size"
        description="The maximum % of your account per trade"
      />

      <app-input
        v-model="config.twsHost"
        label="TWS hostname"
        description="Where is TWS currently running (e.g localhost)"
      />

      <app-input
        v-model="config.twsPort"
        label="TWS port"
        description="The port that the TWS API is running on"
      />

      <app-button @click="submit">Continue</app-button>
    </app-panel>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from "vue";
  import axios from "axios";
  import AppButton from "@/components/AppButton.vue";
  import AppHeader from "@/components/AppHeader.vue";
  import AppInput from "@/components/AppInput.vue";
  import AppPanel from "@/components/AppPanel.vue";

  export default defineComponent({
    components: {
      AppButton,
      AppHeader,
      AppInput,
      AppPanel,
    },
    setup() {
      const config = ref({
        maxRisk: 0.5,
        maxSize: 33,
        twsHost: "localhost",
        twsPort: 4000,
      });

      return { config };
    },
    methods: {
      submit() {
        axios
          .post("/configure", this.config)
          .then(() => {
            this.$router.replace("/");
          })
          .catch((error) => {
            alert("Error");
          });
      },
    },
  });
</script>
