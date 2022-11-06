<script setup>
import Badge from "./Badge.vue";

defineProps({
  text: {
    type: String,
    required: true
  },
  value: {
    type: Boolean,
    required: true
  },
  color: {
    type: String
  },
  colorTrue: {
    type: String,
    default: "var(--color-badge-good)"
  },
  colorFalse: {
    type: String,
    default: "var(--color-badge-bad)"
  }
});
</script>

<template>
  <Badge :text="text" :value="value ? 'Yes' : 'No'" :color="color ?? (value ? colorTrue : colorFalse)" />
</template>
