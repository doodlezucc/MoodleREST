<script setup>
import ObjectEntry from "../code/ObjectEntry.vue";

defineProps({
  request: {
    type: Object,
    required: true
  },
});
</script>

<template>
  <code v-if="Object.keys(request).length">
      <ObjectEntry v-for="(prop, key) in request" :name="key" :field="prop" />
    </code>
  <p v-else>
    <i>No request parameters.</i>
  </p>
</template>