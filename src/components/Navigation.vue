<script setup>
defineProps({
  path: {
    type: Array,
    required: true,
  }
});
</script>

<template>
  <nav>
    <span v-for="(segment, index) in path">
      <span v-if="index > 0" :key="index" class="separator"></span>
      <a :href="segment[1]" :key="segment[0]">{{ segment[0] }}</a>
    </span>
  </nav>
</template>
