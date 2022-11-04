<script setup>
import simpleType from "./js/datatype";

const { field } = defineProps({
  field: {
    type: Object,
    required: true
  }
});

const simple = simpleType(field.type);
let name = field.type;

if (field.nullable) {
  name += "?"
}

</script>

<template>
  <i :data-type="simple">{{ name }}</i>
</template>
