<script setup>
import Field from "./Field.vue";
import simpleType from '@/js/datatype';

const { name, field } = defineProps({
  name: {
    type: String,
    required: true
  },
  field: {
    type: Object,
    required: true
  }
});

const simple = simpleType(field.type);
let def = field.default;
if (def != undefined) {
  if (simple === "string") {
    def = `"${def}"`;
  } else if (simple === "bool") {
    def = (def === 0) ? "true" : "false";
  }
}
</script>

<template>
  <li>
    <span :class="{ key: true, required: field.required }">{{ name }}</span>
    <span v-if="field.default != undefined" class="comment"> (defaults to
      <span :data-type="simple" style="font-weight: normal;">{{ def }}</span>)
    </span>
    -
    <Field :field=field />
  </li>
</template>
