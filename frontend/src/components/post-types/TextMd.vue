<script setup>
import DatedPostHeader from "../DatedPostHeader.vue"
import MarkdownContent from "../MarkdownContent.vue"

defineProps({
  post: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <article class="text-md-post">
    <DatedPostHeader :title="post.name" :date="post.date" />
    <MarkdownContent :source="post.text" />
  </article>
</template>

<style scoped>
.text-md-post {
  display: flex;
  flex-direction: column;
  gap: clamp(1.75rem, 4vw, 2.75rem);
}
</style>
