<script setup>
import { computed } from "vue"

import MediaCarousel from "../MediaCarousel.vue"
import PostTag from "../PostTag.vue"
import RelatedPostLink from "../RelatedPostLink.vue"

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const photos = computed(() => {
  const items = [props.post.mainFile, ...(props.post.files ?? [])]
    .filter(Boolean)
    .filter((item) => item.mediaType === "image")

  return items.filter(
    (item, index) =>
      items.findIndex((candidate) => candidate.id === item.id) === index,
  )
})
</script>

<template>
  <article class="travel-post">
    <h1>{{ post.name }}</h1>

    <MediaCarousel :items="photos" :label="`Фотографии: ${post.name}`" />

    <div v-if="post.text" class="travel-post__text">{{ post.text }}</div>

    <RelatedPostLink
      v-if="post.relatedPost"
      :related-post="post.relatedPost"
    />

    <ul v-if="post.tags?.length" class="travel-post__tags" aria-label="Теги">
      <PostTag
        v-for="tag in post.tags"
        :key="tag.code"
        :name="tag.name"
      />
    </ul>
  </article>
</template>

<style scoped>
.travel-post {
  display: flex;
  flex-direction: column;
  gap: clamp(1.75rem, 4vw, 2.75rem);
}

.travel-post h1 {
  margin: 0;
  color: var(--color-text);
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(2rem, 6vw, 3.4rem);
  font-weight: 500;
  line-height: 1.05;
  overflow-wrap: anywhere;
}

.travel-post__text {
  color: var(--color-text);
  font-size: 1rem;
  line-height: 1.65;
  white-space: pre-line;
}

.travel-post__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0;
  margin: -0.5rem 0 0;
  list-style: none;
}

</style>
