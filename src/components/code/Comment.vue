<script setup>
defineProps({
  content: {
    type: String
  }
});
</script>

<template>
  <span class="comment" v-if="content"> //
    <span>{{ content }}</span>
  </span>
</template>