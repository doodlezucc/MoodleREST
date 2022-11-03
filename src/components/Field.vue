<script setup>
import Comment from "./Comment.vue";
import simpleType from "./js/datatype";

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

const dataType = simpleType(field.type);
</script>

<template>
  <span v-if="field.type === 'object'">
    <i><span :data-type="dataType">object</span></i> {
    <Comment :content=field.description />
    <ul>
      <li v-for="(prop, key) in field.properties">
        <span :class="{ key: true, required: prop.required }">{{ key }}</span>
        -
        <Field :field=prop />
      </li>
    </ul>}
  </span>
  <span v-else-if="field.type === 'array'">
    <i><span :data-type="dataType">array</span></i> [
    <ul>
      <li>
        <Field :field=field.items :isArray="true" />
      </li>
    </ul>]
  </span>
  <span v-else>
    <i :data-type="dataType">{{ field.type }}</i>
    <Comment :content=field.description />
  </span>
</template>
