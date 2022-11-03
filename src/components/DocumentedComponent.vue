<script setup>
import Function from "./DocumentedFunction.vue";

defineProps({
    name: {
        type: String
    },
    functions: {
        type: Object,
        required: true
    }
});
</script>

<template>
    <h2 v-if="name">{{ name }}</h2>

    <ul class="big-items">
        <li v-for="(body, fn) in functions">
            <a :href="'#' + fn" class="item">
                <b>{{ fn }}</b>
                <i>{{ body.description }}</i>
            </a>
        </li>
    </ul>
</template>
