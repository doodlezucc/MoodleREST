<script setup>
import ref389 from "../api/moodle-3.8.9.json";

import Response from "./Response.vue";
import Request from "./Request.vue";

defineProps({
  version: {
    type: String,
    required: true
  }
});

const ref = ref389;
const fns = Object.fromEntries(Object.entries(ref.functions).slice(0, 10));
</script>

<template>
  <h1 class="green">{{ version }}</h1>

  <ul class="unlist">
    <li v-for="(fn, fnName) in fns">
      <h2>{{ fnName }}</h2>
      <span>{{ fn.description }}</span>

      <h3>Request</h3>
      <Request :request=fn.request />

      <h3>Response</h3>
      <Response v-if="fn.response" :response=fn.response />
    </li>
  </ul>
</template>
