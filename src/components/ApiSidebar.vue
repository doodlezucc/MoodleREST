<script setup>
import SidebarItem from "./SidebarItem.vue";

defineProps({
  api: {
    type: Object,
    required: true
  },
  active: {
    type: Array,
    required: true
  }
});
</script>

<template>
  <aside>
    <input type="text" placeholder="Search...">
    <ul>
      <SidebarItem v-for="(component, key) in api" :name="key" :children="component" :active="active" />
    </ul>
  </aside>
</template>
