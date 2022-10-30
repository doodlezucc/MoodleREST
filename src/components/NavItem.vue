<script setup>
const { name, children, path } = defineProps({
  name: {
    type: String,
    required: true,
  },
  children: {
    type: Object,
    required: true
  },
  path: {
    type: String,
    required: true
  }
});

const isEndpoint = 'IMPL' in children
</script>

<template>
  <li>
    <a :class="{ path: !isEndpoint }" :href=path>{{ name }}</a>
    <ul v-if="!isEndpoint">
      <NavItem v-for="(value, key) in children" :path="path + '_' + key" :name=key :children=value />
    </ul>
  </li>
</template>
