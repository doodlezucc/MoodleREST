<script setup>
const { text, regex } = defineProps({
  text: {
    type: String,
    required: true
  },
  regex: {
    type: RegExp,
    required: true
  }
});

const parts = [];
let start = 0;

for (const match of text.matchAll(regex)) {
  parts.push(text.substring(start, match.index));
  start = match.index + match[0].length
  parts.push(text.substring(match.index, start));
}
parts.push(text.substring(start));
</script>

<template>
  <span v-for="(part, index) in parts" :class="{ highlight: index % 2 == 1 }">{{ part }}</span>
</template>
