<script setup>
import Response from "./Response.vue";
import Request from "./Request.vue";

defineProps({
  api: {
    type: Object,
    required: true,
  }
});

</script>

<template>
  <h1 class="green">{{ api.version }}</h1>

  <ul class="unlist">
    <li v-for="(fn, fnName) in api.functions">
      <h2>{{ fnName }}</h2>
      <span>{{ fn.description }}</span>

      <h3>Request</h3>
      <Request :request=fn.request />

      <h3>Response</h3>
      <Response v-if="fn.response" :response=fn.response />
    </li>
  </ul>
</template>
