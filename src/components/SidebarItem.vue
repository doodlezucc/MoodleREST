<script setup>
import { Query } from "../js/search";
import Highlighted from "./Highlighted.vue";

const { name, active, children, query } = defineProps({
  name: {
    type: String,
    required: true,
  },
  active: {
    type: Array,
    required: true
  },
  children: {
    type: Object,
    default: null
  },
  query: {
    type: Query
  }
});

const isEndpoint = !children;
</script>

<template>
  <li :class="{ path: !isEndpoint, active: active.includes(name) }">
    <a :href="'#' + name" :title="name">
      <Highlighted v-if="query && query.terms.join('').length > 1" :text="name" :regex="query.regex"
        :key="query.regex.source" />
      <span v-else>{{ name }}</span>
    </a>
    <ul v-if="!isEndpoint">
      <SidebarItem v-for="(_, key) in children" :name=key :active="active" />
    </ul>
  </li>
</template>
