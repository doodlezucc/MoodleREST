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
  <p>{{ body.description }}</p>

  <div><b>Version</b>: {{ version }}</div>
  <!-- <div v-if="body.services.length"><b>Services</b>: {{ body.services.join(', ') }}</div> -->
  <!-- <div v-else><b>Services</b>: none</div> -->
  <div v-if="body.deprecated"><b>Deprecated</b>: {{ body.deprecated }}</div>
  <div v-if="body.todo"><b>TODO</b>: {{ body.todo }}</div>

  <h3>Request</h3>
  <Request :request=body.request />

  <h3>Response</h3>
  <Response :response=body.response />
</template>
