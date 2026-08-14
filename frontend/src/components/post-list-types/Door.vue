<script setup>
import Door from "../post-types/Door.vue"

defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div>
    <Door
      v-for="post in posts"
      :key="post.id ?? post.number"
      :post="post"
    />
  </div>
</template>
