<script setup>
import NavItem from "./NavItem.vue";

const { api, root } = defineProps({
  api: {
    type: Object,
    required: true,
  },
  root: {
    type: String,
    required: true,
  }
});

class Impl {
  constructor(val) {
    this.IMPL = val
  }
}

const fns = api.functions
const structure = {}

for (const key in fns) {
  const path = key.split("_")
  let parent = structure
  for (let i = 0; i < path.length; i++) {
    const seg = path[i]
    if (seg in parent) {
      parent = parent[seg]
    } else if (i < path.length - 1) {
      parent = parent[seg] = {}
    } else {
      parent[seg] = new Impl(fns[key])
    }
  }
}

function flattenObject(obj) {
  const keys = Object.keys(obj)
  const nObj = {}
  for (const key of keys) {
    if (obj[key] instanceof Impl) {
      nObj[key] = obj[key]
      continue
    }

    const child = flattenObject(obj[key])
    const chKeys = Object.keys(child)
    if (chKeys.length == 1) {
      const onlyKey = chKeys[0]
      const nKey = key + "_" + onlyKey
      nObj[nKey] = child[onlyKey]
    } else {
      nObj[key] = child
    }
  }
  return nObj
}

const flat = flattenObject(structure)
</script>

<template>
  <nav>
    <input type="text" placeholder="Search...">
    <ul>
      <NavItem v-for="(value, key) in flat" :name=key :children=value :path="'/' + root + '#' + key" />
    </ul>
  </nav>
</template>
