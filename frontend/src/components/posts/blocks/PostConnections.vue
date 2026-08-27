<script setup>
import { computed } from "vue"

import PostTag from "./PostTag.vue"
import PostRowList from "../list-types/PostRowList.vue"

const props = defineProps({
  projectCode: {
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
})

const relatedItems = computed(() =>
  props.relatedPosts.map((post) => ({
    key: post.id ?? `${post.link}-${post.number}`,
    link: post.link,
    image: post.thumbnail,
    label: post.label,
    alt: post.label,
    date: post.date,
  })),
)
</script>

<template>
  <div
    v-if="relatedPosts.length || tags.length"
    class="post-connections"
  >
    <section
      v-if="relatedPosts.length"
      class="post-connections__related"
      aria-labelledby="related-posts-title"
    >
      <h2 id="related-posts-title">связанные посты</h2>
      <PostRowList :items="relatedItems" />
    </section>

    <ul v-if="tags.length" class="post-connections__tags" aria-label="Теги">
      <PostTag
        v-for="tag in tags"
        :key="tag.code"
        :code="tag.code"
        :name="tag.name"
        :project-code="projectCode"
      />
    </ul>
  </div>
</template>

<style scoped>
.post-connections {
  display: contents;
}

.post-connections__related {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding-top: 1rem;
}

.post-connections__related h2 {
  margin: 0;
  color: var(--color-muted);
  font-size: 0.78rem;
  font-weight: 750;
  letter-spacing: 0.08em;
  text-transform: uppercase;
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
