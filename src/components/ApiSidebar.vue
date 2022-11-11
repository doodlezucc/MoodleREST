<script setup>
import { ref } from "vue";
import { Entry } from "../js/search";
import SearchBar from "./SearchBar.vue";
import SidebarItem from "./SidebarItem.vue";

const { api, active } = defineProps({
  api: {
    type: Object,
    required: true
  },
  active: {
    type: Array,
    required: true
  }
});

const entries = [];
for (const category in api) {
  const fns = api[category];

  for (const fnname in fns) {
    const fn = fns[fnname];
    entries.push(new Entry(fnname, fn.description));
  }
}

const query = ref("");
const results = ref([]);

const doFilter = ref(false);

function onSearch(q, res) {
  query.value = q;
  results.value = res;
  doFilter.value = q.length > 0;
}
</script>

<template>
  <aside>
    <SearchBar :entries="entries" @search="onSearch" />
    <ul v-if="!doFilter">
      <SidebarItem v-for="(component, key) in api" :name="key" :children="component" :active="active" />
    </ul>
    <ul v-else>
      <SidebarItem v-for="result of results" :name="result.entry.title" :active="active" />
    </ul>
  </aside>
</template>
