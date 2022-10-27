<script setup>
import Field from "./Field.vue";

defineProps({
    response: {
        type: Object,
        required: true
    },
});
</script>

<template>
    <code>
        <Field :field=response />
    </code>
</template>