<script setup>
import { ref, toRef, watch } from 'vue';
import { onBeforeRouteUpdate, routeLocationKey, useRoute, useRouter } from 'vue-router';
import ApiNav from '../components/ApiNav.vue';
import Documentation from '../components/Documentation.vue';
import Overview from '../components/Overview.vue';

defineProps({
  api: {
    type: Object,
    required: true
  },
  root: {
    type: String,
    required: true
  }
});

const route = useRoute()

const fn = ref()
function setDocFn(val) {
  fn.value = (val ?? route.hash).substring(1)
  console.log("updated fn")
}

setDocFn()
onBeforeRouteUpdate((to, from) => {
  setDocFn(to.hash)
})
</script>

<template>
  <ApiNav :api=api :root=root />
  <main>
    <Documentation v-if="fn" :api=api :fn=fn :key=fn />
    <Overview v-else :api=api />
  </main>
</template>
