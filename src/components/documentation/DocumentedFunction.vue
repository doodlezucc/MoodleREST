<script setup>
import Response from "./Response.vue";
import Request from "./Request.vue";
import Badge from "../Badge.vue";
import BoolBadge from "../BoolBadge.vue";

const { body } = defineProps({
  body: {
    type: Object,
    required: true,
  }
});

let version = 'any';
if (body.since) {
  version = '≥' + body.since;
}
</script>

<template>
  <div class="badge-list">
    <Badge v-if="body.requiresLogin" text='Login required' :color="'var(--color-badge-bad)'" />
    <Badge v-if="!body.ajaxAllowed" text='No AJAX' :color="'var(--color-badge-bad)'" />
  </div>
  <div class="badge-list">
    <Badge text='Version' :value="version" />
    <Badge v-if="body.deprecated" text='Deprecated' :value="body.deprecated" :color="'var(--color-badge-bad)'" />
    <Badge v-if="body.todo" text='TODO' :value="body.todo" :color="'var(--color-badge-bad)'" />
    <Badge v-if="body.services.length" text='Services' :value="body.services.join(', ')"
      :color="'var(--color-badge-good)'" />
  </div>
  <p>{{ body.description }}</p>

  <h3>Request</h3>
  <Request :request=body.request />

  <h3>Response</h3>
  <Response :response=body.response />
</template>
