<script setup>
import Field from "./Field.vue";

defineProps({
    request: {
        type: Object,
        required: true
    },
});
</script>

<template>
    <table v-if="Object.keys(request).length">
        <tr>
            <th>Parameter</th>
            <th>Description</th>
            <th>Type</th>
            <th>Default</th>
        </tr>
        <tr v-for="(param, paramName) in request">
            <td>
                <code class="inline">
                    <u v-if="param.required">
                        <b>{{ paramName }}</b>
                    </u>
                    <span v-else>{{ paramName }}</span>
                </code>
            </td>
            <td>{{ param.description }}</td>
            <td>
                <code class="inline">{{ param.type }}</code>
            </td>

            <td>
                <i v-if="param.required">required</i>
                <code v-else class="inline">{{ param.type === "string" ? `"${param.default}"` : param.default }}</code>
            </td>
        </tr>
    </table>
    <p v-else>
        <i>No request parameters.</i>
    </p>
</template>