<script setup>
import { Searcher, makeQuery } from "../js/search";

const { entries } = defineProps({
  entries: {
    type: Array,
    required: true
  }
});

defineEmits(['search']);

const searcher = new Searcher(entries);

function toQuery(event) {
  return makeQuery(event.target.value);
}

function search(event) {
  const query = toQuery(event);
  const results = searcher.search(query);
  return results;
}
</script>

<template>
  <input type="text" placeholder="Search..." @input="event => $emit('search', toQuery(event), search(event))">
</template>