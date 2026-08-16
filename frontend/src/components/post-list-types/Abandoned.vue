<script setup>
import RatedPostGrid from "../RatedPostGrid.vue"

defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <RatedPostGrid :posts="posts" />
</template>
