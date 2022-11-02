<script setup>
import Comment from "./Comment.vue";

defineProps({
    field: {
        type: Object,
        required: true
    },
});
</script>

<template>
    <span v-if="field.type === 'object'">
        <i>object</i> {
        <Comment :content=field.description />
        <ul>
            <li v-for="(prop, key) in field.properties">
                <span :class="{ required: prop.required }">{{ key }}</span>
                -
                <Field :field=prop />
            </li>
        </ul>}
    </span>
    <span v-else-if="field.type === 'array'">
        <i>array of </i>
        <Field :field=field.items />
        <!-- <Comment :content=field.items.description /> -->
    </span>
    <span v-else>
        <i>{{ field.type }}</i>
        <Comment :content=field.description />
    </span>
</template>
