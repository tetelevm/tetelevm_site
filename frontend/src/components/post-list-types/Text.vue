<script setup>
import Text from "../post-types/Text.vue"

defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div>
    <Text
      v-for="post in posts"
      :key="post.id ?? post.number"
      :post="post"
    />
  </div>
</template>
