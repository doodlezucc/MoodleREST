<script setup>
import Response from "./Response.vue";
import Request from "./Request.vue";
import Badge from "../Badge.vue";

defineProps({
  body: {
    type: Object,
    required: true,
  }
});
</script>

<template>
  <div class="badge-list">
    <Badge v-if="body.since" text='Since' :value="body.since" />
    <Badge v-if="body.deprecated" text='Deprecated' :value="body.deprecated" />
    <Badge v-if="body.todo" text='TODO' :value="body.todo" />
  </div>
  <p>{{ body.description }}</p>

  <h3>Request</h3>
  <Request :request=body.request />

  <h3>Response</h3>
  <Response :response=body.response />
</template>
