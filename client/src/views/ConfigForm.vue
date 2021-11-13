<template>
  <div>
    <input
      class="mb-4"
      type="checkbox"
      name="fetchAccountSize"
      v-model="config.fetchAccountSize"
    />
    <label class="ml-4 mb-4" for="fetchAccountSize"
      >Obtain account size automatically?</label
    >

    <div
      v-if="!config.fetchAccountSize"
      class="bg-gray-100 p-4 rounded-lg border border-gray-200 mb-4"
    >
      <app-input
        v-model="config.accountSize"
        label="Account size"
        description="How much trading capital should KTrade use for its calculations"
      />
    </div>

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
        fetchAccountSize: true,
        accountSize: 0,
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
