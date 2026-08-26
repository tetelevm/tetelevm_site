<script setup>
import MarkdownContent from "../blocks/MarkdownContent.vue"
import PostLayout from "../blocks/PostLayout.vue"

defineProps({
  post: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <PostLayout :post="post">
    <MarkdownContent :source="post.text" />
  </PostLayout>
</template>
