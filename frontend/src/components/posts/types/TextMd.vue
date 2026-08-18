<script setup>
import DatedPostHeader from "../blocks/DatedPostHeader.vue"
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
  <PostLayout>
    <DatedPostHeader :title="post.name" :date="post.date" />
    <MarkdownContent :source="post.text" />
  </PostLayout>
</template>
