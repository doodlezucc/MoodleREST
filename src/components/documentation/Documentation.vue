<script setup>
import CompDoc from "./DocumentedComponent.vue";
import FuncDoc from "./DocumentedFunction.vue";

const { api, name } = defineProps({
  api: {
    type: Object,
    required: true,
  },
  name: {
    type: String,
    required: true
  }
});

let isComponent = false
let body
for (const compname in api) {
  const comp = api[compname]
  if (compname === name) {
    body = comp
    isComponent = true
    break
  }

  if (name in comp) {
    body = comp[name]
    break
  }
}
</script>

<template>
  <h1>{{ name }}</h1>
  <CompDoc v-if="isComponent" :functions=body />
  <FuncDoc v-else :body=body />
</template>
