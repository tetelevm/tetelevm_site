<script setup>
import PostConnections from "./PostConnections.vue"
import PostNavigation from "./PostNavigation.vue"

defineProps({
  projectCode: {
    type: String,
    required: true,
  },
  projectName: {
    type: String,
    required: true,
  },
  relatedPosts: {
    type: Array,
    default: () => [],
  },
  tags: {
    type: Array,
    default: () => [],
  },
  previousPost: {
    type: Object,
    default: null,
  },
  nextPost: {
    type: Object,
    default: null,
  },
})
</script>

<template>
  <section
    v-if="relatedPosts.length || tags.length || previousPost || nextPost"
    class="post-footer"
    aria-label="Дополнительная навигация поста"
  >
    <PostConnections
      :project-code="projectCode"
      :related-posts="relatedPosts"
      :tags="tags"
    />
    <PostNavigation
      :project-name="projectName"
      :previous-post="previousPost"
      :next-post="nextPost"
    />
  </section>
</template>

<style scoped>
.post-footer {
  display: flex;
  flex-direction: column;
  gap: clamp(1.75rem, 4vw, 2.5rem);
}
</style>
