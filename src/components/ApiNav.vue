<script setup>
import NavItem from "./NavItem.vue";

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
      <NavItem v-for="(component, key) in api" :name=key :children=component />
    </ul>
  </aside>
</template>
