<script setup>
import CompDoc from "./DocumentedComponent.vue";

const { api } = defineProps({
  api: {
    type: Object,
    required: true,
  }
});
</script>

<template>
  <h1>Overview</h1>
  <p>
    Welcome to the unofficial, automatically generated Moodle API reference for web services! Using these functions,
    developers can programmatically interact with a Moodle instance.
  </p>
  <p>
    Take a look at Moodle's <a href="https://docs.moodle.org/dev/Web_services">documentation on web services</a>
    to learn more about the API infrastructure. For information on how to write a <b>client implementation</b>, follow
    their guide on <a href="https://docs.moodle.org/dev/Creating_a_web_service_client">creating a web service
      client</a>.
  </p>

  <code>
    https://your.moodle.address/login/token.php
  </code>

  <code>
    https://your.moodle.address/webservice/rest/server.php?wstoken=[TOKEN]&wsfunction=[FUNCTION]&moodlewrestformat=json
  </code>

  <p>Functions are sorted by component/plugin.</p>

  <CompDoc v-for="(value, key) in api" :name=key :functions=value />
</template>
