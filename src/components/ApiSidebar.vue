<script setup>
import SidebarItem from "./SidebarItem.vue";

defineProps({
  api: {
    type: Object,
    required: true,
  }
});
</script>

<template>
  <aside>
    <input type="text" placeholder="Search...">
    <ul>
      <SidebarItem v-for="(component, key) in api" :name=key :children=component />
    </ul>
  </aside>
</template>
