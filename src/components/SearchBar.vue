<script setup>
import { Searcher } from "../js/search";

const { entries } = defineProps({
  entries: {
    type: Array,
    required: true
  }
});

defineEmits(['search']);

const searcher = new Searcher(entries);

function search(event) {
  const query = event.target.value;
  const results = searcher.search(query);
  return results;
}
</script>

<template>
  <input type="text" placeholder="Search..." @input="event => $emit('search', event.target.value, search(event))">
</template>