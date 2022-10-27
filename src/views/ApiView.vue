<script setup>
import Documentation from '../components/Documentation.vue';

defineProps({
  api: {
    type: Object,
    required: true
  }
});
</script>

<template>
  <main>
    <nav></nav>
    <Documentation :api=api />
  </main>
</template>
