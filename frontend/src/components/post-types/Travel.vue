<script setup>
import { computed } from "vue"

import DatedPostHeader from "../DatedPostHeader.vue"
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
  return (props.post.files ?? []).filter((item) => item.mediaType === "photo")
})
</script>

<template>
  <article class="travel-post">
    <DatedPostHeader :title="post.name" :date="post.date" />

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

.travel-post__text {
  color: var(--color-text);
  font-size: 1.2rem;
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
