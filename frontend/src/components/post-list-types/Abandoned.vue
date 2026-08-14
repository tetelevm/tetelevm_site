<script setup>
import Abandoned from "../post-types/Abandoned.vue"

defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div>
    <Abandoned
      v-for="post in posts"
      :key="post.id ?? post.number"
      :post="post"
    />
  </div>
</template>
