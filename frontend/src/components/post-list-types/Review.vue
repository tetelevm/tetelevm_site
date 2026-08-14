<script setup>
import Review from "../post-types/Review.vue"

defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div>
    <Review
      v-for="post in posts"
      :key="post.id ?? post.number"
      :post="post"
    />
  </div>
</template>
