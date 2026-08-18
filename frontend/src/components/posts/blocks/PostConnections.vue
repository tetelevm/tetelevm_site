<script setup>
import PostTag from "./PostTag.vue"
import RelatedPostLink from "./RelatedPostLink.vue"

defineProps({
  relatedPost: {
    type: Object,
    default: null,
  },
  tags: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div
    v-if="relatedPost || tags.length"
    class="post-connections"
  >
    <RelatedPostLink
      v-if="relatedPost"
      :related-post="relatedPost"
    />

    <ul v-if="tags.length" class="post-connections__tags" aria-label="Теги">
      <PostTag
        v-for="tag in tags"
        :key="tag.code"
        :name="tag.name"
      />
    </ul>
  </div>
</template>

<style scoped>
.post-connections {
  display: contents;
}

.post-connections__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0;
  margin: -0.5rem 0 0;
  list-style: none;
}
</style>
