<script setup>
import Response from "./Response.vue";
import Request from "./Request.vue";

defineProps({
  name: {
    type: String,
    required: true
  },
  body: {
    type: Object,
    required: true,
  }
});
</script>

<template>
  <h2>{{ name }}</h2>
  <span>{{ body.description }}</span>

  <h3>Request</h3>
  <Request :request=body.request />

  <h3>Response</h3>
  <Response v-if="body.response" :response=body.response />
</template>
