<script setup>
import Field from "../code/Field.vue";

defineProps({
  response: {
    type: Object
  }
});
</script>

<template>
  <code v-if="response">
        <li><Field :field=response :is-response=true /></li>
    </code>
  <p v-else>
    <i>No response.</i>
  </p>
</template>