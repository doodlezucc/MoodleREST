<script setup>
const { name, children } = defineProps({
  name: {
    type: String,
    required: true,
  },
  children: {
    type: Object,
    default: null
  }
});

const isEndpoint = !children
</script>

<template>
  <li :class="{ path: !isEndpoint }">
    <a :href="'#' + name" :title="name">{{ name }}</a>
    <ul v-if="!isEndpoint">
      <SidebarItem v-for="(_, key) in children" :name=key />
    </ul>
  </li>
</template>
