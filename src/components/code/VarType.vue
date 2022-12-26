<script setup>
import { simpleType, typeDescription } from "@/js/datatype";

const { field, isResponse } = defineProps({
  field: {
    type: Object,
    required: true
  },
  isResponse: {
    type: Boolean,
    default: false
  }
});

const simple = simpleType(field.type);
let name = field.type;

if (field.nullable) {
  name += "?";
}

const description = typeDescription(field.type);
let comment = null;
let commentType = null;

if (description) {
  commentType = description.id;
  if (field.nullable) {
    commentType += " (nullable)";
  }

  if (isResponse) {
    comment = description.response ?? description.comment;
  } else {
    comment = description.comment;
  }
}

</script>

<template>
  <i :data-type="simple" class="with-tooltip">
    {{ name }}
    <div class="tooltip" v-if="comment">
      <span :data-type="simple">{{ commentType }}</span>
      <pre> - </pre>
      <span>{{ comment }}</span>
    </div>
  </i>
</template>
