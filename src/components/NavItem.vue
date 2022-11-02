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
  <li>
    <a :class="{ path: !isEndpoint }" :href="'#' + name">{{ name }}</a>
    <ul v-if="!isEndpoint">
      <NavItem v-for="(value, key) in children" :name=key />
    </ul>
  </li>
</template>
