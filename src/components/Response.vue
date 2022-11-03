<script setup>
import Field from "./Field.vue";

defineProps({
    response: {
        type: Object
    },
});
</script>

<template>
    <code v-if="response">
        <Field :field=response />
    </code>
    <p v-else>
        <i>No response.</i>
    </p>
</template>