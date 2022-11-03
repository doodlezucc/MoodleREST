<script setup>
import { RouterView } from "vue-router";
import PageHeader from "./components/Header.vue";
import PageFooter from "./components/Footer.vue";
</script>

<template>
  <PageHeader />

  <div class="main">
    <RouterView />
  </div>

  <PageFooter />
</template>
