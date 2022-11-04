<script setup>
import Response from "./Response.vue";
import Request from "./Request.vue";

defineProps({
  body: {
    type: Object,
    required: true,
  }
});
</script>

<template>
  <p>{{ body.description }}</p>

  <h3>Request</h3>
  <Request :request=body.request />

  <h3>Response</h3>
  <Response :response=body.response />
</template>
