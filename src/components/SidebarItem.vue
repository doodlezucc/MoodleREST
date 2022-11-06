<script setup>
import { apiNameToPath } from '@/js/api-helpers.js';

const { name, active, children } = defineProps({
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
  }
});

const isEndpoint = !children;
</script>

<template>
  <li :class="{ path: !isEndpoint, active: active.includes(name) }">
    <a :href="'#' + name" :title="name">{{ name }}</a>
    <ul v-if="!isEndpoint">
      <SidebarItem v-for="(_, key) in children" :name=key :active="active" />
    </ul>
  </li>
</template>
