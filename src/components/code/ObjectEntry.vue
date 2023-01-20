<script setup>
import Field from "./Field.vue";
import { simpleType } from '@/js/datatype';

const { name, field, isResponse } = defineProps({
  name: {
    type: String,
    required: true
  },
  field: {
    type: Object,
    required: true
  },
  isResponse: {
    type: Boolean,
    default: false,
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
    <span v-if="field.default != undefined" class="comment separator">(defaults to
      <span :data-type="simple" style="font-weight: normal;">{{ def }}</span>)
      <span class="comment separator-end">:</span>
    </span>
    <span v-else class="comment separator">: </span>
    <Field :field=field :is-response="isResponse" />
  </li>
</template>
