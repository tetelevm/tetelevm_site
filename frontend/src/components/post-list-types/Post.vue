<script setup>
import TextPostList from "../TextPostList.vue"

defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <TextPostList :posts="posts" />
</template>
