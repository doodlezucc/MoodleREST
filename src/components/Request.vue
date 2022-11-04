<script setup>
import ObjectEntry from "./ObjectEntry.vue";

defineProps({
    request: {
        type: Object,
        required: true
    },
});

function isPlain(type) {
    return type !== 'object' && type !== 'array'
}
</script>

<template>
    <!-- <table v-if="Object.keys(request).length">
        <tr>
            <th>Parameter</th>
            <th>Description</th>
            <th>Type</th>
            <th>Default</th>
        </tr>
        <tr v-for="(param, paramName) in request">
            <td>
                <code class="inline">
                    <span :class="{ required: param.required }">{{ paramName }}</span>
                </code>
            </td>
            <td v-if="isPlain(param.type)">{{ param.description }}</td>
            <td v-if="isPlain(param.type)">
                <code class="inline" :data-type="simpleType(param.type)">{{ param.type }}</code>
            </td>
            <td v-else colspan="2">
                <code><Field :field=param /></code>
            </td>

            <td>
                <i v-if="param.required">required</i>
                <code v-else
                    class="inline">{{ simpleType(param.type) === "string" ? `"${param.default}"` : param.default }}</code>
            </td>
        </tr>
    </table> -->
    <code v-if="Object.keys(request).length">
      <ObjectEntry v-for="(prop, key) in request" :name="key" :field="prop" />
        <!-- <li><Field :field="{ type: 'object', properties: request }" /></li> -->
    </code>
    <p v-else>
        <i>No request parameters.</i>
    </p>
</template>