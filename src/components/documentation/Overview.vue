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
  <p>A collection of all web service functions available from the get go, sorted by component/plugin.</p>

  <CompDoc v-for="(value, key) in api" :name=key :functions=value />
</template>
