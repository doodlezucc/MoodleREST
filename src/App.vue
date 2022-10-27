<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <header>
    <h1>Moodle API Reference</h1>
  </header>

  <div class="main">
    <nav></nav>
    <RouterView />
  </div>

  <footer>
    <p>Footer</p>
  </footer>
</template>

<style scoped>
.main {
  flex: 1;
}
</style>