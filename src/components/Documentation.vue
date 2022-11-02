<script setup>
import Response from "./Response.vue";
import Request from "./Request.vue";
import { computed } from "@vue/reactivity";

const { api, fn } = defineProps({
  api: {
    type: Object,
    required: true,
  },
  fn: {
    type: String,
    required: true
  }
});

let func
for (const compname in api) {
  const comp = api[compname]
  if (fn in comp) {
    func = comp[fn]
    break
  }
}
// const func = api.functions[fn]
</script>

<template>
  <h2>{{ fn }}</h2>
  <span>{{ func.description }}</span>

  <h3>Request</h3>
  <Request :request=func.request />

  <h3>Response</h3>
  <Response v-if="func.response" :response=func.response />
</template>
