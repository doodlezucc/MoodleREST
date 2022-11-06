<script setup>
defineProps({
  text: {
    type: String,
    required: true
  },
  value: {
    type: String
  },
  color: {
    type: String,
    default: "var(--color-primary)"
  }
});
</script>

<template>
  <span class="badge">
    <span v-if="value != undefined">{{ text }}</span>
    <b :style="`background-color:${color}`">{{ value ?? text }}</b>
  </span>
</template>
