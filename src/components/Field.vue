<script setup>
import Comment from "./Comment.vue";
import VarType from "./VarType.vue";
import ObjectEntry from "./ObjectEntry.vue";

const { field } = defineProps({
  field: {
    type: Object,
    required: true
  },
  isArray: {
    type: Boolean,
    default: false
  }
});
</script>

<template>
  <span v-if="field.type === 'object'">
    <VarType :field="field" /> {
    <Comment :content=field.description />
    <ul>
      <ObjectEntry v-for="(prop, key) in field.properties" :name="key" :field="prop" />
    </ul>}
  </span>
  <span v-else-if="field.type === 'array'">
    <VarType :field="field" /> [
    <ul>
      <li>
        <Field :field=field.items :isArray="true" />
      </li>
    </ul>]
  </span>
  <span v-else>
    <VarType :field="field" />
    <Comment :content=field.description />
  </span>
</template>
