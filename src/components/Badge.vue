<script setup>
defineProps({
  text: {
    type: String,
    required: true
  },
  value: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: "var(--color-primary)"
  }
});
</script>

<template>
  <span class="badge">
    <span>{{ text }}</span>
    <b :style="`background-color:${color}`">{{ value }}</b>
  </span>
</template>
