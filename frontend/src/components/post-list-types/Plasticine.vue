<script setup>
import Plasticine from "../post-types/Plasticine.vue"

defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div>
    <Plasticine
      v-for="post in posts"
      :key="post.id ?? post.number"
      :post="post"
    />
  </div>
</template>
