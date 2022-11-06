<script setup>
import { ref } from 'vue';
import { onBeforeRouteUpdate, useRoute } from 'vue-router';
import { apiNameToPath, apiNameToPathHref } from '@/js/api-helpers.js';

import ApiSidebar from '../components/ApiSidebar.vue';
import Documentation from '../components/documentation/Documentation.vue';
import Overview from '../components/documentation/Overview.vue';
import Navigation from '../components/Navigation.vue';

const { api } = defineProps({
  api: {
    type: Object,
    required: true
  }
});

const route = useRoute();

const fn = ref();
function setDocFn(val) {
  const nval = (val ?? route.hash).substring(1);
  if (nval !== fn.value) {
    fn.value = nval;
    document.querySelector('main')?.scrollTo({ top: 0 });
  }
}

setDocFn();
onBeforeRouteUpdate((to, _) => {
  setDocFn(to.hash);
});

function navPath() {
  let path = [['API Reference', '']];
  if (fn.value) {
    path = path.concat(apiNameToPathHref(fn.value, api));
  }
  return path;
}

function activePath() {
  return apiNameToPath(fn.value, api);
}
</script>

<template>
  <ApiSidebar :api=api :active="activePath()" />
  <main>
    <Navigation :path="navPath()" />
    <Documentation v-if="fn" :api=api :name=fn :key=fn />
    <Overview v-else :api=api />
  </main>
</template>
