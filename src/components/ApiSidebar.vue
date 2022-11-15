<script setup>
import { ref, toRaw } from "vue";
import { apiSearchEntries } from "../js/api-helpers";
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

const entries = apiSearchEntries(api);

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
