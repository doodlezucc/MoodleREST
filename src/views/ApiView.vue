<script setup>
import { ref } from 'vue';
import { onBeforeRouteUpdate, useRoute } from 'vue-router';
import ApiSidebar from '../components/ApiSidebar.vue';
import Documentation from '../components/documentation/Documentation.vue';
import Overview from '../components/documentation/Overview.vue';

defineProps({
  api: {
    type: Object,
    required: true
  }
});

const route = useRoute()

const fn = ref()
function setDocFn(val) {
  fn.value = (val ?? route.hash).substring(1)
  document.querySelector("main")?.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

setDocFn()
onBeforeRouteUpdate((to, from) => {
  setDocFn(to.hash)
})
</script>

<template>
  <ApiSidebar :api=api />
  <main>
    <Documentation v-if="fn" :api=api :name=fn :key=fn />
    <Overview v-else :api=api />
  </main>
</template>
